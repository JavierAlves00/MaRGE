import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout
from ui.window_main import MainWindow


class DialogWithMainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog with Main Window')
        self.setGeometry(0, 0, 1920, 1080)

        # Crear un layout vertical para el diálogo
        layout = QVBoxLayout(self)

        # Crear una instancia de MainWindow
        #self.main_window = MainWindow()
        demo = True
        # Open the main gui
        self.main_window = MainWindow(None, True)
        # self.main_gui = MainController(self.session, False)
        self.main_window.show()
        # Añadir el QMainWindow directamente al layout
        layout.addWidget(self.main_window)

        # Establecer el layout del diálogo
        self.setLayout(layout)

        self.exec_()


