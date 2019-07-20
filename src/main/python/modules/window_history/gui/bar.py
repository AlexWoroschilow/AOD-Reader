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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class HistoryToolbar(QtWidgets.QToolBar):
    exportCsv = QtCore.pyqtSignal(object)
    exportAnki = QtCore.pyqtSignal(object)
    listClean = QtCore.pyqtSignal(object)

    def __init__(self):
        super(HistoryToolbar, self).__init__()

        self.setOrientation(Qt.Vertical)

        icon = QtGui.QIcon('icons/csv')
        csv = QtWidgets.QAction(icon, self.tr('Export to CSV'), self)
        csv.triggered.connect(self.exportCsv.emit)
        self.addAction(csv)

        icon = QtGui.QIcon('icons/anki')
        anki = QtWidgets.QAction(icon, self.tr('Export to Anki'), self)
        anki.triggered.connect(self.exportAnki.emit)
        self.addAction(anki)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)

        icon = QtGui.QIcon('icons/trash')
        clean = QtWidgets.QAction(icon, self.tr('Cleanup the history'), self)
        clean.triggered.connect(self.listClean.emit)
        self.addAction(clean)

    def close(self):
        super(HistoryToolbar, self).deleteLater()
        return super(HistoryToolbar, self).close()
