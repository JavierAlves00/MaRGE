import sys

from PyQt5.QtWidgets import QApplication, QDialog

from ui_ayuda_nuevo_exp import Ui_ayuda_nuevo_exp
from pathlib import Path
from PyQt5.QtCore import Qt, QTimer
import variables
import utilidades


class frm_ayuda_nuevo_exp(QDialog, Ui_ayuda_nuevo_exp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_pantalla()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_fecha_hora)
        self.timer.start(1000)  # Actualiza cada segundo
        self.refrescar_fecha_hora()  # Inicializa con la fecha y hora actual
        self.exec_()

    def config_pantalla(self):
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.l_logo.setGeometry(0, 0, 1920, 1080)
        self.l_logo.setScaledContents(True)
        self.frame.setGeometry(int((variables.vg_ancho_pantalla / 2)) - int(self.frame.width() / 2), 40, int(self.frame.width()), int(self.frame.height()))
        self.fondo_sombra.setGeometry(self.frame.x(), self.frame.y(), self.frame.width(), self.frame.height())
        utilidades.sombra_frame_verde(self, self.fondo_sombra)
        self.l_usuario_acceso.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_fecha_hora.setStyleSheet("font-size: 40px; color: #787878;")
        self.l_usuario_acceso.setText("  " + variables.vg_usuario_nombre)

        self.btn_home.clicked.connect(self.volver_home)


    def volver_home(self):
        self.close()
    def refrescar_fecha_hora(self):
        utilidades.actualizar_fecha_hora(self.l_fecha_hora)

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = frm_ayuda_alt_usuarios()
    sys.exit(app.exec())
"""