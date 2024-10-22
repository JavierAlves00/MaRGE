import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit

from controller_main import MainController


class Formulario(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Crear widgets
        self.label = QLabel('Nombre:', self)
        self.textbox = QLineEdit(self)
        self.button = QPushButton('Enviar', self)

        # Conectar el botón a la función
        self.button.clicked.connect(self.on_click)

        # Crear layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        # Establecer layout
        self.setLayout(layout)

        # Configurar la ventana principal
        self.setWindowTitle('Formulario Simple')
        self.show()

    def on_click(self):
        # Obtener el texto de la caja de texto y mostrarlo en la consola
        session = [{'project': 'None', 'study': 'Phantom', 'side': 'Left', 'orientation': 'Supine', 'subject_id': '2024.06.17.15.32', 'study_id': '2024.06.17.15.32', 'subject_name': 'Name', 'subject_surname': 'Surname', 'subject_birthday': 'YY/MM/DD', 'subject_weight': 'kg', 'subject_height': 'cm', 'scanner': 'Physio V1.01', 'rf_coil': 'RF01', 'seriesNumber': 0}]
        nombre = self.textbox.text()
        variable3 = MainController(session, True)
        variable3.show()
        print(f'Hola, {nombre}!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Formulario()
    sys.exit(app.exec_())
