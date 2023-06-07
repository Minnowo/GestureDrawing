
import os
import sys
import qbittorrentapi
import sys
from dotenv import load_dotenv

import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from .gui import GUIClient
from .core import CoreLogging as logging


from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt



def main():
    load_dotenv()
    logging.setup_logger()

    try:
        app = QW.QApplication([])
        mainwindow = GUIClient.ClientWidnow(None)

        mainwindow.show()

        app.exec()

    finally:
        pass
        # CG.client_instance.auth_log_out()
