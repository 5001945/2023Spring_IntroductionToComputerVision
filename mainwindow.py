import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from imagedialog import ImagePopup


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Computer Vision Final Project")

        self.open_btn = QPushButton("Open Image...")
        self.setCentralWidget(self.open_btn)
        self.open_btn.clicked.connect(self.open_img)

    @Slot()
    def open_img(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "..", "Image Files (*.png;*.jpg;*.bmp);;All Files (*.*)")
        if filename:
            img = QImage(filename)
            img.convertTo(QImage.Format.Format_RGBA8888)
            if img.isNull():
                QMessageBox.information(self, "Error", "Cannot load image.")
            else:
                popup = ImagePopup(self, filename, img)
                popup.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
