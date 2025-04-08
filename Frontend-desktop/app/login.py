import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QPixmap

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema Circulatorio")
        self.setGeometry(0, 0, 400, 400)  # Aumenté un poco el tamaño vertical
        self.setFixedSize(400, 400)
        self.center_window()
        
        self.token = None
        self.user_id = None
        
        self.load_styles("style.qss")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Más espacio entre elementos
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título con estilo
        self.title_label = QLabel("Sistema Médico")
        self.title_label.setObjectName("login_title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Separador horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #3498DB;")
        separator.setFixedHeight(2)
        
        # Sección de datos de acceso
        access_label = QLabel("Acceso al Sistema")
        access_label.setObjectName("access_subtitle")
        access_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Ingrese su nombre de usuario")
        
        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText("Ingrese su contraseña")
        
        # Botón de login con ID para estilos específicos
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.clicked.connect(self.verificar_login)
        
        # Añadiendo widgets al layout
        layout.addWidget(self.title_label)
        layout.addWidget(separator)
        layout.addWidget(access_label)
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)
        
        # Centrar el botón
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_login)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Pie de página
        footer = QLabel("© 2024 - Sistema Circulatorio")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        layout.addStretch()
        layout.addWidget(footer)
        
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
                        self, "Éxito", f"Bienvenido al Sistema")
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