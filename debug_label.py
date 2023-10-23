import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.label = QLabel("Press and hold Ctrl, click, and release", self)
        self.setCentralWidget(self.label)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Ctrl + Mouse Click/Release Example")

    def mouseMoveEvent(self, event):
        # Check if the Ctrl key is pressed during mouse move
        if event.modifiers() == Qt.ControlModifier:
            x, y = event.x(), event.y()
            self.label.setText(f"Ctrl + Mouse Move: ({x}, {y})")

    def mousePressEvent(self, event):
        # Check if the Ctrl key is pressed during mouse press
        if event.modifiers() == Qt.ControlModifier:
            x, y = event.x(), event.y()
            self.label.setText(f"Ctrl + Mouse Press: ({x}, {y})")

    def mouseReleaseEvent(self, event):
        # Check if the Ctrl key is pressed during mouse release
        if event.modifiers() == Qt.ControlModifier:
            x, y = event.x(), event.y()
            self.label.setText(f"Ctrl + Mouse Release: ({x}, {y})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
