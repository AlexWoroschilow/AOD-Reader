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
from PyQt5.QtCore import Qt

from .preview import PreviewWidget
from .widget import CollectionContainerWidget


class PreviewScrollArea(QtWidgets.QScrollArea):
    book = QtCore.pyqtSignal(object)
    columns = 2

    def __init__(self, parent):
        super(PreviewScrollArea, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.container = CollectionContainerWidget(self)
        self.setWidget(self.container)

        self.show()

    def resizeEvent(self, event):
        size = event.size()
        columns = math.floor(size.width() / 200)
        if columns and self.columns != columns:
            self.columns = columns if columns > 0 else 1
            self.show()
        return super(PreviewScrollArea, self).resizeEvent(event)

    def show(self, status=None, storage=None):

        widgets = []
        layout = self.container.layout()
        for x in range(0, layout.count()):
            item = layout.itemAt(x)
            if item is None: layout.takeAt(x)
            if item is None: continue
            widgets.append(item.widget())

        for x, widget in enumerate(widgets, start=0):
            i = math.floor(x / self.columns)
            j = math.floor(x % self.columns)
            layout.addWidget(widget, i, j)

        return super(PreviewScrollArea, self).show()

    def append(self, book=None):
        if book is None:
            return None

        layout = self.container.layout()
        position = layout.count()

        widget = PreviewWidget(book)
        widget.book.connect(self.book.emit)
        widget.setFixedHeight(200)

        i = math.floor(position / self.columns)
        j = math.floor(position % self.columns)

        layout.addWidget(widget, i, j)

    def close(self):
        super(PreviewScrollArea, self).deleteLater()
        return super(PreviewScrollArea, self).close()
