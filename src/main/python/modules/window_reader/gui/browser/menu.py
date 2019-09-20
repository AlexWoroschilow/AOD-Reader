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

from . import SettingsTitle
from . import WidgetSettings

from .scroll import SettingsScrollArea


class SettingsSpacer(QtWidgets.QWidget):
    def __init__(self):
        super(SettingsSpacer, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


class SettingsMenu(QtWidgets.QWidgetAction):
    zoom = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, parent, config):
        super(SettingsMenu, self).__init__(parent)

        container = SettingsScrollArea()

        container.addWidget(SettingsTitle('Shortcuts'))
        container.addWidget(QtWidgets.QLabel('Esc - back to library'))
        container.addWidget(QtWidgets.QLabel('Ctl+E - export book'))
        container.addWidget(SettingsSpacer())

        container.addWidget(SettingsTitle('Reader'))
        container.addWidget(QtWidgets.QLabel('Font size:'))

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.valueChanged.connect(lambda x: self.zoom.emit(x / 10))

        slider.setValue(float(config.get('browser.zoom')) * 10)
        slider.setTickInterval(5)
        slider.setMinimum(0)
        slider.setMaximum(50)

        container.addWidget(slider)

        container.addWidget(QtWidgets.QLabel('...'))
        container.addWidget(SettingsSpacer())

        container.addWidget(SettingsTitle('Dictionary'))
        container.addWidget(QtWidgets.QLabel('...'))
        container.addWidget(SettingsSpacer())

        container.addWidget(SettingsTitle('History'))
        container.addWidget(QtWidgets.QLabel('...'))
        container.addWidget(SettingsSpacer())

        self.setDefaultWidget(container)
