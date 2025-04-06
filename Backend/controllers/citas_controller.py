from fastapi import APIRouter
import mysql.connector
from fastapi import HTTPException
from config.config import get_db_connection
from models.citas_model import Cita
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date, time


class CitasController:

    def get_citas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM citas")
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
                "SELECT * FROM citas WHERE id = %s", (id,))
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

    def get_citas_paciente(self, paciente_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM citas WHERE paciente_id = %s", (paciente_id,))
            results = cursor.fetchall()
            citas = []
            if results:
                for result in results:
                    cita = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'fecha': result[3],
                        'hora': result[4],
                        'estado': result[5]
                    }
                    citas.append(cita)
                return {"resultado": citas}
            else:
                return {"resultado": "No se encontraron citas para este paciente"}
        except Exception as error:
            return {"resultado": str(error)}

    def get_citas_medico(self, medico_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM citas WHERE medico_id = %s", (medico_id,))
            results = cursor.fetchall()
            citas = []
            if results:
                for result in results:
                    cita = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'fecha': result[3],
                        'hora': result[4],
                        'estado': result[5]
                    }
                    citas.append(cita)
                return {"resultado": citas}
            else:
                return {"resultado": "No se encontraron citas para este médico"}
        except Exception as error:
            return {"resultado": str(error)}

    def get_citas_fecha(self, fecha):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM citas WHERE fecha = %s", (fecha,))
            results = cursor.fetchall()
            citas = []
            if results:
                for result in results:
                    cita = {
                        'id': result[0],
                        'paciente_id': result[1],
                        'medico_id': result[2],
                        'fecha': result[3],
                        'hora': result[4],
                        'estado': result[5]
                    }
                    citas.append(cita)
                return {"resultado": citas}
            else:
                return {"resultado": "No se encontraron citas para esta fecha"}
        except Exception as error:
            return {"resultado": str(error)}

    def verificar_disponibilidad(self, medico_id, fecha, hora):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM citas WHERE medico_id = %s AND fecha = %s AND hora = %s",
                (medico_id, fecha, hora))
            result = cursor.fetchone()
            if result:
                return False  # No disponible
            else:
                return True  # Disponible
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    def post_cita(self, nueva_cita: Cita):
        try:
            # Verificar disponibilidad
            if not self.verificar_disponibilidad(nueva_cita.medico_id, nueva_cita.fecha, nueva_cita.hora):
                return {"resultado": "Horario no disponible para este médico"}

            conn = get_db_connection()
            cursor = conn.cursor()
            paciente_id = nueva_cita.paciente_id
            medico_id = nueva_cita.medico_id
            fecha = nueva_cita.fecha
            hora = nueva_cita.hora
            estado = nueva_cita.estado if nueva_cita.estado else "Pendiente"
            
            cursor.execute("""
            INSERT INTO citas (paciente_id, medico_id, fecha, hora, estado) 
            VALUES (%s, %s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, hora, estado))
            
            conn.commit()
            conn.close()
            return {"informacion": "Cita registrada correctamente"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_cita(self, id: int, cita_actualizada: Cita):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM citas WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="La cita no se encuentra en la base de datos")
                
            # Si cambia el médico, fecha u hora, verificar disponibilidad
            if cita_actualizada.medico_id and cita_actualizada.fecha and cita_actualizada.hora:
                cursor.execute(
                    "SELECT medico_id, fecha, hora FROM citas WHERE id = %s", (id,))
                cita_actual = cursor.fetchone()
                
                if (cita_actualizada.medico_id != cita_actual[0] or 
                    cita_actualizada.fecha != cita_actual[1] or 
                    cita_actualizada.hora != cita_actual[2]):
                    if not self.verificar_disponibilidad(
                        cita_actualizada.medico_id, 
                        cita_actualizada.fecha, 
                        cita_actualizada.hora):
                        return {"resultado": "Horario no disponible para este médico"}
            
            paciente_id = cita_actualizada.paciente_id
            medico_id = cita_actualizada.medico_id
            fecha = cita_actualizada.fecha
            hora = cita_actualizada.hora
            estado = cita_actualizada.estado
            
            cursor.execute("""
            UPDATE citas SET 
            paciente_id = %s,
            medico_id = %s,
            fecha = %s,
            hora = %s,
            estado = %s
            WHERE id = %s
            """, (paciente_id, medico_id, fecha, hora, estado, id))
            
            conn.commit()
            return {"informacion": "Cita actualizada correctamente"}
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
                "SELECT id FROM citas WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "La cita no se encuentra en la base de datos"}
            
            cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE citas AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Cita eliminada correctamente"}
        except Exception as error:
            return {"resultado": str(error)}


citas_controller = CitasController()