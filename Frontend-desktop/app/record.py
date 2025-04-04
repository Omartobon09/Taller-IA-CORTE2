import sys
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QApplication
from PyQt6.QtCore import Qt, QFile, QTextStream
class Record(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Historial de Pacientes")
        self.setFixedSize(500, 400)

        self.load_styles("style.qss")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Historial de Pacientes")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.paciente_selector = QComboBox()
        self.paciente_selector.setObjectName("paciente_selector")  
        self.paciente_selector.addItems(["Seleccione un paciente", "Juan Pérez", "Ana Gómez", "Carlos Rodríguez"])
        self.paciente_selector.currentIndexChanged.connect(self.load_history)  

        self.historial_texto = QTextEdit()
        self.historial_texto.setObjectName("historial_texto") 
        self.historial_texto.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.paciente_selector)
        layout.addWidget(self.historial_texto)

        self.setLayout(layout)

    def load_history(self):
        paciente = self.paciente_selector.currentText()

        # Simulación local, quitar después de conectar la API
        historial = {
            "Juan Pérez": "📅 2024-04-01\nDiagnóstico: Hipertensión\nRecomendación: Controlar el estrés.\n\n📅 2024-05-12\nDiagnóstico: Taquicardia\nRecomendación: Evitar cafeína.",
            "Ana Gómez": "📅 2024-06-10\nDiagnóstico: Arritmia\nRecomendación: Revisar con un cardiólogo.",
            "Carlos Rodríguez": "📅 2024-03-22\nDiagnóstico: Presión baja\nRecomendación: Beber más líquidos."
        }

        self.historial_texto.setText(historial.get(paciente, "No hay historial disponible."))

        # API
        """
        if paciente != "Seleccione un paciente":
            url = f"http://aqui-api.com/historial?paciente={paciente}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    self.historial_texto.setText(data.get("historial", "No hay historial disponible."))
                else:
                    self.historial_texto.setText("Error al obtener datos de la API.")
            except requests.exceptions.RequestException:
                self.historial_texto.setText("Error de conexión con la API.")
        """

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Record()
    ventana.show()
    sys.exit(app.exec())
