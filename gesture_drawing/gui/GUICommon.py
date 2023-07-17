import os
import qtpy
import logging


from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG



class InfiniteProgressBar(QW.QProgressBar):
    def __init__(self, step_amount=10,timer_speed_ms=100):
        super().__init__()

        self.timer_delay = timer_speed_ms
        self.step_amount = step_amount

        self.timer = QC.QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        self.progress_value = 0

    def update_progress(self):
        self.progress_value = (self.progress_value + self.step_amount) % 100
        self.setValue(self.progress_value)

    def stop_progress(self):
        self.timer.stop()

    def start_progress(self):
        self.timer.start(self.timer_delay)

    def reset_progress(self):
        self.progress_value = 0
        self.reset()

