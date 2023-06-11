import numpy as np

from PySide6.QtGui import QImage


def qimage_to_ndarray(image: QImage) -> np.ndarray:
    """Converts QImage to np.ndarray format."""
    assert image.format() == QImage.Format.Format_RGBA8888
    w, h = image.size().toTuple()
    array = np.frombuffer(image.bits(), dtype=np.uint8).reshape((h, w, 4))
    return np.delete(array, 3, axis=2)
    # return array

def ndarray_to_qimage(array: np.ndarray) -> QImage:
    h, w, *_ = array.shape
    image = QImage(array.data, w, h, w*3, QImage.Format.Format_RGB888)
    image.convertTo(QImage.Format.Format_RGBA8888)
    return image
