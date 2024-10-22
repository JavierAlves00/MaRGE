import sqlite3
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import utilidades
from frm_ayuda_acceso import frm_ayuda_acceso
from frm_msg import frm_msg
from ui_mod_usuarios import Ui_mod_usuarios
from pathlib import Path
from PyQt5.QtCore import Qt

import variables

class frm_mod_usuarios(QDialog, Ui_mod_usuarios):
    def __init__(self, parent=None):
        super(frm_mod_usuarios, self).__init__(parent)
        self.setupUi(self)
        self.config_pantalla()
        self.mostrar_datos_usuario()
        self.exec_()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo.setGeometry(0,0,1920,1080)
        self.l_logo.setScaledContents(True)
        self.btn_aceptar.clicked.connect(self.modificar_datos)
        self.btn_cancelar.clicked.connect(self.cerrar_mod_usuarios)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.le_nombre.setFocus()
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self,self.fondo_sombra)

        #self.btn_ayuda.setEnabled(False)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

    def mostrar_ayuda(self):
        from frm_ayuda_mod_usuarios import frm_ayuda_mod_usuarios
        ventana5 = frm_ayuda_mod_usuarios()
    def mostrar_datos_usuario(self):
        conn = sqlite3.connect(variables.vg_ruta_app+'/db/physioMRI.db')
        cur = conn.cursor()
        query = 'SELECT * FROM usuarios Where idUsuario=?'
        cur.execute(query, (variables.vg_idUsuario,))
        campo = cur.fetchone()
        cur.close()
        self.le_nombre.setText(campo[1])
        self.le_password.setText(campo[2])
        self.le_password2.setText(campo[2])
        self.cb_acceso.setCurrentIndex(campo[3]-1)

    def modificar_datos(self):
        conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
        cur = conn.cursor()
        if self.le_password.text()==self.le_password2.text():
            fecha_hora_actual = datetime.now()
            fecha_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
            cur.execute("UPDATE usuarios SET nombre = ?, password = ?, fecha_modificacion = ?, idNivelAcceso = ? WHERE idUsuario = ?", (self.le_nombre.text(), self.le_password.text(), fecha_formateada ,self.cb_acceso.currentIndex()+1, variables.vg_idUsuario))
            conn.commit()
            cur.close()
            self.close()
        else:
            ventana = frm_msg(variables.msg_contrasenya2)

    def cerrar_mod_usuarios(self):
        self.close()

    def ayuda_usuarios(self):
        pass




