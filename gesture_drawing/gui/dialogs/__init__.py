
import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from .SettingsDialog import SettingsDialog
from .HydrusSearchDialog import HydrusSearchDialog



def show_file_dialog(parent=None):
        file_dialog = QW.QFileDialog(parent)
        file_dialog.setFileMode(QW.QFileDialog.ExistingFiles)

        if file_dialog.exec_() == QW.QFileDialog.Accepted:

            return file_dialog.selectedFiles()

        return []

def show_folder_dialog(parent=None):
        file_dialog = QW.QFileDialog(parent)
        file_dialog.setFileMode(QW.QFileDialog.Directory)
        file_dialog.setOption(QW.QFileDialog.ShowDirsOnly, True)

        if file_dialog.exec_() == QW.QFileDialog.Accepted:

            return file_dialog.selectedFiles()[0]

        return None
