import math

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPaintEvent, QPen, QPixmap, QPainter, Qt, QIntValidator
from PySide6.QtWidgets import *


PEN_RADIUS = 3
MOUSE_RADIUS = 5
POINT_INIT = 10

def qnorm(p1: QPoint, p2: QPoint):
    return math.sqrt((p1.x() - p2.x())**2 + (p1.y() - p2.y())**2)


class ImageLabel(QLabel):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setMouseTracking(True)
        self.quadrangle: list[MyPoint] = []
        self.scale = 1.0

    def setImage(self, image: QImage):
        self.setPixmap(QPixmap.fromImage(image))
        img_size = self.pixmap().size()
        self.resize(img_size)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        super().mouseMoveEvent(ev)
        x = int(ev.position().x())
        y = int(ev.position().y())

        if ev.buttons() & Qt.MouseButton.LeftButton == Qt.MouseButton.NoButton:  # not holding left button
            mp = QPoint(x, y)
            for point in self.quadrangle:
                point.state = ''
            
            nearest_point = sorted(self.quadrangle, key=lambda point: qnorm(mp, point))[0]
            if qnorm(mp, nearest_point) < MOUSE_RADIUS:
                nearest_point.state = 'near'
            self.repaint()

        else:  # holding left button
            for point in self.quadrangle:
                if point.state == 'hold':
                    point.setX(x)
                    point.setY(y)
                    self.repaint()
                    break

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super().mousePressEvent(ev)
        if ev.button() == Qt.MouseButton.LeftButton:
            x = int(ev.position().x())
            y = int(ev.position().y())
            mp = QPoint(x, y)

            nearest_point = sorted(self.quadrangle, key=lambda point: qnorm(mp, point))[0]
            if qnorm(mp, nearest_point) < MOUSE_RADIUS:
                nearest_point.state = 'hold'
                # print(nearest_point.toTuple())
                self.repaint()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        super().mouseReleaseEvent(ev)
        if ev.button() == Qt.MouseButton.LeftButton:
            x = int(ev.position().x())
            y = int(ev.position().y())
            mp = QPoint(x, y)
            for point in self.quadrangle:
                point.state = ''
            
            nearest_point = sorted(self.quadrangle, key=lambda point: qnorm(mp, point))[0]
            if qnorm(mp, nearest_point) < MOUSE_RADIUS:
                nearest_point.state = 'near'
            self.repaint()

    def paintEvent(self, ev: QPaintEvent) -> None:
        super().paintEvent(ev)
        if self.quadrangle:
            painter = QPainter(self)
            for point in self.quadrangle:
                if point.state == 'hold':
                    painter.setPen(QPen(QColor("#C000FFFF"), 2 * PEN_RADIUS, c=Qt.PenCapStyle.RoundCap))
                elif point.state == 'near':
                    painter.setPen(QPen(QColor("#C0FFFF00"), 2 * MOUSE_RADIUS, c=Qt.PenCapStyle.RoundCap))
                else:
                    painter.setPen(QPen(QColor("#C0FF0000"), 2 * PEN_RADIUS, c=Qt.PenCapStyle.RoundCap))
                painter.drawPoint(point)

            painter.setPen(QPen(Qt.GlobalColor.red, 1))
            for i in range(len(self.quadrangle) - 1):
                painter.drawLine(self.quadrangle[i], self.quadrangle[i+1])
            painter.drawLine(self.quadrangle[-1], self.quadrangle[0])
            painter.end()

    def change_scale(self, scale: float):
        pass


class MyPoint(QPoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = ''  # '', 'near', 'hold'
        self.real_x: int = 0
        self.real_y: int = 0
