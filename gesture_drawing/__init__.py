
import os
import sys
import sys
from dotenv import load_dotenv

import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from .gui import GUIClient
from .gui import GUICommon
from .core import CoreLogging as logging
from .core import CoreController
from .core import CoreConstants as CC


def main():
    logging.setup_logging(CC.LOG_FILE)
    logging.add_unhandled_exception_hook()

    controller = CoreController.ClientController()

    controller.boot_everything()

    try:
        GUICommon.enable_hi_dpi()

        app = QW.QApplication([])
        app.setApplicationName("Gesture Drawing")
        app.setPalette( GUICommon.get_darkModePalette(app))
        

        mainwindow = GUIClient.ClientWindow(controller)

        mainwindow.show()

        app.exec()

    finally:
        controller.shutdown_everything()
