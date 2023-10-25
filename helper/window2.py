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
from PyQt5.QtWidgets import QSplitter,QApplication, QMainWindow, QPushButton, QListWidget, QListWidgetItem,QSlider
import sys
import cv2
import numpy as np
import os
from PyQt5.QtGui import QCloseEvent
class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.graphics_view = GraphicView(self.central_widget)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)


        # graphic 2
        self.graphics_view2 = GraphicView(self.central_widget)
        self.scene2 = QGraphicsScene()
        self.graphics_view2.setScene(self.scene2)

        layout = QVBoxLayout(self.central_widget)
        # Add QSpliter 
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(self.graphics_view2)

        
        layout.addWidget(splitter)

        self.image_item = None
        self.image_item2 = None
        # add image to 2 graphics view
        self.image1 = cv2.imread("image/1.jpg")
        self.image2 = cv2.imread("image/2.jpg")
        # import pdb;pdb.set_trace()
        self.load_image(self.image1, self.image2)
        self.graphics_view.clicked.connect(self.handle_view1_click)
        self.graphics_view2.clicked.connect(self.handle_view2_click)

        self.mouse_click_point_1 = []
        self.mouse_click_point_2 = []

    def closeEvent(self, event: QCloseEvent):
        # print("Window 1 is about to close.")
        self.destroyed.emit()  # Emit the custom signal
        super().closeEvent(event)
    
    def reset_point(self):
        self.mouse_click_point_1 = []
        self.mouse_click_point_2 = []
    
    def load_image(self,image1, image2):
        self.image1 = image1
        self.image2 = image2
        self.display_image_1(self.image1)
        self.display_image_2(self.image2)


    def handle_view1_click(self, pixel_coordinates):
        # print("Clicked on CustomGraphicsView1:", pixel_coordinates)
        self.mouse_click_point_1.append((int(pixel_coordinates.x()),int(pixel_coordinates.y())))
        # print(self.clicked_point)
        self.draw_points1()

    def draw_points1(self):
        # Create a copy of the original image_data
        image_with_points = np.copy(self.image1)

        # Draw points on the copy
        for i, point in enumerate(self.mouse_click_point_1, 1):
            cv2.circle(image_with_points, point, 5, (255, 0, 0), -1)
            # Add number to the point
            cv2.putText(image_with_points, str(i), (point[0] - 10, point[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)

        # Display the image with points
        self.display_image_1(image_with_points)



    def handle_view2_click(self, pixel_coordinates):
        # print("Clicked on CustomGraphicsView2:", pixel_coordinates)
        self.mouse_click_point_2.append((int(pixel_coordinates.x()),int(pixel_coordinates.y())))
        # print(self.clicked_point)
        self.draw_points2()

    def draw_points2(self):
        # Create a copy of the original image_data
        image_with_points = np.copy(self.image2)

        # Draw points on the copy
        for i, point in enumerate(self.mouse_click_point_2, 1):
            cv2.circle(image_with_points, point, 5, (255, 0, 0), -1)
            # Add number to the point
            cv2.putText(image_with_points, str(i), (point[0] - 10, point[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)

        # Display the image with points
        self.display_image_2(image_with_points)
        

    def display_image_1(self, image_data):
        # Convert the NumPy array to a QImage
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # Remove the previous pixmap from the scene
        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
            self.image_item = None

        # Set the pixmap to the QGraphicsPixmapItem
        self.image_item = self.scene.addPixmap(pixmap)

        # Set the scene rect to the image size
        self.graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
    
    def display_image_2(self, image_data):
        # Convert the NumPy array to a QImage
        height, width, channel = image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # Remove the previous pixmap from the scene
        if self.image_item2 is not None:
            self.scene2.removeItem(self.image_item2)
            self.image_item2 = None

        # Set the pixmap to the QGraphicsPixmapItem
        self.image_item2 = self.scene2.addPixmap(pixmap)

        # Set the scene rect to the image size
        self.graphics_view2.setSceneRect(0, 0, pixmap.width(), pixmap.height())

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

    def mousePressEvent(self, event):
        # Get the position in image coordinates
        # print("CustomGraphicViewer: ", event.pos())

        pos_in_image = self.mapToScene(event.pos())
        pixel_x = int(pos_in_image.x())
        pixel_y = int(pos_in_image.y())
        # print(f"Clicked at pixel location: ({pixel_x}, {pixel_y})")
        self.event_click = (pixel_x, pixel_y)
        # import pdb;pdb.set_trace()
        # Continue with the default behavior
        self.clicked.emit(pos_in_image)
        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        # Get the position of the wheel event in the view
        wheel_pos = event.pos()

        # Map the wheel position to the scene coordinates
        pos_in_scene_before_zoom = self.mapToScene(wheel_pos)

        # Zoom with the mouse wheel
        factor = 1.2 if event.angleDelta().y() > 0 else 1.0 / 1.2

        self.zoom_factor *= factor
        self.setTransform(QTransform.fromScale(self.zoom_factor, self.zoom_factor))

        # Map the wheel position to the scene coordinates after zoom
        pos_in_scene_after_zoom = self.mapToScene(wheel_pos)
        # pos_in_scene_after_zoom = wheel_pos
        # print(pos_in_scene_after_zoom)
        # Adjust the view center to keep the cursor position fixed
        delta = pos_in_scene_after_zoom - pos_in_scene_before_zoom
        # print(delta.x(), delta.y())
        # print("checkkking")
        self.centerOn(pos_in_scene_after_zoom)

        # Continue with the default behavior
        super().wheelEvent(event)

if __name__ == "__main__":
    # app = QApplication([])
    main_window = MainWindow2()
    main_window.show()
    app.exec_()