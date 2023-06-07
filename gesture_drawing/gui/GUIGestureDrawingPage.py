
import random
import sys
import PySide6.QtCore
import PySide6.QtGui
import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from ..core import CoreLogging as logging
from ..core import CoreData as CD


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



class GestureDrawingPage(QW.QWidget):
    def __init__(self):
        super().__init__()

        self.images:list[str] = []
        self.image_index = -1
        self.session_duration: int = -1
        self.timer_interval = 1000  # 1 second
        self.show_hover_panel_lower_than_percentage = 0.8
        self.current_image_time = 0

        self.viewer = ImageViewer(self)
        self.viewer.setVerticalScrollBarPolicy(QC.Qt.ScrollBarAlwaysOff)
        self.viewer.setHorizontalScrollBarPolicy(QC.Qt.ScrollBarAlwaysOff)
        # needed to prevent eating the mouse move event
        self.viewer.setAttribute(QC.Qt.WA_TransparentForMouseEvents)

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
        layout.addWidget(self.end_session_button)

        self.file_info_button = QW.QPushButton("File Info")
        layout.addWidget(self.file_info_button)

        self.delete_file_button = QW.QPushButton("Delete File")
        layout.addWidget(self.delete_file_button)

        self.grid_button = QW.QPushButton("Grid")
        layout.addWidget(self.grid_button)
        parent_layout.addLayout(layout)

        self.flip_image_button = QW.QPushButton("Flip Image")
        layout.addWidget(self.flip_image_button)

        self.greyscale_button = QW.QPushButton("Greyscale Mode")
        self.greyscale_button.clicked.connect(self.viewer.toggle_grey)
        layout.addWidget(self.greyscale_button)

        self.timer = QC.QTimer(self)
        self.timer.timeout.connect(self._timer_tick)
        self.timer.setInterval(self.timer_interval)

        self.setMouseTracking(True)

        self.resizeEvent(None)
        self._timer_tick()

    def _set_image(self, path: str = None):

        pix_map = self.viewer.pixmap

        if not path:
            new_pixmap = QG.QPixmap()
        else:
            new_pixmap = QG.QPixmap(path)

        self.viewer.pixmap = new_pixmap

        del pix_map


    def _internal_finished(self):
        self.images = []
        self.images_iter = None 
        self.session_duration = -1
        self.timer.stop()
        self._set_image()

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
        
        self.viewer.resize(self.size())
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
            self.finished()
            return

        image = self.images[index]

        self.image_index = index

        logging.info("Showing next image %s", image)

        if not image:
            self._internal_finished()
            self.finished()
            return

        self.timer_label.setText(str(self.session_duration))
        self.timer_label.adjustSize()

        self.current_image_time = 0

        self._set_image(image)

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
        """
        Called when the session is finished,
        
        Should be set by the parent who wants to do something when this happens
        """
        pass 