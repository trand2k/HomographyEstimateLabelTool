import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QApplication, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTransform

class RotatableGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setSceneRect(-50, -50, 100, 100)

        rect_item = QGraphicsRectItem(-20, -20, 40, 40)
        self.scene().addItem(rect_item)

    def rotate_view(self, angle):
        transform = QTransform()
        transform.rotate(angle)
        self.setTransform(transform)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.graphics_view = RotatableGraphicsView()
        layout.addWidget(self.graphics_view)

        rotate_button = QPushButton("Rotate View", self)
        # rotate_button.clicked.connect(self.rotate_view)
        layout.addWidget(rotate_button)

        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(0)
        slider.setMaximum(360)
        slider.setValue(0)
        slider.valueChanged.connect(self.slider_value_changed)
        layout.addWidget(slider)

        self.setLayout(layout)

    def rotate_view(self, angle):
        self.graphics_view.rotate_view(angle)

    def slider_value_changed(self, value):
        self.rotate_view(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
