# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from time import strftime

class Timer(QtWidgets.QLCDNumber):

    timeout_duration = 15
    time_left_in_seconds = 0

    # emitted when exceeded time limit
    timeover = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        #QtWidgets.QLCDNumber.__init__(self)
        super(Timer, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        # decrement counter after each interval
        self.cid = self.timer.timeout.connect(self.decrement_counter)

    def set_timeout_duration(self, timeout_duration):
        self.timeout_duration = timeout_duration
    
    def get_timeout_duration(self):
        return self.timeout_duration

    def set_time_left_in_seconds(self, time_left_in_seconds):
        self.time_left_in_seconds = time_left_in_seconds

    def get_time_left_in_seconds(self):
        return self.time_left_in_seconds

    def start_timer(self):
        self.timer.start(self.timeout_duration*100)
        # set interval to 1 second
        self.timer.setInterval(1000)

        self.time_left_in_seconds = self.timeout_duration
        
        minute = self.time_left_in_seconds//60
        seconds = self.time_left_in_seconds - minute*60
        self.display("{:02d}:{:02d}".format(minute, seconds))

    def stop_timer(self):
        self.timer.stop()
        self.display("00:00")

    def pause_timer(self):
        self.timer.stop()

    def decrement_counter(self):
        self.time_left_in_seconds -= 1
        if self.time_left_in_seconds == -1:
            # emit timeout signal on timeout
            self.timeover.emit()
            self.timer.stop()
        else:
            minutes = self.time_left_in_seconds // 60
            seconds = self.time_left_in_seconds - minutes*60
            self.display("{:02d}:{:02d}".format(minutes, seconds))

