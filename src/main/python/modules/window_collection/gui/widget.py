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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .bar import CollectionToolbarWidget
from .dashboard.scroll import PreviewScrollArea


class CollectionWidget(QtWidgets.QWidget):
    search = QtCore.pyqtSignal(object)
    settings = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, parent, storage):
        super(CollectionWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        toolbar = CollectionToolbarWidget()
        toolbar.search.connect(self.search.emit)
        toolbar.settings.connect(self.settings.emit)
        self.layout().addWidget(toolbar)

        scroll = PreviewScrollArea(self, storage.collection())
        scroll.book.connect(self.book.emit)
        self.layout().addWidget(scroll)
