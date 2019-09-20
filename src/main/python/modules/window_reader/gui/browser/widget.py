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
import functools
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .bar import BrowserToolbarWidget


class BrowserWidget(QtWidgets.QFrame):
    settings = QtCore.pyqtSignal(object)
    translate = QtCore.pyqtSignal(object)
    back = QtCore.pyqtSignal(object)
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)
    export = QtCore.pyqtSignal(object)
    zoom = QtCore.pyqtSignal(object)

    @inject.params(browser='window.browser', translator='window.translator')
    def __init__(self, parent, browser=None, translator=None):
        super(BrowserWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.toolbar = BrowserToolbarWidget(self)
        self.toolbar.back.connect(self.back.emit)
        self.toolbar.export.connect(self.export.emit)
        self.toolbar.zoom.connect(self.zoom.emit)

        self.layout().addWidget(self.toolbar)

        self.browser = browser
        self.browser.setMinimumWidth(300)
        self.browser.translate.connect(translator.translate.emit)
        self.browser.translate.connect(self.translate.emit)
        self.translator = translator

        splitter = QtWidgets.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        splitter.addWidget(self.browser)
        splitter.addWidget(self.translator)

        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 2)

        self.layout().addWidget(splitter)

        self.zoom.connect(self.browser.zoom.emit)
        self.page.connect(self.browser.bookPage.emit)
        self.book.connect(self.browser.book.emit)
        self.book.connect(self.toolbar.book.emit)
