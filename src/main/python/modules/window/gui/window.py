# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .content import WindowContent


class MainWindow(QtWidgets.QMainWindow):
    settings = QtCore.pyqtSignal(object)
    reader = QtCore.pyqtSignal(object)
    translate = QtCore.pyqtSignal(object)
    collection = QtCore.pyqtSignal(object)
    exit = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('AOD-EBookReader')

        if os.path.exists('icons/reader.svg'):
            self.setWindowIcon(QtGui.QIcon("icons/reader"))

        if os.path.exists('css/stylesheet.qss'):
            with open('css/stylesheet.qss') as stream:
                self.setStyleSheet(stream.read())
