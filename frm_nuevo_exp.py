import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
import subprocess
import configs.hw_config as hw
from PyQt5.QtCore import Qt, QTimer, QRegExp, QDate, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QIcon, QPixmap, QCursor, QColor
import os

from controller.controller_toolbar_sequences import SequenceController
from ui.window_main import MainWindow
from controller.controller_main import MainController
import variables
import utilidades
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QAction, QLabel, QVBoxLayout, QTableWidget, QSpacerItem, \
    QSizePolicy, QWidget
from ui_nuevo_exp import Ui_nuevo_exp
from frm_scan import frm_scan

from concurrent.futures import Future



class frm_nuevo_exp(QDialog, Ui_nuevo_exp):
    def __init__(self, parent=None):
    #def __init__(self, controller):
        super().__init__()
        #self.session = {}
        #self.session['directory'] = 'experiments/acquisitions/%s/%s' % (
        #    variables.vg_paciente, variables.vg_fechaHora)
        #self.main_gui = MainController(self.session, demo=False, parent=self)
        self.setupUi(self)
        self.config_pantalla()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo
        self.main_gui = None

        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual
        #self.exec_()

    def config_pantalla(self):
        self.le_dni.setText(variables.vg_paciente)
        self.le_nombre.setText(variables.vg_nombre)
        self.le_1apellido.setText(variables.vg_apellido1)
        self.le_2apellido.setText(variables.vg_apellido2)
        self.le_cipsns.setText(variables.vg_cipnsns)
        self.le_altura.setText(variables.vg_altura)
        self.le_peso.setText(variables.vg_peso)
        self.pte_observ.setPlainText(variables.vg_observaciones)
        self.cb_genero.setCurrentText(variables.vg_genero)

        #self.btn_ayuda.setEnabled(False)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

        if self.le_dni.text=='':
            self.le_dni.setText(variables.vg_paciente)

        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo_2.setGeometry(0, 0, 1920, 1080)
        self.l_logo_2.setScaledContents(True)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_azul(self,self.fondo_sombra)
        self.btn_cerrar.clicked.connect(self.volver_home)
        #self.btn_aceptar_nuevo.clicked.connect(self.abrir_frm_scan)
        self.btn_aceptar_nuevo.clicked.connect(self.abrir_frm_scan)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  " + variables.vg_usuario_nombre)


        #self.pb_mano.clicked.connect(self.poner_protocolo_mano)
        self.pb_munyeca.clicked.connect(self.poner_protocolo_munyeca)
        self.pb_antebrazo.clicked.connect(self.poner_protocolo_antebrazo)
        #self.pb_codo.clicked.connect(self.poner_protocolo_codo)

        self.pb_mano.setEnabled(False)
        self.pb_codo.setEnabled(False)
        self.pb_pie.setEnabled(False)
        self.pb_tobillo.setEnabled(False)
        self.pb_gemelo.setEnabled(False)
        self.pb_rodilla.setEnabled(False)

        self.pb_mano.setStyleSheet("border-radius: 15px; border: none;")
        self.pb_munyeca.setStyleSheet("border-radius: 15px; border: none;")
        self.pb_antebrazo.setStyleSheet("border-radius: 15px; border: none;")
        self.pb_codo.setStyleSheet("border-radius: 15px; border: none;")


        self.l_protocolo.setStyleSheet("font-size:30px;")
        self.rb_derecha.clicked.connect(self.lado_derecha_text)
        self.rb_izquierda.clicked.connect(self.lado_izquierda_text)
        self.rb_prono.clicked.connect(self.orientacion_pronacion_text)
        self.rb_supi.clicked.connect(self.orientacion_supinador_text)

        # máscara de entrada de datos que limita a letras, números y acentos
        reg_ex = QRegExp("[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+")
        input_validator = QRegExpValidator(reg_ex, self.le_nombre)
        self.le_nombre.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_ex, self.le_1apellido)
        self.le_1apellido.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_ex, self.le_2apellido)
        self.le_2apellido.setValidator(input_validator)

        # máscara de entrada de datos que limita a letras y números
        reg_ex = QRegExp("[a-zA-Z0-9]+")
        input_validator = QRegExpValidator(reg_ex, self.le_dni)
        self.le_dni.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_ex, self.le_cipsns)
        self.le_cipsns.setValidator(input_validator)

        # máscara de entrada de datos que limita a números y solo 3 dígitos
        self.le_altura.setValidator(QIntValidator(0, 999))
        self.le_peso.setValidator(QIntValidator(0, 999))


        QApplication.instance().focusChanged.connect(self.on_focusChanged)

        self.le_dni.editingFinished.connect(self.comprobar_existe_paciente)

        self.btn_aceptar_nuevo.clicked.connect(self.comprobar_existe_paciente)

        self.poner_protocolo_munyeca()


        #if variables.vg_vengo_buscar:
            # actualizar datos del estudio realizado
        variables.vg_id_lado = 1
        variables.vg_id_orientacion = 1
        variables.vg_id_protocolo = 4
       # self.comprobar_existe_paciente()
        #else:
            #variables.vg_id_lado = 1
            #variables.vg_id_orientacion = 1
            #variables.vg_id_protocolo = 4
            #self.comprobar_existe_paciente()


    def mostrar_ayuda(self):
        from frm_ayuda_nuevo_exp import frm_ayuda_nuevo_exp
        ventana5=frm_ayuda_nuevo_exp()

    def on_focusChanged(self, old, new):
        if old in [self.le_dni, self.le_cipsns] and old.text()=='':
        #if self.le_dni.text()=='' or self.le_cipsns.text()=='' or self.le_nombre.text()=='':
            old.setStyleSheet("border-radius: 2px; border-color: #A8141A;border-radius: 5px; padding: 5px")
            for widget in [self.le_dni, self.le_cipsns]:
                if widget.text()=='':
                    widget.setFocus()  # Set focus on the first empty QLineEdit
                    break

        elif old in [self.le_dni, self.le_cipsns] and old.text()!='':
            #old.setStyleSheet(None)
            pass

    def volver_home(self):
        variables.vg_paciente = ''
        variables.vg_nombre = ''
        variables.vg_apellido1 = ''
        variables.vg_apellido2 = ''
        variables.vg_fAlta = ''
        variables.vg_genero = ''
        variables.vg_peso = ''
        variables.vg_altura = ''
        variables.vg_observaciones = ''
        variables.vg_edad = ''
        variables.vg_fNacimiento = ''
        variables.vg_hAlta = ''
        variables.vg_cipnsns = ''
        variables.vg_id_estudio = ''
        variables.vg_id_nombre_protocolo = ''
        variables.vg_id_protocolo = ''
        variables.vg_protocolo_secuencia = ''
        #variables.vg_vengo_buscar = False
        self.close()

    def poner_protocolo_mano(self):
        variables.vg_id_protocolo = 5
        if self.rb_derecha.isChecked():
            self.l_protocolo.setText("Protocolo: Mano derecha")
        else:
            self.l_protocolo.setText("Protocolo: Mano izquierda")
        if self.rb_prono.isChecked():
            self.l_protocolo.setText(self.l_protocolo.text()+" prono")
        else:
            self.l_protocolo.setText(self.l_protocolo.text() + " supino")

        utilidades.sombra_frame_resaltar(self, self.pb_mano)
        utilidades.sombra_frame_desactivar(self, self.pb_munyeca)
        utilidades.sombra_frame_desactivar(self, self.pb_antebrazo)
        utilidades.sombra_frame_desactivar(self, self.pb_codo)

    def poner_protocolo_munyeca(self):
        variables.vg_id_protocolo = 4
        if self.rb_derecha.isChecked():
            self.l_protocolo.setText("Protocolo: Muñeca derecha")
            variables.vg_id_nombre_protocolo = "Muñeca derecha"
        else:
            self.l_protocolo.setText("Protocolo: Muñeca izquierda")
            variables.vg_id_nombre_protocolo = "Muñeca izquierda"
        if self.rb_prono.isChecked():
            self.l_protocolo.setText(self.l_protocolo.text() + " prono")
            variables.vg_id_nombre_protocolo = variables.vg_id_nombre_protocolo + " prono"
        else:
            self.l_protocolo.setText(self.l_protocolo.text() + " supino")
            variables.vg_id_nombre_protocolo = variables.vg_id_nombre_protocolo + " supino"

        utilidades.sombra_frame_resaltar(self, self.pb_munyeca)
        utilidades.sombra_frame_desactivar(self, self.pb_mano)
        utilidades.sombra_frame_desactivar(self, self.pb_antebrazo)
        utilidades.sombra_frame_desactivar(self, self.pb_codo)

    def poner_protocolo_antebrazo(self):
        variables.vg_id_protocolo = 3
        #v_protocolo = 3
        if self.rb_derecha.isChecked():
            self.l_protocolo.setText("Protocolo: Antebrazo derecho")
            variables.vg_id_nombre_protocolo = "Antebrazo derecho"
        else:
            self.l_protocolo.setText("Protocolo: Antebrazo izquierdo")
            variables.vg_id_nombre_protocolo = "Antebrazo izquierdo"
        if self.rb_prono.isChecked():
            self.l_protocolo.setText(self.l_protocolo.text() + " prono")
            variables.vg_id_nombre_protocolo = variables.vg_id_nombre_protocolo + " prono"
        else:
            self.l_protocolo.setText(self.l_protocolo.text() + " supino")
            variables.vg_id_nombre_protocolo = variables.vg_id_nombre_protocolo + " supino"

        utilidades.sombra_frame_resaltar(self, self.pb_antebrazo)
        utilidades.sombra_frame_desactivar(self, self.pb_mano)
        utilidades.sombra_frame_desactivar(self, self.pb_munyeca)
        utilidades.sombra_frame_desactivar(self, self.pb_codo)

    def poner_protocolo_codo(self):
        variables.vg_id_protocolo = 2
        #v_protocolo = 2
        if self.rb_derecha.isChecked():
            self.l_protocolo.setText("Protocolo: Codo derecha")
        else:
            self.l_protocolo.setText("Protocolo: Codo izquierda")
        if self.rb_prono.isChecked():
            self.l_protocolo.setText(self.l_protocolo.text() + " prono")
        else:
            self.l_protocolo.setText(self.l_protocolo.text() + " supino")

        utilidades.sombra_frame_resaltar(self, self.pb_codo)
        utilidades.sombra_frame_desactivar(self, self.pb_mano)
        utilidades.sombra_frame_desactivar(self, self.pb_munyeca)
        utilidades.sombra_frame_desactivar(self, self.pb_antebrazo)

    def lado_derecha_text(self):
        self.l_lado.setText("Derecho")
    def lado_izquierda_text(self):
        self.l_lado.setText("Izquierdo")
    def orientacion_supinador_text(self):
        self.l_orientacion.setText("Supino")
    def orientacion_pronacion_text(self):
        self.l_orientacion.setText("Prono")
    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)

    #def abrir_frm_scanV2(self):
    def iniciar_scan(self):

        self.updateSessionDict()

        self.session['directory'] = 'experiments/acquisitions/%s/%s' % (
            variables.vg_paciente, variables.vg_fechaHora)

            #"pacientes.dniNie, estudios_fecha_hora")

        if not os.path.exists(self.session['directory']):
            os.makedirs(self.session['directory'])

        # Open the main gui
        if self.main_gui is None: # si no se ha iniciado antes
            self.main_gui = MainController(self.session, demo=False, parent=self)

            self.main_gui.setStyleSheet("background-color:  #22262A")
            self.main_gui.toolbar_sequences.setStyleSheet("background-color:  #22262A")
            self.main_gui.toolbar_figures.setStyleSheet("background-color:  #22262A")
            self.main_gui.toolbar_protocols.setStyleSheet("background-color:  #22262A")
            self.main_gui.history_list.setStyleSheet("background-color:  #22262A")
            self.main_gui.console.setStyleSheet("background-color:  #22262A")
            self.main_gui.custom_and_protocol.setStyleSheet("background-color:  #22262A")
            self.main_gui.input_table.setStyleSheet("background-color:  #22262A")
            self.main_gui.figures_layout.setStyleSheet("background-color:  #22262A")

            # Cambiar el alto de las filas usando CSS
            self.main_gui.history_list.setStyleSheet("""
                    QListWidget {
                        color: white;
                        font-size: 18px;  /* Cambiar el tamaño de fuente si es necesario */
                        padding: 5px;    /* Espaciado alrededor del contenido */
                    }
                    QListWidget::item {
                        height: 30px;     /* Altura de cada fila */
                    }
                    QListWidget::item:selected {
                        background-color: #22262A;  /* Color de fondo de selección */
                        color: #9ffcfd;                /* Color de texto de selección */
                    }                    
                """)

            # Cambiar el alto de las filas usando CSS
            self.main_gui.custom_and_protocol.setStyleSheet("""
                    QListWidget {
                        color: white;
                        font-size: 18px;  /* Cambiar el tamaño de fuente si es necesario */
                        padding: 5px;    /* Espaciado alrededor del contenido */
                    }
                    QListWidget::item {
                        height: 30px;     /* Altura de cada fila */
                    }
                    QListWidget::item:selected {
                        background-color: #22262A;  /* Color de fondo de selección */
                        color: #9ffcfd;                /* Color de texto de selección */
                    }                    
                """)

            self.main_gui.figures_layout.clearFiguresLayout()

            self.main_gui.console.setStyleSheet("color: white")
            self.main_gui.input_table.setStyleSheet("color: white")


            self.main_gui.toolbar_marcos.action_server.setChecked(True)

            # Aplicar configuración nuevo diseño
            self.main_gui.toolbar_protocols.setVisible(False)
            self.main_gui.toolbar_protocols.setVisible(True)
            # self.main_window.toolbar_sequences.setVisible(False)
            self.main_gui.toolbar_figures.setVisible(True)

            self.main_gui.toolbar_figures.action_postprocessing.setVisible(False)
            self.main_gui.toolbar_figures.action_screenshot.setVisible(False)
            #self.main_gui.toolbar_figures.action_full_screen.setVisible(False)

            self.main_gui.toolbar_protocols.action_del_protocol.setVisible(False)
            self.main_gui.toolbar_protocols.action_new_protocol.setVisible(False)
            self.main_gui.toolbar_protocols.action_del_sequence.setVisible(False)
            self.main_gui.toolbar_protocols.action_new_sequence.setVisible(False)


          #  self.main_gui.history_list.itemDoubleClicked.connect(self.ayadir_imagen)

            self.main_gui.toolbar_sequences.action_acquire.setVisible(False)
            self.main_gui.toolbar_sequences.action_view_sequence.setVisible(False)
            self.main_gui.toolbar_sequences.action_add_to_list.setVisible(False)
            self.main_gui.toolbar_sequences.action_iterate.setVisible(False)
            self.main_gui.toolbar_sequences.action_load_parameters.setVisible(False)
            self.main_gui.toolbar_sequences.action_save_parameters.setVisible(False)
            self.main_gui.toolbar_sequences.action_save_parameters_cal.setVisible(False)

            self.main_gui.toolbar_sequences.setIconSize(QSize(100, 100))
            self.main_gui.toolbar_figures.setIconSize(QSize(100, 100))
            self.main_gui.toolbar_protocols.setIconSize(QSize(100, 100))

            self.main_gui.toolbar_sequences.action_bender.setIcon(QIcon('template/black/bender.png'))
            self.main_gui.toolbar_sequences.action_autocalibration.setIcon(QIcon('template/black/calibration-light.png'))
            self.main_gui.toolbar_sequences.action_localizer.setIcon(QIcon('template/black/localizer-light.png'))

            self.main_gui.toolbar_figures.action_full_screen.setIcon(QIcon('template/black/ampliar.png'))

            # Agregar un espaciador
            spacer = QWidget()
            spacer.setFixedWidth(50)  # Establecer el ancho fijo
            self.main_gui.toolbar_sequences.addWidget(spacer)  # Agregar el espaciador

            self.main_gui.toolbar_sequences.action_autocalibration.setEnabled(True)
            self.main_gui.toolbar_sequences.action_localizer.setEnabled(True)
            self.main_gui.toolbar_sequences.action_bender.setEnabled(True)

            self.main_gui.toolbar_sequences.setMovable(False)
            self.main_gui.toolbar_marcos.setMovable(False)
            self.main_gui.toolbar_protocols.setMovable(False)
            self.main_gui.toolbar_figures.setMovable(False)

            ########### nuevos botones para añadir imagenes y poder seleccionar el FOV ###############

            # mostrar imagen para FOV
            self.btn_anadirimg = QAction(QIcon('template/black/anadirimg.png'), 'Imagen', self)
            self.btn_anadirimg.triggered.connect(self.ayadir_imagen)
            self.main_gui.toolbar_figures.addAction(self.btn_anadirimg)

            # añadir imagen para FOV
            self.btn_masimg = QAction(QIcon('template/black/masimg.png'), 'MasImagen', self)
            self.btn_masimg.triggered.connect(self.mas_imagen)
            self.main_gui.history_list.doubleClicked.connect(self.mas_imagen)
            self.main_gui.toolbar_figures.addAction(self.btn_masimg)

            ############################################################################################
            # Agregar un espaciador
            spacer = QWidget()
            spacer.setFixedWidth(50)  # Establecer el ancho fijo
            self.main_gui.toolbar_protocols.addWidget(spacer)  # Agregar el espaciador

            self.btn_ayuda_scan = QAction(QIcon('template/black/ayuda.png'), 'Ayuda', self)
            self.btn_ayuda_scan.triggered.connect(self.mostrar_ayuda)
            self.main_gui.toolbar_protocols.addAction(self.btn_ayuda_scan)

            self.btn_cerrar_scan = QAction(QIcon('template/black/icono_home.png'), 'Cerrar', self)
            self.btn_cerrar_scan.triggered.connect(self.cerrar_scan)
            self.main_gui.toolbar_protocols.addAction(self.btn_cerrar_scan)

            self.btn_localizador = QAction(QIcon('template/black/localizer-light.png'), 'Localizador', self)
            self.btn_localizador.triggered.connect(self.empezar_localizador)
            self.main_gui.toolbar_protocols.addAction(self.btn_localizador)






            self.main_gui.history_list.itemChanged.connect(self.cambio_linea)

            self.main_gui.toolbar_marcos.action_start.setVisible(False)
            self.main_gui.toolbar_marcos.action_copybitstream.setIcon(QIcon('template/black/M.png'))
            self.main_gui.toolbar_marcos.action_server.setIcon(QIcon('template/black/server-light.png'))
            self.main_gui.toolbar_marcos.action_gpa_init.setIcon(QIcon('template/black/gpa.png'))

            self.main_gui.menu.hide()

            self.main_gui.toolbar_marcos.setIconSize(QSize(100, 100))
            # self.main_window.setStyleSheet(Path('qss/estilos.qss').read_text())
            self.main_gui.custom_and_protocol.custom_widget.setVisible(False)
            self.main_gui.custom_and_protocol.setTabVisible(0, False)
            self.main_gui.custom_and_protocol.setTabText(1, "")
            self.main_gui.custom_and_protocol.setTabIcon(1, QIcon())

            self.main_gui.protocol_list.setVisible(False)
            self.main_gui.toolbar_marcos.action_server.setChecked(True)
            self.main_gui.toolbar_sequences.setDisabled(False)
            self.main_gui.toolbar_sequences.setEnabled(True)

            self.main_gui.toolbar_marcos.setVisible(False)

        else: # en caso de que ya se aha iniciado scan
            self.main_gui.toolbar_marcos.setVisible(False)
            self.main_gui.input_table.clearContents()
            self.main_gui.figures_layout.clearFiguresLayout()

            self.main_gui.history_list.show()
            self.main_gui.sequence_list.show()
            self.main_gui.sequence_inputs.show()
            self.main_gui.console.show()
            self.main_gui.input_table.show()
            self.main_gui.custom_and_protocol.show()

            self.main_gui.saveSessionToSequences(self.session)
            self.main_gui.console.setup_console()
            self.main_gui.history_list.delete_items()
            self.main_gui.console.clear_console()
            self.main_gui.setWindowTitle(self.session['directory'])
            self.main_gui.setDemoMode(False)

        if variables.vg_act_marcos == True:
            # si el proceso de activación se ha concluido
            self.main_gui.toolbar_marcos.setVisible(False)
            self.main_gui.toolbar_marcos.action_server.setChecked(True)
            self.main_gui.toolbar_sequences.setDisabled(False)
            self.main_gui.toolbar_sequences.setEnabled(True)

        self.main_gui.setWindowModality(Qt.ApplicationModal)
        self.main_gui.setAttribute(Qt.WA_DeleteOnClose)
        self.main_gui.setWindowFlags(Qt.FramelessWindowHint)  # Quitar bordes y título del formulario
        self.main_gui.showMaximized()
        self.main_gui.raise_()
        self.main_gui.activateWindow()

    def ampliarimg(self):
        self.main_gui.toolbar_figures.doFullScreen()

    def cambio_linea(self, item):
        print("Ha cambiado la línea")
        index = self.main_gui.history_list.row(item)
        print(f"Elemento en el índice {index} ha cambiado a: {item.text()}")


    def start_accion(self):
        # Mensaje de carga
        print("Ejecutando localizador, por favor espere...")
        # Inicia un hilo para ejecutar el localizador
        thread = threading.Thread(target=self.main_gui.toolbar_marcos.copyBitStream)
        thread.start()

        # Mensaje de carga
        print("Ejecutando localizador, por favor espere...")

        # Espera a que termine el hilo
        thread.join()

        # Mensaje de finalización
        print("Localizador terminado.")


    def empezar_localizador(self, *args):
        self.main_gui.toolbar_sequences.startLocalizer()

    def monitorizar_localizador(self, future):
        try:
            future.result()  # Espera a que el localizador termine
            print("LOCALIZADOR TERMINADO")
            #self.status_label.setText('Estado: Localizador completado.')
        except Exception as e:
            #self.status_label.setText(f'Error: {e}')
            pass
        finally:
            #self.button.setEnabled(True)  # Reactiva el botón
            pass

    def ayadir_imagen(self, item):
        #if len(self.main_gui.history_list.figures) >= 3:
        self.main_gui.history_list.figures = []

        item = self.main_gui.history_list.currentItem()
        #print('Doble clic en:', item.text())
        self.main_gui.history_list.updateHistoryFigure(item)
        self.main_gui.history_list.clicked_item = item
        self.main_gui.history_list.addFigure()

    def mas_imagen(self, item):
        if len(self.main_gui.history_list.figures) >= 3:
            self.main_gui.history_list.figures = []

        item = self.main_gui.history_list.currentItem()
        print('Doble clic en:', item.text())
        self.main_gui.history_list.updateHistoryFigure(item)
        self.main_gui.history_list.clicked_item = item
        self.main_gui.history_list.addFigure()

    def start_long_process(self):
        # Cambiar el cursor a un cursor de espera
        self.setCursor(Qt.WaitCursor)
        cursor_img = QPixmap('logogif.gif')  # Usa una imagen estática como cursor
        cursor = QCursor(cursor_img)
        QApplication.setOverrideCursor(cursor)  # Cambia el cursor en toda la aplicación
        self.setCursor(Qt.WaitCursor)

    def long_process(self):
        # Simula un proceso largo
        variables.vg_act_marcos = True
        #self.main_gui.toolbar_marcos.startMaRCoS()
        self.main_gui.toolbar_sequences.autocalibration()
        print("PROCESO FINALIZDO")

    def on_process_finished(self):
        # Restaurar el cursor a su estado original
        self.unsetCursor()
        print("Proceso largo completado.")
        # Restauramos el cursor original
        QApplication.restoreOverrideCursor()

    def abrir_marcos(self):
        #star MaRCoS personalizado
        # cambiar cursor
        """Cambia el cursor por uno personalizado, realiza un proceso y luego restaura el cursor."""
        # Cambiamos el cursor a una imagen personalizada
        cursor_img = QPixmap('logogif.gif')  # Usa una imagen estática como cursor
        cursor = QCursor(cursor_img)
        QApplication.setOverrideCursor(cursor)  # Cambia el cursor en toda la aplicación

        # Simulamos un proceso largo
        self.main_gui.toolbar_marcos.startMaRCoS()
        #self.simular_proceso_largo()

        # Restauramos el cursor original
        QApplication.restoreOverrideCursor()

    def cerrar_scan(self):
        #print("directorio:  "+ self.session['directory'])
        # cerrar  MaRCoS server
        try:
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "killall marcos_server"])
            time.sleep(1.5)
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "~/marcos_server"])
        except:
            pass

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
                #Sino ha obtenido imágenes, eliminamos la carpeta
                os.rmdir(self.session['directory'])
                #print("El directorio está vacío")
        else:
            pass


        self.main_gui.toolbar_figures.doFullScreen()
        self.main_gui.hide()
        #self.parent.show()
    def mostrar_ayuda(self):
        from frm_ayuda_scan import frm_ayuda_scan
        ventana5 = frm_ayuda_scan()

    def abrir_frm_scan(self):
        if self.le_dni.text()!='' and self.le_cipsns.text()!='':
            #si existe actualizar datos en pantalla...

            v_nomApeSnsDni = self.le_nombre.text() + ' ' + self.le_1apellido.text() + ' ' + self.le_2apellido.text() + ' ' + self.le_cipsns.text() + ' ' + self.le_dni.text()
            fecha_hora_actual = datetime.now()
            #date = self.de_fecha_nacimiento.date()
            #cumpleanyos = datetime(date().day(),date().month(),date().year())

            #diferencia = fecha_hora_actual - cumpleanyos
            fecha_formateada = fecha_hora_actual.strftime("%d/%m/%Y")
            hora_formateada = fecha_hora_actual.strftime("%H:%M:%S")
            dia_formateada = fecha_hora_actual.strftime("%d")
            mes_formateada = fecha_hora_actual.strftime("%m")
            anyo_formateada = fecha_hora_actual.strftime("%Y")
            hora_format2 = fecha_hora_actual.strftime("%H")
            minuto_format2 = fecha_hora_actual.strftime("%M")
            segundo_format2 = fecha_hora_actual.strftime("%S")

            #v_edad = (diferencia.days // 365.25)
            v_edad = 30 # Pdte. Cambiar
            #Obetener valor de Lado
            if self.rb_derecha.isChecked():
                variables.vg_id_lado = 1
            else:
                variables.vg_id_lado = 2
            #Obetener valor de Orientación
            if self.rb_prono.isChecked():
               variables.vg_id_orientacion = 2
            else:
               variables.vg_id_orientacion = 1
            # si no existe el paciente
            if not self.v_existe:
                # guardar datos en la bd
                conn = sqlite3.connect(variables.vg_ruta_app+'/db/physioMRI.db')
                cur = conn.cursor()

                #se da de alta el paciente
                cur.execute("insert into pacientes (nombre,apellido1, apellido2, nomApeSnsDni, CIPSNS, dniNie, fechaNacimiento, edad, peso, altura, genero, fechaAlta, horaAlta, diaAlta, mesAlta, anyoAlta, observaciones ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(self.le_nombre.text(), self.le_1apellido.text(),self.le_2apellido.text(),v_nomApeSnsDni, self.le_cipsns.text(), self.le_dni.text(),self.de_fecha_nacimiento.text(),v_edad, self.le_peso.text(), self.le_altura.text(), self.cb_genero.currentText(), fecha_formateada, hora_formateada, dia_formateada, mes_formateada, anyo_formateada, self.pte_observ.toPlainText()))
                conn.commit()
                variables.vg_id_paciente = cur.lastrowid

                #actualizar variables para guardar imágenes
                cur.close()
                variables.vg_paciente = self.le_dni.text()
                variables.vg_fechaHora = f"{dia_formateada}{mes_formateada}{anyo_formateada}_{hora_format2}{minuto_format2}{segundo_format2}"

                self.iniciar_scan()
            else:
                # modificar datos por si hubiera actualizado información
                conn = sqlite3.connect(variables.vg_ruta_app+'/db/physioMRI.db')
                cur = conn.cursor()
                cur.execute("""
                UPDATE pacientes 
                SET nombre = ?, apellido1 = ?, apellido2 = ?, nomApeSnsDni = ?, CIPSNS = ?, 
                dniNie = ?, fechaNacimiento = ?, edad = ?, peso = ?, altura = ?, 
                genero = ?, fechaAlta = ?, horaAlta = ?, diaAlta = ?, mesAlta = ?, 
                anyoAlta=?, observaciones = ? WHERE dniNie = ?
                """, (self.le_nombre.text(), self.le_1apellido.text(), self.le_2apellido.text(),
                  v_nomApeSnsDni, self.le_cipsns.text(), self.le_dni.text(),
                  self.de_fecha_nacimiento.text(), v_edad, self.le_peso.text(),
                  self.le_altura.text(), self.cb_genero.currentText(), fecha_formateada,
                  hora_formateada, dia_formateada, mes_formateada, anyo_formateada,
                  self.pte_observ.toPlainText(), self.le_dni.text()))
                conn.commit()

                cur.close()
                variables.vg_paciente = self.le_dni.text()
                variables.vg_fechaHora = f"{dia_formateada}{mes_formateada}{anyo_formateada}_{hora_format2}{minuto_format2}{segundo_format2}"
                # comprobar si los datos obligatorios estan rellenados
                self.iniciar_scan()

        else:
            if self.le_cipsns.text()=='':
                self.le_cipsns.setFocus()
                self.le_cipsns.setStyleSheet("border-radius: 2px; border-color: #A8141A;border-radius: 5px; padding: 5px")

    def comprobar_existe_paciente(self):
        if self.le_dni.text()!='':
            self.v_existe= False

            # Comprobar si el paciente existe
            conn = sqlite3.connect(variables.vg_ruta_app + '/db/physioMRI.db')
            cur = conn.cursor()
            cur.execute('SELECT nombre, apellido1, apellido2, cipsns, dniNie, fechaNacimiento,peso, altura, genero, observaciones, id_paciente FROM pacientes WHERE dniNie="' + self.le_dni.text() + '"')
            campo = cur.fetchone()

            if campo is None:
                # no existe el paciente
                self.v_existe = False
            else:
                # sí existe el paciente
                self.v_existe = True
                self.le_nombre.setText(campo[0])
                self.le_1apellido.setText(campo[1])
                self.le_2apellido.setText(campo[2])
                self.le_cipsns.setText(campo[3])
                self.de_fecha_nacimiento.setDate(QDate.fromString(campo[5], 'dd/MM/yyyy'))
                self.le_peso.setText(str(campo[6]))
                self.le_altura.setText(str(campo[7]))
                self.cb_genero.setCurrentText(campo[8])
                self.pte_observ.setPlainText(campo[9])
                variables.vg_id_paciente = campo[10]

                self.le_dni.setEnabled(False)
                self.le_dni.setStyleSheet(("background-color: #22262A; color: #646F7A"))
                self.le_cipsns.setEnabled(False)
                self.le_cipsns.setStyleSheet(("background-color: #22262A; color: #646F7A"))

                conn.close()

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



"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_nuevo_exp()
    ventana.show()
    app.exec_()
"""