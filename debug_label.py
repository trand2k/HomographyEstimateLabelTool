from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow 1")
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Switch to MainWindow 2", self)
        self.button.clicked.connect(self.switch_to_main_window2)

    def switch_to_main_window2(self):
        self.hide()
        main_window2.show()

class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow 2")
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Switch to MainWindow 1", self)
        self.button.clicked.connect(self.switch_to_main_window1)

    def switch_to_main_window1(self):
        self.hide()
        main_window1.show()

app = QApplication([])

main_window1 = MainWindow1()
main_window2 = MainWindow2()

main_window1.show()

app.exec_()
