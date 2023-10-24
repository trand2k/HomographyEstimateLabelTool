from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MyMainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 2")

        button = QPushButton("Close Window", self)
        button.clicked.connect(self.close)

        self.setCentralWidget(button)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        button = QPushButton("Open Window", self)
        button.clicked.connect(self.open_window)

        self.setCentralWidget(button)
        self.window1 = MyMainWindow2()
    def open_window(self):
        print("Open Window")
        # window1 = MyMainWindow2()
        self.window1.show()

if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec_()