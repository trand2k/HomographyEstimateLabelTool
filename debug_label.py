import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a combo box
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Option 1")
        self.comboBox.addItem("Option 2")
        self.comboBox.addItem("Option 3")

        # Create a label to display the selected item
        self.label = QLabel("Selected: ", self)  # Initialize with a default text
        self.label.setAlignment(Qt.AlignCenter)

        # Create a reset button
        self.resetButton = QPushButton("Reset Combo Box", self)
        self.resetButton.clicked.connect(self.reset_combo_box)

        # Create a layout and add the combo box, label, and button to it
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.label)
        layout.addWidget(self.resetButton)

        # Create a central widget and set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)

        # Connect the combo box's currentIndexChanged signal to a slot
        self.comboBox.currentIndexChanged.connect(self.update_label)

    def update_label(self):
        # Update the label with the selected item
        selected_item = self.comboBox.currentText()
        self.label.setText(f"Selected: {selected_item}")

    def reset_combo_box(self):
        # Clear all items in the combo box
        self.comboBox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
