from fastapi import APIRouter, Path
from models.usuarios_model import Usuarios
from controllers.usuarios_controller import UsuariosController

router = APIRouter()

usuarios_controller = UsuariosController()


@router.get("/usuarios")
def obtener_usuarios():
    return usuarios_controller.get_usuarios()


@router.get("/usuarios/{id}")
def obtener_usuario_por_id(id: int = Path(..., description="ID del usuario")):
    return usuarios_controller.get_usuario_id(id)


@router.get("/usuarios/rol/{rol_id}")
def obtener_usuarios_por_rol(rol_id: int):
    return usuarios_controller.get_usuarios_by_rol(rol_id)


@router.post("/usuarios")
def crear_usuario(nuevo_usuario: Usuarios):
    return usuarios_controller.post_usuario(nuevo_usuario)


@router.put("/usuarios/{id}")
def actualizar_usuario(id: int, usuario_actualizado: Usuarios):
    return usuarios_controller.update_usuario(id, usuario_actualizado)


@router.delete("/usuarios/{id}")
def eliminar_usuario(id: int):
    return usuarios_controller.delete_usuario(id)
