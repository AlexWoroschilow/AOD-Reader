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
import inject
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .list import ContentPagesWidget
from .list import ContentTableWidget
from .browser.widget import BrowserWidget
from .tab import PageContentTable


# class WindowContent(QtWidgets.QTabWidget):
#
#     @inject.params(kernel='kernel', logger='logger')
#     def __init__(self, parent=None, kernel=None, logger=None):
#         super(WindowContent, self).__init__(parent)
#         self.setTabPosition(QtWidgets.QTabWidget.West)
#         self.setContentsMargins(0, 0, 0, 0)
#

class ReaderWidget(QtWidgets.QTabWidget):
    settings = QtCore.pyqtSignal(object)
    translate = QtCore.pyqtSignal(object)
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)
    back = QtCore.pyqtSignal(object)

    @inject.params(history='widget.history')
    def __init__(self, parent=None, history=None):
        super(ReaderWidget, self).__init__(parent)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.history = history

        self.ctable = ContentTableWidget(self)
        self.ctable.page.connect(self.page.emit)

        self.cpages = ContentPagesWidget(self)
        self.cpages.page.connect(self.page.emit)

        tab = PageContentTable()
        tab.addTab(self.cpages, 'Pages')
        tab.addTab(self.ctable, 'Content table')

        self.browser = BrowserWidget(self)
        self.browser.translate.connect(self.translate.emit)
        self.browser.back.connect(self.back.emit)

        splitter = QtWidgets.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        splitter.addWidget(tab)
        splitter.addWidget(self.browser)

        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 3)

        self.insertTab(0, splitter, 'Reader')
        self.insertTab(1, history, 'History')

        self.book.connect(self.browser.book.emit)
        self.page.connect(self.browser.page.emit)

        self.book.connect(self.history.book.emit)
        self.translate.connect(self.history.translate.emit)

        self.book.connect(self.ctable.book.emit)
        self.book.connect(self.cpages.book.emit)
