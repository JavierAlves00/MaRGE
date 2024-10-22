from pathlib import Path
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog

import utilidades
import variables

from ui_configuracion import Ui_config


class frm_config(QDialog, Ui_config):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.configuracion()

        self.exec_()

    def configuracion(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo_2.setGeometry(0, 0, 1920, 1080)
        self.l_logo_2.setScaledContents(True)
        self.bnt_home.clicked.connect(self.abrir_home)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self,self.fondo_sombra)
        self.cb_idioma.setFocus()



    def abrir_home(self):
        self.close()


