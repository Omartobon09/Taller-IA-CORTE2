from fastapi import APIRouter
import mysql.connector
from fastapi import HTTPException
from config.config import get_db_connection
from models.usuarios_model import Usuario
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import hashlib
import re


class UsuariosController:

    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'nombre': data[1],
                    'email': data[2],
                    # No se devuelve la contraseña por seguridad
                    'documento': data[4],
                    'telefono': data[5],
                    'fecha_nacimiento': data[6],
                    'rol_id': data[7],
                    'especialidad': data[8],
                    'creado_en': data[9]
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
                "SELECT * FROM usuarios WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                usuario = {
                    'id': result[0],
                    'nombre': result[1],
                    'email': result[2],
                    # No se devuelve la contraseña por seguridad
                    'documento': result[4],
                    'telefono': result[5],
                    'fecha_nacimiento': result[6],
                    'rol_id': result[7],
                    'especialidad': result[8],
                    'creado_en': result[9]
                }
                return {"resultado": usuario}
            else:
                return {"resultado": "Usuario no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def get_medicos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Asumiendo que el rol_id = 2 es para médicos
            cursor.execute("SELECT * FROM usuarios WHERE rol_id = 1")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'nombre': data[1],
                    'email': data[2],
                    'documento': data[4],
                    'telefono': data[5],
                    'especialidad': data[8]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_usuario(self, nuevo_usuario: Usuario):

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que el email no exista
        cursor.execute("SELECT id FROM usuarios WHERE email = %s",
                       (nuevo_usuario.email,))
        if cursor.fetchone():
            return {"resultado": "El email ya está registrado"}

        # Verificar que el documento no exista
        cursor.execute(
            "SELECT id FROM usuarios WHERE documento = %s", (nuevo_usuario.documento,))
        if cursor.fetchone():
            return {"resultado": "El documento ya está registrado"}

        nombre = nuevo_usuario.nombre
        email = nuevo_usuario.email
        password = nuevo_usuario.password
        documento = nuevo_usuario.documento
        telefono = nuevo_usuario.telefono
        fecha_nacimiento = nuevo_usuario.fecha_nacimiento
        rol_id = nuevo_usuario.rol_id
        especialidad = nuevo_usuario.especialidad if nuevo_usuario.especialidad else ""
        creado_en = nuevo_usuario.creado_en if nuevo_usuario.creado_en else datetime.now()

        cursor.execute("""
            INSERT INTO usuarios 
            (nombre, email, password, documento, telefono, fecha_nacimiento, rol_id, especialidad, creado_en) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, email,password, documento, telefono, fecha_nacimiento, rol_id, especialidad, creado_en))

        conn.commit()
        conn.close()
        return {"informacion": "Usuario registrado correctamente"}

    def update_usuario(self, id: int, usuario_actualizado: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El usuario no se encuentra en la base de datos")

            # Verificar si se actualiza el email
            if usuario_actualizado.email:
                if not self.validar_email(usuario_actualizado.email):
                    return {"resultado": "Formato de email inválido"}

                cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s",
                               (usuario_actualizado.email, id))
                if cursor.fetchone():
                    return {"resultado": "El email ya está registrado por otro usuario"}

            # Verificar si se actualiza el documento
            if usuario_actualizado.documento:
                cursor.execute("SELECT id FROM usuarios WHERE documento = %s AND id != %s",
                               (usuario_actualizado.documento, id))
                if cursor.fetchone():
                    return {"resultado": "El documento ya está registrado por otro usuario"}

            nombre = usuario_actualizado.nombre
            email = usuario_actualizado.email

            # Procesar contraseña solo si se proporciona una nueva
            password_sql = ""
            password_values = []

            if usuario_actualizado.password and usuario_actualizado.password.strip():
                if not self.validar_password(usuario_actualizado.password):
                    return {"resultado": "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número"}

                hashed_password = hashlib.sha256(
                    usuario_actualizado.password.encode()).hexdigest()
                password_sql = ", password = %s"
                password_values = [hashed_password]

            documento = usuario_actualizado.documento
            telefono = usuario_actualizado.telefono
            fecha_nacimiento = usuario_actualizado.fecha_nacimiento
            rol_id = usuario_actualizado.rol_id
            especialidad = usuario_actualizado.especialidad

            query = f"""
            UPDATE usuarios SET 
            nombre = %s,
            email = %s,
            documento = %s,
            telefono = %s,
            fecha_nacimiento = %s,
            rol_id = %s,
            especialidad = %s
            {password_sql}
            WHERE id = %s
            """

            values = [nombre, email, documento, telefono, fecha_nacimiento,
                      rol_id, especialidad] + password_values + [id]

            cursor.execute(query, tuple(values))

            conn.commit()
            return {"informacion": "Usuario actualizado correctamente"}
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
                "SELECT id FROM usuarios WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El usuario no se encuentra en la base de datos"}

            # Verificar si existen registros relacionados en otras tablas
            cursor.execute(
                "SELECT id FROM citas WHERE paciente_id = %s OR medico_id = %s", (id, id))
            if cursor.fetchone():
                return {"resultado": "No se puede eliminar el usuario porque tiene citas asociadas"}

            cursor.execute(
                "SELECT id FROM historial_medico WHERE paciente_id = %s OR medico_id = %s", (id, id))
            if cursor.fetchone():
                return {"resultado": "No se puede eliminar el usuario porque tiene historiales médicos asociados"}

            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE usuarios AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Usuario eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}


usuarios_controller = UsuariosController()
