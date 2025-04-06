from fastapi import APIRouter
import mysql.connector
from fastapi import HTTPException
from config.config import get_db_connection
from models.historial_medico_model import HistorialMedico
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class HistorialMedicoController:

    def get_historiales(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historial_medico")
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
                "SELECT * FROM historial_medico WHERE id = %s", (id,))
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
                return {"resultado": "Historial no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}

    def get_historial_paciente(self, paciente_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM historial_medico WHERE paciente_id = %s ORDER BY fecha DESC", 
                (paciente_id,))
            results = cursor.fetchall()
            historiales = []
            if results:
                for result in results:
                    historial = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'diagnostico': result[3],
                        'recomendaciones': result[4],
                        'fecha': result[5]
                    }
                    historiales.append(historial)
                return {"resultado": historiales}
            else:
                return {"resultado": "No se encontraron registros de historial para este paciente"}
        except Exception as error:
            return {"resultado": str(error)}

    def get_historial_medico_doctor(self, medico_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM historial_medico WHERE medico_id = %s ORDER BY fecha DESC", 
                (medico_id,))
            results = cursor.fetchall()
            historiales = []
            if results:
                for result in results:
                    historial = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'diagnostico': result[3],
                        'recomendaciones': result[4],
                        'fecha': result[5]
                    }
                    historiales.append(historial)
                return {"resultado": historiales}
            else:
                return {"resultado": "No se encontraron registros de historial para este médico"}
        except Exception as error:
            return {"resultado": str(error)}
            
    def get_historial_fecha_rango(self, fecha_inicio, fecha_fin):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM historial_medico WHERE fecha BETWEEN %s AND %s ORDER BY fecha DESC", 
                (fecha_inicio, fecha_fin))
            results = cursor.fetchall()
            historiales = []
            if results:
                for result in results:
                    historial = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'diagnostico': result[3],
                        'recomendaciones': result[4],
                        'fecha': result[5]
                    }
                    historiales.append(historial)
                return {"resultado": historiales}
            else:
                return {"resultado": "No se encontraron registros en ese rango de fechas"}
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
            fecha = nuevo_historial.fecha if nuevo_historial.fecha else datetime.now()
            
            cursor.execute("""
            INSERT INTO historial_medico 
            (paciente_id, medico_id, diagnostico, recomendaciones, fecha) 
            VALUES (%s, %s, %s, %s, %s)
            """, (paciente_id, medico_id, diagnostico, recomendaciones, fecha))
            
            conn.commit()
            conn.close()
            return {"informacion": "Historial médico registrado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_historial(self, id: int, historial_actualizado: HistorialMedico):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM historial_medico WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="El registro de historial no se encuentra en la base de datos")
            
            paciente_id = historial_actualizado.paciente_id
            medico_id = historial_actualizado.medico_id
            diagnostico = historial_actualizado.diagnostico
            recomendaciones = historial_actualizado.recomendaciones
            fecha = historial_actualizado.fecha
            
            cursor.execute("""
            UPDATE historial_medico SET 
            paciente_id = %s,
            medico_id = %s,
            diagnostico = %s,
            recomendaciones = %s,
            fecha = %s
            WHERE id = %s
            """, (paciente_id, medico_id, diagnostico, recomendaciones, fecha, id))
            
            conn.commit()
            return {"informacion": "Registro de historial actualizado correctamente"}
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
                "SELECT id FROM historial_medico WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "El registro de historial no se encuentra en la base de datos"}
            
            cursor.execute("DELETE FROM historial_medico WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE historial_medico AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Registro de historial eliminado correctamente"}
        except Exception as error:
            return {"resultado": str(error)}


historial_medico_controller = HistorialMedicoController()