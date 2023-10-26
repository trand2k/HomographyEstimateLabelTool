import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QToolBar, QVBoxLayout, QWidget, QUndoStack


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Undo Redo Example')
        self.setGeometry(100, 100, 800, 600)

        # Create a QTextEdit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create an undo stack
        self.undo_stack = QUndoStack(self)

        # Create actions for undo and redo
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.redo)

        # Create a toolbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Add undo and redo actions to the toolbar
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)

        # Connect the undo stack to the text edit for undo and redo support
        self.undo_stack.setUndoLimit(10)  # Set the maximum number of undo actions
        self.text_edit.document().undoAvailable.connect(undo_action.setEnabled)
        self.text_edit.document().redoAvailable.connect(redo_action.setEnabled)

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
