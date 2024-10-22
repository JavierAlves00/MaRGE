# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prueba_centro.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_alt_usuarios(object):
    def setupUi(self, alt_usuarios):
        alt_usuarios.setObjectName("alt_usuarios")
        alt_usuarios.resize(953, 684)
        self.widget = QtWidgets.QWidget(alt_usuarios)
        self.widget.setGeometry(QtCore.QRect(430, 210, 350, 369))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_cancelar = QtWidgets.QPushButton(self.widget)
        self.btn_cancelar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_cancelar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../template/black/icono_cancelar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cancelar.setIcon(icon)
        self.btn_cancelar.setIconSize(QtCore.QSize(100, 100))
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.gridLayout.addWidget(self.btn_cancelar, 0, 1, 1, 1)
        self.l_nombre_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nombre_2.setFont(font)
        self.l_nombre_2.setObjectName("l_nombre_2")
        self.gridLayout.addWidget(self.l_nombre_2, 3, 0, 1, 3)
        self.btn_aceptar = QtWidgets.QPushButton(self.widget)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_aceptar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../template/black/icono_aceptar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_aceptar.setIcon(icon1)
        self.btn_aceptar.setIconSize(QtCore.QSize(100, 100))
        self.btn_aceptar.setObjectName("btn_aceptar")
        self.gridLayout.addWidget(self.btn_aceptar, 0, 0, 1, 1)
        self.le_nombre = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_nombre.setFont(font)
        self.le_nombre.setObjectName("le_nombre")
        self.gridLayout.addWidget(self.le_nombre, 2, 0, 1, 2)
        self.btn_ayuda = QtWidgets.QPushButton(self.widget)
        self.btn_ayuda.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../template/black/ayuda.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ayuda.setIcon(icon2)
        self.btn_ayuda.setIconSize(QtCore.QSize(100, 100))
        self.btn_ayuda.setObjectName("btn_ayuda")
        self.gridLayout.addWidget(self.btn_ayuda, 0, 2, 1, 1)
        self.le_password = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_password.setFont(font)
        self.le_password.setObjectName("le_password")
        self.gridLayout.addWidget(self.le_password, 4, 0, 1, 2)
        self.l_nombre_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nombre_4.setFont(font)
        self.l_nombre_4.setObjectName("l_nombre_4")
        self.gridLayout.addWidget(self.l_nombre_4, 7, 0, 1, 3)
        self.cb_acceso = QtWidgets.QComboBox(self.widget)
        self.cb_acceso.setObjectName("cb_acceso")
        self.cb_acceso.addItem("")
        self.cb_acceso.addItem("")
        self.gridLayout.addWidget(self.cb_acceso, 8, 0, 1, 2)
        self.l_nombre_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nombre_3.setFont(font)
        self.l_nombre_3.setObjectName("l_nombre_3")
        self.gridLayout.addWidget(self.l_nombre_3, 5, 0, 1, 3)
        self.l_nombre = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nombre.setFont(font)
        self.l_nombre.setObjectName("l_nombre")
        self.gridLayout.addWidget(self.l_nombre, 1, 0, 1, 3)
        self.le_password2 = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_password2.setFont(font)
        self.le_password2.setObjectName("le_password2")
        self.gridLayout.addWidget(self.le_password2, 6, 0, 1, 2)

        self.retranslateUi(alt_usuarios)
        self.cb_acceso.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(alt_usuarios)

    def retranslateUi(self, alt_usuarios):
        _translate = QtCore.QCoreApplication.translate
        alt_usuarios.setWindowTitle(_translate("alt_usuarios", "Form"))
        self.l_nombre_2.setText(_translate("alt_usuarios", "Contraseña"))
        self.l_nombre_4.setText(_translate("alt_usuarios", "Nivel de Acceso"))
        self.cb_acceso.setItemText(0, _translate("alt_usuarios", "Admin"))
        self.cb_acceso.setItemText(1, _translate("alt_usuarios", "User"))
        self.l_nombre_3.setText(_translate("alt_usuarios", "Repetir Contraseña"))
        self.l_nombre.setText(_translate("alt_usuarios", "Nombre"))
