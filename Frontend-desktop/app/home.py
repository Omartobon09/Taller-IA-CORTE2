import sys
from PyQt6.QtWidgets import QApplication,QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QFile, QTextStream


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sistema Circulatorio - Módulo Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(400,300)
        self.center_window()
        
        self.load_styles("style.qss")
        
        layout = QVBoxLayout()
        
        title = QLabel("Sistema Circulatorio")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        menu_layout = QHBoxLayout()
        btn_pacientes = QPushButton("Pacientes")
        btn_historial = QPushButton("Historial")
        btn_acerca_de = QPushButton("Acerca de")

        menu_layout.addWidget(btn_pacientes)
        menu_layout.addWidget(btn_historial)
        menu_layout.addWidget(btn_acerca_de)
        
        layout.addLayout(menu_layout)
        
        content = QLabel("Bienvenido al módulo principal. Aquí puedes encontrar información sobre el Sistema Circulatorio y sus enfermedades.")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setWordWrap(True)
        layout.addWidget(content)
        
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
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
        
        
if __name__ =="__main___":
    app = QApplication(sys.argv)
    ventana = Home()
    ventana.show()
    sys.exit(app.exec())

    