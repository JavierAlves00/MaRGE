import sys
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFileDialog, QMainWindow, \
    QSizePolicy
from PyQt5.QtCore import Qt


class DicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dicom Viewer')

        self.dicom_image = None
        self.contrast = 1.0
        self.zoom = 1.0
        self.start_point = None
        self.end_point = None
        self.rect = None

        self.initUI()

    def initUI(self):
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QVBoxLayout(main_widget)
        button_layout = QHBoxLayout()

        # Image display
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        main_layout.addWidget(self.canvas)

        # Buttons
        load_button = QPushButton('Cargar DICOM')
        load_button.clicked.connect(self.load_dicom)
        button_layout.addWidget(load_button)

        zoom_button = QPushButton('Zoom')
        zoom_button.clicked.connect(self.adjust_zoom)
        button_layout.addWidget(zoom_button)

        contrast_button = QPushButton('Contraste')
        contrast_button.clicked.connect(self.adjust_contrast)
        button_layout.addWidget(contrast_button)

        distance_button = QPushButton('Marcar Distancia')
        distance_button.clicked.connect(self.mark_distance)
        button_layout.addWidget(distance_button)

        # Add layouts to main layout
        main_layout.addLayout(button_layout)

        # Canvas interaction
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def load_dicom(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm)")
        if file_path:
            dicom_data = pydicom.dcmread(file_path)
            self.dicom_image = dicom_data.pixel_array
            self.display_image()

    def display_image(self):
        if self.dicom_image is not None:
            self.ax.clear()
            self.ax.imshow(self.dicom_image, cmap='gray')
            self.canvas.draw()

    def adjust_zoom(self):
        if self.dicom_image is not None:
            self.zoom = self.zoom * 1.2 if self.zoom < 4.0 else 1.0  # Toggle zoom
            zoomed_image = self.zoom_image(self.dicom_image, self.zoom)
            self.ax.clear()
            self.ax.imshow(zoomed_image, cmap='gray')
            self.canvas.draw()

    def zoom_image(self, image, zoom_factor):
        height, width = image.shape
        center_x, center_y = width // 2, height // 2
        new_width, new_height = int(width / zoom_factor), int(height / zoom_factor)

        cropped_image = image[
                        max(center_y - new_height // 2, 0):min(center_y + new_height // 2, height),
                        max(center_x - new_width // 2, 0):min(center_x + new_width // 2, width)
                        ]

        zoomed_image = np.clip(cropped_image, 0, 255)
        return zoomed_image

    def adjust_contrast(self):
        if self.dicom_image is not None:
            self.contrast = self.contrast + 0.2 if self.contrast < 2.0 else 1.0  # Toggle contraste
            adjusted_image = self.adjust_image_contrast(self.dicom_image, self.contrast)
            self.ax.clear()
            self.ax.imshow(adjusted_image, cmap='gray')
            self.canvas.draw()

    def adjust_image_contrast(self, image, contrast_factor):
        return np.clip(image * contrast_factor, 0, 255)

    def mark_distance(self):
        pass

    def on_press(self, event):
        if event.inaxes!=self.ax:
            return
        self.start_point = (event.xdata, event.ydata)
        if self.rect:
            self.rect.remove()
        self.rect = Rectangle(self.start_point, 0, 0, linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(self.rect)

    def on_release(self, event):
        if event.inaxes!=self.ax or self.start_point is None:
            return
        self.end_point = (event.xdata, event.ydata)
        x0, y0 = self.start_point
        x1, y1 = self.end_point
        distance = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        print(f"Distance: {distance:.2f}")

    def on_motion(self, event):
        if self.start_point is None or event.inaxes!=self.ax:
            return
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        width = x1 - x0
        height = y1 - y0
        self.rect.set_width(width)
        self.rect.set_height(height)
        self.canvas.draw()


if __name__=='__main__':
    app = QApplication(sys.argv)
    viewer = DicomViewer()
    viewer.show()
    sys.exit(app.exec_())
