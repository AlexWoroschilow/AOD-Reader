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
from PyQt5 import QtWidgets

from .scroll import SettingsScrollArea
from .settings.widget import WidgetSettingsSearch


class SettingsMenu(QtWidgets.QWidgetAction):
    started = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self, parent, thread):
        super(SettingsMenu, self).__init__(parent)

        widget_search = WidgetSettingsSearch(thread)
        widget_search.started.connect(self.started.emit)
        widget_search.finished.connect(self.finished.emit)
        widget_search.progress.connect(self.progress.emit)

        container = SettingsScrollArea()
        container.addWidget(widget_search)
        self.setDefaultWidget(container)
