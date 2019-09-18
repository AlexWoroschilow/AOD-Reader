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
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .list import ContentPagesWidget
from .list import ContentTableWidget
from .browser.widget import BrowserWidget
from .tab import PageContentTable


class ReaderWidget(QtWidgets.QTabWidget):
    settings = QtCore.pyqtSignal(object)
    translate = QtCore.pyqtSignal(object)
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)
    export = QtCore.pyqtSignal(object)
    back = QtCore.pyqtSignal(object)

    ebook = None

    @inject.params(history='widget.history')
    def __init__(self, parent=None, history=None):
        super(ReaderWidget, self).__init__(parent)

        self.setTabPosition(QtWidgets.QTabWidget.South)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        ctable = ContentTableWidget(self)
        ctable.page.connect(self.page.emit)

        cpages = ContentPagesWidget(self)
        cpages.page.connect(self.page.emit)
        # If the page was selected in the content table list
        # we need to mark the similar page in the content pages list
        ctable.page.connect(cpages.pageOpen)
        # If the page was selected in the content pages list
        # we need to mark the similar page in the content table list
        cpages.page.connect(ctable.pageOpen)
        # There may be some history with the book
        # we have to open the page user stopped to read at
        # in the "content table" tab and in the "content pages" tab
        self.page.connect(ctable.pageOpen)
        self.page.connect(cpages.pageOpen)

        tab_bar = PageContentTable()
        tab_bar.addTab(cpages, 'Pages')
        tab_bar.addTab(ctable, 'Content table')

        browser = BrowserWidget(self)
        browser.export.connect(lambda x: self.export.emit(self.ebook))
        browser.translate.connect(self.translate.emit)
        browser.back.connect(self.back.emit)

        splitter = QtWidgets.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        splitter.addWidget(tab_bar)
        splitter.addWidget(browser)

        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 3)

        self.addTab(splitter, 'Reader')
        self.addTab(history, 'History')

        self.book.connect(browser.book.emit)
        self.page.connect(browser.page.emit)
        self.book.connect(history.book.emit)
        self.translate.connect(history.translate.emit)

        self.book.connect(ctable.book.emit)
        self.book.connect(cpages.book.emit)

    @inject.params(config='config')
    def open(self, ebook=None, config=None):
        if ebook is None: return None
        if config is None: return None

        self.ebook = ebook

        self.book.emit(ebook)

        unique = ebook.get_unique()
        if unique is None: return None

        page = config.get('{}.page'.format(unique), '')
        if page is None or not len(page): return None

        self.page.emit(page)
