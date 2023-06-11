import abc

from PySide6.QtWidgets import QWidget


class ImageDialogWidgetBase(QWidget):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_next_widget(self) -> 'ImageDialogWidgetBase | bool':
        pass
