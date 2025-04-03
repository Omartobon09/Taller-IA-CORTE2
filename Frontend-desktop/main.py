import sys
from PyQt6.QtWidgets import QApplication
from app.login import Login
# from database.database import conectar_bd

if __name__== "__main__":
    # app = QApplication(sys.argv)
    
    # conexion = conectar_bd()
    ventana_login = Login()
    ventana_login.show()
    
    # if conexion:
        # conexion.close() 
    
    sys.exit(app.exec())