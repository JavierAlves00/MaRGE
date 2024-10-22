import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDesktopWidget

from alt_usuarios2 import Ui_alt_usuarios


class frm_prueba_centro(QMainWindow, Ui_alt_usuarios):
    def __init__(self, parent=None):
        super(frm_prueba_centro, self).__init__(parent)
        self.setupUi(self)
        self.widget.setGeometry(int((self.widget)/2)-int(self.widget.width()/2),int((self.height())/2)-int(self.widget.height()/2) , self.widget.width(),self.widget.height())
        print(1920/2)
        print(1080/2)
        print("Ancho "+str(self.widget.width()))
        print("Alto "+str(self.widget.height()))

    def resizeEvent(self, event):
        # Llamamos a la función cuando se redimensiona el formulario
        self.on_resize()

    def on_resize(self):
        # Esta es la función que se llamará cuando se redimensione el formulario
        print("El formulario ha sido redimensionado")
        self.widget.setGeometry(int((1920 / 2)) - int(self.widget.width() / 2), int((
                    1080 / 2)) - int(self.widget.height() / 2), self.widget.width(), self.widget.height())
def main():
    app = QApplication(sys.argv)
    ventana = frm_prueba_centro()
    ventana.showMaximized()
    app.exec_()


if __name__=='__main__':
    main()
