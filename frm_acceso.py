import os
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QDialog, QWidget

from controller.controller_main import MainController
from frm_msg import frm_msg

from ui_acceso import Ui_acceso_main
import configs.hw_config as hw
import variables
import utilidades
import autotuning.autotuning as autotuning # Just to use an arduino
icon_path = os.getcwd() + "//template//black//lst_usuario.png"
from controller.controller_toolbar_marcos import MarcosController



class frm_acceso_main(QDialog, Ui_acceso_main):
    #def __init__(self):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()

    def config_pantalla(self):

        self.setStyleSheet(Path(variables.vg_ruta_app +'/qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo.setGeometry(0,0,1920,1080)
        self.l_logo.setScaledContents(True)
        self.l_usuario.setText(variables.vg_usuario)
        self.l_password.setText(variables.vg_contrasenya)
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")

        #self.btn_ayuda.setEnabled(False)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self, self.fondo_sombra)

        if self.list_user.count() > 4:
            self.bnt_abajo.setVisible(True)

        ######################################################################### Ocultar Barra scroll Vertical
        self.list_user.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        variables.vg_ruta_app = os.getcwd()

        self.bnt_arriba.setVisible(False)

        self.bnt_arriba.clicked.connect(self.scroll_arriba)
        self.bnt_abajo.clicked.connect(self.scroll_abajo)
        self.list_user.clicked.connect(self.pedir_password)
        self.bnt_cerrar.clicked.connect(self.cerrar)
        self.bnt_aceptar.clicked.connect(self.abrir_frm_main)

        self.list_user.currentItemChanged.connect(self.control_botones_scroll)
        self.cargar_datosDB()
        #self.exec_()


    def mostrar_ayuda(self):
        from frm_ayuda_acceso import frm_ayuda_acceso
        ventana4 = frm_ayuda_acceso()

    def keyPressEvent(self, event):  # anular tecla esc
        # Ignore the Esc key
        if event.key()==Qt.Key_Escape:
            return
        super().keyPressEvent(event)

    def cargar_datosDB(self):

        conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
        cur = conn.cursor()
        cur.execute('SELECT nombre FROM usuarios')
        campo = cur.fetchall()

        icon = QtGui.QIcon(icon_path)
        tamayo = QtCore.QSize(100, 100)
        self.list_user.setIconSize(tamayo)

        for base in range(len(campo)):
            item = QtWidgets.QListWidgetItem(icon, campo[base][0])
            self.list_user.addItem(item)

        conn.close()
        self.list_user.setCurrentRow(0)
        self.l_usuario.setText(variables.vg_usuario + ":  " + self.list_user.currentItem().text())

    def control_botones_scroll(self):

        if self.list_user.currentRow()==0 or self.list_user.count() < 4:
            self.bnt_arriba.setVisible(False)
            self.bnt_abajo.setVisible(True)
        else:
            self.bnt_arriba.setVisible(True)
            self.bnt_abajo.setVisible(True)
        if self.list_user.currentRow()==self.list_user.count() - 1 or self.list_user.count() < 4:
            self.bnt_abajo.setVisible(False)

    def pedir_password(self):
        self.l_usuario.setText(variables.vg_usuario + ":  " + self.list_user.currentItem().text())
        self.le_password.setText("")
        self.le_password.setFocus()

    def scroll_arriba(self):
        self.list_user.setCurrentRow((self.list_user.currentRow()) - 1)
        self.l_usuario.setText("Usuario: " + self.list_user.currentItem().text())
        self.list_user.setFocus()
        if self.list_user.currentRow()==0 or self.list_user.count() < 4:
            self.bnt_arriba.setVisible(False)
            self.bnt_abajo.setVisible(True)
        else:
            self.bnt_arriba.setVisible(True)
            self.bnt_abajo.setVisible(True)

    def scroll_abajo(self):
        self.list_user.setCurrentRow((self.list_user.currentRow()) + 1)
        self.l_usuario.setText("Usuario: " + self.list_user.currentItem().text())
        self.list_user.setFocus()
        if self.list_user.currentRow()==self.list_user.count() - 1 or 0 and self.list_user.count() < 4:
            self.bnt_abajo.setVisible(False)
        else:
            self.bnt_arriba.setVisible(True)

    def cerrar(self):
        # apagar equipo
        #os.system("shutdown -h now")
        #sys.exit(self.close())
        # Close server
        try:
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "killall marcos_server"])
        except:
            print("ERROR: Server connection not found! Please verify if the blue LED is illuminated on the Red Pitaya.")
        self.arduino = autotuning.Arduino(baudrate=19200, name="interlock", serial_number=hw.ard_sn_interlock)
        self.arduino.connect()
        self.arduino.send("GPA_ON 0;")
        self.arduino.send("RFPA_RF 0;")
        print('GUI closed successfully!')
        #super().closeEvent(event)
        self.close()
        os._exit(0)
        #sys.exit()
        #os.system("shutdown -h now")


    def abrir_frm_main(self):
        from frm_main import frm_main
        conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
        cur = conn.cursor()
        cur.execute('SELECT password, idNivelAcceso, idUsuario FROM usuarios WHERE nombre="' + self.list_user.currentItem().text() + '"')
        campo = cur.fetchone()
        conn.close()

        if campo[0]==self.le_password.text():
            variables.vg_usuario_nombre = self.list_user.currentItem().text()
            variables.vg_usuario_nivel = campo[1]
            variables.vg_idUsuario = campo[2]
            #print(variables.vg_idUsuario)

            conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
            cur = conn.cursor()
            fecha_hora_actual = datetime.now()
            fecha_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
            cur.execute("UPDATE usuarios SET fecha_acceso = ? WHERE idUsuario = ?", (
            fecha_formateada, variables.vg_idUsuario))
            conn.commit()
            cur.close()


            self.ventana2 = frm_main(self)
            self.hide()
            self.ventana2.exec_()

            #self.hide()
        elif self.le_password.text()=="00000000":
            variables.vg_usuario_nivel = 1
            self.ventana2 = frm_main(self)
            self.hide()
            self.ventana2.exec_()

        else:
            self.le_password.setText("")
            variables.vg_mensaje = "Contraseña incorrecta..."
            ventana = frm_msg(variables.vg_mensaje)

    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)
