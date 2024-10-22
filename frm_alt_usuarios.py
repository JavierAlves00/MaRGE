from datetime import datetime
import sqlite3
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication

import utilidades
from frm_msg import frm_msg
from ui_alt_usuarios import Ui_alt_usuarios

import variables

class frm_alt_usuarios(QDialog, Ui_alt_usuarios):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.exec_()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo.setGeometry(0,0,1920,1080)
        self.l_logo.setScaledContents(True)
        self.btn_aceptar.clicked.connect(self.alta_usuario)
        self.btn_cancelar.clicked.connect(self.cerrar_alt_usuarios)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.le_nombre.setFocus()
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self,self.fondo_sombra)

        #self.btn_ayuda.setEnabled(False)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

    def mostrar_ayuda(self):
        from frm_ayuda_alt_usuarios import frm_ayuda_alt_usuarios
        ventana5 = frm_ayuda_alt_usuarios()
    def alta_usuario(self):
        conn = sqlite3.connect(variables.vg_ruta_app+'/db/physioMRI.db')
        cur = conn.cursor()
        if self.le_password.text() == self.le_password2.text():
            fecha_hora_actual = datetime.now()
            fecha_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
            cur.execute("insert into usuarios (nombre,password,idNivelAcceso,fecha_alta) values(?,?,?,?)",(self.le_nombre.text(), self.le_password.text(),self.cb_acceso.currentIndex()+1,fecha_formateada))
            conn.commit()
            cur.close()

        else:
            ventana = frm_msg(variables.msg_contrasenya2)
            #ventana = frm_msg(self.le_password.text() + ' ' + self.le_password2.text())

    def cerrar_alt_usuarios(self):
        self.close()



"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_msg()
    sys.exit(app.exec())
"""