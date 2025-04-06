from fastapi import APIRouter, Path
from models.historial_medico_model import HistorialMedico
from controllers.historial_medico_controller import HistorialMedicoController

router = APIRouter()
historial_medico_controller = HistorialMedicoController()

@router.get("/historiales")
def obtener_historiales():
    return historial_medico_controller.get_historiales()

@router.get("/historiales/{id}")
def obtener_historial_por_id(id: int):
    return historial_medico_controller.get_historial_id(id)

@router.get("/historiales/paciente/{paciente_id}")
def obtener_historiales_por_paciente(paciente_id: int):
    return historial_medico_controller.get_historiales_by_paciente(paciente_id)

@router.get("/historiales/medico/{medico_id}")
def obtener_historiales_por_medico(medico_id: int):
    return historial_medico_controller.get_historiales_by_medico(medico_id)

@router.post("/historiales")
def crear_historial(nuevo_historial: HistorialMedico):
    return historial_medico_controller.post_historial(nuevo_historial)

@router.put("/historiales/{id}")
def actualizar_historial(id: int, historial_actualizado: HistorialMedico):
    return historial_medico_controller.update_historial(id, historial_actualizado)

@router.delete("/historiales/{id}")
def eliminar_historial(id: int):
    return historial_medico_controller.delete_historial(id)