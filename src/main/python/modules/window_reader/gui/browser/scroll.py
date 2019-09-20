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
import os
import platform
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class WidgetSettings(QtWidgets.QWidget):
    columns = 1

    def __init__(self):
        super(WidgetSettings, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)


class SettingsScrollArea(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super(SettingsScrollArea, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignTop)
        self.setWidgetResizable(True)

        self.container = WidgetSettings()
        self.setWidget(self.container)

        stylesheet = 'css/{}.qss'.format(platform.system().lower())
        if not os.path.exists(stylesheet):
            return None

        self.setStyleSheet(open(stylesheet).read())

    def addWidget(self, widget):
        self.container.addWidget(widget)

    def close(self):
        super(SettingsScrollArea, self).deleteLater()
        return super(SettingsScrollArea, self).close()
