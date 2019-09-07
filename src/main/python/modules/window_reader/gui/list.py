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
import math
import inject

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class ContentTableWidget(QtWidgets.QListWidget):
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(ContentTableWidget, self).__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(200)

        self.clicked.connect(self.pageEvent)
        self.book.connect(self.bookEvent)

    def pageEvent(self, index=None):
        for index in self.selectedIndexes():
            item = self.itemFromIndex(index)
            self.page.emit(item.href)

    def bookEvent(self, book=None):

        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        for element in book.get_content_table():
            title, href, order = element

            item = QtWidgets.QListWidgetItem(title)
            item.setIcon(QtGui.QIcon("icons/folder-light"))
            item.href = href
            self.addItem(item)

    def clean(self):
        if self.model() is not None:
            self.model().clear()

    def close(self):
        super(ContentTableWidget, self).deleteLater()
        return super(ContentTableWidget, self).close()


class ContentPagesWidget(QtWidgets.QListWidget):
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(ContentPagesWidget, self).__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(200)

        self.clicked.connect(self.pageEvent)
        self.book.connect(self.bookEvent)

    def pageEvent(self, index=None):
        for index in self.selectedIndexes():
            item = self.itemFromIndex(index)
            self.page.emit(item.href)

    def bookEvent(self, book=None):

        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        for index, page in enumerate(book.get_pages(), start=1):
            item = QtWidgets.QListWidgetItem('Page: {}'.format(index))
            item.setIcon(QtGui.QIcon("icons/folder-light"))
            item.href = page
            self.addItem(item)

    def clean(self):
        if self.model() is not None:
            self.model().clear()

    def close(self):
        super(ContentPagesWidget, self).deleteLater()
        return super(ContentPagesWidget, self).close()
