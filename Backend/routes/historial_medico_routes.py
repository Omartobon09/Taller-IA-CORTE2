from fastapi import APIRouter, HTTPException
from controllers.historial_medico_controller import historial_medico_controller
from models.historial_medico_model import HistorialMedico
from datetime import date

router = APIRouter()

# ✅ Traer todos los historiales médicos
@router.get("/get/historiales")
async def get_historiales():
    return historial_medico_controller.get_historiales()

# ✅ Traer historial por ID
@router.get("/get/historiales/{id}")
async def get_historial_id(id: int):
    return historial_medico_controller.get_historial_id(id)

# ✅ Traer historiales por paciente
@router.get("/get/historiales/paciente/{paciente_id}")
async def get_historial_paciente(paciente_id: int):
    return historial_medico_controller.get_historial_paciente(paciente_id)

# ✅ Traer historiales por médico
@router.get("/get/historiales/medico/{medico_id}")
async def get_historial_medico_doctor(medico_id: int):
    return historial_medico_controller.get_historial_medico_doctor(medico_id)

# ✅ Traer historiales por rango de fechas
@router.get("/get/historiales/fechas/{fecha_inicio}/{fecha_fin}")
async def get_historial_fecha_rango(fecha_inicio: date, fecha_fin: date):
    return historial_medico_controller.get_historial_fecha_rango(fecha_inicio, fecha_fin)

# ✅ Registrar nuevo historial médico
@router.post("/post/historiales")
async def post_historial(nuevo_historial: HistorialMedico):
    return historial_medico_controller.post_historial(nuevo_historial)

# ✅ Actualizar un historial médico
@router.put("/update/historiales/{id}")
async def update_historial(id: int, historial_actualizado: HistorialMedico):
    return historial_medico_controller.update_historial(id, historial_actualizado)

# ✅ Eliminar un historial médico
@router.delete("/delete/historiales/{id}")
async def delete_historial(id: int):
    return historial_medico_controller.delete_historial(id)
