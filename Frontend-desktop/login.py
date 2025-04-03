import sys, sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QFile, QTextStream
#from database import verificar_usuario

# Conectar a la base de datos
#def conectar_bd():
#    return sqlite3.connect("sistema.db")

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema Circulatorio")
        self.setGeometry(0, 0, 400, 300)
        self.setFixedSize(400,300)
        self.center_window()
        
        self.load_styles("style.qss")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self.verificar_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.input_user.text()
        contraseña = self.input_pass.text()

        if usuario == "admin" and contraseña == "1234":
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
     
       
    # Verificar si un usuario existe
    #def verificar_usuario(usuario, contraseña):
    #    conn = conectar_bd()
    #    cursor = conn.cursor()
    #
    #   cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
    #   resultado = cursor.fetchone()

    #   conn.close()
    #   return resultado is not None
    
    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
    
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Login()
    ventana.show()
    sys.exit(app.exec())
