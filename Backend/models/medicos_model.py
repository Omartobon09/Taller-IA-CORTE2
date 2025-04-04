from pydantic import BaseModel


class Medicos(BaseModel):
    usuario_id: int
    especialidad: str
    telefono: str
