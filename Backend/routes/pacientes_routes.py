from fastapi import APIRouter, Path
from models.pacientes_model import Pacientes
from controllers.pacientes_controller import PacientesController

router = APIRouter()


pacientes_controller= PacientesController()

@router.get("/pacientes")
def obtener_pacientes():
    return pacientes_controller.get_pacientes()

@router.get("/pacientes/{id}")
def obtener_paciente_por_id(id: int = Path(..., description="ID del paciente")):
    return pacientes_controller.get_paciente_id(id)

@router.get("/pacientes/usuario/{usuario_id}")
def obtener_pacientes_por_usuario(usuario_id: int):
    return pacientes_controller.get_pacientes_by_usuario(usuario_id)

@router.post("/pacientes")
def crear_paciente(nuevo_paciente: Pacientes):
    return pacientes_controller.post_paciente(nuevo_paciente)

@router.put("/pacientes/{id}")
def actualizar_paciente(id: int, paciente_actualizado: Pacientes):
    return pacientes_controller.update_paciente(id, paciente_actualizado)

@router.delete("/pacientes/{id}")
def eliminar_paciente(id: int):
    return pacientes_controller.delete_paciente(id)