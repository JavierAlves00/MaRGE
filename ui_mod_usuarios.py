# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mod_usuarios.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mod_usuarios(object):
    def setupUi(self, mod_usuarios):
        mod_usuarios.setObjectName("mod_usuarios")
        mod_usuarios.resize(1920, 1080)
        self.frame = QtWidgets.QFrame(mod_usuarios)
        self.frame.setGeometry(QtCore.QRect(320, 140, 350, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.l_nombre = QtWidgets.QLabel(self.frame)
        self.l_nombre.setGeometry(QtCore.QRect(10, 129, 321, 29))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nombre.setFont(font)
        self.l_nombre.setObjectName("l_nombre")
        self.cb_acceso = QtWidgets.QComboBox(self.frame)
        self.cb_acceso.setGeometry(QtCore.QRect(10, 430, 331, 40))
        self.cb_acceso.setObjectName("cb_acceso")
        self.cb_acceso.addItem("")
        self.cb_acceso.addItem("")
        self.le_password2 = QtWidgets.QLineEdit(self.frame)
        self.le_password2.setGeometry(QtCore.QRect(10, 334, 331, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_password2.setFont(font)
        self.le_password2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password2.setObjectName("le_password2")
        self.l_password = QtWidgets.QLabel(self.frame)
        self.l_password.setGeometry(QtCore.QRect(10, 215, 321, 29))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_password.setFont(font)
        self.l_password.setObjectName("l_password")
        self.l_password2 = QtWidgets.QLabel(self.frame)
        self.l_password2.setGeometry(QtCore.QRect(10, 304, 331, 29))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_password2.setFont(font)
        self.l_password2.setObjectName("l_password2")
        self.l_nivelacceso = QtWidgets.QLabel(self.frame)
        self.l_nivelacceso.setGeometry(QtCore.QRect(10, 395, 321, 29))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_nivelacceso.setFont(font)
        self.l_nivelacceso.setObjectName("l_nivelacceso")
        self.le_password = QtWidgets.QLineEdit(self.frame)
        self.le_password.setGeometry(QtCore.QRect(10, 246, 331, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_password.setFont(font)
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setObjectName("le_password")
        self.le_nombre = QtWidgets.QLineEdit(self.frame)
        self.le_nombre.setGeometry(QtCore.QRect(10, 159, 331, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_nombre.setFont(font)
        self.le_nombre.setObjectName("le_nombre")
        self.btn_cancelar = QtWidgets.QPushButton(self.frame)
        self.btn_cancelar.setGeometry(QtCore.QRect(118, 10, 112, 108))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_cancelar.sizePolicy().hasHeightForWidth())
        self.btn_cancelar.setSizePolicy(sizePolicy)
        self.btn_cancelar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_cancelar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("template/black/icono_cancelar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cancelar.setIcon(icon)
        self.btn_cancelar.setIconSize(QtCore.QSize(100, 100))
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.btn_ayuda = QtWidgets.QPushButton(self.frame)
        self.btn_ayuda.setGeometry(QtCore.QRect(230, 10, 112, 108))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ayuda.sizePolicy().hasHeightForWidth())
        self.btn_ayuda.setSizePolicy(sizePolicy)
        self.btn_ayuda.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_ayuda.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("template/black/ayuda.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ayuda.setIcon(icon1)
        self.btn_ayuda.setIconSize(QtCore.QSize(100, 100))
        self.btn_ayuda.setObjectName("btn_ayuda")
        self.btn_aceptar = QtWidgets.QPushButton(self.frame)
        self.btn_aceptar.setGeometry(QtCore.QRect(6, 10, 112, 108))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_aceptar.sizePolicy().hasHeightForWidth())
        self.btn_aceptar.setSizePolicy(sizePolicy)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_aceptar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("template/black/icono_aceptar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_aceptar.setIcon(icon2)
        self.btn_aceptar.setIconSize(QtCore.QSize(100, 100))
        self.btn_aceptar.setObjectName("btn_aceptar")
        self.fondo_sombra = QtWidgets.QPushButton(mod_usuarios)
        self.fondo_sombra.setGeometry(QtCore.QRect(650, 600, 75, 23))
        self.fondo_sombra.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fondo_sombra.setText("")
        self.fondo_sombra.setFlat(False)
        self.fondo_sombra.setObjectName("fondo_sombra")
        self.l_logo = QtWidgets.QLabel(mod_usuarios)
        self.l_logo.setGeometry(QtCore.QRect(900, 290, 451, 201))
        self.l_logo.setText("")
        self.l_logo.setPixmap(QtGui.QPixmap("logo/logo_empresa.png"))
        self.l_logo.setObjectName("l_logo")
        self.l_logo.raise_()
        self.fondo_sombra.raise_()
        self.frame.raise_()

        self.retranslateUi(mod_usuarios)
        self.cb_acceso.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mod_usuarios)
        mod_usuarios.setTabOrder(self.le_nombre, self.le_password)
        mod_usuarios.setTabOrder(self.le_password, self.le_password2)

    def retranslateUi(self, mod_usuarios):
        _translate = QtCore.QCoreApplication.translate
        mod_usuarios.setWindowTitle(_translate("mod_usuarios", "Form"))
        self.l_nombre.setText(_translate("mod_usuarios", "Nombre"))
        self.cb_acceso.setItemText(0, _translate("mod_usuarios", "Admin"))
        self.cb_acceso.setItemText(1, _translate("mod_usuarios", "User"))
        self.l_password.setText(_translate("mod_usuarios", "Contraseña"))
        self.l_password2.setText(_translate("mod_usuarios", "Repetir Contraseña"))
        self.l_nivelacceso.setText(_translate("mod_usuarios", "Nivel de Acceso"))
