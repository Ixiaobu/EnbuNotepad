from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
import sys

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
            file_dialog.setFileMode(QFileDialog.ExistingFile)

            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    selected_file = selected_files[0]
                    self.setText(selected_file)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.custom_text_edit = CustomTextEdit()
        self.custom_text_edit.setPlaceholderText("Click here to select an image")
        self.custom_text_edit.setReadOnly(True)

        layout.addWidget(self.custom_text_edit)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())