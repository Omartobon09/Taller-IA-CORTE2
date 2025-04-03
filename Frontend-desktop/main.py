import sys
from PyQt6.QtWidgets import QApplication
from login import Login

if __name__== "__main__":
    app = QApplication(sys.argv)
    
    ventana_login = Login()
    ventana_login.show()
    
    sys.exit(app.exec())