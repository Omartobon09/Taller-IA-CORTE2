from fastapi import APIRouter, HTTPException
import mysql.connector
from config.config import get_db_connection
from models.medicos_model import Medicos
from fastapi.encoders import jsonable_encoder

class MedicosController:
    def get_medicos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gestion_medica.medicos")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'usuario_id': data[1],
                    'especialidad': data[2],
                    'telefono': data[3]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_medico_id(self, id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.medicos WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                medico = {
                    'id': result[0],
                    'usuario_id': result[1],
                    'especialidad': result[2],
                    'telefono': result[3]
                }
                return {"resultado": medico}
            else:
                return {"resultado": "Médico no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_medicos_by_especialidad(self, especialidad):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.medicos WHERE especialidad = %s", (especialidad,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'usuario_id': data[1],
                    'especialidad': data[2],
                    'telefono': data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_medico(self, nuevo_medico: Medicos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            usuario_id = nuevo_medico.usuario_id
            especialidad = nuevo_medico.especialidad
            telefono = nuevo_medico.telefono
            cursor.execute("""
            INSERT INTO gestion_medica.medicos 
            (usuario_id, especialidad, telefono) 
            VALUES (%s, %s, %s)
            """, (usuario_id, especialidad, telefono))
            conn.commit()
            conn.close()
            return {"informacion": "Médico registrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_medico(self, id: int, medico_actualizado: Medicos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.medicos WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El médico no se encuentra en la base de datos")
            usuario_id = medico_actualizado.usuario_id
            especialidad = medico_actualizado.especialidad
            telefono = medico_actualizado.telefono
            cursor.execute("""
            UPDATE gestion_medica.medicos SET 
            usuario_id = %s,
            especialidad = %s,
            telefono = %s
            WHERE id = %s
            """, (usuario_id, especialidad, telefono, id))
            conn.commit()
            return {"informacion": "Médico actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_medico(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.medicos WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El médico no se encuentra en la base de datos"}
            cursor.execute("DELETE FROM gestion_medica.medicos WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE gestion_medica.medicos AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Médico eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

medicos_controller = MedicosController()