#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication 

import gui

def main():
    app = QApplication(sys.argv)
    window = gui.MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
