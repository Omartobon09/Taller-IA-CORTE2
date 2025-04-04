import sys
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFileDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QPixmap

class Patient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Módulo de Pacientes")
        self.setFixedSize(600, 500)

        self.load_styles("style.qss")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Gestión de Pacientes")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.doc_input = QLineEdit()
        self.doc_input.setPlaceholderText("Ingrese el documento del paciente")
        
        self.search_btn = QPushButton("Buscar Paciente")
        self.search_btn.clicked.connect(self.load_patient)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        
        self.upload_btn = QPushButton("Subir Imagen")
        self.upload_btn.clicked.connect(self.upload_image)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("No hay imagen cargada")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.upload_btn)
        
        layout.addWidget(title)
        layout.addWidget(self.doc_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.info_text)
        layout.addWidget(self.image_label)
        
        self.setLayout(layout)
    
    def load_patient(self):
        doc = self.doc_input.text().strip()
        if not doc:
            self.info_text.setText("Ingrese un documento válido.")
            return
        
        # Simulación local
        pacientes = {
            "123456": "Nombre: Juan Pérez\nDiagnóstico: Hipertensión\nRecomendación: Reducir consumo de sal.",
            "789012": "Nombre: Ana Gómez\nDiagnóstico: Arritmia\nRecomendación: Evaluación con cardiólogo.",
        }
        
        self.info_text.setText(pacientes.get(doc, "Paciente no encontrado."))
        
        # API 
        """
        url = f"http://api.example.com/paciente?doc={doc}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.info_text.setText(
                    f"Nombre: {data['nombre']}\n"
                    f"Diagnóstico: {data['diagnostico']}\n"
                    f"Recomendación: {data['recomendacion']}"
                )
            else:
                self.info_text.setText("Paciente no encontrado.")
        except requests.exceptions.RequestException:
            self.info_text.setText("Error de conexión con la API.")
        """
    
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
    
    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Patient()
    ventana.show()
    sys.exit(app.exec())
