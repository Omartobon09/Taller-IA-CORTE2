from fastapi import APIRouter, HTTPException
from controllers.usuarios_controller import usuarios_controller
from models.usuarios_model import Usuario

router = APIRouter()

# ✅ Traer todos los usuarios


@router.get("/get/usuarios")
async def get_usuarios():
    return usuarios_controller.get_usuarios()

# ✅ Traer usuario por ID


@router.get("/get/usuarios/{id}")
async def get_usuario_id(id: int):
    return usuarios_controller.get_usuario_id(id)

# ✅ Traer médicos (usuarios con rol_id = 2)


@router.get("/get/medicos")
async def get_medicos():
    return usuarios_controller.get_medicos()


@router.get("/get/usuario/documento/{documento}")
async def get_usuario_por_documento(documento: str):
    return usuarios_controller.get_usuario_por_documento(documento)

# ✅ Registrar nuevo usuario


@router.post("/post/usuarios")
async def post_usuario(nuevo_usuario: Usuario):
    return usuarios_controller.post_usuario(nuevo_usuario)

# ✅ Actualizar un usuario


@router.put("/update/usuarios/{id}")
async def update_usuario(id: int, usuario_actualizado: Usuario):
    return usuarios_controller.update_usuario(id, usuario_actualizado)

# ✅ Eliminar un usuario


@router.delete("/delete/usuarios/{id}")
async def delete_usuario(id: int):
    return usuarios_controller.delete_usuario(id)
