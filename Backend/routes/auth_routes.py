from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from config.config import get_db_connection
from models.usuarios_model import Usuarios

router = APIRouter()

# Configuración para encriptación de contraseñas
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY5ODk4NDEwNiwiaWF0IjoxNjk4OTg0MTA2fQ.W3U9ivlk6ZW1qteEuUvGOjUDp8ed20sBNPKDi4rXWE4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo extendido para incluir hash


class UsuarioDB(Usuarios):
    hashed_password: str


class TokenData(BaseModel):
    username: str | None = None

# Obtener usuario desde base de datos


def get_user(db, email: str):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user

# Verificar contraseña encriptada


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Crear JWT


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Ruta login


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db_connection()
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/usuario")
async def obtener_usuario_autenticado(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        db = get_db_connection()
        user = get_user(db, email)
        if user is None:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Token inválido o expirado")
