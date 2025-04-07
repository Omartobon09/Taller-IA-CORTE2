from fastapi import APIRouter, HTTPException
from controllers.citas_controller import CitasController
from models.citas_model import Cita
from datetime import date, time

router = APIRouter()
citas_controller = CitasController()

# ✅ Traer todas las citas


@router.get("/get/citas")
async def get_citas():
    return citas_controller.get_citas()

# ✅ Traer cita por ID


@router.get("/get/citas/{id}")
async def get_cita_id(id: int):
    return citas_controller.get_cita_id(id)

# ✅ Traer citas por paciente


@router.get("/get/citas/paciente/{paciente_id}")
async def get_citas_paciente(paciente_id: int):
    return citas_controller.get_citas_paciente(paciente_id)

# ✅ Traer citas por médico


@router.get("/get/citas/medico/{medico_id}")
async def get_citas_medico(medico_id: int):
    return citas_controller.get_citas_medico(medico_id)

# ✅ Traer citas por fecha


@router.get("/get/citas/fecha/{fecha}")
async def get_citas_fecha(fecha: date):
    return citas_controller.get_citas_fecha(fecha)


@router.get("/verificar-disponibilidad")
def verificar(medico_id: int, fecha: str, hora: str):
    return CitasController().verificar_disponibilidad(medico_id, fecha, hora)


# ✅ Registrar nueva cita
@router.post("/post/citas")
async def post_cita(nueva_cita: Cita):
    return citas_controller.post_cita(nueva_cita)

# ✅ Actualizar una cita


@router.put("/update/citas/{id}")
async def update_cita(id: int, cita_actualizada: Cita):
    return citas_controller.update_cita(id, cita_actualizada)

# ✅ Eliminar una cita


@router.delete("/delete/citas/{id}")
async def delete_cita(id: int):
    return citas_controller.delete_cita(id)
