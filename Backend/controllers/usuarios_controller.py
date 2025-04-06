from fastapi import APIRouter, HTTPException
import mysql.connector
from config.config import get_db_connection
from models.usuarios_model import Usuarios
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class UsuariosController:
    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gestion_medica.usuarios")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'nombre': data[1],
                    'email': data[2],
                    'password': data[3],
                    'rol_id': data[4],
                    'creado_en': data[5]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_usuario_id(self, id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.usuarios WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                usuario = {
                    'id': result[0],
                    'nombre': result[1],
                    'email': result[2],
                    'password': result[3],
                    'rol_id': result[4],
                    'creado_en': result[5]
                }
                return {"resultado": usuario}
            else:
                return {"resultado": "Usuario no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_usuarios_by_rol(self, rol_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.usuarios WHERE rol_id = %s", (rol_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'nombre': data[1],
                    'email': data[2],
                    'password': data[3],
                    'rol_id': data[4],
                    'creado_en': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_usuario(self, nuevo_usuario: Usuarios):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            nombre = nuevo_usuario.nombre
            email = nuevo_usuario.email
            password = nuevo_usuario.password
            rol_id = nuevo_usuario.rol_id
            cursor.execute("""
            INSERT INTO gestion_medica.usuarios 
            (nombre, email, password, rol_id, creado_en) 
            VALUES (%s, %s, %s, %s, NOW())
            """, (nombre, email, password, rol_id))
            conn.commit()
            conn.close()
            return {"informacion": "Usuario registrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_usuario(self, id: int, usuario_actualizado: Usuarios):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.usuarios WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El usuario no se encuentra en la base de datos")
            nombre = usuario_actualizado.nombre
            email = usuario_actualizado.email
            password = usuario_actualizado.password
            rol_id = usuario_actualizado.rol_id
            cursor.execute("""
            UPDATE gestion_medica.usuarios SET 
            nombre = %s,
            email = %s,
            password = %s,
            rol_id = %s
            WHERE id = %s
            """, (nombre, email, password, rol_id, id))
            conn.commit()
            return {"informacion": "Usuario actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_usuario(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.usuarios WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El usuario no se encuentra en la base de datos"}
            cursor.execute("DELETE FROM gestion_medica.usuarios WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE gestion_medica.usuarios AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Usuario eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

usuarios_controller = UsuariosController()