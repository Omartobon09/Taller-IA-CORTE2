from fastapi import APIRouter, Path
from models.medicos_model import Medicos
from controllers.medicos_controller import MedicosController

router = APIRouter()


medicos_controller = MedicosController()


@router.get("/medicos")
def obtener_medicos():
    return medicos_controller.get_medicos()


@router.get("/medicos/{id}")
def obtener_medico_por_id(id: int = Path(..., description="ID del médico")):
    return medicos_controller.get_medico_id(id)


@router.get("/medicos/especialidad/{especialidad}")
def obtener_medicos_por_especialidad(especialidad: str):
    return medicos_controller.get_medicos_by_especialidad(especialidad)


@router.post("/medicos")
def crear_medico(nuevo_medico: Medicos):
    return medicos_controller.post_medico(nuevo_medico)


@router.put("/medicos/{id}")
def actualizar_medico(id: int, medico_actualizado: Medicos):
    return medicos_controller.update_medico(id, medico_actualizado)


@router.delete("/medicos/{id}")
def eliminar_medico(id: int):
    return medicos_controller.delete_medico(id)
