import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QFile, QTextStream
from app.about import About
from app.record import Record
from app.patient import Patient


class Home(QMainWindow):
    def __init__(self, token=None, medico_id=None):
        super().__init__()
        self.token = token
        self.medico_id = medico_id

        self.setWindowTitle("Sistema Circulatorio - Módulo Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.center_window()

        self.load_styles("style.qss")

        layout = QVBoxLayout()

        title = QLabel("Sistema Circulatorio - CUL")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.image_label = QLabel()
        pixmap = QPixmap("assets/circulatory_system.jpg")
        self.image_label.setPixmap(pixmap.scaled(
            400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        content = QLabel(
            "Bienvenido al módulo principal. Aquí puedes encontrar información sobre el "
            "Sistema Circulatorio, enfermedades más comunes:\n\n"
            "🩸 Hipertensión\n❤️ Arritmias\n🫀 Infartos\n🩸 Trombosis\n\n"
            "Utiliza el menú para explorar los módulos disponibles."
        )
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setWordWrap(True)
        layout.addWidget(content)

        menu_layout = QHBoxLayout()
        btn_pacientes = QPushButton("Pacientes")
        btn_pacientes.clicked.connect(self.show_patient)

        btn_historial = QPushButton("Historial")
        btn_historial.clicked.connect(self.show_record)

        btn_acerca_de = QPushButton("Acerca de")
        btn_acerca_de.clicked.connect(self.show_about)

        menu_layout.addWidget(btn_pacientes)
        menu_layout.addWidget(btn_historial)
        menu_layout.addWidget(btn_acerca_de)

        layout.addLayout(menu_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)

    def show_about(self):
        self.about_window = About()
        self.about_window.show()

    def show_record(self):
        # Modificado para pasar token y medico_id
        self.record_window = Record(token=self.token, medico_id=self.medico_id)
        self.record_window.show()

    def show_patient(self):
        # Modificado para pasar token y medico_id
        self.patient_window = Patient(
            token=self.token, medico_id=self.medico_id)
        self.patient_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Home()
    ventana.show()
    sys.exit(app.exec())
