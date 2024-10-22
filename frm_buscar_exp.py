import os
import re
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import numpy as np
import pydicom

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon, QImage
from PyQt5.QtWidgets import QDialog, QTreeView, QTreeWidgetItem, QApplication
from pydantic import json

import utilidades
import variables
from controller.controller_main import MainController
from controller.controller_session import SessionController
from dialog import DialogWithMainWindow
from frm_msg import frm_msg
from frm_nuevo_exp import frm_nuevo_exp
from ui.window_main import MainWindow
from ui_buscar_exp import Ui_buscar_exp
from frm_scan import frm_scan
import psutil




icon_path = variables.vg_ruta_app + "/template/black/pacientes.png"
icon_path2 = variables.vg_ruta_app + "/template/black/exped.png"


lista_items_pacientes = []
lista_items_estudios = []

class frm_buscar_exp(QDialog, Ui_buscar_exp):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.cargar_datosDB()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo
        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual
        #self.exec_()
        #self.show()


    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.list_pacientes.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_estudios.setColumnCount(2)
        self.list_estudios.setHeaderHidden(True)
        # Ocultar la segunda columna
        self.list_estudios.setColumnHidden(1, True)
        self.list_estudios.setIconSize(QSize(60, 60))
        self.list_estudios.setEditTriggers(QTreeView.NoEditTriggers)

        self.list_estudios.itemClicked.connect(self.on_item_clicked)

        # Botones del formulario
        self.btn_usb.clicked.connect(self.copiar_usb)
        self.btn_usb_des.clicked.connect(self.desconectar_usb)
        self.btn_ayadir.clicked.connect(self.abrir_frm_scan)
        self.btn_ayuda.clicked.connect(self.abrir_frm_scan)
        self.btn_home.clicked.connect(self.close)
        self.btn_abajo_pacientes.clicked.connect(self.scroll_abajo_pacientes)
        self.btn_arriba_pacientes.clicked.connect(self.scroll_arriba_pacientes)


        self.btn_abajo_estudios.clicked.connect(self.scroll_abajo_estudios)
        self.btn_arriba_estudios.clicked.connect(self.scroll_arriba_estudios)



        self.btn_usb.setVisible(False)
        self.btn_usb_des.setVisible(False)

        # Actualizar visibilidad de botones al inicio
        self.actualizar_visible_botones_estudios()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo.setGeometry(0, 0, 1920, 1080)
        self.l_logo.setScaledContents(True)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self,self.fondo_sombra)


        self.le_txtbuscar.textChanged.connect(self.cargar_datosDB_filtro)
        self.list_pacientes.clicked.connect(self.actualiza_inf_pacientes)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  " + variables.vg_usuario_nombre)

        self.l_nombre_i.setStyleSheet("color: #D2E3F7;")
        self.l_1apellido_i.setStyleSheet("color: #D2E3F7;")
        self.l_2apellido_i.setStyleSheet("color: #D2E3F7;")
        self.l_cipsns_i.setStyleSheet("color: #D2E3F7;")
        self.l_dni_i.setStyleSheet("color: #D2E3F7;")
        self.l_fecha_nacimiento_i.setStyleSheet("color: #D2E3F7;")
        self.l_edad_i.setStyleSheet("color: #D2E3F7;")
        self.l_peso_i.setStyleSheet("color: #D2E3F7;")
        self.l_altura_i.setStyleSheet("color: #D2E3F7;")
        self.l_genero_i.setStyleSheet("color: #D2E3F7;")
        self.l_fechaAlta_i.setStyleSheet("color: #D2E3F7;")
        self.l_horaAlta_i.setStyleSheet("color: #D2E3F7;")
        self.l_observ_i.setStyleSheet("color: #D2E3F7;")
        self.list_pacientes.currentItemChanged.connect(self.control_botones_scroll_pacientes)
        self.list_estudios.currentItemChanged.connect(self.cambio_item_estudio)


        self.cargar_datosDB()


    def mostrar_ayuda(self):
        from frm_ayuda_buscar_exp import frm_ayuda_buscar_exp
        ventana5 = frm_ayuda_buscar_exp()
    def tamano_directorio(self, ruta):
        total = 0
        for ruta_raiz, directorios, archivos in os.walk(ruta):
            for f in archivos:
                fp = os.path.join(ruta_raiz, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
        return total

    def tamanyo_carpeta(self, path):
        """Devuelve el tamaño de una carpeta en bytes"""
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += path.tamanyo_carpeta(entry.path)
        return total

    def espacio_libre_usb(self, path):
        """Devuelve el espacio libre en un disco en bytes"""
        stat = os.statvfs(path)
        return stat.f_bsize * stat.f_bavail


    def copiar_usb(self):
        # Ejecuta el comando lsblk y guarda el resultado en una variable
        result = os.popen('lsblk -o NAME,MOUNTPOINT,VENDOR,MODEL,TRAN').read()
        #print(result)
        pattern = re.compile(r"sdb1", re.MULTILINE)
        match = pattern.search(result)
        if match:
            self.btn_usb_des.setVisible(True)
            variables.vg_unidad_usb = "/dev/sdb1"
            #variables.vg_mensaje = "Dispositivo USB conectado."
            #ventana = frm_msg(variables.vg_mensaje)
            device = match.group()
            #return {'device': "/dev/" + device, 'mountpoint': mountpoint}
            #variables.vg_mensaje = str({'device': "/dev/" + device, 'mountpoint': ''})
            #ventana = frm_msg(variables.vg_mensaje)
            mountpoint = str("/dev/" + device)
            df_result = os.popen('df -h ' + mountpoint).read()
            for line in result.split('\n'):
                if 'sdb1' in line:
                    self.mountpoint_ruta = line.split()[1]  #

            lines = df_result.split('\n')
            if len(lines) > 1:
                fields = lines[1].split()
                if len(fields) > 3:
                    free_space = fields[3]

                    tamanyo_usb_bytes = self.espacio_libre_usb(mountpoint)
                    tamanyo_carpeta_bytes = self.tamano_directorio(variables.vg_ruta_app + '/' + variables.vg_ruta_dicom)
                    #tamanyo_carpeta_bytes = self.tamanyo_carpeta(variables.vg_ruta_app+'/experiments/acquisitions/1111/04072024_154021/dcm')
                    #tamanyo_carpeta_bytes = self.tamanyo_carpeta(variables.vg_ruta_app + '/experiments')
                    #variables.vg_mensaje = str(tamanyo_usb_bytes)
                    #ventana = frm_msg(variables.vg_mensaje)



                    #variables.vg_mensaje = str((tamanyo_usb_bytes - tamanyo_carpeta_bytes))
                    #ventana = frm_msg(variables.vg_mensaje)
                    if (tamanyo_usb_bytes - tamanyo_carpeta_bytes) > 10:

                        variables.vg_mensaje = "Preparado para realizar la copia..."
                        ventana = frm_msg(variables.vg_mensaje)
                        self.copiar_directorio(variables.vg_ruta_app + '/' + variables.vg_ruta_dicom, '/media/physio/USB DISK/'+ self.l_dni_i.text() + '/')
#                        self.copiar_directorio(variables.vg_ruta_app + '/' + variables.vg_ruta_dicom, slf.mountpoint_ruta + '/' + self.l_dni_i.text() + '/')

                        #Copiar carpeta Dicom
                        if os.path.exists('/media/physio/USB DISK/microdicom'):
                           shutil.rmtree('/media/physio/USB DISK/microdicom')

                        #shutil.copytree(variables.vg_ruta_app +'/microdicom', self.mountpoint_ruta+'/microdicom')
                        shutil.copytree(variables.vg_ruta_app + '/microdicom', '/media/physio/USB DISK/microdicom')

                        # copiar archivo
                        #os.makedirs(self.mountpoint_ruta+'/dcm')
                        #self.copiar_directorio(variables.vg_ruta_app + '/' + variables.vg_ruta_dicom, self.mountpoint_ruta+'/dcm')
                        variables.vg_mensaje = "Archivos copiados."
                        ventana = frm_msg(variables.vg_mensaje)

                    else:
                        variables.vg_mensaje = "No hay espacio suficiente en el dispositivo USB."
                        ventana = frm_msg(variables.vg_mensaje)


        else:
            #print("Por favor, inserte un dispositivo USB.")
            variables.vg_mensaje  = "Por favor, inserte un dispositivo USB."
            ventana = frm_msg(variables.vg_mensaje)

    def copiar_directorio(self,src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
            shutil.copy(src, dst)
        else:
            shutil.rmtree(dst)
            os.makedirs(dst)
            shutil.copy(src, dst)




    def desconectar_usb(self):

        # Desmontar la unidad
        subprocess.run(['umount', variables.vg_unidad_usb], check=True)

        subprocess.run(['udisksctl', 'power-off', '-b', variables.vg_unidad_usb], check=True)

        variables.vg_mensaje = "Unidad USB desmontada y expuldada. Puede retirar el USB."
        ventana = frm_msg(variables.vg_mensaje)

        self.btn_usb_des.setVisible(False)

    def cargar_datosDB(self):
        self.list_pacientes.clear()
        conn = sqlite3.connect('db/physioMRI.db')
        cur = conn.cursor()
        cur.execute('SELECT nombre, apellido1, apellido2, cipsns, dninie, fechaNacimiento, edad, peso, altura, genero, fechaAlta, horaAlta, observaciones, id_paciente FROM pacientes')
        campo = cur.fetchall()
        icon = QtGui.QIcon(icon_path)
        tamayo = QtCore.QSize(65, 65)
        self.list_pacientes.setIconSize(tamayo)
        lista_items_pacientes.clear()
        for base in range(len(campo)):
            item = QtWidgets.QListWidgetItem(icon, str(campo[base][1])+' '+campo[base][2]+' '+campo[base][0])
            lista_items_pacientes.append(str(campo[base][13]))
            self.list_pacientes.addItem(item)

        if self.list_pacientes.count() > 4:
            self.btn_abajo_pacientes.setVisible(True)

        if self.list_pacientes.count() > 0:
            self.l_nombre_i.setText(campo[0][0])
            self.l_1apellido_i.setText(campo[0][1])
            self.l_2apellido_i.setText(campo[0][2])
            self.l_cipsns_i.setText(campo[0][3])
            self.l_dni_i.setText(campo[0][4])
            self.l_fecha_nacimiento_i.setText(campo[0][5])
            self.l_edad_i.setText(str(campo[0][6]))
            self.l_peso_i.setText(str(campo[0][7])+" "+variables.vg_medidaPeso)
            self.l_altura_i.setText(str(campo[0][8]))
            self.l_genero_i.setText(campo[0][9])
            self.l_fechaAlta_i.setText(campo[0][10])
            self.l_horaAlta_i.setText(campo[0][11])
            self.l_observ_i.setText(str(campo[0][12]))
            self.list_pacientes.setCurrentRow(0)
        conn.close()

        self.actualiza_datos_estudios()



    def cargar_datosDB_filtro(self):
        conn = sqlite3.connect('db/physioMRI.db')
        cur = conn.cursor()
        cur.execute("SELECT nombre, apellido1, apellido2, cipsns, dninie, fechaNacimiento, edad, peso, altura, genero, fechaAlta, horaAlta, observaciones, id_paciente FROM pacientes WHERE nomApeSnsDni LIKE '%" + self.le_txtbuscar.text() + "%'")
        campo = cur.fetchall()
        icon = QtGui.QIcon(icon_path)
        tamayo = QtCore.QSize(65, 65)
        self.list_pacientes.setIconSize(tamayo)
        lista_items_pacientes.clear()
        self.list_pacientes.clear()
        for base in range(len(campo)):
            item = QtWidgets.QListWidgetItem(icon, str(campo[base][1])+' '+campo[base][2]+' '+campo[base][0])
            lista_items_pacientes.append(str(campo[base][13]))
            self.list_pacientes.addItem(item)

        if self.list_pacientes.count() > 0:
            self.l_nombre_i.setText(campo[0][0])
            self.l_1apellido_i.setText(campo[0][1])
            self.l_2apellido_i.setText(campo[0][2])
            self.l_cipsns_i.setText(campo[0][3])
            self.l_dni_i.setText(campo[0][4])
            self.l_fecha_nacimiento_i.setText(campo[0][5])
            self.l_edad_i.setText(str(campo[0][6]))
            self.l_peso_i.setText(str(campo[0][7])+" "+variables.vg_medidaPeso)
            self.l_altura_i.setText(str(campo[0][8]))
            self.l_genero_i.setText(campo[0][9])
            self.l_fechaAlta_i.setText(campo[0][10])
            self.l_horaAlta_i.setText(campo[0][11])
            self.l_observ_i.setText(str(campo[0][12]))
            self.list_pacientes.setCurrentRow(0)
            self.actualiza_datos_estudios()
        else:
            self.l_nombre_i.setText("")
            self.l_1apellido_i.setText("")
            self.l_2apellido_i.setText("")
            self.l_cipsns_i.setText("")
            self.l_dni_i.setText("")
            self.l_fecha_nacimiento_i.setText("")
            self.l_edad_i.setText(str(""))
            self.l_peso_i.setText(str(""))
            self.l_altura_i.setText(str(""))
            self.l_genero_i.setText("")
            self.l_fechaAlta_i.setText("")
            self.l_horaAlta_i.setText("")
            self.l_observ_i.setText(str(""))
        conn.close()


    def actualiza_inf_pacientes(self):
        conn = sqlite3.connect('db/physioMRI.db')
        cur = conn.cursor()
        cur.execute("SELECT nombre, apellido1, apellido2, cipsns, dninie, fechaNacimiento, edad, peso, altura, genero, fechaAlta, horaAlta, observaciones, id_paciente FROM pacientes WHERE id_paciente = " + str(lista_items_pacientes[self.list_pacientes.currentRow()]))
        campo = cur.fetchall()
        self.l_nombre_i.setText(campo[0][0])
        self.l_1apellido_i.setText(campo[0][1])
        self.l_2apellido_i.setText(campo[0][2])
        self.l_cipsns_i.setText(campo[0][3])
        self.l_dni_i.setText(campo[0][4])
        self.l_fecha_nacimiento_i.setText(campo[0][5])
        self.l_edad_i.setText(str(campo[0][6]))
        self.l_peso_i.setText(str(campo[0][7]) + " " + variables.vg_medidaPeso)
        self.l_altura_i.setText(str(campo[0][8]))
        self.l_genero_i.setText(campo[0][9])
        self.l_fechaAlta_i.setText(campo[0][10])
        self.l_horaAlta_i.setText(campo[0][11])
        self.l_observ_i.setText(str(campo[0][12]))
        conn.close()
        self.actualiza_datos_estudios()


    def control_botones_scroll_pacientes(self):
        if self.list_pacientes.currentRow()==0 or self.list_pacientes.count() < 4:
            self.btn_arriba_pacientes.setVisible(False)
            self.btn_abajo_pacientes.setVisible(True)
        else:
            self.btn_arriba_pacientes.setVisible(True)
            self.btn_abajo_pacientes.setVisible(True)
        if self.list_pacientes.currentRow()==self.list_pacientes.count() - 1 or self.list_pacientes.count() < 4:
            self.btn_abajo_pacientes.setVisible(False)


    def scroll_arriba_pacientes(self):
        self.list_pacientes.setCurrentRow((self.list_pacientes.currentRow()) - 1)
        self.list_pacientes.setFocus()
        if self.list_pacientes.currentRow()==0 or self.list_pacientes.count() < 4:
            self.btn_arriba_pacientes.setVisible(False)
            self.btn_abajo_pacientes.setVisible(True)
        else:
            self.btn_arriba_pacientes.setVisible(True)
            self.btn_abajo_pacientes.setVisible(True)

        self.actualiza_inf_pacientes()

    def scroll_abajo_pacientes(self):
        self.list_pacientes.setCurrentRow((self.list_pacientes.currentRow()) + 1)
        self.list_pacientes.setFocus()
        if self.list_pacientes.currentRow()==self.list_pacientes.count() - 1 or 0 and self.list_pacientes.count() < 4:
            self.btn_abajo_pacientes.setVisible(False)
        else:
            self.btn_arriba_pacientes.setVisible(True)

        self.actualiza_inf_pacientes()

    def cambio_item_estudio(self, current, previous):
        self.actualizar_visible_botones_estudios()

    def actualizar_visible_botones_estudios(self):
        current_item = self.list_estudios.currentItem()
        if current_item:
            index = self.list_estudios.indexOfTopLevelItem(current_item)
            if index==-1:
                parent_item = current_item.parent()
                if parent_item:
                        index = parent_item.indexOfChild(current_item)
                else:
                    return
         # Verificar si hay elementos arriba o abajo
            has_previous = index > 0
            has_next = index < (self.list_estudios.topLevelItemCount() - 1) if not current_item.parent() else index < (current_item.parent().childCount() - 1)

            self.btn_arriba_estudios.setVisible(has_previous)
            self.btn_abajo_estudios.setVisible(has_next)
        else:
            self.btn_arriba_estudios.setVisible(False)
            self.btn_abajo_estudios.setVisible(False)

    def scroll_arriba_estudios(self):
        current_item = self.list_estudios.currentItem()
        if current_item:
            index = self.list_estudios.indexOfTopLevelItem(current_item)
            if index==-1:
                parent_item = current_item.parent()
                if parent_item:
                    index = parent_item.indexOfChild(current_item)
                    if index > 0:
                        self.list_estudios.setCurrentItem(parent_item.child(index - 1))
            elif index > 0:
                self.list_estudios.setCurrentItem(self.list_estudios.topLevelItem(index - 1))

    def scroll_abajo_estudios(self):
        current_item = self.list_estudios.currentItem()
        if current_item:
            index = self.list_estudios.indexOfTopLevelItem(current_item)
            if index==-1:
                parent_item = current_item.parent()
                if parent_item:
                    index = parent_item.indexOfChild(current_item)
                    if index < parent_item.childCount() - 1:
                        self.list_estudios.setCurrentItem(parent_item.child(index + 1))
            elif index < self.list_estudios.topLevelItemCount() - 1:
                self.list_estudios.setCurrentItem(self.list_estudios.topLevelItem(index + 1))


    def volver_home(self):
        self.close()
        #self.hide()

    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)

    def abrir_frm_scan(self):

        fecha_hora_actual = datetime.now()
        dia_formateada = fecha_hora_actual.strftime("%d")
        mes_formateada = fecha_hora_actual.strftime("%m")
        anyo_formateada = fecha_hora_actual.strftime("%Y")
        hora_format2 = fecha_hora_actual.strftime("%H")
        minuto_format2 = fecha_hora_actual.strftime("%M")
        segundo_format2 = fecha_hora_actual.strftime("%S")

        variables.vg_paciente = self.l_dni_i.text()
        variables.vg_fechaHora = f"{dia_formateada}{mes_formateada}{anyo_formateada}_{hora_format2}{minuto_format2}{segundo_format2}"
        variables.vg_apellido1 = self.l_1apellido_i.text()
        variables.vg_apellido2 = self.l_2apellido_i.text()
        variables.vg_nombre = self.l_nombre_i.text()
        variables.vg_cipnsns = self.l_cipsns_i.text()
        variables.vg_fNacimiento = self.l_fecha_nacimiento_i.text()
        variables.vg_altura = self.l_altura_i.text()
        variables.vg_peso = self.l_peso_i.text()
        variables.vg_genero = self.l_genero_i.text()
        variables.vg_fAlta = self.l_fechaAlta_i.text()
        variables.vg_hAlta = self.l_horaAlta_i.text()
        variables.vg_observaciones = self.l_observ_i.toPlainText()
        variables.vg_edad = self.l_edad_i.text()
        #variables.vg_vengo_buscar = True
        self.ventana3 = frm_nuevo_exp(self)
        self.ventana3.exec_()
        #ventana3 = frm_scan()

    def on_item_clicked(self, item, column):
        hidden_value = item.text(1)
        variables.vg_ruta_dicom = item.text(1)
        print(variables.vg_ruta_dicom)
        # Obtener el valor de la columna oculta
        if hidden_value != '':
           self.hs_imagen.setVisible(True)
           # cargar archivo dicom.dcm
           self.dicom_dataset = pydicom.dcmread(hidden_value)
           self.image_data = self.dicom_dataset.pixel_array
           # Verify if the DICOM image is 3D
           self.is_3d = len(self.image_data.shape)==3
           self.l_imagen.setScaledContents(True)
           self.update_image(0)  # Visualiza la primera imagen
           self.hs_imagen.setMinimum(0)
           self.hs_imagen.setMaximum(self.image_data.shape[0] - 1 if self.is_3d else 0)
           self.hs_imagen.setValue(0)
           self.hs_imagen.valueChanged.connect(self.slider_moved)
           self.btn_usb.setVisible(True)
        else:
           self.btn_usb.setVisible(False)
           self.l_imagen.clear()
           self.hs_imagen.setVisible(False)
           self.index_label.setText("")


        # Alternar la expansión/contracción del elemento
        if item.childCount() > 0:
            if item.isExpanded():
                self.list_estudios.collapseItem(item)
            else:
                self.list_estudios.expandItem(item)


    def slider_moved(self, position):
        self.update_image(position)
        self.update_index_label(position)
    def update_index_label(self, index):
        total_images = self.image_data.shape[0] if self.is_3d else 1
        self.index_label.setText(f"Imagen {index + 1} de {total_images}")

    def update_image(self, index):
        if self.is_3d:
            image_data = self.image_data[index]
        else:
            image_data = self.image_data

        qimage = self.convert_to_qimage(image_data)
        self.l_imagen.setPixmap(QPixmap.fromImage(qimage))
        self.update_index_label(index)

    def convert_to_qimage(self, image_data):
        # Normalize the image data to 8-bit
        image_data = ((image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data)) * 255).astype(np.uint8)

        # Get dimensions
        height, width = image_data.shape

        # Create QImage
        qimage = QImage(image_data.data, width, height, width, QImage.Format_Grayscale8)

        return qimage

    def actualiza_datos_estudios(self):
        self.list_estudios.clear()
        self.l_imagen.clear()
        self.index_label.clear()
        self.hs_imagen.setVisible(False)
        item_actual = self.list_pacientes.currentRow()
        if item_actual is not None and item_actual >= 0:
            conn = sqlite3.connect('db/physioMRI.db')
            cur = conn.cursor()
            cur.execute("Select A.id_paciente, B.protocolo, C.lado, D.orientacion, B.imagen, A.id_estudio FROM estudios AS A "+
                        "JOIN protocolos AS B ON A.id_protocolo=B.id_protocolo "+
                        "JOIN lado AS C ON A.id_lado=C.id_lado "+
                        "JOIN orientacion AS D ON A.id_orientacion=D.id_orientacion "+
                        "WHERE A.id_paciente ="+ str(lista_items_pacientes[self.list_pacientes.currentRow()]))
            parents = cur.fetchall()

            for parent in parents:
                parent_item = QTreeWidgetItem([parent[1]+ " "+parent[2]+" "+parent[3]])
                parent_item.setData(1, Qt.UserRole, 1)
                #icono = QIcon("template/black/"+parent[4]).pixmap(QSize(60, 60))
                icono = QIcon(QPixmap("template/black/"+parent[4]).scaled(60, 60))
                parent_item.setIcon(0, icono)


                # Obtener datos de hijos
                cur.execute('SELECT nombre, ruta_imagen FROM secuencias_estudio WHERE id_estudio=?', (parent[5],))
                children = cur.fetchall()

                for child in children:
                    child_item = QTreeWidgetItem([child[0], child[1]])
                    parent_item.addChild(child_item)
                    icono = QIcon(QPixmap("template/black/escan.png").scaled(60, 60))
                    child_item.setIcon(0, icono)
                    parent_item.setData(2, Qt.UserRole, 2)

                self.list_estudios.addTopLevelItem(parent_item)

            conn.close()

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_buscar_exp()
    ventana.show()
    app.exec_()
"""