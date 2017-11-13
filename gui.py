# -*- coding: utf-8 -*-

import numpy as np
import time
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui, uic

import conf

ui_mainwindow, _ = uic.loadUiType(conf.ui_filename)

class MainWindow(QtWidgets.QMainWindow, ui_mainwindow):

    player_1_url = ""
    player_1_api = ""
    player_2_url = ""
    player_2_api = ""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # setup layout
        self.setupUi(self)
        self.connect_activity()
      
        # 1: black, 0: empty, -1: white
        self.state = np.zeros((17, 17))
        # black stone goes first
        self.color = 'black'

    def connect_activity(self):
        self.player_1_name_lineEdit.textEdited.connect(self.update_player_1_name)
        self.player_1_url_textEdit.textChanged.connect(self.update_player_1_url)
        self.player_1_api_textEdit.textChanged.connect(self.update_player_1_api)

        self.player_2_name_lineEdit.textEdited.connect(self.update_player_2_name)
        self.player_2_url_textEdit.textChanged.connect(self.update_player_2_url)
        self.player_2_api_textEdit.textChanged.connect(self.update_player_2_api)

        self.grid.canvas.mpl_connect('button_press_event', self.button_press_callback)

        self.reset_button.clicked.connect(self.reset)
        self.start_button.clicked.connect(self.start)
        self.clear_button.clicked.connect(self.clear)
    
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

    def update_player_2_name(self, name):
        self.player_2_name_label_2.setText(name)
        self.player_2_button.setText(name)

    def reset(self): 
        self.clear()

    def clear(self):
        self.state = np.zeros((17, 17))
        # clear stone patches 
        self.grid.ax.patches.clear()
        if self.player_2_button.isChecked() == True:
            self.change_turns()
        self.grid.draw()

    def start(self):
        return

    def button_press_callback(self, event):
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
        stone = plt.Circle((xidx, yidx), radius=0.4, fc=self.color,
                           zorder=10)
        self.grid.ax.add_patch(stone)
        self.grid.draw()

        # determine winning condition here
        #TODO: do corresponding action ex. show popup message 

        self.change_turns()

    def change_turns(self):
        if self.player_1_button.isChecked() == True:
            # white goes next
            self.color = 'white'
            self.player_1_button.setChecked(False)
            self.player_2_button.setChecked(True)
            self.player_stone_image.setPixmap(QtGui.QPixmap(conf.white_stone_image_path))

        else:
            # black goes next
            self.color = 'black'
            self.player_1_button.setChecked(True)
            self.player_2_button.setChecked(False)
            self.player_stone_image.setPixmap(QtGui.QPixmap(conf.black_stone_image_path))
