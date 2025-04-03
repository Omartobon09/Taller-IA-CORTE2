import mysql.connector

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña", 
            database="sistema"  
        )
        print("Conexión a MySQL establecida correctamente.")
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None
