from fastapi import APIRouter, HTTPException
import mysql.connector
from config.config import get_db_connection
from models.citas_model import Citas
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date

class CitasController:
    def get_citas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gestion_medica.citas")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'fecha': data[3],
                    'hora': data[4],
                    'estado': data[5]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_cita_id(self, id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.citas WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                cita = {
                    'id': result[0],
                    'paciente_id': result[1],
                    'medico_id': result[2],
                    'fecha': result[3],
                    'hora': result[4],
                    'estado': result[5]
                }
                return {"resultado": cita}
            else:
                return {"resultado": "Cita no encontrada"}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_citas_by_paciente(self, paciente_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.citas WHERE paciente_id = %s", (paciente_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'fecha': data[3],
                    'hora': data[4],
                    'estado': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_citas_by_medico(self, medico_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.citas WHERE medico_id = %s", (medico_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'fecha': data[3],
                    'hora': data[4],
                    'estado': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}
    
    def get_citas_by_fecha(self, fecha):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM gestion_medica.citas WHERE fecha = %s", (fecha,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'paciente_id': data[1],
                    'medico_id': data[2],
                    'fecha': data[3],
                    'hora': data[4],
                    'estado': data[5]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def post_cita(self, nueva_cita: Citas):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            paciente_id = nueva_cita.paciente_id
            medico_id = nueva_cita.medico_id
            fecha = nueva_cita.fecha
            hora = nueva_cita.hora
            estado = nueva_cita.estado if nueva_cita.estado else "pendiente"
            cursor.execute("""
            INSERT INTO gestion_medica.citas 
            (paciente_id, medico_id, fecha, hora, estado) 
            VALUES (%s, %s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, hora, estado))
            conn.commit()
            conn.close()
            return {"informacion": "Cita registrada"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_cita(self, id: int, cita_actualizada: Citas):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.citas WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="La cita no se encuentra en la base de datos")
            paciente_id = cita_actualizada.paciente_id
            medico_id = cita_actualizada.medico_id
            fecha = cita_actualizada.fecha
            hora = cita_actualizada.hora
            estado = cita_actualizada.estado
            cursor.execute("""
            UPDATE gestion_medica.citas SET 
            paciente_id = %s,
            medico_id = %s,
            fecha = %s,
            hora = %s,
            estado = %s
            WHERE id = %s
            """, (paciente_id, medico_id, fecha, hora, estado, id))
            conn.commit()
            return {"informacion": "Cita actualizada"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_cita(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM gestion_medica.citas WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "La cita no se encuentra en la base de datos"}
            cursor.execute("DELETE FROM gestion_medica.citas WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE gestion_medica.citas AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Cita eliminada correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

citas_controller = CitasController()