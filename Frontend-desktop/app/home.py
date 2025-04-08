import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                            QWidget, QPushButton, QHBoxLayout, QDialog, 
                            QTextEdit, QScrollArea)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QFile, QTextStream
from app.about import About
from app.record import Record
from app.patient import Patient


class DiseaseInfoDialog(QDialog):
    def __init__(self, title, info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Área con scroll para mostrar información extensa
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(info)
        
        scroll_area.setWidget(text_edit)
        layout.addWidget(scroll_area)
        
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)


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
        
        # Definir la información de las enfermedades
        self.disease_info = {
            "hipertension": {
                "title": "Hipertensión Arterial",
                "info": """
                <h2>Hipertensión Arterial</h2>
                <p><strong>Definición:</strong> La hipertensión arterial es una condición médica crónica caracterizada por la elevación persistente de la presión arterial en las arterias.</p>
                
                <h3>Valores de referencia:</h3>
                <ul>
                    <li>Normal: &lt;120/80 mmHg</li>
                    <li>Elevada: 120-129/&lt;80 mmHg</li>
                    <li>Hipertensión Etapa 1: 130-139/80-89 mmHg</li>
                    <li>Hipertensión Etapa 2: ≥140/90 mmHg</li>
                    <li>Crisis hipertensiva: &gt;180/120 mmHg</li>
                </ul>
                
                <h3>Síntomas:</h3>
                <p>Generalmente asintomática, pero puede presentar:</p>
                <ul>
                    <li>Dolor de cabeza intenso</li>
                    <li>Visión borrosa</li>
                    <li>Mareos</li>
                    <li>Fatiga</li>
                    <li>Dificultad respiratoria</li>
                </ul>
                
                <h3>Factores de riesgo:</h3>
                <ul>
                    <li>Edad avanzada</li>
                    <li>Antecedentes familiares</li>
                    <li>Sobrepeso y obesidad</li>
                    <li>Consumo elevado de sodio</li>
                    <li>Sedentarismo</li>
                    <li>Consumo excesivo de alcohol</li>
                    <li>Estrés crónico</li>
                </ul>
                
                <h3>Tratamiento:</h3>
                <ul>
                    <li><strong>Cambios en el estilo de vida:</strong> Dieta baja en sodio, actividad física regular, pérdida de peso si es necesario.</li>
                    <li><strong>Farmacológico:</strong> Diuréticos, IECA, ARA-II, bloqueadores de canales de calcio, betabloqueadores.</li>
                    <li><strong>Monitoreo:</strong> Control periódico de la presión arterial.</li>
                </ul>
                
                <h3>Complicaciones:</h3>
                <ul>
                    <li>Enfermedad coronaria</li>
                    <li>Insuficiencia cardíaca</li>
                    <li>Accidente cerebrovascular</li>
                    <li>Enfermedad renal crónica</li>
                    <li>Retinopatía hipertensiva</li>
                </ul>
                """
            },
            "arritmias": {
                "title": "Arritmias Cardíacas",
                "info": """
                <h2>Arritmias Cardíacas</h2>
                <p><strong>Definición:</strong> Las arritmias son alteraciones del ritmo cardíaco normal. Ocurren cuando los impulsos eléctricos que coordinan los latidos del corazón no funcionan adecuadamente.</p>
                
                <h3>Tipos principales:</h3>
                <ul>
                    <li><strong>Taquicardia:</strong> Ritmo cardíaco rápido (&gt;100 latidos por minuto)</li>
                    <li><strong>Bradicardia:</strong> Ritmo cardíaco lento (&lt;60 latidos por minuto)</li>
                    <li><strong>Fibrilación auricular:</strong> Latidos irregulares en las aurículas</li>
                    <li><strong>Fibrilación ventricular:</strong> Latidos rápidos e irregulares en los ventrículos</li>
                    <li><strong>Extrasístoles:</strong> Latidos prematuros o adicionales</li>
                </ul>
                
                <h3>Síntomas:</h3>
                <ul>
                    <li>Palpitaciones (sensación de aleteo o golpeteo en el pecho)</li>
                    <li>Latidos saltados o pausas</li>
                    <li>Mareo o aturdimiento</li>
                    <li>Desmayo (síncope)</li>
                    <li>Fatiga</li>
                    <li>Dificultad para respirar</li>
                    <li>Dolor en el pecho</li>
                </ul>
                
                <h3>Factores de riesgo:</h3>
                <ul>
                    <li>Enfermedad cardíaca coronaria</li>
                    <li>Presión arterial alta</li>
                    <li>Diabetes</li>
                    <li>Edad avanzada</li>
                    <li>Consumo de alcohol o cafeína en exceso</li>
                    <li>Drogas o medicamentos</li>
                    <li>Trastornos tiroideos</li>
                    <li>Apnea del sueño</li>
                </ul>
                
                <h3>Diagnóstico:</h3>
                <ul>
                    <li>Electrocardiograma (ECG)</li>
                    <li>Holter (monitoreo ECG por 24-48 horas)</li>
                    <li>Monitor de eventos cardíacos</li>
                    <li>Prueba de esfuerzo</li>
                    <li>Ecocardiograma</li>
                    <li>Estudio electrofisiológico</li>
                </ul>
                
                <h3>Tratamiento:</h3>
                <ul>
                    <li><strong>Medicamentos:</strong> Antiarrítmicos, betabloqueadores, anticoagulantes</li>
                    <li><strong>Cardioversión:</strong> Procedimiento para restaurar el ritmo normal</li>
                    <li><strong>Ablación por catéter:</strong> Destrucción del tejido cardíaco causante de la arritmia</li>
                    <li><strong>Marcapasos:</strong> Dispositivo para regular el ritmo cardíaco</li>
                    <li><strong>Desfibrilador:</strong> Dispositivo para corregir ritmos peligrosos</li>
                </ul>
                """
            },
            "infartos": {
                "title": "Infarto de Miocardio",
                "info": """
                <h2>Infarto de Miocardio (Ataque Cardíaco)</h2>
                <p><strong>Definición:</strong> Un infarto de miocardio ocurre cuando el flujo sanguíneo que lleva oxígeno al músculo cardíaco se reduce o se bloquea completamente, causando daño al tejido cardíaco.</p>
                
                <h3>Causas principales:</h3>
                <ul>
                    <li>Aterosclerosis (acumulación de placa en las arterias coronarias)</li>
                    <li>Trombosis coronaria (coágulo sanguíneo)</li>
                    <li>Espasmo coronario (contracción súbita de una arteria coronaria)</li>
                </ul>
                
                <h3>Síntomas:</h3>
                <ul>
                    <li><strong>Dolor o malestar en el pecho:</strong> Sensación de presión, opresión, dolor intenso o ardor</li>
                    <li>Dolor que irradia a los brazos (especialmente el izquierdo), hombro, espalda, cuello, mandíbula o estómago</li>
                    <li>Dificultad para respirar</li>
                    <li>Sudoración fría y profusa</li>
                    <li>Náuseas y vómitos</li>
                    <li>Mareo o aturdimiento</li>
                    <li>Fatiga inusual</li>
                </ul>
                
                <h3>Factores de riesgo:</h3>
                <ul>
                    <li>Edad (hombres &gt;45 años, mujeres &gt;55 años)</li>
                    <li>Tabaquismo</li>
                    <li>Hipertensión arterial</li>
                    <li>Colesterol elevado</li>
                    <li>Diabetes</li>
                    <li>Obesidad</li>
                    <li>Sedentarismo</li>
                    <li>Antecedentes familiares</li>
                    <li>Estrés crónico</li>
                </ul>
                
                <h3>Diagnóstico:</h3>
                <ul>
                    <li>Electrocardiograma (ECG)</li>
                    <li>Análisis de sangre para marcadores cardíacos (troponinas)</li>
                    <li>Ecocardiograma</li>
                    <li>Cateterismo cardíaco</li>
                    <li>Tomografía computarizada o resonancia magnética</li>
                </ul>
                
                <h3>Tratamiento:</h3>
                <ul>
                    <li><strong>Inmediato:</strong> Aspirina, terapia trombolítica, angioplastia coronaria</li>
                    <li><strong>Medicamentos:</strong> Antiagregantes plaquetarios, betabloqueadores, estatinas, IECA</li>
                    <li><strong>Procedimientos invasivos:</strong> Angioplastia con stent, cirugía de bypass coronario</li>
                    <li><strong>Rehabilitación cardíaca:</strong> Programa supervisado de ejercicio y educación</li>
                </ul>
                
                <h3>Prevención secundaria:</h3>
                <ul>
                    <li>Cambios en el estilo de vida</li>
                    <li>Control de factores de riesgo</li>
                    <li>Adherencia al tratamiento farmacológico</li>
                    <li>Seguimiento médico regular</li>
                </ul>
                """
            },
            "trombosis": {
                "title": "Trombosis",
                "info": """
                <h2>Trombosis</h2>
                <p><strong>Definición:</strong> La trombosis es la formación de un coágulo sanguíneo (trombo) dentro de un vaso sanguíneo, obstruyendo el flujo de sangre a través del sistema circulatorio.</p>
                
                <h3>Tipos principales:</h3>
                <ul>
                    <li><strong>Trombosis Venosa Profunda (TVP):</strong> Formación de coágulos en venas profundas, generalmente en las piernas</li>
                    <li><strong>Tromboembolismo Pulmonar (TEP):</strong> Coágulo que viaja a los pulmones</li>
                    <li><strong>Trombosis Arterial:</strong> Coágulos en arterias que pueden causar infartos o accidentes cerebrovasculares</li>
                </ul>
                
                <h3>Síntomas:</h3>
                <p><strong>Trombosis Venosa Profunda:</strong></p>
                <ul>
                    <li>Dolor e inflamación en la extremidad afectada</li>
                    <li>Enrojecimiento y calor en la zona</li>
                    <li>Sensibilidad al tacto</li>
                    <li>Venas superficiales dilatadas</li>
                </ul>
                
                <p><strong>Tromboembolismo Pulmonar:</strong></p>
                <ul>
                    <li>Dificultad respiratoria súbita</li>
                    <li>Dolor torácico que empeora al respirar</li>
                    <li>Tos (a veces con sangre)</li>
                    <li>Taquicardia</li>
                    <li>Mareo o desmayo</li>
                </ul>
                
                <h3>Factores de riesgo:</h3>
                <ul>
                    <li>Inmovilización prolongada</li>
                    <li>Cirugía reciente</li>
                    <li>Cáncer</li>
                    <li>Obesidad</li>
                    <li>Embarazo y posparto</li>
                    <li>Anticonceptivos orales o terapia hormonal</li>
                    <li>Edad avanzada</li>
                    <li>Trastornos de coagulación hereditarios</li>
                    <li>Tabaquismo</li>
                    <li>Traumatismos</li>
                </ul>
                
                <h3>Diagnóstico:</h3>
                <ul>
                    <li>Ecografía Doppler</li>
                    <li>Análisis de sangre (dímero D)</li>
                    <li>Venografía</li>
                    <li>Angiografía pulmonar por TC</li>
                    <li>Gammagrafía de ventilación/perfusión</li>
                </ul>
                
                <h3>Tratamiento:</h3>
                <ul>
                    <li><strong>Anticoagulantes:</strong> Heparina, warfarina, anticoagulantes orales de acción directa</li>
                    <li><strong>Trombolíticos:</strong> Para disolver coágulos en casos graves</li>
                    <li><strong>Filtros de vena cava:</strong> Para prevenir el movimiento de coágulos hacia los pulmones</li>
                    <li><strong>Trombectomía:</strong> Extracción quirúrgica del coágulo</li>
                </ul>
                
                <h3>Prevención:</h3>
                <ul>
                    <li>Movilización temprana después de cirugías</li>
                    <li>Medias de compresión</li>
                    <li>Anticoagulación profiláctica en personas de alto riesgo</li>
                    <li>Hidratación adecuada</li>
                    <li>Ejercicios de piernas durante viajes largos</li>
                </ul>
                """
            }
        }
        
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
        
        welcome_label = QLabel(
            "Bienvenido al módulo principal. Aquí puedes encontrar información sobre el "
            "Sistema Circulatorio, enfermedades más comunes:"
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setWordWrap(True)
        layout.addWidget(welcome_label)
        
        # Crear botones para las enfermedades
        diseases_layout = QVBoxLayout()
        
        btn_hipertension = QPushButton("🩸 Hipertensión")
        btn_hipertension.setObjectName("disease_button")
        btn_hipertension.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_hipertension.clicked.connect(lambda: self.show_disease_info("hipertension"))
        diseases_layout.addWidget(btn_hipertension)
        
        btn_arritmias = QPushButton("❤️ Arritmias")
        btn_arritmias.setObjectName("disease_button")
        btn_arritmias.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_arritmias.clicked.connect(lambda: self.show_disease_info("arritmias"))
        diseases_layout.addWidget(btn_arritmias)
        
        btn_infartos = QPushButton("🫀 Infartos")
        btn_infartos.setObjectName("disease_button")
        btn_infartos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_infartos.clicked.connect(lambda: self.show_disease_info("infartos"))
        diseases_layout.addWidget(btn_infartos)
        
        btn_trombosis = QPushButton("🩸 Trombosis")
        btn_trombosis.setObjectName("disease_button")
        btn_trombosis.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_trombosis.clicked.connect(lambda: self.show_disease_info("trombosis"))
        diseases_layout.addWidget(btn_trombosis)
        
        layout.addLayout(diseases_layout)
        
        instruction_label = QLabel("Utiliza el menú para explorar los módulos disponibles.")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)
        
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
    
    def show_disease_info(self, disease):
        """Muestra la información de la enfermedad seleccionada"""
        if disease in self.disease_info:
            info = self.disease_info[disease]
            dialog = DiseaseInfoDialog(info["title"], info["info"], self)
            dialog.exec()
    
    def show_about(self):
        self.about_window = About()
        self.about_window.show()
    
    def show_record(self):
        self.record_window = Record(token=self.token, medico_id=self.medico_id)
        self.record_window.show()
    
    def show_patient(self):
        self.patient_window = Patient(
            token=self.token, medico_id=self.medico_id)
        self.patient_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Agregar estilos adicionales para los botones de enfermedades
    app.setStyleSheet("""
        #disease_button {
            text-align: left;
            padding: 8px;
            margin: 3px;
            background-color: #f0f8ff;
            border: 1px solid #add8e6;
            border-radius: 5px;
        }
        
        #disease_button:hover {
            background-color: #e6f2ff;
            border: 1px solid #87ceeb;
        }
    """)
    
    ventana = Home()
    ventana.show()
    sys.exit(app.exec())