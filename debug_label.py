from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
class MyMainWindow2(QMainWindow):
    request_close = pyqtSignal()  # Custom signal indicating the intention to close

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Window 2")

        button = QPushButton("Close Window", self)
        button.clicked.connect(self.request_close.emit)  # Emit the signal when the button is clicked

        self.setCentralWidget(button)

    def closeEvent(self, event: QCloseEvent):
        # print("Window 1 is about to close.")
        self.destroyed.emit()  # Emit the custom signal
        super().closeEvent(event)
    # def keyPressEvent(self, event):
    #     print("key press")
    #     if event.key() == Qt.Key_A:
    #         self.destroy()
    #         self.destroyed.emit()
            # self.destroy()
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        button = QPushButton("Open Window", self)
        button.clicked.connect(self.open_window)

        self.setCentralWidget(button)
        self.window1 = MyMainWindow2(parent=self)
        self.window1.destroyed.connect(self.handle_window1_closed)

        # Connect the custom signal to a slot method
        # self.window1.request_close.connect(self.handle_request_close)

    def open_window(self):
        print("Open Window")
        self.window1.show()

    def handle_window1_closed(self):
        print("check condition")
        self.window1.destroyed.connect(self.handle_window1_closed)
        # # self.window1 = MyMainWindow2()
        # self.window1.destroyed.connect(self.handle_window1_closed)
        # if self.check_conditions():
        #     # Conditions are met, close window1
        #     self.window1.show()
        # else:
        #     # Conditions are not met, show a warning
        #     QMessageBox.warning(self, "Warning", "Conditions not satisfied. Cannot close Window 1.")
        #     # self.window1.show()

    def check_conditions(self):
        # Replace this with your actual conditions
        return False  # or False
    

if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec_()
