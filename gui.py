# -*- coding: utf-8 -*-

import numpy as np
import time
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from time import strftime
import datetime

import conf
import timer

ui_mainwindow, _ = uic.loadUiType(conf.ui_filename)

class MainWindow(QtWidgets.QMainWindow, ui_mainwindow):
    player_1_url = ''
    player_1_api = ''
    player_2_url = ''
    player_2_api = ''

    player_1_score = 0
    player_2_score = 0
    player_1_name = 'Player 1'
    player_2_name = 'Player 2'

    active = False
    timeout_duration = 15

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # setup layout
        self.setupUi(self)

        self.connect_activity()
      
        # 1: black, 0: empty, -1: white
        size = self.grid.get_size()
        self.state = np.zeros((size, size))
        # black stone goes first
        self.color = 'black'

    def connect_activity(self):
        self.player_1_name_lineEdit.textEdited.connect(self.update_player_1_name)
        self.player_1_url_textEdit.textChanged.connect(self.update_player_1_url)
        self.player_1_api_textEdit.textChanged.connect(self.update_player_1_api)

        self.player_2_name_lineEdit.textEdited.connect(self.update_player_2_name)
        self.player_2_url_textEdit.textChanged.connect(self.update_player_2_url)
        self.player_2_api_textEdit.textChanged.connect(self.update_player_2_api)

        self.tabWidget.currentChanged.connect(self.change_tab)

        self.grid.canvas.mpl_connect('button_press_event', self.button_press_callback)

        self.reset_button.clicked.connect(self.reset)
        self.start_button.clicked.connect(self.start)
        self.clear_button.clicked.connect(self.clear)
        
        self.minute_spin_box.valueChanged.connect(self.update_time_duration)
        self.seconds_spin_box.valueChanged.connect(self.update_time_duration)

        self.size_spin_box.valueChanged.connect(self.update_board_size)

        self.counter.timeover.connect(self.handle_timeover)

    def change_tab(self, id):
        if self.counter.is_set():
            # game is in play
            if id == 0:
                # displaying game screen
                self.counter.resume_timer()
            elif id == 1:
                # displaying options
                self.counter.pause_timer()

    def update_board_size(self, size):
        self.grid.set_size(size)
        
    def update_player_1_url(self):
        self.player_1_url = self.player_1_url_textEdit.toPlainText()

    def update_player_1_api(self):
        self.player_1_api = self.player_1_api_textEdit.toPlainText()

    def update_player_2_url(self):
        self.player_2_url = self.player_2_url_textEdit.toPlainText()

    def update_player_2_api(self):
        self.player_2_api = self.player_2_api_textEdit.toPlainText()

    def update_player_1_name(self, name):
        self.player_1_name_label_2.setText(name)
        self.player_1_button.setText(name)
        self.player_1_name = name

    def update_player_2_name(self, name):
        self.player_2_name_label_2.setText(name)
        self.player_2_button.setText(name)
        self.player_2_name = name

    def update_time_duration(self):
        self.timeout_duration = int(self.minute_spin_box.value()*60 + 
                                    self.seconds_spin_box.value())

    def handle_timeover(self):
        if self.player_1_button.isChecked() == True:
            self.player_2_score += 1
            QtWidgets.QMessageBox.about(self, 'Victory Message', self.player_2_name + ' wins')
            self.player_2_score_display.display(str(self.player_2_score))
        else:
            self.player_1_score += 1
            QtWidgets.QMessageBox.about(self, 'Victory Message', self.player_1_name + ' wins')
            self.player_1_score_display.display(str(self.player_1_score))
        self.active = False

    def reset(self): 
        self.clear()
        self.counter.stop_timer()
        self.active = False

        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_score_display.display(str(self.player_1_score))
        self.player_2_score_display.display(str(self.player_2_score))

    def clear(self):
        # reset timer
        self.counter.stop_timer()
        # reset board
        size = self.grid.get_size()
        self.state = np.zeros((size, size))
        # clear stone patches 
        self.grid.clear_board()
        
        if self.player_2_button.isChecked() == True:
            self.to_player_1()
        self.active = False

    def start(self):
        if self.active:
            return

        self.clear()
        self.active = True
        self.counter.start_timer(self.timeout_duration)

    def button_press_callback(self, event):
        if not self.active:
            return
        if not event.inaxes:
            return
        
        # place POST methods here
        # get x, y index recommendation
        # currently places stone on user input
        xidx = int(event.xdata + 0.5)
        yidx = int(event.ydata + 0.5)

        # check for duplicate placement
        if self.state[xidx, yidx] != 0:
            return
        else:
            self.state[xidx, yidx] = 1 if self.color == 'black' else -1

        # draw stone
        self.grid.place_stone_at((xidx, yidx), self.color)

        # determine winning condition here
        #TODO: do corresponding action ex. show popup message 

        self.change_turns()

    def change_turns(self):
        if self.player_1_button.isChecked() == True:
            # white goes next
            self.to_player_2()
        else:
            # black goes next
            self.to_player_1()

        # reset timer
        self.counter.start_timer(self.timeout_duration)

    def to_player_1(self):
        self.color = 'black'
        self.player_1_button.setChecked(True)
        self.player_2_button.setChecked(False)
        self.player_stone_image.setPixmap(QtGui.QPixmap(conf.black_stone_image_path))

    def to_player_2(self):
        self.color = 'white'
        self.player_1_button.setChecked(False)
        self.player_2_button.setChecked(True)
        self.player_stone_image.setPixmap(QtGui.QPixmap(conf.white_stone_image_path))

