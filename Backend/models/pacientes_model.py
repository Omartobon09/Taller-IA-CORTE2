from pydantic import BaseModel
from datetime import date


class Pacientes(BaseModel):
    usuario_id: int
    documento: str
    fecha_nacimiento: date
    telefono: str
