from typing import TYPE_CHECKING

import numpy as np
import cv2

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from core import get_quadrilateral

from utils.qimage_numpy import ndarray_to_qimage

from imagedialog.widgets.imagedialogwidgetbase import ImageDialogWidgetBase
from imagedialog.widgets.originalpaperwidget import OriginalPaperWidget

if TYPE_CHECKING:
    from imagepopup import ImagePopup
    from imagedialog.widgets import OriginalImageWidget


class DetectPaperWidget(ImageDialogWidgetBase):
    def parent(self) -> 'ImagePopup':
        return super().parent()

    def __init__(self, parent: 'ImagePopup', brother: 'OriginalImageWidget') -> None:
        super().__init__(parent)
        self.scale = brother.scale
        self.quadrilateral = get_quadrilateral(parent.image_array_original)

        image_array_shown = parent.image_array_original.copy()
        cv2.drawContours(image_array_shown, [self.quadrilateral[:, None, :].astype(np.int32)], 0, (0, 0, 255), 20)
        image_array_shown = cv2.resize(image_array_shown, (0, 0), fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LANCZOS4)

        vbox = QVBoxLayout(self)

        self.imglbl = QLabel()
        vbox.addWidget(self.imglbl)

        self.imglbl.setScaledContents(True)
        self.imglbl.setPixmap(QPixmap.fromImage(ndarray_to_qimage(image_array_shown)))
        w, h = self.imglbl.pixmap().size().toTuple()
        self.imglbl.resize(w, h)

    def get_next_widget(self):
        return OriginalPaperWidget(self.parent(), self)
