# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from time import strftime

class Timer(QtWidgets.QLCDNumber):
    # emitted when exceeded time limit
    timeover = QtCore.pyqtSignal()

    def __init__(self, parent=None, time_left_in_seconds=15):
        super(Timer, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        
        self._time_left_in_seconds = time_left_in_seconds

        # decrement counter after each interval
        self.cid = self.timer.timeout.connect(self.decrement_counter)

    @property
    def time_left_in_seconds(self):
        return self._time_left_in_seconds

    @time_left_in_seconds.setter
    def time_left_in_seconds(self, value):
        if value < 0:
            raise ValueError("Timer cannot be set to a negative value")
        self._time_left_in_seconds = value
    
    def start_timer(self, value):
        self.timer.start(value*100)
        self.time_left_in_seconds = value
        # set interval to 1 second
        self.timer.setInterval(1000)
        
        minute = self.time_left_in_seconds//60
        seconds = self.time_left_in_seconds - minute*60
        self.display("{:02d}:{:02d}".format(minute, seconds))

    def stop_timer(self):
        self.display("00:00")
        self.timer.stop()

    def pause_timer(self):
        self.timer.stop()

    def decrement_counter(self):
        self.time_left_in_seconds -= 1
        if self.time_left_in_seconds == -1:
            # emit timeout signal on timeout
            self.timeover.emit()
            self.stop_timer()
        else:
            minutes = self.time_left_in_seconds//60
            seconds = self.time_left_in_seconds - minutes*60
            self.display("{:02d}:{:02d}".format(minutes, seconds))
