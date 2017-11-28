# -*- coding: utf-8 -*-

import numpy as np

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class Board(QtWidgets.QWidget):
    # stone radius
    radius = 0.4

    def __init__(self, size=(5.0, 4.0), dpi=80):
        QtWidgets.QWidget.__init__(self)
        self.fig = Figure(figsize=(11, 11), dpi=dpi)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(True)
        self.ax.get_yaxis().set_visible(True)
        
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        
        self.fig.tight_layout()
        self.setLayout(self.vbox)

        # draw 17*17 go board by default
        ticks = np.arange(17)
        self.ax.set_xticks(ticks)
        self.ax.set_yticks(ticks)
        self.ax.grid(True, color='black')
        # make it look wooden
        self.fig.set_facecolor('#DBB263')
        self.ax.set_facecolor('#DBB263')

    def resizeEvent(self, event): 
        new_size = QtCore.QSize(10, 10)
        new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
        self.resize(new_size)

    def update_size(self, size):
        ticks = np.arange(size)
        self.ax.set_xticks(ticks)
        self.ax.set_yticks(ticks)
        self.ax.set_xlim((0, size-1))
        self.ax.set_ylim((0, size-1))
        self.draw()

    def draw(self):
        self.canvas.draw()

    def place_stone_at(self, coord, color):
        xidx = coord[0]
        yidx = coord[1]
        
        stone = plt.Circle((xidx, yidx), radius=self.radius,
                                         fc=color, zorder=10)
        self.ax.add_patch(stone)
        self.draw()

    def clear_board(self):
        self.ax.patches.clear()
        self.draw()
