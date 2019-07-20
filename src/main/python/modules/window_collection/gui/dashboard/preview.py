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
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .label import PreviewLabel


class PreviewWidget(QtWidgets.QFrame):
    book = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    @inject.params(reader='reader')
    def __init__(self, path=None, reader=None):
        super(PreviewWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        pixmap = QtGui.QPixmap('preview/preview.png')
        book = reader.book(path)
        if book is not None and book:
            cover = book.get_cover_image()
            pixmap = QtGui.QPixmap(cover)

        label = PreviewLabel(self, pixmap)
        label.clicked.connect(lambda x: self.book.emit(book))

        self.layout().addWidget(label)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(15)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

    def close(self):
        super(PreviewWidget, self).deleteLater()
        return super(PreviewWidget, self).close()
