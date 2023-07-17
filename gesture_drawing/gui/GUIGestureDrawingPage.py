
import random
import sys
import qtpy
import logging

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from ..core import CoreData as CD

from . import GUIGraphicsEffects

class ImageViewer(QW.QGraphicsView):
    def __init__(self, parent=None, pixmap:QG.QPixmap=None):
        super().__init__(parent)
        self.setScene(QW.QGraphicsScene(self))

        if not pixmap:
            self.m_pixmapItem = self.scene().addPixmap(QG.QPixmap())
        else:
            self.m_pixmapItem = self.scene().addPixmap(pixmap)

        self.is_grey = False
        self.alternate_image = None


        self.setAlignment(QC.Qt.AlignCenter)

    @property
    def pixmap(self):
        return self.m_pixmapItem.pixmap()

    @pixmap.setter
    def pixmap(self, newPixmap):
        self.m_pixmapItem.setPixmap(newPixmap)
        self.fitInView(self.m_pixmapItem, QC.Qt.KeepAspectRatio)
        
        _ = self.alternate_image
        self.alternate_image = None 
        if _:
            del _

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.m_pixmapItem, QC.Qt.KeepAspectRatio)

    def toggle_grey(self):

        if self.is_grey:
            self.is_grey = False 

        else:
            self.is_grey = True

            if not self.alternate_image:
                self.alternate_image = QG.QPixmap.fromImage(self.m_pixmapItem.pixmap().toImage().convertToFormat(QG.QImage.Format_Grayscale8))

        _ = self.m_pixmapItem.pixmap()
        self.m_pixmapItem.setPixmap(self.alternate_image)
        self.alternate_image = _

    def toggle_mirror_horizontal(self):

        flip_trans =QG.QTransform().scale(-1, 1)

        if self.alternate_image:
            self.alternate_image = self.alternate_image.transformed(flip_trans)

        current_pixmap = self.m_pixmapItem.pixmap()
        mirrored_pixmap = current_pixmap.transformed(flip_trans)
        self.m_pixmapItem.setPixmap(mirrored_pixmap)
        self.fitInView(self.m_pixmapItem, QC.Qt.KeepAspectRatio)



