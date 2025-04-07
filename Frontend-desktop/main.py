import sys
from PyQt6.QtWidgets import QApplication
from app.login import Login
from app.home import Home
# from database.database import conectar_bd

if __name__ == "__main__":
    app = QApplication([])

    login = Login()

    if login.exec():
        # Pasar token y user_id a la ventana principal
        ventana_principal = Home(token=login.token, medico_id=login.user_id)
        ventana_principal.show()

    sys.exit(app.exec())
