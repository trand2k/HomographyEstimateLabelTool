from osgeo import gdal
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QTransform, QPixmap, QImage
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QMenu, QAction, QFileDialog,QListWidget,QListWidgetItem
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import pyqtSignal
app = QApplication(sys.argv)
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QFileDialog,QShortcut,QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QTransform, QWheelEvent,QKeySequence
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QSplitter,QApplication, QMainWindow, QPushButton, QListWidget, QListWidgetItem,QSlider, QMenuBar
import sys
import cv2
import numpy as np
import os
from PyQt5.QtGui import QCloseEvent

class MainWindow2(QWidget):
    def __init__(self):
        super().__init__()

        menubar = self.createMenuBar()


        self.graphics_view = GraphicView(self)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # graphic 2
        self.graphics_view2 = GraphicView(self)
        self.scene2 = QGraphicsScene()
        self.graphics_view2.setScene(self.scene2)

        choose_image_1_button = QPushButton("Choose Image 1")
        choose_image_1_button.clicked.connect(self.choose_image_1)
        choose_image_2_button = QPushButton("Choose Image 2")
        choose_image_2_button.clicked.connect(self.choose_image_2)

        layout = QVBoxLayout(self)

        button_group = QHBoxLayout()

        button_group.addWidget(choose_image_1_button)
        button_group.addWidget(choose_image_2_button)

        layout.addLayout(button_group)

        # Add QSpliter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(self.graphics_view2)

        layout.addWidget(splitter)

        self.image_item = None
        self.image_item2 = None
        # add image to 2 graphics view
        self.image1 = cv2.imread("../image/1.jpg")
        self.image2 = cv2.imread("../image/2.jpg")
        # print(self.image1)
        # import pdb;pdb.set_trace()
        self.load_image(self.image1, self.image2)
        self.graphics_view.clicked.connect(self.handle_view1_click)
        self.graphics_view2.clicked.connect(self.handle_view2_click)

        self.mouse_click_point_1 = []
        self.mouse_click_point_2 = []

        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(0)
        slider.setMaximum(360)
        slider.setValue(0)
        slider.valueChanged.connect(self.slider_value_changed)
        layout.addWidget(slider)

        self.layout().setMenuBar(menubar)

        self.map_base_tiff_file = None
        self.data_homography_save_folder = None
        self.data_sub_map_folder = None
        self.data_sub_map_list = []
        self.map_data = None

    def createMenuBar(self):
        # Create a menu bar
        menubar = QMenuBar()

        # Create a File menu
        fileMenu = menubar.addMenu('File')

        # Create actions for the File menu
        open_all_action = fileMenu.addAction('Open all')
        choose_map_base_action = fileMenu.addAction('Choose map base')
        choose_sub_map_action = fileMenu.addAction('Choose folder sub-map')
        save_action = fileMenu.addAction('Choose folder save homoragapy')

        # Connect actions to functions (you need to implement these functions)
        open_all_action.triggered.connect(self.handle_open_all_click)
        choose_map_base_action.triggered.connect(self.handle_map_base_click)
        choose_sub_map_action.triggered.connect(self.handle_sub_map_click)
        save_action.triggered.connect(self.handle_save_click)

        return menubar
    
    def read_map(self,map_path):
        # print("data path : " , map_path)
        geotiff = gdal.Open(map_path)
        red = geotiff.GetRasterBand(1).ReadAsArray()
        green = geotiff.GetRasterBand(2).ReadAsArray()
        blue = geotiff.GetRasterBand(3).ReadAsArray()
        map_rgb = np.dstack((blue, green, red))
        return map_rgb

    def handle_open_all_click(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open All', options=options)
        if folder_path:
            pass
        pass

    def handle_map_base_click(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Map TIFF file', '', 'Images (*.tif);;All Files (*)', options=options)
        if file_path:
            self.handle_map_base_click_support(file_path)

    def handle_map_base_click_support(self, file_path):
        self.map_base_tiff_file = file_path
        # print(self.map_base_tiff_file)
        self.map_data = self.read_map(self.map_base_tiff_file)
        self.display_image_1(self.map_data)
        


    def handle_sub_map_click(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Image Folder', options=options)
        if folder_path:
            self.handle_sub_map_click_support(folder_path)

    def handle_map_base_click_support(self, folder_path):
        self.data_sub_map_folder = folder_path
        self.data_sub_map_list = [self.data_sub_map_folder + "/" + str(i) for i in os.listdir(self.data_sub_map_folder) if i.endswith((".tif"))]
        pass

    def handle_save_click(self):
        pass


    def choose_image_1(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Map TIFF file', '', 'Images (*.tif);;All Files (*)', options=options)

    def choose_image_2(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Map TIFF file', '', 'Images (*.tif);;All Files (*)', options=options)
    

    def rotate_view(self, angle):
        self.graphics_view.rotate_view(angle)

    def slider_value_changed(self, value):
        self.rotate_view(value)
    
    def closeEvent(self, event: QCloseEvent):
        # print("Window 1 is about to close.")
        self.destroyed.emit()  # Emit the custom signal
        super().closeEvent(event)
    
    def reset_point(self):
        self.mouse_click_point_1 = []
        self.mouse_click_point_2 = []

    def load_image(self, image1, image2):
        self.image1 = image1
        self.image2 = image2
        self.display_image_1(self.image1)
        self.display_image_2(self.image2)

    def handle_view1_click(self, pixel_coordinates):
        self.mouse_click_point_1.append((int(pixel_coordinates.x()), int(pixel_coordinates.y())))
        self.draw_points1()

    def draw_points1(self):
        image_with_points = np.copy(self.image1)

        for i, point in enumerate(self.mouse_click_point_1, 1):
            cv2.circle(image_with_points, point, 5, (255, 0, 0), -1)
            cv2.putText(image_with_points, str(i), (point[0] - 10, point[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)

        self.display_image_1(image_with_points)

    def handle_view2_click(self, pixel_coordinates):
        self.mouse_click_point_2.append((int(pixel_coordinates.x()), int(pixel_coordinates.y())))
        self.draw_points2()

    def draw_points2(self):
        image_with_points = np.copy(self.image2)

        for i, point in enumerate(self.mouse_click_point_2, 1):
            cv2.circle(image_with_points, point, 5, (255, 0, 0), -1)
            cv2.putText(image_with_points, str(i), (point[0] - 10, point[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)

        self.display_image_2(image_with_points)

    def display_image_1(self, image_data):
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
            self.image_item = None

        self.image_item = self.scene.addPixmap(pixmap)
        # print(self.image_item.boundingRect())
        self.graphics_view.setSceneRect(self.image_item.boundingRect())
        # self.graphics_view.show_image(image_data)

    def display_image_2(self, image_data):
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        if self.image_item2 is not None:
            self.scene2.removeItem(self.image_item2)
            self.image_item2 = None

        self.image_item2 = self.scene2.addPixmap(pixmap)
        self.graphics_view2.setSceneRect(self.image_item2.boundingRect())
        # self.graphics_view2.show_image(image_data)

    def keyPressEvent(self, event):
        print("key press")
        if event.key() == Qt.Key_A:
            self.close()

class GraphicView(QGraphicsView):
    clicked = pyqtSignal(QPointF)

    def __init__(self, parent=None):
        super(GraphicView, self).__init__(parent)
        self.setMouseTracking(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.zoom_factor = 1.0
        self.event_click = None
        self.move_mouse_event = None
        self.rotation_angle = 0


    def mousePressEvent(self, event):
        pos_in_image = self.mapToScene(event.pos())
        self.event_click = (pos_in_image.x(), pos_in_image.y())
        self.clicked.emit(pos_in_image)
        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        wheel_pos = event.pos()
        pos_in_scene_before_zoom = self.mapToScene(wheel_pos)
        factor = 1.2 if event.angleDelta().y() > 0 else 1.0 / 1.2

        self.zoom_factor *= factor
        self.setTransform(QTransform.fromScale(self.zoom_factor, self.zoom_factor))

        pos_in_scene_after_zoom = self.mapToScene(wheel_pos)
        delta = pos_in_scene_after_zoom - pos_in_scene_before_zoom
        self.centerOn(pos_in_scene_after_zoom)

        # Apply the rotation angle to the view transform
        transform = QTransform()
        transform.rotate(self.rotation_angle)
        transform.scale(self.zoom_factor, self.zoom_factor)
        self.setTransform(transform)

        super().wheelEvent(event)

    def show_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.setSceneRect(0, 0, width, height)

    def rotate_view(self, angle):
        self.rotation_angle = angle

        # Apply the rotation angle and zoom factor to the view transform
        transform = QTransform()
        transform.rotate(self.rotation_angle)
        transform.scale(self.zoom_factor, self.zoom_factor)
        self.setTransform(transform)

if __name__ == "__main__":
    # app = QApplication([])
    main_window = MainWindow2()
    main_window.show()
    app.exec_()