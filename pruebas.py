import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QGridLayout, QDesktopWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear los widgets
        self.textbox1 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        self.button1 = QPushButton('Button 1', self)
        self.button2 = QPushButton('Button 2', self)
        self.button3 = QPushButton('Button 3', self)

        # Crear el layout
        layout = QGridLayout()

        # Añadir widgets al layout y centrar
        layout.addWidget(self.textbox1, 0, 0)
        layout.addWidget(self.textbox2, 0, 1)
        layout.addWidget(self.textbox3, 0, 2)
        layout.addWidget(self.button1, 1, 0)
        layout.addWidget(self.button2, 1, 1)
        layout.addWidget(self.button3, 1, 2)

      #  layout.setColumnStretch(0, 1)
      #  layout.setColumnStretch(1, 1)
      #  layout.setColumnStretch(2, 1)

        # Establecer el layout principal de la ventana
        self.setLayout(layout)

        # Configurar la ventana
        self.setWindowTitle('Centrar Formulario')
        self.resize(400, 200)
        self.center()
        self.show()

    def center(self):
        # Obtener el rectángulo de la pantalla
        qr = self.frameGeometry()
        # Obtener el centro de la pantalla
        cp = QDesktopWidget().availableGeometry().center()
        # Mover el rectángulo de la ventana al centro de la pantalla
        qr.moveCenter(cp)
        # Mover la ventana al rectángulo centrado
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
