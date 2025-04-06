from fastapi import APIRouter, HTTPException
import mysql.connector
from config.config import get_db_connection
from models.historial_medico_model import HistorialMedico
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class HistorialMedicoController:
    def get_historiales(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gestion_medica.historial_medico")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'diagnostico': data[3],
                    'recomendaciones': data[4],
                    'fecha': data[5]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_historial_id(self, id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.historial_medico WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                historial = {
                    'id': result[0],
                    'paciente_id': result[1],
                    'medico_id': result[2],
                    'diagnostico': result[3],
                    'recomendaciones': result[4],
                    'fecha': result[5]
                }
                return {"resultado": historial}
            else:
                return {"resultado": "Historial médico no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_historiales_by_paciente(self, paciente_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.historial_medico WHERE paciente_id = %s", (paciente_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'diagnostico': data[3],
                    'recomendaciones': data[4],
                    'fecha': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_historiales_by_medico(self, medico_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.historial_medico WHERE medico_id = %s", (medico_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'diagnostico': data[3],
                    'recomendaciones': data[4],
                    'fecha': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_historial(self, nuevo_historial: HistorialMedico):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            paciente_id = nuevo_historial.paciente_id
            medico_id = nuevo_historial.medico_id
            diagnostico = nuevo_historial.diagnostico
            recomendaciones = nuevo_historial.recomendaciones
            cursor.execute("""
            INSERT INTO gestion_medica.historial_medico 
            (paciente_id, medico_id, diagnostico, recomendaciones, fecha) 
            VALUES (%s, %s, %s, %s, NOW())
            """, (paciente_id, medico_id, diagnostico, recomendaciones))
            conn.commit()
            conn.close()
            return {"informacion": "Historial médico registrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_historial(self, id: int, historial_actualizado: HistorialMedico):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.historial_medico WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El historial médico no se encuentra en la base de datos")
            paciente_id = historial_actualizado.paciente_id
            medico_id = historial_actualizado.medico_id
            diagnostico = historial_actualizado.diagnostico
            recomendaciones = historial_actualizado.recomendaciones
            cursor.execute("""
            UPDATE gestion_medica.historial_medico SET 
            paciente_id = %s,
            medico_id = %s,
            diagnostico = %s,
            recomendaciones = %s,
            fecha = NOW()
            WHERE id = %s
            """, (paciente_id, medico_id, diagnostico, recomendaciones, id))
            conn.commit()
            return {"informacion": "Historial médico actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_historial(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.historial_medico WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El historial médico no se encuentra en la base de datos"}
            cursor.execute("DELETE FROM gestion_medica.historial_medico WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE gestion_medica.historial_medico AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Historial médico eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

historial_medico_controller = HistorialMedicoController()