class GestureDrawingPage(QW.QWidget):

    sessionFinishedEvent = QC.Signal(name="GestureDrawingSessionFinished")

    def __init__(self, controller):
        super().__init__()

        self._controller = controller

        self.images:list[str] = []
        self.image_index = -1
        self.session_duration: int = -1
        self.timer_interval = 1000  # 1 second
        self.show_hover_panel_lower_than_percentage = 0.8
        self.current_image_time = 0


        self.scene = QW.QGraphicsScene(self)
        self.graphicsview = QW.QGraphicsView(self.scene, self)
        self.graphicsview.setAlignment(QC.Qt.AlignCenter)
        self.graphicsview.setAttribute(QC.Qt.WA_TransparentForMouseEvents)
        self.graphicsview.setVerticalScrollBarPolicy(QC.Qt.ScrollBarAlwaysOff)
        self.graphicsview.setHorizontalScrollBarPolicy(QC.Qt.ScrollBarAlwaysOff)

        self.invert_graphics_effect:GUIGraphicsEffects.InvertColorsEffect = None

        self.lines = []


        self.pixmap = self.scene.addPixmap(QG.QPixmap())

        self.timer_label = QW.QLabel(self)
        self.timer_label.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignTop)
        self.timer_label.setStyleSheet("background-color: rgba(0, 0, 0, 100); color: white; padding: 5px;")

        # Bottom hover panel
        self.bottom_hover_panel = QW.QWidget(self)
        self.bottom_hover_panel.setObjectName("parentWidget")
        self.bottom_hover_panel.setStyleSheet("#parentWidget { background-color: black; }")
        self.bottom_hover_panel.setVisible(False)

        parent_layout = QW.QVBoxLayout(self.bottom_hover_panel)
        # previous, pause, next button
        layout = QW.QHBoxLayout()
        self.previous_image_button = QW.QPushButton("<-")
        self.previous_image_button.clicked.connect(self.prev_image)
        layout.addWidget(self.previous_image_button)

        self.pause_button = QW.QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        layout.addWidget(self.pause_button)

        self.next_image_button = QW.QPushButton("->")
        self.next_image_button.clicked.connect(self.next_image)
        layout.addWidget(self.next_image_button)
        parent_layout.addLayout(layout)

        # Other buttons
        layout = QW.QHBoxLayout()
        self.end_session_button = QW.QPushButton("End Session")
        self.end_session_button.clicked.connect(self._internal_finished)
        layout.addWidget(self.end_session_button)

        self.grid_button = QW.QPushButton("Grid")
        self.grid_button.setCheckable(True)
        self.grid_button.clicked.connect(self.show_grid)
        layout.addWidget(self.grid_button)
        parent_layout.addLayout(layout)

        self.flip_image_button = QW.QPushButton("Flip Image")
        self.flip_image_button.setCheckable(True)
        self.flip_image_button.clicked.connect(self.mirror)
        layout.addWidget(self.flip_image_button)

        self.greyscale_button = QW.QPushButton("Invert")
        self.greyscale_button.setCheckable(True)
        self.greyscale_button.clicked.connect(self.invert)
        layout.addWidget(self.greyscale_button)

        self.timer = QC.QTimer(self)
        self.timer.timeout.connect(self._timer_tick)
        self.timer.setInterval(self.timer_interval)

        self.setMouseTracking(True)

        self.resizeEvent(None)
        self._timer_tick()

    def _set_image(self, path: str = None):

        pix_map = self.pixmap.pixmap()

        if not path:
            new_pixmap = QG.QPixmap()
        else:
            new_pixmap = QG.QPixmap(path)


        self.pixmap.setPixmap(new_pixmap)

        # important! otherwise some images won't show up properly
        self.scene.setSceneRect(0, 0, new_pixmap.width(), new_pixmap.height())

        self.graphicsview.fitInView(self.pixmap, QC.Qt.KeepAspectRatio)

        del pix_map


    def _internal_finished(self):
        self.images = []
        self.images_iter = None 
        self.session_duration = -1
        self.timer.stop()
        self._set_image()
        self.finished()

    def _timer_tick(self):

        self.current_image_time += 1

        time_on_image = self.session_duration - self.current_image_time 

        self.timer_label.setText(str(time_on_image))
        self.timer_label.adjustSize()

        if time_on_image <= 0:
            self.next_image()

    def resizeEvent(self, event:QG.QResizeEvent):

        self.bottom_hover_panel.adjustSize()
        self.bottom_hover_panel.resize(self.width(), self.bottom_hover_panel.height())
        
        self.graphicsview.setGeometry(0, 0, self.width(), self.height())
        self.graphicsview.fitInView(self.pixmap, QC.Qt.KeepAspectRatio)

        self.timer_label.adjustSize()

        timer_width = self.timer_label.width()
        timer_height = self.timer_label.height()

        self.timer_label.move(self.width() - timer_width - 10, 10)

        self.bottom_hover_panel.setVisible(False)


    def mouseMoveEvent(self, event: QG.QMouseEvent):

        y = event.y()


        if y > self.height() * self.show_hover_panel_lower_than_percentage:
            self.bottom_hover_panel.setVisible(True)
            self.bottom_hover_panel.move(0, self.height() - self.bottom_hover_panel.height())
        else:
            self.bottom_hover_panel.setVisible(False)


    def showEvent(self, event: QG.QShowEvent):
        self.timer.start()

    def hideEvent(self, event: QG.QHideEvent):
        self.timer.stop()

    def leaveEvent(self, event):
        self.bottom_hover_panel.setVisible(False)


    def start_session(self, images: list[str], time:int):

        random.shuffle(images)
        self.images = images 
        self.image_index = -1
        self.session_duration =  time

        self.next_image()

    def prev_image(self):

        _ = self.image_index - 1

        if _ < 0:
            _ = 0

        self.set_image(_)

    def next_image(self):

        self.set_image(self.image_index + 1)


    def set_image(self, index:int):

        if not (index >= 0 and index < len(self.images)):
            self._internal_finished()
            return

        image = self.images[index]

        self.image_index = index

        logging.info("Showing next image %s", image)

        if not image:
            self._internal_finished()
            return

        self.timer_label.setText(str(self.session_duration))
        self.timer_label.adjustSize()

        self.current_image_time = 0

        self._set_image(image)

        if self.grid_button.isChecked():
            self.update_grid()

        self.timer.stop()
        self.timer.start()



    def toggle_pause(self):

        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Resume")
        else:
            self.timer.start()
            self.pause_button.setText("Pause")


    def finished(self):

        self.sessionFinishedEvent.emit()


    def invert(self):

        if self.invert_graphics_effect is None :
            self.invert_graphics_effect = GUIGraphicsEffects.InvertColorsEffect(self.graphicsview)
            self.invert_graphics_effect.setEnabled(False)
            self.graphicsview.setGraphicsEffect(self.invert_graphics_effect)


        self.invert_graphics_effect.setEnabled(self.greyscale_button.isChecked())

        self.scene.invalidate()
        self.graphicsview.viewport().update()

    def mirror(self):

        self.pixmap.setPixmap(self.pixmap.pixmap().transformed(QG.QTransform().scale(-1, 1)))

    def update_grid(self):

        if not self.lines:
            self.show_grid()
            return
        
        for line in self.lines:
            self.scene.removeItem(line)

        self.lines = []
        self.show_grid()

    def show_grid(self):

        if not self.lines:
            w = self.pixmap.pixmap().width()
            w3 = w // 3
            h = self.pixmap.pixmap().height()
            h3 = h // 3

            for i in range(3):

                line = QW.QGraphicsLineItem(i*w3, 0, i*w3, h)
                self.lines.append(line)
                self.scene.addItem(line)

                line = QW.QGraphicsLineItem(0, i*h3, w, i*h3)
                self.lines.append(line)

                self.scene.addItem(line)
                
        for line in self.lines:
            line.setVisible(self.grid_button.isChecked())

        self.scene.invalidate()
        self.graphicsview.viewport().update()

