import numpy as np
import os 
import re
from functools import partial
import logging


import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from ..core import CoreConstants as CC
from ..core import CoreData as CD

from . import dialogs 
from . import GUIMenuPage
from . import GUIGestureDrawingPage

class ClientWindow(QW.QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller

        self.setWindowTitle("Gesture Drawing!")

        self.stacked_widget = QW.QStackedWidget()

        self.menu_panel = GUIMenuPage.MenuPage(controller)
        self.menu_panel.start_button.clicked.connect(self.start)
        self.stacked_widget.addWidget(self.menu_panel)

        self.drawing_panel = GUIGestureDrawingPage.GestureDrawingPage(controller)
        self.drawing_panel.sessionFinishedEvent.connect(self._finished_session)
        self.stacked_widget.addWidget(self.drawing_panel)

        settings_action = self.menuBar().addAction("Settings")
        settings_action.triggered.connect(self.show_settings_dialog)

        # self.stacked_widget.add

        self.setCentralWidget(self.stacked_widget)


    def _finished_session(self):
        logging.info("Finished all images!")
        self.stacked_widget.setCurrentIndex(0)
        self.menuBar().setVisible(True)

    def start(self):

        folder = self.menu_panel.folder_path_box.text()
        draw_time = self.menu_panel.draw_time

        if not os.path.isdir(folder):
            logging.info("Folder %s does not exist!", folder)

        self.menuBar().setVisible(False)
        self.stacked_widget.setCurrentIndex(1)
        self.drawing_panel.start_session(CD.find_files(folder, name_matches=CC.NAME_IS_IMAGE_TYPE_REGEX), draw_time)


    def show_settings_dialog(self):

        dialogs.SettingsDialog(self._controller).exec_()

