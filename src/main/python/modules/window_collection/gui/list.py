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
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class BookThread(QtCore.QThread):
    cover = QtCore.pyqtSignal(object)

    def __init__(self, book=None):
        super(BookThread, self).__init__()
        self.book = book

    def run(self):
        cover = self.book.get_cover_image_content()
        if cover is not None and cover:
            self.cover.emit(cover)

    def __del__(self):
        self.wait()


class BookItem(QtWidgets.QListWidgetItem):

    def __init__(self, book=None):
        super(BookItem, self).__init__()
        self.book = book

        self.thread = BookThread(book)
        self.thread.cover.connect(self.setCoverimage)

        title = book.get_title()
        if title is not None and len(title):
            title = title if len(title) < 50 else \
                "{}...".format(title[0:50])
        self.setText(title)

        self.setIcon(QtGui.QIcon('preview/preview.jpg'))
        self.setSizeHint(QtCore.QSize(250, 250))

        self.thread.start()

    def setCoverimage(self, cover=None):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(cover)
        self.setIcon(QtGui.QIcon(pixmap))


class DictionaryListWidget(QtWidgets.QListWidget):
    book = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DictionaryListWidget, self).__init__()
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setIconSize(QtCore.QSize(150, 200))
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.itemClicked.connect(self.clicked)

    def clicked(self, item):
        self.book.emit(item.book)

    def append(self, book=None):
        item = BookItem(book)
        self.addItem(item)
