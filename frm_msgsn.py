import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from pathlib import Path
import utilidades
from PyQt5.QtCore import Qt
from ui_msgsn import Ui_msgsn


class frm_msgsn(QMainWindow, Ui_msgsn):
    def __init__(self,txt_msg):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.exec_()


    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn_aceptar.clicked.connect(self.cerrar_msg)
        # self.l_msg.setText()
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_rojo(self, self.fondo_sombra)


    def cerrar_msg(self):
        self.close()
