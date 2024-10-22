from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QLabel


# pone la sombra de los formularios dialogos
def sombra_frame_azul(iform, iframe):
    sombra = QGraphicsDropShadowEffect(iform)
    sombra.setBlurRadius(8)
    sombra.setXOffset(1)
    sombra.setYOffset(1)
    sombra.setColor(QColor(20, 200, 220, 255))
    iframe.setGraphicsEffect(sombra)
    iform.update()
    iform.repaint()

def sombra_frame_verde(iform, iframe):
    sombra = QGraphicsDropShadowEffect(iform)
    sombra.setBlurRadius(8)
    sombra.setXOffset(1)
    sombra.setYOffset(1)
    sombra.setColor(QColor(73, 156, 60, 255))
    iframe.setGraphicsEffect(sombra)
    iform.update()
    iform.repaint()

def sombra_frame_rojo(iform, iframe):
    sombra = QGraphicsDropShadowEffect(iform)
    sombra.setBlurRadius(8)
    sombra.setXOffset(1)
    sombra.setYOffset(1)
    sombra.setColor(QColor(168, 37, 26, 255))
    iframe.setGraphicsEffect(sombra)
    iform.update()
    iform.repaint()

def sombra_frame_resaltar(iform, iframe):
    sombra = QGraphicsDropShadowEffect(iform)
    sombra.setBlurRadius(58)
    sombra.setXOffset(5)
    sombra.setYOffset(5)
    sombra.setColor(QColor(255, 131, 3, 255))
    iframe.setGraphicsEffect(sombra)
    iform.update()
    iform.repaint()

def sombra_frame_desactivar(iform, iframe):
    iframe.setGraphicsEffect(None)
    iform.update()
    iform.repaint()

def actualizar_fecha_hora(label: QLabel):
    current_date_time = QDateTime.currentDateTime()
    label.setText(current_date_time.toString("yyyy-MM-dd HH:mm:ss"+" "))