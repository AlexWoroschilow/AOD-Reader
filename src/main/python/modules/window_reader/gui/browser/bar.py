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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .button import PictureButtonFlat
from .label import Title


class BrowserToolbarWidget(QtWidgets.QWidget):
    settings = QtCore.pyqtSignal(object)
    export = QtCore.pyqtSignal(object)
    back = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(BrowserToolbarWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        back = PictureButtonFlat(QtGui.QIcon("icons/back"))
        back.clicked.connect(self.back.emit)
        self.layout().addWidget(back)

        self.title = Title('Test title')
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.title.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.title)

        export = PictureButtonFlat(QtGui.QIcon("icons/export"))
        export.setFlat(False)
        export.clicked.connect(self.export.emit)
        self.layout().addWidget(export)
        self.book.connect(self.bookEvent)

        settings = PictureButtonFlat(QtGui.QIcon("icons/settings"))
        settings.clicked.connect(self.settings.emit)
        self.layout().addWidget(settings)
        self.book.connect(self.bookEvent)

    def bookEvent(self, book=None):
        if book is None:
            return None

        self.title.setText(book.get_title())
