import sys
import cv2 
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QFile, QTextStream
import requests 

# Diccionario local para simular la base de datos de pacientes
pacientes_db = {}


class Patient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Pacientes")
        self.setFixedSize(600, 500)

        self.load_styles("style.qss")
        self.init_ui()

    def init_ui(self):
        """ Configuración de la interfaz gráfica """
        layout = QVBoxLayout()

        title = QLabel("Gestión de Pacientes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.doc_label = QLabel("Documento del Paciente:")
        self.doc_input = QLineEdit()
        self.doc_input.setPlaceholderText("Ingrese el documento del paciente")

        self.btn_search = QPushButton("Buscar")
        self.btn_search.clicked.connect(self.search_patient)

        self.diagnosis_label = QLabel("Diagnóstico:")
        self.diagnosis_text = QTextEdit()

        self.recommendation_label = QLabel("Recomendación:")
        self.recommendation_text = QTextEdit()

        self.btn_save = QPushButton("Guardar")
        self.btn_save.clicked.connect(self.save_data)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("border: 2px solid gray;")
        self.image_label.setScaledContents(True)

        self.btn_camera = QPushButton("Tomar Foto")
        self.btn_camera.clicked.connect(self.open_camera)

        self.btn_upload = QPushButton("Cargar Imagen")
        self.btn_upload.clicked.connect(self.upload_image)

        layout.addWidget(title)
        layout.addWidget(self.doc_label)
        layout.addWidget(self.doc_input)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.diagnosis_label)
        layout.addWidget(self.diagnosis_text)
        layout.addWidget(self.recommendation_label)
        layout.addWidget(self.recommendation_text)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_camera)
        layout.addWidget(self.btn_upload)

        self.setLayout(layout)

    def search_patient(self):
        """ Busca un paciente en la base de datos local o API (desactivada) """
        doc = self.doc_input.text().strip()

        if not doc:
            QMessageBox.warning(self, "Error", "Ingrese un documento válido.")
            return

        # Buscar en el diccionario local
        if doc in pacientes_db:
            paciente = pacientes_db[doc]
            self.diagnosis_text.setText(paciente.get("diagnostico", ""))
            self.recommendation_text.setText(paciente.get("recomendacion", ""))
            QMessageBox.information(self, "Paciente encontrado", "Datos cargados correctamente.")
        else:
            QMessageBox.warning(self, "No encontrado", "Paciente no encontrado.")

        """
        # API 
        try:
            response = requests.get(f"http://tu-api.com/pacientes/{doc}")
            if response.status_code == 200:
                data = response.json()
                self.diagnosis_text.setText(data["diagnostico"])
                self.recommendation_text.setText(data["recomendacion"])
                QMessageBox.information(self, "Paciente encontrado", "Datos cargados correctamente.")
            else:
                QMessageBox.warning(self, "No encontrado", "Paciente no encontrado en la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar con la API: {e}")
        """

    def save_data(self):
        """ Guarda los datos del paciente en la base de datos local o API (desactivada) """
        doc = self.doc_input.text().strip()
        diagnosis = self.diagnosis_text.toPlainText().strip()
        recommendation = self.recommendation_text.toPlainText().strip()

        if not doc or not diagnosis or not recommendation:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Guardar en el diccionario local
        pacientes_db[doc] = {
            "diagnostico": diagnosis,
            "recomendacion": recommendation,
            "imagen": None  
        }

        QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")

        """
        # API
        try:
            response = requests.post("http://tu-api.com/pacientes", json={
                "documento": doc,
                "diagnostico": diagnosis,
                "recomendacion": recommendation
            })
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Datos guardados en la API correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudieron guardar los datos en la API.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar con la API: {e}")
        """

    def open_camera(self):
        """ Abre la cámara, toma una foto y la almacena localmente """
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            QMessageBox.critical(self, "Error", "No se pudo abrir la cámara.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            self.display_image(image_path)
            self.save_image_to_local_db(image_path)
        else:
            QMessageBox.warning(self, "Error", "No se pudo capturar la imagen.")

    def upload_image(self):
        """ Imagen guardarla localmente """
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")

        if file_path:
            self.display_image(file_path)
            self.save_image_to_local_db(file_path)

    def save_image_to_local_db(self, image_path):
        """ Guarda la imagen en la base de datos local o API (desactivada) """
        doc = self.doc_input.text().strip()
        if not doc:
            QMessageBox.warning(self, "Error", "Ingrese un documento antes de subir la imagen.")
            return

        if doc in pacientes_db:
            pacientes_db[doc]["imagen"] = image_path
            QMessageBox.information(self, "Éxito", "Imagen guardada correctamente.")

        """
        # API
        try:
            files = {'file': open(image_path, 'rb')}
            response = requests.post(f"http://tu-api.com/pacientes/{doc}/imagen", files=files)
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Imagen subida correctamente a la API.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo subir la imagen a la API.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar con la API: {e}")
        """

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            
    def display_image(self, path):
        """ imagenen en la interfaz """
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Patient()
    ventana.show()
    sys.exit(app.exec())
