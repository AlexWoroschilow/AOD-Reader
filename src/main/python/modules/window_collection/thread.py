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

from PyQt5 import QtCore
import time


class CollectionThread(QtCore.QThread):
    started = QtCore.pyqtSignal(float)
    progress = QtCore.pyqtSignal(float)
    book = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(int)

    def __del__(self):
        self.wait()

    @inject.params(storage='storage', reader='reader')
    def run(self, storage=None, reader=None):
        self.started.emit(0)

        collection = storage.collection()
        collection_len = len(collection)
        for index, path in enumerate(collection, start=1):
            self.progress.emit(index / collection_len * 100)
            with reader.book(path) as book:
                self.book.emit(book)
        self.finished.emit(100)
