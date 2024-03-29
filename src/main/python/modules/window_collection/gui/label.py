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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class PreviewLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent, picture=None):
        super(PreviewLabel, self).__init__(parent)

        self.setPixmap(picture.scaledToWidth(180, Qt.FastTransformation))

    def mousePressEvent(self, event):
        self.clicked.emit(event)
