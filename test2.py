import sys
import sqlite3
from pathlib import Path

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap


class TreeViewDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle("QTreeView con SQLite")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(Path('qss/estilos.qss').read_text())
        # Crear el QTreeView
        self.treeView = QTreeView()
        self.treeView.setIconSize(QSize(60, 60))
        self.treeView.setEditTriggers(QTreeView.NoEditTriggers)

        # Crear el modelo de datos
        self.model = QStandardItemModel()

        # Conectar a la base de datos SQLite
        self.connection = sqlite3.connect("db/physioMRI.db")

        # Cargar datos desde SQLite
        self.load_data_from_db()

        # Configurar el QTreeView con el modelo
        self.treeView.setModel(self.model)

        # Ocultar el encabezado de las columnas
        self.treeView.setHeaderHidden(True)

        # Crear el layout y añadir el QTreeView
        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
        self.treeView.clicked.connect(self.on_treeview_clicked)

    def on_treeview_clicked(self, index):
        # Obtener el ítem seleccionado
        item = self.model.itemFromIndex(index)

        # Si el ítem está desplegado, contraerlo; de lo contrario, expandirlo
        if self.treeView.isExpanded(index):
            self.treeView.collapse(index)
        else:
            self.treeView.expand(index)

    def load_data_from_db(self):
        cursor = self.connection.cursor()

        # Obtener las categorías
        #cursor.execute("SELECT A.id_estudio, B.protocolo, A.id_lado FROM estudios AS A JOIN protocolos AS B ON A.id_protocolo=B.id_protocolo WHERE A.id_paciente=1")
        cursor.execute("Select A.id_paciente, B.protocolo, C.lado, D.orientacion, B.imagen FROM estudios AS A "+
                       "JOIN protocolos AS B ON A.id_protocolo=B.id_protocolo " +
                       "JOIN lado AS C ON A.id_lado=C.id_lado " +
                       "JOIN orientacion AS D ON A.id_orientacion=D.id_orientacion " +
                       "WHERE A.id_paciente = 1")

        categories = cursor.fetchall()

        for category_id, category_name, category_lado, category_orientacion, category_imagen in categories:
            category_item = QStandardItem(str(category_name)+" "+str(category_lado)+" "+str(category_orientacion))
           # category_icon = QPixmap("template/black/"+category_imagen)
            category_icon = QIcon("template/black/"+category_imagen).pixmap(QSize(60, 60))  # Tamaño del icono 100x100 px
           # category_item.setIcon(QIcon(category_icon))  # Convertir QPixmap a QIcon
            category_item.setIcon(QIcon(category_icon))  # Convertir QPixmap a QIcon

            self.model.appendRow(category_item)


            # Obtener las subcategorías de cada categoría
            cursor.execute("SELECT nombre FROM secuencias_protocolo WHERE id_estudio = ?", (category_id,))
            subcategories = cursor.fetchall()
            for subcategory_name, in subcategories:
                subcategory_item = QStandardItem(subcategory_name)

                subcategory_icon = QIcon("template/black/escan.png").pixmap(QSize(60, 60))  # Tamaño del icono 100x100 px
                subcategory_item.setIcon(QIcon(subcategory_icon))  # Convertir QPixmap a QIcon
                category_item.appendRow(subcategory_item)

            # Añadir la categoría al modelo
            self.model.appendRow(category_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeViewDemo()
    window.show()
    sys.exit(app.exec_())
