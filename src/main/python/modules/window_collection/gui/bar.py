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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .text import SearchField
from .button import PictureButtonFlat


class CollectionToolbarWidget(QtWidgets.QWidget):
    search = QtCore.pyqtSignal(object)
    settings = QtCore.pyqtSignal(object)
    clean = QtCore.pyqtSignal(object)

    def __init__(self):
        super(CollectionToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(spacer)

        search = SearchField()
        search.returnPressed.connect(lambda x=None: self.search.emit(search.text()))
        search.setMinimumWidth(500)
        search.setMinimumHeight(55)
        self.layout().addWidget(search)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(spacer)

        settings = PictureButtonFlat(QtGui.QIcon('icons/icons'))
        settings.clicked.connect(self.settings.emit)
        self.layout().addWidget(settings)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), search)
        shortcut.activated.connect(lambda event=None: search.setText(None))
        shortcut.activatedAmbiguously.connect(search.clearFocus)
        shortcut.activated.connect(search.clearFocus)
        shortcut.activated.connect(lambda x=None: self.clean.emit(None))
