import sys
import time
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog

import utilidades
import variables
from frm_ayuda_acceso import frm_ayuda_acceso
from frm_buscar_exp import frm_buscar_exp
from frm_nuevo_exp import frm_nuevo_exp

from ui_main import Ui_frm_main
from frm_config import frm_config
from frm_usuarios import frm_usuarios
import warnings
import subprocess
import configs.hw_config as hw
import experiment as ex
import numpy as np
import autotuning.autotuning as autotuning # Just to use an arduino
import platform

class frm_main(QDialog, Ui_frm_main):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo
        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual

    def config_pantalla(self):
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1020))
        self.l_logo.setGeometry(0,0,1920,1080)
        self.l_logo.setScaledContents(True)
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.btn_cerrar.clicked.connect(self.cerrar_aplicacion)
        #self.btn_cerrar.clicked.connect(self.close)
        self.btn_config.clicked.connect(self.abrir_config)
        self.btn_usuarios.clicked.connect(self.abrir_usuarios)
        self.btn_nuevo.clicked.connect(self.abrir_nuevo_exp)
        self.btn_consultar.clicked.connect(self.abrir_buscar_exp)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  "+variables.vg_usuario_nombre)

        self.btn_config.setEnabled(False)
        #self.btn_ayuda.setEnabled(False)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

        #------------   botones que se hacen visibles o no, dependiendo del nivel de acceso del usuario ----------

        if variables.vg_usuario_nivel == 1:
            self.btn_usuarios.setVisible(True)
            self.btn_config.setVisible(True)
        else:
            self.btn_usuarios.setVisible(False)
            self.btn_config.setVisible(False)

        # --------------------------------------------------------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.frame.setGeometry(QtCore.QRect(10, 20, 1901, 151))

    def mostrar_ayuda(self):
        from frm_ayuda_main import frm_ayuda_main
        ventana5 = frm_ayuda_main()

    def keyPressEvent(self, event):
        # Ignore the Esc key
        if event.key() == Qt.Key_Escape:
            return
        super().keyPressEvent(event)

    def abrir_nuevo_exp(self):
        ventana3 = frm_nuevo_exp()
        ventana3.exec_()

    def abrir_config(self):
        ventana3 = frm_config()

    def abrir_usuarios(self):
        ventana3 = frm_usuarios()

    def cerrar_aplicacion(self):
        self.close()
        from frm_acceso import frm_acceso_main
        ventana3 = frm_acceso_main()
        ventana3.le_password.setText("")
        ventana3.exec_()

    def abrir_buscar_exp(self):
        self.ventana3 = frm_buscar_exp(self)
        self.ventana3.exec_()

    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)
