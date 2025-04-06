from pydantic import BaseModel
from datetime import datetime


class Usuario(BaseModel):
    nombre: str
    email: str
    password: str
    documento: str
    telefono: str
    fecha_nacimiento: datetime
    rol_id: int
    especialidad: str 
    creado_en: datetime
