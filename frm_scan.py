import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QAction, QMainWindow
from frm_app import frm_app
import utilidades
import variables
from frm_msg import frm_msg


from ui_scan import Ui_scan


class frm_scan(QMainWindow, Ui_scan):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo

        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual

        #self.updateSessionDict()
        #session=['directory']
        # Create folder
        #session['directory'] = 'experiments/acquisitions/%s/%s/%s/%s' % (session['project'], session['subject_id'], session['study'], session['side'])
       # if not os.path.exists(self.session['directory']):
       #     os.makedirs(self.session['directory'])

        # Crear un layout vertical para el diálogo
        layout = QVBoxLayout(self)

        # Crear una instancia de MainWindow
        # self.main_window = MainWindow()
        self.demo = False
        # variables.main_window = None
        # Open the main gui
        self.updateSessionDict()

        #self.session['directory'] = 'experiments/acquisitions/%s/%s/%s/%s' % (
        # self.session['project'], self.session['subject_id'], self.session['study'], self.session['side'])

        self.session['directory'] = 'experiments/acquisitions/%s/%s' % (
            variables.vg_paciente, variables.vg_fechaHora)

            #"pacientes.dniNie, estudios_fecha_hora")

        if not os.path.exists(self.session['directory']):
            os.makedirs(self.session['directory'])

        #print("---------------------- "+str(self.session)+ " "+ str(self.demo)+" ----------------------------")
        from ui.window_main import MainWindow
        from controller.controller_main import MainController

        # Open the main gui
        if frm_nuevo_exp.main_gui is None:
            frm_nuevo_exp.main_gui = MainController(self.session, demo=False, parent=self)

        else:
            frm_nuevo_exp.main_gui.saveSessionToSequences(self.session)
            frm_nuevo_exp.main_gui.console.setup_console()
            frm_nuevo_exp.main_gui.history_list.delete_items()
            frm_nuevo_exp.main_gui.console.clear_console()
            frm_nuevo_exp.main_gui.setWindowTitle(self.session['directory'])
            frm_nuevo_exp.main_gui.setDemoMode(False)



        frm_nuevo_exp.main_gui.setWindowModality(Qt.ApplicationModal)
        frm_nuevo_exp.main_gui.setAttribute(Qt.WA_DeleteOnClose)
        frm_nuevo_exp.main_gui.show()
        frm_nuevo_exp.main_gui.raise_()
        frm_nuevo_exp.main_gui.activateWindow()

            # self.hide()
        #self.main_gui.show()







        # Aplicar configuración nuevo diseño
        frm_app.main_gui.toolbar_protocols.setVisible(False)
        #self.main_window.toolbar_sequences.setVisible(False)
        frm_app.main_gui.toolbar_figures.setVisible(False)

        frm_app.main_gui.toolbar_sequences.action_acquire.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_view_sequence.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_add_to_list.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_iterate.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_load_parameters.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_save_parameters.setVisible(False)
        frm_app.main_gui.toolbar_sequences.action_save_parameters_cal.setVisible(False)

        frm_app.main_gui.toolbar_sequences.setIconSize(QSize(100, 100))

        frm_app.main_gui.toolbar_sequences.action_bender.setIcon(QIcon('template/black/bender.png'))
        frm_app.main_gui.toolbar_sequences.addSeparator()
        frm_app.main_gui.toolbar_sequences.action_autocalibration.setIcon(QIcon('template/black/calibration-light.png'))
        frm_app.main_gui.toolbar_sequences.action_localizer.setIcon(QIcon('template/black/localizer-light.png'))

        botones = frm_app.main_gui.toolbar_sequences.actions()
        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[0])
        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[1])
        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[2])


        frm_app.main_gui.toolbar_sequences.setMovable(False)
        frm_app.main_gui.toolbar_marcos.setMovable(False)


        self.btn_ayuda_scan = QAction(QIcon('template/black/ayuda.png'), 'Ayuda', self)
        self.btn_ayuda_scan.triggered.connect(self.mostrar_ayuda)
        #self.btn_ayuda_scan.triggered.connect(self.ayuda_scan)
        frm_app.main_gui.toolbar_sequences.addAction(self.btn_ayuda_scan)

        #self.btn_ayuda_scan.setEnabled(False)


        self.btn_cerrar_scan = QAction(QIcon('template/black/icono_home.png'), 'Cerrar', self)
        self.btn_cerrar_scan.triggered.connect(self.cerrar_scan)
        frm_app.main_gui.toolbar_sequences.addAction(self.btn_cerrar_scan)

        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[8])
        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[9])
        frm_app.main_gui.toolbar_sequences.insertSeparator(botones[10])


        #self.main_window.toolbar_marcos.action_start.setIcon(QIcon('template/black/initGPA.png'))
        frm_app.main_gui.toolbar_marcos.action_start.setVisible(False)
        frm_app.main_gui.toolbar_marcos.action_copybitstream.setIcon(QIcon('template/black/M.png'))
        frm_app.main_gui.toolbar_marcos.action_server.setIcon(QIcon('template/black/server-light.png'))
        frm_app.main_gui.toolbar_marcos.action_gpa_init.setIcon(QIcon('template/black/gpa.png'))

        botones = self.main_window.toolbar_marcos.actions()
        frm_app.main_gui.toolbar_marcos.insertSeparator(botones[1])
        frm_app.main_gui.toolbar_marcos.insertSeparator(botones[2])
        frm_app.main_gui.toolbar_marcos.insertSeparator(botones[3])
        #self.main_window.toolbar_marcos.insertSeparator(botones[5])

        frm_app.main_gui.menu.hide()

        frm_app.main_gui.toolbar_marcos.setIconSize(QSize(100,100))
        #self.main_window.setStyleSheet(Path('qss/estilos.qss').read_text())
        frm_app.main_gui.custom_and_protocol.custom_widget.setVisible(False)
        frm_app.main_gui.custom_and_protocol.setTabVisible(0, False)
        frm_app.main_gui.custom_and_protocol.setTabText(1, "")
        frm_app.main_gui.custom_and_protocol.setTabIcon(1, QIcon())

        frm_app.main_gui.protocol_list.setVisible(False)


        #self.main_window.contr

        # self.main_gui = MainController(self.session, False)
        #self.main_window.show()
        # Añadir el QMainWindow directamente al layout
        layout.addWidget(frm_app.main_gui)

        # Establecer el layout del diálogo
        self.setLayout(layout)


        self.frm_scan.show()


        """
        # main_script.py
        import subprocess

        # Comando para ejecutar el otro script
        command = ["python", "ui/window_session.py"]

        # Ejecutar el otro script
        result = subprocess.run(command, capture_output=True, text=True)
        """
    def updateSessionDict(self):
        """
        Updates the session dictionary with the current session information.

        self.session = {
            'project': self.project_combo_box.currentText(),
            'study': self.study_combo_box.currentText(),
            'side': self.side_combo_box.currentText(),
            'orientation': self.orientation_combo_box.currentText(),
            'subject_id': self.id_line_edit.text(),
            'study_id': self.idS_line_edit.text(),
            'subject_name': self.name_line_edit.text(),
            'subject_surname': self.surname_line_edit.text(),
            'subject_birthday': self.birthday_line_edit.text(),
            'subject_weight': self.weight_line_edit.text(),
            'subject_height': self.height_line_edit.text(),
            'scanner': self.scanner_line_edit.text(),
            'rf_coil': self.rf_coil_combo_box.currentText(),
            'seriesNumber': 0,
        }
        """
        self.session = {
            'project': '',
            'study': '',
            'side': '',
            'orientation': '',
            'subject_id': '',
            'study_id': '',
            'subject_name': '',
            'subject_surname': '',
            'subject_birthday': '',
            'subject_weight': '',
            'subject_height': '',
            'scanner': '',
            'rf_coil': '',
            'seriesNumber': 0,
        }
        # hw.b1Efficiency = hw.antenna_dict[self.session['rf_coil']]


    def cerrar_scan(self):
        #print("directorio:  "+ self.session['directory'])
        #Comprobar si ha obtenido imágenes o no
        if os.path.exists(self.session['directory']):
            if os.listdir(self.session['directory']):
                #print("El directorio contiene archivos")
                fecha_hora_actual = datetime.now()

                fecha_formateada = fecha_hora_actual.strftime("%d/%m/%Y")
                hora_formateada = fecha_hora_actual.strftime("%H:%M:%S")
                #copiar rutas de archivos dicom a la bd
                conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
                cur = conn.cursor()
                cur.execute("insert into estudios (id_paciente, id_protocolo, id_lado, id_orientacion, fechaEstudio, horaEstudio) values(?,?,?,?,?,?)", (
                    variables.vg_id_paciente, variables.vg_id_protocolo, variables.vg_id_lado,
                    variables.vg_id_orientacion, fecha_formateada, hora_formateada))
               # variables.vg_mensaje = "insert into estudios (id_paciente, id_protocolo, id_lado, id_orientacion, fechaEstudio, horaEstudio) values(?,?,?,?,?,?)", (
                #    variables.vg_id_paciente, variables.vg_id_protocolo, variables.vg_id_lado, variables.vg_id_orientacion, fecha_formateada, hora_formateada)
              #  ventana = frm_msg(variables.vg_mensaje)

                conn.commit()
                variables.vg_id_estudio = cur.lastrowid
                # Usa os.listdir para obtener los nombres de archivos
                for filename in os.listdir(self.session['directory']+"/dcm"):
                    # Usa os.path.join para obtener la ruta completa del archivo
                    full_path = os.path.join(self.session['directory']+"/dcm", filename)
                    if os.path.isfile(full_path):
                        #print(full_path)
                        cur.execute("insert into secuencias_estudio (id_paciente, id_estudio,id_protocolo, nombre, ruta_imagen) values(?,?,?,?,?)", (
                        variables.vg_id_paciente, variables.vg_id_estudio, variables.vg_id_protocolo, filename.split('.')[0], full_path))

                conn.commit()
                cur.close()
            else:
                #Si no ha obetnido imágenes, eliminamos la carpeta
                os.rmdir(self.session['directory'])
                #print("El directorio está vacío")
        else:
            pass

        #self.show()
       # self.hide()
        #self.parent.show()
    def mostrar_ayuda(self):
        from frm_ayuda_scan import frm_ayuda_scan
        ventana5 = frm_ayuda_scan()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo_2. setGeometry(0,0,1920,1080)
        self.l_logo_2.setScaledContents(True)
        variables.vg_ancho_pantalla = 1920  # resolución pantalla width
        variables.vg_alto_pantalla = 1080  # resolución pantalla height
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self, self.fondo_sombra)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  " + variables.vg_usuario_nombre)
    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)




