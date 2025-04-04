from pydantic import BaseModel
from datetime import datetime


class Usuarios(BaseModel):
    nombre: str
    email: str
    password_hash: str
    rol_id: int
    creado_en: datetime
