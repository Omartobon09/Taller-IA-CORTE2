from fastapi import APIRouter, HTTPException
from controllers.citas_controller import CitasController
from models.citas_model import Citas

router = APIRouter()
citas_controller = CitasController()

@router.get("/get/citas")
async def get_citas():
    return citas_controller.get_citas()

@router.get("/get/citas/{id}")
async def get_cita_id(id: int):
    return citas_controller.get_cita_id(id)

@router.get("/get/citas/paciente/{paciente_id}")
async def get_citas_by_paciente(paciente_id: int):
    return citas_controller.get_citas_by_paciente(paciente_id)

@router.get("/get/citas/medico/{medico_id}")
async def get_citas_by_medico(medico_id: int):
    return citas_controller.get_citas_by_medico(medico_id)

@router.get("/get/citas/fecha/{fecha}")
async def get_citas_by_fecha(fecha: str):
    return citas_controller.get_citas_by_fecha(fecha)

@router.post("/post/citas")
async def post_cita(nueva_cita: Citas):
    return citas_controller.post_cita(nueva_cita)

@router.put("/update/citas/{id}")
async def update_cita(id: int, cita_actualizada: Citas):
    return citas_controller.update_cita(id, cita_actualizada)

@router.delete("/delete/citas/{id}")
async def delete_cita(id: int):
    return citas_controller.delete_cita(id)
