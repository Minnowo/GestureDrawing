

from typing import Optional
import PySide6.QtCore
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG


class GraphicsEffectMixer(QW.QGraphicsEffect):

    def __init__(self, parent:QC.QObject | None = None) -> None:
        super().__init__(parent)

        self.effects:list[QW.QGraphicsEffect] = []

    def add_graphics_effect(self, effet:QW.QGraphicsEffect):

        self.effects.append(effet)

    def draw(self, painter):

        for effect in self.effects:

            if effect.isEnabled():

                effect.draw(painter)



class InvertColorsEffect(QW.QGraphicsEffect):

    def draw(self, painter):

        source_pixmap : QG.QPixmap
        location :QC.QPoint
        source_pixmap, location = self.sourcePixmap(mode=QW.QGraphicsEffect.PadToEffectiveBoundingRect)

        if not source_pixmap.isNull():

            painter.drawPixmap(location, source_pixmap)
            painter.setCompositionMode(QG.QPainter.CompositionMode.CompositionMode_Difference)
            painter.fillRect(self.boundingRect(), QC.Qt.white)


class TransformEffect(QW.QGraphicsEffect):

    def __init__(self, transform:QG.QTransform=None, parent: QC.QObject | None = ...) -> None:
        super().__init__(parent)
        self.transform = transform

        if not self.transform:
            self.transform = QG.QTransform().scale(-1, 1)
    

    def draw(self, painter):

        source_pixmap : QG.QPixmap
        location :QC.QPoint
        source_pixmap, location = self.sourcePixmap(mode=QW.QGraphicsEffect.PadToEffectiveBoundingRect)

        if not source_pixmap.isNull():

            painter.drawPixmap(location,  source_pixmap.transformed(self.transform))
