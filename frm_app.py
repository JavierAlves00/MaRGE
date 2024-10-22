import ctypes
import json
import os
import subprocess
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow

from configs import sys_config

from ui_app import Ui_mw_app
from PyQt5.QtGui import QGuiApplication
import platform
import variables
import ctypes
import subprocess
import faulthandler

# Run the gui
faulthandler.enable()


# *****************************************************************************
# Get the directory of the current script
main_directory = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory (one level up)
parent_directory = os.path.dirname(main_directory)

# Define the subdirectories you want to add to sys.path
subdirs = ['marcos_client']



# Add the subdirectories to sys.path
for subdir in subdirs:
    full_path = os.path.join(parent_directory, subdir)
    sys.path.append(full_path)


# Add folders
if not os.path.exists('experiments/parameterization'):
    os.makedirs('experiments/parameterization')
if not os.path.exists('calibration'):
    os.makedirs('calibration')
if not os.path.exists('protocols'):
    os.makedirs('protocols')
#if not os.path.exists(sys_config.screenshot_folder):
#    os.makedirs(sys_config.screenshot_folder)


# Obtenemos el sistema operativo: Windows o Linux -------------------------------------------
# almacenamos la resolución de pantalla -----------------------------------------------------
os_name = platform.system()

if os_name=="Windows":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # Permite obtener la resolución real en Windows
    variables.vg_ancho_pantalla = user32.GetSystemMetrics(0)
    variables.vg_alto_pantalla = user32.GetSystemMetrics(1)
elif os_name=="Linux":
    output = subprocess.check_output('xrandr | grep "\\*" | cut -d" " -f4', shell=True)
    resolution = output.decode().strip()
    #width, height = resolution.split('x')
    width = 1920
    height = 1080
    variables.vg_ancho_pantalla = int(width)
    variables.vg_alto_pantalla = int(height)
    variables.vg_paciente = ''
    variables.vg_fechaHora = ''
#----------------------------------------------------------------------------------------------

class frm_app(QMainWindow, Ui_mw_app):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #-------------------------------------------------------- logotipo de la empresa -------------------------
        self.l_logo.setGeometry(0,0,int(variables.vg_ancho_pantalla),int(variables.vg_alto_pantalla))
        self.l_logo.setScaledContents(True)
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        #-------------------------------------------------------- ruta de la app ---------------------------------
        variables.vg_ruta_app = os.getcwd()
        #-------------------------------------------------------- carga archivo de configuración -----------------
        with open("config.json", encoding='utf-8') as contenido:
            datos = json.load(contenido)
            variables.vg_idioma = datos["idioma"]
            variables.vg_logo = datos["logo"]
            variables.vg_qss = datos["qss"]
            variables.vg_medidaPeso = "Kg."
        #-------------------------------------------------- Volcado variables según idioma ------------------------
        with open(variables.vg_ruta_app+'/idiomas/'+variables.vg_idioma+'.json', encoding='utf-8') as contenido:
            datos = json.load(contenido)
            variables.vg_aceptar = datos["aceptar"]
            variables.vg_cancelar = datos["cancelar"]
            variables.vg_salir = datos["salir"]
            variables.vg_msg_eliminar = datos["msg_eliminar"]
            variables.vg_usuario = datos["usuario"]
            variables.vg_contrasenya = datos["contrasenya"]
            variables.msg_contrasenya = datos["msg_contrasenya"]
            variables.msg_contrasenya2 = datos["msg_contrasenya2"]
        # ---------------------------------------------------------------------------------------------------------
      #  self.abrir_frm_acceso_main()

      #  self.abrir_inicio_hardware()

    def abrir_inicio_hardware(self):
        from frm_inicio import frm_inicio
        self.ventana3 = frm_inicio()
        self.ventana3.exec_()

    def abrir_frm_acceso_main(self):
        from frm_acceso import frm_acceso_main
        self.ventana3 = frm_acceso_main(self)
        self.ventana3.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_app()
    ventana.show()
    ventana.abrir_inicio_hardware()
    sys.exit(app.exec())












