import shutil
from typing import TYPE_CHECKING

import numpy as np
import cv2

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPaintEvent, QPen, QPixmap, QPainter, Qt, QIntValidator
from PySide6.QtWidgets import *
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

from core import get_pdf

from utils.qimage_numpy import ndarray_to_qimage

from imagedialog.widgets.imagedialogwidgetbase import ImageDialogWidgetBase

if TYPE_CHECKING:
    from imagepopup import ImagePopup
    from imagedialog.widgets import OcrWidget

class PdfViewWidget(ImageDialogWidgetBase):
    def parent(self) -> 'ImagePopup':
        return super().parent()

    def __init__(self, parent: 'ImagePopup', brother: 'OcrWidget') -> None:
        super().__init__(parent)
        self.temp_filename = get_pdf(brother.results, brother.each_fonts)
        self.pdf = QPdfDocument()
        self.pdf.load(self.temp_filename)

        vbox = QVBoxLayout(self)

        self.pdfview = QPdfView()
        vbox.addWidget(self.pdfview)
        self.pdfview.setDocument(self.pdf)
    
    def get_next_widget(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save As", "..", "PDF Files (*.pdf);;All Files (*.*)")
        if filename:
            try:
                self.pdfview.close()
                del self.pdfview
                self.pdf.close()
                del self.pdf
                shutil.move(self.temp_filename, filename)
                return True
            except Exception:
                return False
        return False
