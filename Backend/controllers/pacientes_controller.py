from fastapi import APIRouter, HTTPException
import mysql.connector
from config.config import get_db_connection
from models.pacientes_model import Pacientes
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date

class PacientesController:
    def get_pacientes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gestion_medica.pacientes")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'usuario_id': data[1],
                    'documento': data[2],
                    'fecha_nacimiento': data[3],
                    'telefono': data[4]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_paciente_id(self, id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.pacientes WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                paciente = {
                    'id': result[0],
                    'usuario_id': result[1],
                    'documento': result[2],
                    'fecha_nacimiento': result[3],
                    'telefono': result[4]
                }
                return {"resultado": paciente}
            else:
                return {"resultado": "Paciente no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_pacientes_by_usuario(self, usuario_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.pacientes WHERE usuario_id = %s", (usuario_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'usuario_id': data[1],
                    'documento': data[2],
                    'fecha_nacimiento': data[3],
                    'telefono': data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_paciente(self, nuevo_paciente: Pacientes):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            usuario_id = nuevo_paciente.usuario_id
            documento = nuevo_paciente.documento
            fecha_nacimiento = nuevo_paciente.fecha_nacimiento
            telefono = nuevo_paciente.telefono
            cursor.execute("""
            INSERT INTO gestion_medica.pacientes 
            (usuario_id, documento, fecha_nacimiento, telefono) 
            VALUES (%s, %s, %s, %s)
            """, (usuario_id, documento, fecha_nacimiento, telefono))
            conn.commit()
            conn.close()
            return {"informacion": "Paciente registrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_paciente(self, id: int, paciente_actualizado: Pacientes):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.pacientes WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El paciente no se encuentra en la base de datos")
            usuario_id = paciente_actualizado.usuario_id
            documento = paciente_actualizado.documento
            fecha_nacimiento = paciente_actualizado.fecha_nacimiento
            telefono = paciente_actualizado.telefono
            cursor.execute("""
            UPDATE gestion_medica.pacientes SET 
            usuario_id = %s,
            documento = %s,
            fecha_nacimiento = %s,
            telefono = %s
            WHERE id = %s
            """, (usuario_id, documento, fecha_nacimiento, telefono, id))
            conn.commit()
            return {"informacion": "Paciente actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_paciente(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.pacientes WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El paciente no se encuentra en la base de datos"}
            cursor.execute("DELETE FROM gestion_medica.pacientes WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE gestion_medica.pacientes AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Paciente eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

pacientes_controller = PacientesController()