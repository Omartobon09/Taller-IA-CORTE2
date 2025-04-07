import sys
import cv2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QFile, QTextStream
import requests
from ultralytics import YOLO
from datetime import datetime

pacientes_db = {}
API_URL = "http://localhost:8000/get/usuario/documento/"
HISTORIAL_URL = "http://localhost:8000/post/historiales"


class Patient(QWidget):
    def __init__(self, token=None, medico_id=None):
        super().__init__()
        self.setWindowTitle("Gestión de Pacientes")
        self.setFixedSize(600, 550)

        # Token y ID de médico recibidos del login
        self.token = token
        self.medico_id = medico_id

        # Cargar modelo YOLOv8
        self.yolo_model = YOLO("yolov8n.pt")
        
        # Variable para almacenar el ID del paciente actual
        self.paciente_id = None

        self.load_styles("style.qss")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Gestión de Pacientes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.doc_label = QLabel("Documento del Paciente:")
        self.doc_input = QLineEdit()
        self.doc_input.setPlaceholderText("Ingrese el documento del paciente")

        self.btn_search = QPushButton("Buscar")
        self.btn_search.clicked.connect(self.search_patient)

        self.name_label = QLabel("Nombre del Paciente:")
        self.name_display = QLineEdit()
        self.name_display.setReadOnly(True)
        self.name_display.setPlaceholderText("Nombre aparecerá aquí")

        self.diagnosis_label = QLabel("Diagnóstico:")
        self.diagnosis_text = QTextEdit()

        self.recommendation_label = QLabel("Recomendación:")
        self.recommendation_text = QTextEdit()

        self.btn_save = QPushButton("Guardar")
        self.btn_save.clicked.connect(self.save_data)

        self.image_label = QLabel()
        self.image_label.setFixedSize(250, 250)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setScaledContents(True)

        self.btn_camera = QPushButton("Tomar Foto")
        self.btn_camera.clicked.connect(self.open_camera)

        self.btn_upload = QPushButton("Cargar Imagen")
        self.btn_upload.clicked.connect(self.upload_image)

        layout.addWidget(title)
        layout.addWidget(self.doc_label)
        layout.addWidget(self.doc_input)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_display)
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
        doc = self.doc_input.text().strip()

        if not doc:
            QMessageBox.warning(self, "Error", "Ingrese un documento válido.")
            return

        try:
            response = requests.get(API_URL + doc)
            data = response.json()
            resultado = data.get("resultado")

            if isinstance(resultado, dict):
                self.name_display.setText(resultado.get("nombre", ""))
                # Guardar el ID del paciente para usarlo al guardar el historial
                self.paciente_id = resultado.get("id")
                QMessageBox.information(
                    self, "Paciente encontrado", "Datos cargados correctamente.")
            else:
                QMessageBox.warning(self, "No encontrado",
                                    "Paciente no encontrado.")
                self.name_display.clear()
                self.paciente_id = None

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo conectar a la API.\n{e}")

    def save_data(self):
        if not self.token or not self.medico_id:
            QMessageBox.warning(
                self, "Error", "No hay sesión activa. Por favor, inicie sesión nuevamente.")
            return
            
        if not self.paciente_id:
            QMessageBox.warning(
                self, "Error", "Debe buscar un paciente válido primero.")
            return
            
        doc = self.doc_input.text().strip()
        diagnosis = self.diagnosis_text.toPlainText().strip()
        recommendation = self.recommendation_text.toPlainText().strip()
        nombre = self.name_display.text().strip()

        if not doc or not diagnosis or not recommendation or not nombre:
            QMessageBox.warning(
                self, "Error", "Todos los campos son obligatorios.")
            return

        # Guardar en base de datos local
        pacientes_db[doc] = {
            "nombre": nombre,
            "diagnostico": diagnosis,
            "recomendacion": recommendation,
            "imagen": pacientes_db.get(doc, {}).get("imagen", None)
        }
        
        # Preparar datos para enviar a la API
        historial_data = {
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "diagnostico": diagnosis,
            "recomendaciones": recommendation,
            "fecha": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                HISTORIAL_URL,
                json=historial_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code in (200, 201):
                QMessageBox.information(
                    self, "Éxito", "Historial médico registrado correctamente en la base de datos.")
                # Limpiar los campos después de guardar
                self.diagnosis_text.clear()
                self.recommendation_text.clear()
            else:
                QMessageBox.warning(
                    self, "Error", f"No se pudo registrar el historial. Error: {response.status_code}\n{response.text}")
                
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al conectar con el servidor:\n{str(e)}")

    def open_camera(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            QMessageBox.critical(self, "Error", "No se pudo abrir la cámara.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Aplicar detección con YOLO
            results = self.yolo_model.predict(frame, verbose=False)
            annotated_frame = results[0].plot()

            cv2.imshow(
                "Detección con YOLOv8 - 's' para guardar, 'q' para salir", annotated_frame)
            key = cv2.waitKey(1)

            if key == ord('s'):
                image_path = "captured_image.jpg"
                cv2.imwrite(image_path, annotated_frame)
                self.display_image(image_path)
                self.save_image_to_local_db(image_path)
                break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            # Aplicar detección con YOLO
            results = self.yolo_model.predict(file_path, verbose=False)
            annotated_img = results[0].plot()

            output_path = "detected_image.jpg"
            cv2.imwrite(output_path, annotated_img)

            self.display_image(output_path)
            self.save_image_to_local_db(output_path)

    def save_image_to_local_db(self, image_path):
        doc = self.doc_input.text().strip()
        if not doc:
            QMessageBox.warning(
                self, "Error", "Ingrese un documento antes de subir la imagen.")
            return

        if doc in pacientes_db:
            pacientes_db[doc]["imagen"] = image_path
        else:
            pacientes_db[doc] = {"imagen": image_path}

        QMessageBox.information(
            self, "Éxito", "Imagen guardada correctamente.")

    def display_image(self, path):
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(
            self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())