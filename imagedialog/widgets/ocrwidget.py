from typing import TYPE_CHECKING

import numpy as np
import cv2

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPaintEvent, QPen, QPixmap, QPainter, Qt, QIntValidator
from PySide6.QtWidgets import *

from core import get_ocr_results, get_corresponding_fonts

from utils.qimage_numpy import ndarray_to_qimage

from imagedialog.widgets.imagedialogwidgetbase import ImageDialogWidgetBase
from imagedialog.widgets.pdfviewwidget import PdfViewWidget

if TYPE_CHECKING:
    from imagepopup import ImagePopup
    from imagedialog.widgets import OriginalPaperWidget

class OcrWidget(ImageDialogWidgetBase):
    def parent(self) -> 'ImagePopup':
        return super().parent()

    def __init__(self, parent: 'ImagePopup', brother: 'OriginalPaperWidget') -> None:
        super().__init__(parent)
        self.results = get_ocr_results(brother.a4_array)
        self.each_fonts = get_corresponding_fonts(brother.a4_array, self.results)

        image_array_shown = cv2.cvtColor(brother.a4_array.copy(), cv2.COLOR_GRAY2RGB)
        for (bbox, text, prob) in self.results:
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            cv2.rectangle(image_array_shown, tl, br, (0, 255, 0), 5)
        image_array_shown = cv2.resize(image_array_shown, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LANCZOS4)
        # image_array_shown = np.stack([image_array_shown] * 3, axis=2)

        vbox = QVBoxLayout(self)

        self.imglbl = QLabel()
        vbox.addWidget(self.imglbl)

        self.imglbl.setScaledContents(True)
        self.imglbl.setPixmap(QPixmap.fromImage(ndarray_to_qimage(image_array_shown)))
        w, h = self.imglbl.pixmap().size().toTuple()
        self.imglbl.resize(w, h)
    
    def get_next_widget(self):
        return PdfViewWidget(self.parent(), self)
