import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QFile, QTextStream

class About(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Acerca de")
        self.setFixedSize(400, 300)

        self.load_styles("style.qss")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Acerca de")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content = QLabel(
            "Este software fue desarrollado por Jennifer, Nicolas y Omar.\nVersión: 1.0.0\nFecha: 2024"
        )
        content.setObjectName("content")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(content)

        self.setLayout(layout)

    def load_styles(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = About()
    ventana.show()
    sys.exit(app.exec())