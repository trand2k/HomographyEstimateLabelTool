import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel("Press arrow keys", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.label)

        self.setup_shortcuts()

    def setup_shortcuts(self):
        arrow_up_sequence = QKeySequence(QKeySequence.MoveToPreviousLine)
        arrow_down_sequence = QKeySequence(QKeySequence.MoveToNextLine)
        arrow_left_sequence = QKeySequence(QKeySequence.MoveToPreviousChar)
        arrow_right_sequence = QKeySequence(QKeySequence.MoveToNextChar)

        shortcut_arrow_up = QShortcut(arrow_up_sequence, self)
        shortcut_arrow_up.activated.connect(self.on_arrow_up)

        shortcut_arrow_down = QShortcut(arrow_down_sequence, self)
        shortcut_arrow_down.activated.connect(self.on_arrow_down)

        shortcut_arrow_left = QShortcut(arrow_left_sequence, self)
        shortcut_arrow_left.activated.connect(self.on_arrow_left)

        shortcut_arrow_right = QShortcut(arrow_right_sequence, self)
        shortcut_arrow_right.activated.connect(self.on_arrow_right)

    def on_arrow_up(self):
        self.label.setText("Arrow Up Pressed")

    def on_arrow_down(self):
        self.label.setText("Arrow Down Pressed")

    def on_arrow_left(self):
        self.label.setText("Arrow Left Pressed")

    def on_arrow_right(self):
        self.label.setText("Arrow Right Pressed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
