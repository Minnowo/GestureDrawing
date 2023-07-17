import json
import os
import qtpy
import logging


from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from ...core import CoreConstants as CC
from ...core import CoreController
from ...core import CoreHydrusAPI
from ...core import CoreData

from ..GUICommon import InfiniteProgressBar



class HydrusSearchDialog(QW.QDialog):
    def __init__(self, controller:CoreController.ClientController=None, parent=None):
        super().__init__(parent)

        self._controller:CoreController.ClientController = controller 
        self.is_searching = False

        self._controller.update_hydrus()

        self.hy_client =  CoreHydrusAPI.get_client()

        all_services = self.hy_client.get_services()

        file_service = [
            "local_files",
            "all_local_files",
            "all_local_media",
            "all_known_files",
            "trash",
        ]

        tag_service = [
            "all_known_tags",
            "local_tags",
        ]


        layout = QW.QVBoxLayout()
        self.setLayout(layout)


        self.lineEdit__search_box = QW.QLineEdit()
        self.lineEdit__search_box.setToolTip("Enter tags to search")

        self.button__search_button= QW.QPushButton("Search")
        self.button__search_button.setToolTip("Search for files")

        self.combobox__file_service = QW.QComboBox()
        _ = 0
        for i in file_service:

            for s in all_services[i]:

                self.combobox__file_service.addItem(s['name'], userData=s['service_key'])

                if s['name'].lower() == 'my files':
                    self.combobox__file_service.setCurrentIndex(_)

                _ += 1


        self.combobox__tag_service = QW.QComboBox()
        for i in tag_service:

            for s in all_services[i]:

                self.combobox__tag_service.addItem(s['name'], userData=s['service_key'])

        self.listview__tags_display_box = QW.QListView()
        self.listview__tags_display_box.setSizePolicy(
            QW.QSizePolicy.Expanding,
            QW.QSizePolicy.Expanding,
        )
        self.model = QC.QStringListModel()
        self.listview__tags_display_box.setModel(self.model)
        self.proxy_model = QC.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.listview__tags_display_box.setModel(self.proxy_model)

        self.infiniteProgressBar__search_progress = InfiniteProgressBar()
        self.infiniteProgressBar__search_progress.setVisible(False)


        _layout = QW.QHBoxLayout()
        _layout.addWidget(self.lineEdit__search_box)
        _layout.addWidget(self.button__search_button)
        layout.addLayout(_layout)

        _layout = QW.QHBoxLayout()
        _layout.addWidget(self.combobox__file_service)
        _layout.addWidget(self.combobox__tag_service)
        layout.addLayout(_layout)
        layout.addWidget(self.infiniteProgressBar__search_progress)
        layout.addWidget(self.listview__tags_display_box)


        self.button_box = QW.QDialogButtonBox(
            QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Cancel, self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)


        self.search_timeout_timer = QC.QTimer(self)
        self.search_timeout_ms = 400

        self.search_timeout_timer.timeout.connect(self._search_hydrus_tags)
        self.combobox__file_service.currentIndexChanged.connect(self._file_service_changed)
        self.combobox__tag_service.currentIndexChanged.connect(self._tag_service_changed)
        self.button__search_button.clicked.connect(self.search_hydrus_tags)
        self.lineEdit__search_box.textChanged.connect(self._search_text_change)


    def _search_text_change(self):
        self.search_hydrus_tags()

    def _file_service_changed(self):
        self.search_hydrus_tags()

    def _tag_service_changed(self):
        self.search_hydrus_tags()

    def reject(self) -> None:
        return super().reject()

    def accept(self) -> None:
        return super().accept()


    def _search_hydrus_tags(self):


        if self.is_searching:

            return

        try:
            self.is_searching = True

            file_service_key = self.combobox__file_service.itemData(self.combobox__file_service.currentIndex())
            tag_service_key = self.combobox__tag_service.itemData(self.combobox__tag_service.currentIndex())

            text = self.lineEdit__search_box.text()

            search = self.hy_client.search_tags(text, 
                                    tag_service_key=tag_service_key,
                                    file_service_keys=[file_service_key])

            tags = search['tags']

            self.model.setStringList(
                [f"{tag['value']} ({tag['count']})" for tag in tags]
            )

        finally:
            self.infiniteProgressBar__search_progress.reset_progress()
            self.infiniteProgressBar__search_progress.stop_progress()
            self.infiniteProgressBar__search_progress.setVisible(False)
            self.search_timeout_timer.stop()
            self.is_searching = False

    
    def search_hydrus_tags(self):

        self.infiniteProgressBar__search_progress.setVisible(True)
        self.infiniteProgressBar__search_progress.start_progress()

        self.search_timeout_timer.stop()
        self.search_timeout_timer.start(self.search_timeout_ms)

