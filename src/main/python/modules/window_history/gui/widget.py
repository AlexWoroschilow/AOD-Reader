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
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .bar import HistoryToolbar
from .table import HistoryTable


class HistoryWidget(QtWidgets.QWidget):
    translate = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    rowUpdate = QtCore.pyqtSignal(object)
    rowRemove = QtCore.pyqtSignal(object)
    rowClean = QtCore.pyqtSignal(object)

    listClean = QtCore.pyqtSignal(object)

    exportCsv = QtCore.pyqtSignal(object)
    exportAnki = QtCore.pyqtSignal(object)

    history = None

    def __init__(self):
        super(HistoryWidget, self).__init__()
        self.logger = logging.getLogger('history')
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.toolbar = HistoryToolbar()
        self.toolbar.exportCsv.connect(lambda x=None: self.exportCsv.emit(self.history))
        self.toolbar.exportAnki.connect(lambda x=None: self.exportAnki.emit(self.history))
        self.toolbar.listClean.connect(lambda x=None: self.listClean.emit(self.history))

        self.table = HistoryTable()
        self.table.rowUpdate.connect(self.rowUpdate.emit)
        self.table.rowRemove.connect(self.rowRemove.emit)
        self.table.rowClean.connect(self.rowClean.emit)

        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.table)

        self.rowRemove.connect(self.rowRemoveEvent)
        self.rowUpdate.connect(self.rowUpdateEvent)
        self.listClean.connect(self.listCleanEvent)
        self.translate.connect(self.translateEvent)
        self.book.connect(self.bookEvent)

    def listCleanEvent(self, event=None):
        if self.history is None:
            return None

        message = self.tr("Are you sure you want to clean up the history?")
        reply = QtWidgets.QMessageBox.question(self, 'clean up the history?', message, QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None
        self.history.clean()

        count = self.history.count
        collection = self.history.history
        self.table.history(collection, count)

    def rowRemoveEvent(self, row=None):
        if row is None:
            return None
        if self.history is None:
            return None

        index, data, word, translation = row
        self.history.remove(index, data, word, translation)

    def rowUpdateEvent(self, row=None):
        if row is None:
            return None
        if self.history is None:
            return None

        index, data, word, translation = row
        self.history.update(index, data, word, translation)

    def translateEvent(self, word=None):
        if word is None:
            return None
        if self.history is None:
            return None

        try:
            self.history.add(word)

            count = self.history.count
            collection = self.history.history
            self.table.history(collection, count)

        except Exception as ex:
            self.logger.exception(ex)

    @inject.params(factory="history.factory")
    def bookEvent(self, book=None, factory=None):
        if book is None:
            return None

        try:

            self.history = factory(book)
            if self.history is None:
                return None

            count = self.history.count
            collection = self.history.history
            self.table.history(collection, count)

        except Exception as ex:
            self.logger.exception(ex)

    def resizeEvent(self, event):
        self.table.setFixedSize(self.size())

    def close(self, window=None):
        super(HistoryWidget, self).deleteLater()
        return super(HistoryWidget, self).close()
