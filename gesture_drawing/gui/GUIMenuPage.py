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
from ..core import CoreHydrusAPI

from . import dialogs

class MenuPage(QW.QWidget):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller

        self.draw_time = 30
        self.selected_folder_path = ""


        self.folder_path_box = QW.QLineEdit()
        self.folder_path_box.setPlaceholderText("/path/to/image/folder")
        self.folder_path_box.setText("/home/minno/Pictures/gallery-dl")

        self.browse_button = QW.QPushButton("Browse For Folder")
        self.browse_button.clicked.connect(self._ask_choose_folder)

        self.browse_hydrus = QW.QPushButton("Browse Hydrus")
        self.browse_hydrus.clicked.connect(self._browse_hydrus)
        self.browse_hydrus.setEnabled(CoreHydrusAPI.HYDRUS_API_OK)

        self.folder_summary_label = QW.QLabel("Found 116 images in 20 subfolders")

        self.set_time_buttons :list[QW.QPushButton]= []
        self.default_time_buttons :list[tuple[int, str]]= [(30, "30s"),
                                     (45, "45s"),
                                     (60, "1m"),
                                     (120, "2m"),
                                     (360, "5m"),
                                     (720, "10m")]

        for (time, label) in self.default_time_buttons:

            btn = QW.QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(partial(self._set_time_button_clicked, btn, time))

            self.set_time_buttons.append(btn)

        
        self.start_button = QW.QPushButton("Start")


        layout = QW.QVBoxLayout(self)
        layout_2 = QW.QHBoxLayout()
        layout_2.addWidget(self.folder_path_box)
        layout_2.addWidget(self.browse_button)
        layout.addLayout(layout_2)

        layout.addWidget(self.folder_summary_label)
        layout.addWidget(self.browse_hydrus)
        layout.addStretch(1)

        layout_3 = QW.QHBoxLayout()
        for b in self.set_time_buttons:
            layout_3.addWidget(b)
        layout.addLayout(layout_3)

        layout.addWidget(self.start_button)


    def _browse_hydrus(self):

        dialogs.HydrusSearchDialog(self._controller, self).exec_()

    def _ask_choose_folder(self):

        folder_path = dialogs.show_folder_dialog()

        if not folder_path:
            return

        if os.path.isdir(folder_path):
            self.selected_folder_path = folder_path
            self.folder_path_box.setText(folder_path)

            file_count, folder_count = CD.count_files_and_folders(folder_path)

            self.folder_summary_label.setText("Found {} images in {} subfolders".format(file_count, folder_count))


    def _set_time_button_clicked(self, button: QW.QPushButton, time: int):

        for btn in self.set_time_buttons:
            if btn == button: continue

            btn.setChecked(False)

        self.set_draw_time_seconds(time)

    def set_draw_time_seconds(self, draw_time):
        self.draw_time = draw_time
        logging.info("Draw time set to %d seconds", self.draw_time)
