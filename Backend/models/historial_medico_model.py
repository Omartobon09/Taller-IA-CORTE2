from pydantic import BaseModel
from datetime import datetime


class HistorialMedico(BaseModel):
    paciente_id: int
    medico_id: int
    diagnostico: str
    recomendaciones: str
    fecha: datetime
