import sys
from pathlib import Path
import utilidades
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect, QVBoxLayout

import variables
from ui_msg import Ui_msg


class frm_msg(QDialog, Ui_msg):
    def __init__(self, txt_msg):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.exec_()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.bnt_aceptar.clicked.connect(self.cerrar_msg)
        self.l_msg.setText(str(variables.vg_mensaje))
        self.fondo_sombra.setGeometry(self.frame.x(),self.frame.y(),self.frame.width(),self.frame.height())
        utilidades.sombra_frame_rojo(self,self.fondo_sombra)

    def cerrar_msg(self):
        self.close()

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_msg("")
    sys.exit(app.exec())
"""