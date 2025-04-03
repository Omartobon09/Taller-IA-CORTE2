import sys
from PyQt6.QtWidgets import QApplication
from app.login import Login
from app.home import Home
# from database.database import conectar_bd

if __name__== "__main__":
    app = QApplication([])
    
    # conexion = conectar_bd()
    
    login = Login()
    
    if login.exec():
        ventana_principal = Home()
        ventana_principal.show()
    
    # if conexion:
        # conexion.close() 
    
    sys.exit(app.exec())