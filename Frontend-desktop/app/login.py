import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QFile, QTextStream


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema Circulatorio")
        self.setGeometry(0, 0, 400, 300)
        self.setFixedSize(400, 300)
        self.center_window()

        self.token = None
        self.user_id = None

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

        try:
            response = requests.post(
                "http://127.0.0.1:8000/login",
                data={"username": usuario, "password": contraseña},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            if response.status_code == 200:
                self.token = response.json().get("access_token")

                # Hacer la petición para obtener los datos del usuario logueado
                user_response = requests.get(
                    "http://127.0.0.1:8000/usuario",
                    headers={"Authorization": f"Bearer {self.token}"}
                )

                if user_response.status_code == 200:
                    self.user_id = user_response.json().get("id")
                    QMessageBox.information(
                        self, "Éxito", f"Bienvenido")
                    self.accept()
                else:
                    QMessageBox.warning(
                        self, "Error", "No se pudo obtener el ID del médico")

            else:
                QMessageBox.warning(
                    self, "Error", "Usuario o contraseña incorrectos")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error de red",
                                 f"No se pudo conectar al servidor:\n{str(e)}")

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)
