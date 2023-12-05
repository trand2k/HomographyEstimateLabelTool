import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    task_completed = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.count = 201
    def run(self):
        for i in range(1, self.count):
            self.update_progress.emit(int(i/(self.count//100)))
            self.msleep(100)  # Simulate some work

        # Task completed, emit the signal
        self.task_completed.emit()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        start_button = QPushButton('Start Task', self)
        start_button.clicked.connect(self.start_task)
        layout.addWidget(start_button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Qt Progress Bar Example')
        self.show()

    def start_task(self):
        self.worker_thread = WorkerThread()
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_completed.connect(self.task_completed)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def task_completed(self):
        print("Task completed. Do something here.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
