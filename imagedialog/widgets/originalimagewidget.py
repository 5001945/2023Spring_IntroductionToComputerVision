from typing import TYPE_CHECKING

import cv2

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from utils.qimage_numpy import ndarray_to_qimage

from imagedialog.widgets.imagedialogwidgetbase import ImageDialogWidgetBase
from imagedialog.widgets.detectpaperwidget import DetectPaperWidget

if TYPE_CHECKING:
    from imagepopup import ImagePopup


class OriginalImageWidget(ImageDialogWidgetBase):
    def parent(self) -> 'ImagePopup':
        return super().parent()

    def __init__(self, parent: 'ImagePopup') -> None:
        super().__init__(parent)
        self.scale = 800 / max(parent.image_array_original.shape[:2])  # 긴 쪽을 800픽셀로 맞춘다.

        image_array_shown = cv2.resize(parent.image_array_original, (0, 0), fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LANCZOS4)

        vbox = QVBoxLayout(self)
        # self.scrollArea = QScrollArea()

        self.imglbl = QLabel()
        vbox.addWidget(self.imglbl)
        # self.scrollArea.setWidget(self.imglbl)

        self.imglbl.setScaledContents(True)
        self.imglbl.setPixmap(QPixmap.fromImage(ndarray_to_qimage(image_array_shown)))
        w, h = self.imglbl.pixmap().size().toTuple()
        self.imglbl.resize(w, h)

    def get_next_widget(self):
        return DetectPaperWidget(self.parent(), self)
