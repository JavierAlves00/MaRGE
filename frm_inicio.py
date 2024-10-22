import sys
import time

from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui, QtCore, QtWidgets
import variables
from pathlib import Path
import autotuning.autotuning as autotuning # Just to use an arduino
import configs.hw_config as hw
import experiment as ex
import numpy as np
import platform
import subprocess

class frm_inicio(QDialog):
    def __init__(self):
        super().__init__()
        # Configuración del diálogo
        self.setWindowTitle("Pantalla de Carga")
        self.resize(400, 500)  # Establecer tamaño del diálogo
        #self.setStyleSheet("background-color: #22262A;")  # Color de fondo gris
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(Path(variables.vg_ruta_app + '/qss/estilos.qss').read_text())
        # Crear un layout vertical
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # Centrar contenido
        self.v_errores = 0 # indica si hay algún error si es mayor de 0
        # Espacio en blanco para centrar verticalmente
        spacer_top = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_top)

        # Texto de carga
        self.loading_label = QLabel("Iniciando sistema", self)
        self.loading_label.setStyleSheet("color: white; font-size: 25px;")  # Fuente a 25px y color blanco
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)

        # Espacio de 100px
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Crear un layout horizontal para las imágenes
        self.image_layout = QHBoxLayout()
        self.image_labels = []  # Lista para almacenar las etiquetas de imagen

        # Espacio antes de la primera imagen
        self.image_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Cargar y añadir las 5 imágenes led
        for i in range(5):
            image = QPixmap(f"template/black/led_apagado.png")
            label = QLabel(self)
            label.setPixmap(image.scaled(30, 30))  # Escalar imagen si es necesario
            self.image_labels.append(label)  # Guardar la etiqueta en la lista
            self.image_layout.addWidget(label)
            if i < 5:  # Agregar separación solo entre las imágenes
                spacer = QLabel(" " * 5)  # Espacio de 20px
                self.image_layout.addWidget(spacer)

        # Espacio después de la última imagen
        self.image_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(self.image_layout)

        # Espacio de 100px entre las imágenes y el botón "Continuar"
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.bnt_aceptar = QtWidgets.QPushButton(self)
        self.bnt_aceptar.setGeometry(QtCore.QRect(10, 7, 112, 108))
        self.bnt_aceptar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bnt_aceptar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("template/black/icono_aceptar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bnt_aceptar.setIcon(icon1)
        self.bnt_aceptar.setIconSize(QtCore.QSize(100, 100))
        layout.addWidget(self.bnt_aceptar, alignment=QtCore.Qt.AlignHCenter)  # Centrando horizontalmente
        self.bnt_aceptar.clicked.connect(self.abrir_frm_acceso)  # Conectar la acción del botón
        self.bnt_aceptar.setEnabled(False)

        self.setLayout(layout)

        # Centrando el diálogo en la pantalla
        self.center()

        # Inicializar el control de inicio
        #self.image_index = 0
        #self.image_paths = [
        #    "template/black/led_on.png",
        #    "template/black/led_on.png",
        #    "template/black/led_on.png",
        #    "template/black/led_on.png",
        #    "template/black/led_on.png",
        #    "template/black/led_off.png",
        #]

        self.current_step = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_step)

        self.start_process()

    def start_process(self):
        self.current_step = 0
        self.loading_label.setText("Iniciando sistema...")
        self.run_step()  # Inicia el primer paso

    def run_step(self):
        if self.current_step < 5:
            getattr(self, f'step_{self.current_step + 1}')()  # Llama al método correspondiente
        else:
            if self.v_errores > 0:
                self.loading_label.setText("Error inicio sistema. \n \n Póngase en contacto \n con el S.A.T")
            else:
                self.loading_label.setText("Sistema preparado.")

            self.timer.stop()  # Detiene el temporizador
            self.bnt_aceptar.setEnabled(True)
            self.update()

    def step_1(self):
        self.loading_label.setText("Iniciando sistema...")
        self.arduino = autotuning.Arduino(baudrate=19200, name="interlock", serial_number=hw.ard_sn_interlock)
        self.arduino.connect()
        self.change_image(0, "template/black/led_on.png")
        self.update()
        self.timer.start(1000)  # Espera 1 segundo antes de continuar
        self.current_step += 1

    def step_2(self):
        self.loading_label.setText("Iniciando sistema...")
        self.search_sdrlab()
        self.update()
        self.timer.start(1000)
        self.current_step += 1

    def step_3(self):
        self.loading_label.setText("Iniciando sistema...")
        self.mi_copyBitStream()
        self.update()
        self.timer.start(1000)
        self.current_step += 1

    def step_4(self):
        self.loading_label.setText("Iniciando sistema...")
        self.mi_controlMarcosServer()
        self.update()
        self.timer.start(1000)
        self.current_step += 1

    def step_5(self):
        self.loading_label.setText("Iniciando sistema...")
        self.mi_initgpa()
        self.update()
        self.timer.start(1000)
        self.current_step += 1

    def search_sdrlab(self):
        # Get the IP of the SDRLab
        try:
            hw.rp_ip_address = self.get_sdrlab_ip()[0]
        except:
            print("ERROR: No SDRLab found.")
            self.change_image(1, "template/black/led_off.png")
            self.v_errores += 1
            self.update()

    def get_sdrlab_ip(self):
        print("Searching for SDRLabs...")

        ip_addresses = []
        subnet = '192.168.1.'
        timeout = 0.1  # Adjust timeout value as needed

        for i in range(101, 132):  # Scan IP range 192.168.1.101 to 192.168.1.132
            ip = subnet + str(i)
            try:
                if platform.system() == 'Linux':
                    result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL,
                                            timeout=timeout)
                elif platform.system() == 'Windows':
                    result = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL,
                                            timeout=timeout)
                if result.returncode == 0:
                    print(f"Checking ip {ip}...")
                    # Attempt SSH connection without authentication
                    ssh_command = ['ssh', '-o', 'BatchMode=yes', '-o', f'ConnectTimeout={5}',
                                   f'{"root"}@{ip}', 'exit']
                    ssh_result = subprocess.run(ssh_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    if ssh_result.returncode == 0:  # SSH was successful
                        ip_addresses.append(ip)
                    else:
                        print(f"WARNING: No SDRLab found at ip {ip}.")
                        self.change_image(1, "template/black/led_off.png")
                        self.v_errores += 1
                        self.update()
            except:
                pass

        for ip in ip_addresses:
            print("READY: SDRLab found at IP " + ip)
            self.change_image(1,"template/black/led_on.png")
            time.sleep(1.5)
            self.update()

        return ip_addresses

    def mi_controlMarcosServer(self):
        try:
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "killall marcos_server"])
            time.sleep(1.5)
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "~/marcos_server"])
            time.sleep(1.5)
            expt = ex.Experiment(init_gpa=False)
            expt.add_flodict({'grad_vx': (np.array([100]), np.array([0])), })
            expt.run()
            expt.__del__()
            print("READY: Server connected!")
            self.change_image(3, "template/black/led_on.png")
            self.update()



        except Exception as e:
            print("ERROR: Server not connected!")
            print("ERROR: Try to connect to the server again.")
            print(e)
            self.change_image(3, "template/black/led_off.png")
            self.v_errores += 1
            self.update()

    def mi_copyBitStream(self):
        try:
            subprocess.run([hw.bash_path, "--", "./communicateRP.sh", hw.rp_ip_address, "killall marcos_server"])
            subprocess.run([hw.bash_path, '--', './copy_bitstream.sh', hw.rp_ip_address, 'rp-122'], timeout=10)
            time.sleep(1.5)

            print("READY: MaRCoS updated")
            self.change_image(2, "template/black/led_on.png")
            self.update()
        except subprocess.TimeoutExpired as e:
            print("ERROR: MaRCoS init timeout")
            print(e)
            self.change_image(2, "template/black/led_off.png")
            self.v_errores += 1
            self.update()

    def mi_initgpa(self):
        """
        Initializes the GPA board.
        """
        link = False
        while not link:
            try:
                # Check if GPA available
                received_string = self.arduino.send("GPA_VERB 1;").decode()
                if received_string[0:4] != ">OK;":
                    print("WARNING: GPA not available.")
                    self.change_image(4, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:
                    print("READY: GPA available.")
                    self.change_image(4, "template/black/led_on.png")
                    self.update()

                # Remote communication with GPA
                received_string = self.arduino.send("GPA_SPC:CTL 1;").decode()  # Activate remote control
                if received_string[0:4] != ">OK;":  # If wrong response
                    print("WARNING: Error enabling GPA remote control.")
                    self.change_image(4, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:  # If good response
                    print("READY: GPA remote communication succeed.")
                    self.change_image(4, "template/black/led_on.png")
                    self.update()


                # Check if RFPA available
                received_string = self.arduino.send("RFPA_VERB 1;").decode()
                if received_string[0:4] != ">OK;":
                    print("WARNING: RFPA not available.")
                    self.change_image(5, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:
                    print("READY: RFPA available.")
                    self.change_image(5, "template/black/led_on.png")
                    self.update()

                # Remote communication with RFPA
                received_string = self.arduino.send("RFPA_SPC:CTL 1;").decode()
                if received_string[0:4] != ">OK;":
                    print("WARNING: Error enabling RFPA remote control.")
                    self.change_image(5, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:
                    print("READY: RFPA remote communication succeed.")
                    self.change_image(5, "template/black/led_on.png")
                    self.update()

                # Disable power module
                self.arduino.send("GPA_ON 0;")
                self.arduino.send("RFPA_RF 0;")
                # Run init_gpa sequence
                expt = ex.Experiment(init_gpa=True)
                expt.add_flodict({
                    'grad_vx': (np.array([100]), np.array([0])), })
                expt.run()
                expt.__del__()
                link = True
                print("READY: GPA init done!")

                # Enable power modules
                # Enable GPA module
                received_string = self.arduino.send("GPA_ON 1;").decode()  # Enable power module
                if received_string[0:4] != ">OK;":  # If wrong response
                    print("WARNING: Error activating GPA power module.")
                    self.change_image(4, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:  # If good reponse
                    print("READY: GPA power enabled.")
                    self.change_image(4, "template/black/led_on.png")
                    self.update()

                # Enable RFPA module
                received_string = self.arduino.send("RFPA_RF 1;").decode()
                if received_string[0:4] != ">OK;":
                    print("WARNING: Error activating RFPA power module.")
                    self.change_image(5, "template/black/led_off.png")
                    self.v_errores += 1
                    self.update()
                    return
                else:
                    print("READY: RFPA power enabled.")
                    self.change_image(5, "template/black/led_on.png")
                    self.update()

            except:
                link = False
                time.sleep(1)
        else:
            print("ERROR: No connection to the server")
            print("Please, connect to MaRCoS server first")

    def center(self):
        # Obtener la geometría de la pantalla
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def abrir_frm_acceso(self):
        # Aquí puedes agregar la acción que deseas realizar al hacer clic en el botón
        from frm_acceso import frm_acceso_main
        self.ventana3 = frm_acceso_main(self)
        self.close()
        self.ventana3.exec_()

    def change_image(self, index, new_image_path):
        # Método para cambiar la imagen en una etiqueta específica
        if 0 <= index < len(self.image_labels):
            new_image = QPixmap(new_image_path)
            self.image_labels[index].setPixmap(new_image.scaled(30, 30))  # Cambiar imagen y escalar
            self.image_labels[index].repaint()

    def update_images(self):
        if self.image_index < len(self.image_paths):
            self.change_image(self.image_index, self.image_paths[self.image_index])
            self.image_index += 1
        else:
            self.timer.stop()  # Detener el temporizador cuando se complete
            self.bnt_aceptar.setEnabled(True)
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = frm_inicio()
    dialog.exec_()  # Mostrar el diálogo de manera modal
"""