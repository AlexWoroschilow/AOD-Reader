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


class ContentItemWidget(QtWidgets.QListWidgetItem):
    def __init__(self, title=None, page=None):
        super(ContentItemWidget, self).__init__(title)

        self.setIcon(QtGui.QIcon("icons/folder-light"))
        self.href = page


class ContentWidget(QtWidgets.QListWidget):
    page = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(ContentWidget, self).__init__(parent)
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

        if self.model() is None or not self.model():
            self.setModel(QtGui.QStandardItemModel())

        for element in book.get_content_table():
            title, href, order = element
            self.addItem(ContentItemWidget(title, href))

    def clean(self):
        if self.model() is not None:
            self.model().clear()

    def pageOpen(self, page=None):
        model = self.model()
        if model is None: return None

        self.clearSelection()

        for x in range(0, model.rowCount()):

            index = model.index(x)
            if index is None: continue

            widget = self.itemFromIndex(index)
            if widget is None: continue

            if widget.href != page:
                continue

            flag = QtCore.QItemSelectionModel.Select
            self.selectionModel().setCurrentIndex(index, flag)

    def close(self):
        super(ContentWidget, self).deleteLater()
        return super(ContentWidget, self).close()


class ContentTableWidget(ContentWidget):
    pass


class ContentPagesWidget(ContentWidget):

    def bookEvent(self, book=None):
        if self.model() is None or not self.model():
            self.setModel(QtGui.QStandardItemModel())

        for index, href in enumerate(book.get_pages(), start=1):
            title = 'Page: {}'.format(index)
            self.addItem(ContentItemWidget(title, href))
