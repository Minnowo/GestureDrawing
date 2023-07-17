
import os
import qtpy
import logging


from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from ...core import CoreConstants as CC
from ...core import CoreController



class SettingsDialog(QW.QDialog):
    def __init__(self, controller:CoreController.ClientController=None, parent=None):
        super().__init__(parent)

        self._controller:CoreController.ClientController = controller 
        self._old_https_setting = self._controller.get_setting("hydrus", "verify_https")

        layout = QW.QVBoxLayout()
        self.setLayout(layout)

        tab_widget = QW.QTabWidget()
        layout.addWidget(tab_widget)



        hydrus_tab = QW.QWidget()
        settings_layout =QW. QVBoxLayout()
        hydrus_tab.setLayout(settings_layout)

        self.line_edit__hydrus_api_url = QW.QLineEdit()
        self.line_edit__hydrus_api_url.setPlaceholderText("127.0.0.1")
        self.line_edit__hydrus_api_url.setText(self._controller.get_setting("hydrus", "host"))
        self.spinbox__hydrus_api_port= QW.QSpinBox()
        self.spinbox__hydrus_api_port.setMinimum(0)
        self.spinbox__hydrus_api_port.setMaximum(9999999)
        self.spinbox__hydrus_api_port.setValue(self._controller.get_setting("hydrus", "port"))
        self.line_edit__hydrus_api_key = QW.QLineEdit()
        self.line_edit__hydrus_api_key.setPlaceholderText("API Key")
        self.line_edit__hydrus_api_key.setText(self._controller.get_setting("hydrus", "api_key"))
        self.button__request_api_key = QW.QPushButton("Request API Key")
        self.button__request_api_key.clicked.connect(self.request_api_key)
        self.label__api_persm_valid_display = QW.QLabel('')
        self.label__api_persm_valid_display.setVisible(False)
        self.button__verify_api_perms = QW.QPushButton("Verify API Key Permission")
        self.button__verify_api_perms.clicked.connect(self.verify_api_perms)
        self.checkbox__verify_https = QW.QCheckBox("Verify https")
        self.checkbox__verify_https.setChecked(self._old_https_setting) 
        self.checkbox__verify_https.stateChanged.connect(self.verify_https_changed)
        

        _layouthz1 = QW.QHBoxLayout()
        _layouthz1.addWidget(self.line_edit__hydrus_api_url)
        _layouthz1.addWidget(self.spinbox__hydrus_api_port)
        settings_layout.addLayout(_layouthz1)
        settings_layout.addWidget(self.line_edit__hydrus_api_key)
        settings_layout.addWidget(self.checkbox__verify_https)
        settings_layout.addStretch(1)
        settings_layout.addWidget(self.button__request_api_key)
        _layouthz1 = QW.QHBoxLayout()
        _layouthz1.addWidget(self.button__verify_api_perms)
        _layouthz1.addWidget(self.label__api_persm_valid_display)
        settings_layout.addLayout(_layouthz1)

        
        tab_widget.addTab(hydrus_tab, "Hydrus Settings")


        self.button_box = QW.QDialogButtonBox(
            QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Cancel, self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)


    def verify_https_changed(self):

        self._controller.set_setting(('hydrus', 'verify_https'), self.checkbox__verify_https.isChecked())

    def verify_api_perms(self):

        e = self._controller.verify_hydrus_api()

        if e:
            self.label__api_persm_valid_display.setText("API Key Is Vald")
        else:
            self.label__api_persm_valid_display.setText("API Key Is NOT Vald")

        self.label__api_persm_valid_display.setVisible(True)

    def request_api_key(self):

        api_key = self._controller.get_hydrus_api_key()

        if api_key is None:
            return

        self.line_edit__hydrus_api_key.setText(api_key)

    def save(self):

        ip = self.line_edit__hydrus_api_url.text().strip()
        if ip and ip != self._controller.get_setting("hydrus", "host"): 
            logging.info("Updating hydrus host path")
            self._controller.set_setting(("hydrus", "host",), ip)

        port = self.spinbox__hydrus_api_port.value()
        if port and port != self._controller.get_setting("hydrus", "port"):
            logging.info("Updating hydrus api port")
            self._controller.set_setting(("hydrus", "port"), port)

        api_key = self.line_edit__hydrus_api_key.text().strip()
        if api_key and api_key != self._controller.get_setting("hydrus", "api_key"):
            logging.info("Updating hydrus api key")
            self._controller.set_setting(("hydrus", "api_key"), api_key)

        return True 

    def reject(self) -> None:
        self._controller.set_setting(('hydrus', 'verify_https'), self._old_https_setting)
        return super().reject()

    def accept(self) -> None:

        if not self.save():
            return

        return super().accept()
