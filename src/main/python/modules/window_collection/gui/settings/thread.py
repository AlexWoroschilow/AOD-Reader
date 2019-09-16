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


class SearchThread(QtCore.QThread):
    started = QtCore.pyqtSignal(float)
    progress = QtCore.pyqtSignal(float)
    book = QtCore.pyqtSignal(object)
    book_page = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(int)

    def __del__(self):
        self.wait()

    @inject.params(storage='storage', reader='reader', search='search')
    def run(self, storage=None, reader=None, search=None):
        self.started.emit(0)

        collection = storage.collection()
        collection_len = len(collection)
        for index, path in enumerate(collection, start=1):
            percent = index / collection_len * 100
            self.progress.emit(percent)

            with reader.book(path) as book:
                self.book.emit(book)
                try:
                    unique = book.get_unique()
                    if search.has_in_index(unique):
                        continue

                    title = book.get_title()
                    for page in book.get_pages():
                        # search.append_book_page(book, title, unique, page)
                        self.book_page.emit((book, title, unique, page))
                        self.progress.emit(percent)

                except Exception as ex:
                    print(ex)
                    continue

        self.finished.emit(100)
