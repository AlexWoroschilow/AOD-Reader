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
from .menu import SettingsMenu


class BrowserToolbarWidget(QtWidgets.QWidget):
    settings = QtCore.pyqtSignal(object)
    export = QtCore.pyqtSignal(object)
    back = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)
    zoom = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(BrowserToolbarWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        back = PictureButtonFlat(QtGui.QIcon("icons/back"))
        back.setShortcut('Esc')
        back.clicked.connect(self.back.emit)
        self.layout().addWidget(back)

        self.title = Title('Test title')
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.title.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.title)

        export = PictureButtonFlat(QtGui.QIcon("icons/export"))
        export.setShortcut('Ctrl+E')
        export.setFlat(False)
        export.clicked.connect(self.export.emit)
        self.layout().addWidget(export)
        self.book.connect(self.bookEvent)

        settings = PictureButtonFlat(QtGui.QIcon("icons/icons"))
        settings.clicked.connect(self.settings.emit)
        settings.clicked.connect(self.menu)
        self.layout().addWidget(settings)
        self.book.connect(self.bookEvent)

    def bookEvent(self, book=None):
        if book is None:
            return None

        self.title.setText(book.get_title())

    def menu(self, event=None):
        menu = QtWidgets.QMenu()

        menu_widget = SettingsMenu(self)
        menu_widget.zoom.connect(self.zoom.emit)

        menu.addAction(menu_widget)
        menu.exec_(QtGui.QCursor.pos())
