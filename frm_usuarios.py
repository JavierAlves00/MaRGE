import os
import sqlite3
from pathlib import Path

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QApplication

import utilidades
from frm_ayuda_usuarios import frm_ayuda_usuarios
from frm_mod_usuarios import frm_mod_usuarios
#from test.main import ventana_principal
from ui_usuarios import Ui_usuarios
from frm_alt_usuarios import Ui_alt_usuarios, frm_alt_usuarios
import variables

icon_path = os.getcwd() + "//template//black//lst_usuario.png"

class frm_usuarios(QDialog, Ui_usuarios):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.cargar_datosDB()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo
        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual
        self.exec_()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.list_user.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.bnt_home.clicked.connect(self.abrir_home)
        self.bnt_nuevo.clicked.connect(self.nuevo_usuario)
        self.bnt_modificar.clicked.connect(self.modificar_usuario)
        self.l_logo.setGeometry(0, 0, 1920, 1080)
        self.l_logo.setScaledContents(True)
        self.bnt_arriba.setVisible(False)
        self.bnt_arriba.clicked.connect(self.scroll_arriba)
        self.bnt_abajo.clicked.connect(self.scroll_abajo)
        self.bnt_ayuda.clicked.connect(self.mostrar_ayuda)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self, self.fondo_sombra)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  " + variables.vg_usuario_nombre)

        self.list_user.currentItemChanged.connect(self.actualizar_idUsuario)

    def actualizar_idUsuario(self):
        item = self.list_user.currentItem()
        # Obtiene el dato de la segunda columna
        data = item.data(Qt.UserRole + 1)
        variables.vg_idUsuario = data

    def cargar_datosDB(self):
        conn = sqlite3.connect(variables.vg_ruta_app+'/db/physioMRI.db')
        cur = conn.cursor()
        cur.execute('SELECT nombre, idUsuario FROM usuarios')
        campo = cur.fetchall()
        icon = QtGui.QIcon(icon_path)
        tamayo = QtCore.QSize(65, 65)
        self.list_user.setIconSize(tamayo)


        for base in range(len(campo)):
            item = QtWidgets.QListWidgetItem(icon, campo[base][0])
            item.setData(Qt.UserRole + 1, campo[base][1])
            self.list_user.addItem(item)

        conn.close()
        self.list_user.setCurrentRow(0)

    def control_botones_scroll(self):
        if self.list_user.currentRow()==0 or self.list_user.count() < 4:
            self.bnt_arriba.setVisible(False)
            self.bnt_abajo.setVisible(True)
        else:
            self.bnt_arriba.setVisible(True)
            self.bnt_abajo.setVisible(True)
        if self.list_user.currentRow()==self.list_user.count() - 1 or self.list_user.count() < 4:
            self.bnt_abajo.setVisible(False)


    def scroll_arriba(self):
        self.list_user.setCurrentRow((self.list_user.currentRow()) - 1)
        self.list_user.setFocus()
        if self.list_user.currentRow()==0 or self.list_user.count() < 4:
            self.bnt_arriba.setVisible(False)
            self.bnt_abajo.setVisible(True)
        else:
            self.bnt_arriba.setVisible(True)
            self.bnt_abajo.setVisible(True)

    def scroll_abajo(self):
        self.list_user.setCurrentRow((self.list_user.currentRow()) + 1)
        self.list_user.setFocus()
        if self.list_user.currentRow()==self.list_user.count() - 1 or 0 and self.list_user.count() < 4:
            self.bnt_abajo.setVisible(False)
        else:
            self.bnt_arriba.setVisible(True)


    def nuevo_usuario(self):
        ventana3 = frm_alt_usuarios()

    def modificar_usuario(self):
        item = self.list_user.currentItem()
        # Obtiene el dato de la segunda columna
        data = item.data(Qt.UserRole + 1)
        variables.vg_idUsuario = data
        ventana3 = frm_mod_usuarios()

    def abrir_home(self):
        self.close()

    def mostrar_ayuda(self):
        ventana3 = frm_ayuda_usuarios()

    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)

