
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

        layout = QW.QVBoxLayout()
        self.setLayout(layout)


        self.button_box = QW.QDialogButtonBox(
            QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Cancel, self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)



    def reject(self) -> None:
        return super().reject()

    def accept(self) -> None:
        return super().accept()
