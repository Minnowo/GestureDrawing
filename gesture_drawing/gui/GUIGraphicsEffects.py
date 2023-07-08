

from typing import Optional

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG


class InvertColorsEffect(QW.QGraphicsEffect):

    def draw(self, painter):

        source_pixmap : QG.QPixmap
        location :QC.QPoint

        _ =  self.sourcePixmap(mode=QW.QGraphicsEffect.PadToEffectiveBoundingRect)

        # older version of qtpy returns tuple
        if isinstance(_, tuple):
            source_pixmap, location = _
        else:
            source_pixmap = _
            location = QC.QPoint()

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

        _ =  self.sourcePixmap(mode=QW.QGraphicsEffect.PadToEffectiveBoundingRect)

        # older version of qtpy returns tuple
        if isinstance(_, tuple):
            source_pixmap, location = _
        else:
            source_pixmap = _
            location = QC.QPoint()

        if not source_pixmap.isNull():

            painter.drawPixmap(location,  source_pixmap.transformed(self.transform))
