
import os
import sys
import sys
from dotenv import load_dotenv

import qtpy

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from .gui import GUIClient
from .core import CoreLogging as logging
from .core import CoreController
from .core import CoreConstants as CC

def get_darkModePalette( app=None ) :
    
    darkPalette = app.palette()
    darkPalette.setColor(QG.QPalette.Window, QG.QColor( 53, 53, 53 ) )
    darkPalette.setColor(QG.QPalette.WindowText,QC.Qt.white )
    darkPalette.setColor(QG.QPalette.Disabled, QG.QPalette.WindowText, QG.QColor( 127, 127, 127 ) )
    darkPalette.setColor(QG.QPalette.Base, QG.QColor( 42, 42, 42 ) )
    darkPalette.setColor(QG.QPalette.AlternateBase, QG.QColor( 66, 66, 66 ) )
    darkPalette.setColor(QG.QPalette.ToolTipBase, QC.Qt.white )
    darkPalette.setColor(QG.QPalette.ToolTipText, QC.Qt.white )
    darkPalette.setColor(QG.QPalette.Text, QC.Qt.white )
    darkPalette.setColor(QG.QPalette.Disabled, QG.QPalette.Text, QG.QColor( 127, 127, 127 ) )
    darkPalette.setColor(QG.QPalette.Dark, QG.QColor( 35, 35, 35 ) )
    darkPalette.setColor(QG.QPalette.Shadow, QG.QColor( 20, 20, 20 ) )
    darkPalette.setColor(QG.QPalette.Button, QG.QColor( 53, 53, 53 ) )
    darkPalette.setColor(QG.QPalette.ButtonText, QC.Qt.white )
    darkPalette.setColor(QG.QPalette.Disabled, QG.QPalette.ButtonText, QG.QColor( 127, 127, 127 ) )
    darkPalette.setColor(QG.QPalette.BrightText, QC.Qt.red )
    darkPalette.setColor(QG.QPalette.Link, QG.QColor( 42, 130, 218 ) )
    darkPalette.setColor(QG.QPalette.Highlight, QG.QColor( 42, 130, 218 ) )
    darkPalette.setColor(QG.QPalette.Disabled, QG.QPalette.Highlight, QG.QColor( 80, 80, 80 ) )
    darkPalette.setColor(QG.QPalette.HighlightedText, QC.Qt.white )
    darkPalette.setColor(QG.QPalette.Disabled, QG.QPalette.HighlightedText, QG.QColor( 127, 127, 127 ), )
    
    return darkPalette

def main():
    logging.setup_logging(CC.LOG_FILE)
    logging.add_unhandled_exception_hook()

    controller = CoreController.ClientController()

    controller.boot_everything()

    try:
        app = QW.QApplication([])
        app.setApplicationName("Gesture Drawing")
        app.setPalette( get_darkModePalette(app))
        

        mainwindow = GUIClient.ClientWindow(controller)

        mainwindow.show()

        app.exec()

    finally:
        controller.shutdown_everything()
