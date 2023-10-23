from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QGraphicsView, QGraphicsScene, QSizePolicy, QSplitter

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Resizable Elements')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Create a QPushButton
        button = QPushButton('Resizable Button')
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create a QGraphicsView
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        graphics_view.setScene(scene)

        # Create a QWidget to hold the QVBoxLayout
        widget_with_layout = QWidget()
        widget_layout = QVBoxLayout(widget_with_layout)
        widget_layout.addWidget(button)

        # Create a QSplitter and add the QWidget and QGraphicsView to it
        splitter = QSplitter()
        splitter.addWidget(widget_with_layout)
        splitter.addWidget(graphics_view)

        layout.addWidget(splitter)

        self.setLayout(layout)

        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
