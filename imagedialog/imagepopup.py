import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QBrush, QColor, QImage, QMouseEvent, QPaintEvent, QPen, QPixmap, QPainter, Qt, QIntValidator
from PySide6.QtWidgets import *

from utils.qimage_numpy import qimage_to_ndarray

from imagedialog.widgets import OriginalImageWidget, DetectPaperWidget
if TYPE_CHECKING:
    from imagedialog.widgets import ImageDialogWidgetBase


class ImagePopup(QDialog):
    def __init__(self, parent: QWidget, path: str, image: QImage) -> None:
        super().__init__(parent)

        self.image_array_original = qimage_to_ndarray(image)

        self.setWindowTitle(path)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # initialize UI
        self.vbox = QVBoxLayout(self)

        self.description_lbl = QLabel()
        self.vbox.addWidget(self.description_lbl)

        self.widgets = [
            OriginalImageWidget(self),
        ]
        for w in self.widgets:
            self.vbox.addWidget(w)
            w.hide()
        self.widgets[0].show()

        grid2 = QGridLayout()
        self.vbox.addLayout(grid2)
        self.prev_btn = QPushButton("< Prev")
        self.prev_btn.clicked.connect(self.prev)
        grid2.addWidget(self.prev_btn, 0, 0)
        self.next_btn = QPushButton("Next >")
        self.next_btn.clicked.connect(self.next)
        grid2.addWidget(self.next_btn, 0, 2)
        grid2.setColumnStretch(0, 1)
        grid2.setColumnStretch(1, 2)
        grid2.setColumnStretch(2, 1)

        self.set_prev_next_state()

    @property
    def current_widget(self) -> 'ImageDialogWidgetBase':
        return self.widgets[-1]
    
    def set_prev_next_state(self):
        widget_numbers = len(self.widgets)
        if widget_numbers == 1:
            self.prev_btn.setEnabled(False)
        else:
            self.prev_btn.setEnabled(True)

        if widget_numbers == 5:
            self.next_btn.setText("Finish")
        else:
            self.next_btn.setText("Next >")

    @Slot()
    def prev(self):
        self.current_widget.hide()
        self.vbox.replaceWidget(self.current_widget, self.widgets[-2])
        self.widgets.pop()
        self.set_prev_next_state()
        self.current_widget.show()

    @Slot()
    def next(self):
        self.current_widget.hide()
        widget = self.current_widget.get_next_widget()
        if widget is True:
            self.close()
            return
        elif widget is False:
            return
        self.widgets.append(widget)
        self.vbox.replaceWidget(self.widgets[-2], self.current_widget)
        self.set_prev_next_state()
        self.current_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ImagePopup()
    win.show()
    app.exec()
