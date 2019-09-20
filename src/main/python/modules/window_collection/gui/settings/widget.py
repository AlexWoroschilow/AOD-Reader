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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui

from . import SettingsTitle
from . import WidgetSettings


class WidgetSettingsSearch(WidgetSettings):
    started = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self, thread):
        super(WidgetSettingsSearch, self).__init__()

        thread.progress.connect(self.progress.emit)
        thread.finished.connect(self.finished.emit)
        thread.started.connect(self.started.emit)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Fulltext search'))

        progressbar = QtWidgets.QProgressBar(self)
        progressbar.setVisible(False)
        self.layout.addWidget(progressbar)

        self.rebuild = QtWidgets.QPushButton("update search index")
        self.rebuild.setIcon(QtGui.QIcon("icons/refresh"))
        self.rebuild.setToolTip("Build new index. This may take some time.")
        self.rebuild.clicked.connect(thread.start)
        self.rebuild.setFlat(True)
        self.layout.addWidget(self.rebuild)

        thread.started.connect(lambda x: self.rebuild.setVisible(False))
        thread.progress.connect(lambda x: self.rebuild.setVisible(False))
        thread.finished.connect(lambda x: self.rebuild.setVisible(True))

        thread.started.connect(lambda x: progressbar.setVisible(True))
        thread.progress.connect(lambda x: progressbar.setVisible(True))
        thread.progress.connect(lambda x: progressbar.setValue(x))
        thread.finished.connect(lambda x: progressbar.setVisible(False))

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(spacer)

        self.setLayout(self.layout)

        self.show()
