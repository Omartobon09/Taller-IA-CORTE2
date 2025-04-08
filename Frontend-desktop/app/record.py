import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QFile, QTextStream


class Record(QWidget):
    def __init__(self, token=None, medico_id=None):
        super().__init__()
        self.token = token
        self.medico_id = medico_id

        self.setWindowTitle("Historial de Pacientes")
        self.setFixedSize(500, 400)

        self.load_styles("style.qss")
        self.init_ui()

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Consultar Historial Médico")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_documento = QLineEdit()
        self.input_documento.setPlaceholderText("Ingrese documento del paciente")

        self.btn_buscar = QPushButton("Buscar Historial")
        self.btn_buscar.clicked.connect(self.buscar_historial)

        self.historial_texto = QTextEdit()
        self.historial_texto.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.input_documento)
        layout.addWidget(self.btn_buscar)
        layout.addWidget(self.historial_texto)

        self.setLayout(layout)

    def buscar_historial(self):
        documento = self.input_documento.text()
        headers = {"Authorization": f"Bearer {self.token}"}

        # Paso 1: Obtener paciente por documento
        url_paciente = f"http://127.0.0.1:8000/get/usuario/documento/{documento}"
        try:
            response_paciente = requests.get(url_paciente, headers=headers)
            if response_paciente.status_code == 200:
                datos = response_paciente.json()
                if "resultado" in datos and "id" in datos["resultado"]:
                    paciente_id = datos["resultado"]["id"]
                else:
                    self.historial_texto.setText("❌ No se encontró un paciente con ese documento.")
                    return
            else:
                self.historial_texto.setText("❌ Error al buscar el paciente.")
                return
        except requests.exceptions.RequestException:
            self.historial_texto.setText("❌ Error al conectar con el servidor.")
            return

        # Paso 2: Obtener historial por paciente_id
        url_historial = f"http://127.0.0.1:8000/get/historiales/paciente/{paciente_id}"
        try:
            response_historial = requests.get(url_historial, headers=headers)
            if response_historial.status_code == 200:
                data_historial = response_historial.json()
                if "resultado" in data_historial:
                    historiales = data_historial["resultado"]
                    
                    # Filtrar por medico_id
                    historiales_filtrados = [h for h in historiales if h["medico_id"] == self.medico_id]

                    if historiales_filtrados:
                        texto = ""
                        for h in historiales_filtrados:
                            fecha = h["fecha"].split("T")[0]  # Solo fecha
                            texto += (
                                f"📅 Fecha: {fecha}\n"
                                f"🩺 Diagnóstico: {h['diagnostico']}\n"
                                f"📋 Recomendaciones: {h['recomendaciones']}\n\n"
                            )
                        self.historial_texto.setText(texto)
                    else:
                        self.historial_texto.setText("ℹ️ No hay historiales médicos registrados por este médico.")
                else:
                    self.historial_texto.setText("❌ No se pudo interpretar la respuesta del historial.")
            else:
                self.historial_texto.setText("❌ Error al obtener el historial médico.")
        except requests.exceptions.RequestException:
            self.historial_texto.setText("❌ Error al conectar con el servidor.")
