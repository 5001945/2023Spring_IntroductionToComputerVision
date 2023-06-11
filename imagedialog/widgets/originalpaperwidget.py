from typing import TYPE_CHECKING

import numpy as np
import cv2

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from core import get_a4

from utils.qimage_numpy import ndarray_to_qimage

from imagedialog.widgets.imagedialogwidgetbase import ImageDialogWidgetBase
from imagedialog.widgets.ocrwidget import OcrWidget

if TYPE_CHECKING:
    from imagepopup import ImagePopup
    from imagedialog.widgets import DetectPaperWidget


class OriginalPaperWidget(ImageDialogWidgetBase):
    def parent(self) -> 'ImagePopup':
        return super().parent()

    def __init__(self, parent: 'ImagePopup', brother: 'DetectPaperWidget') -> None:
        super().__init__(parent)
        self.a4_array = get_a4(parent.image_array_original, brother.quadrilateral)

        image_array_shown = cv2.resize(self.a4_array, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LANCZOS4)
        image_array_shown = np.stack([image_array_shown] * 3, axis=2)

        vbox = QVBoxLayout(self)

        self.imglbl = QLabel()
        vbox.addWidget(self.imglbl)

        self.imglbl.setScaledContents(True)
        self.imglbl.setPixmap(QPixmap.fromImage(ndarray_to_qimage(image_array_shown)))
        w, h = self.imglbl.pixmap().size().toTuple()
        self.imglbl.resize(w, h)
    
    def get_next_widget(self):
        return OcrWidget(self.parent(), self)
