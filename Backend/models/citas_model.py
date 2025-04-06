from pydantic import BaseModel
from datetime import date, time


class Cita(BaseModel):
    paciente_id: int
    medico_id: int
    fecha: date
    hora: time
    estado: str
