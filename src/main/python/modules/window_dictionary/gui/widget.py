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
import functools
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .text import TranslationWidget


class Translator(QtWidgets.QWidget):
    translate = QtCore.pyqtSignal(object)

    @inject.params(dictionary='dictionary')
    def __init__(self, parent=None, dictionary=None):
        super(Translator, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumWidth(300)

        self.translator = TranslationWidget(self)
        self.translator.setTranslation(dictionary.translate('welcome'))
        self.layout().addWidget(self.translator)

        self.translate.connect(self.onTranslateEvent)

    @inject.params(dictionary='dictionary')
    def onTranslateEvent(self, string=None, dictionary=None):
        translations = dictionary.translate(string)
        self.translator.setTranslation(translations)

    def close(self):
        super(Translator, self).deleteLater()
        return super(Translator, self).close()
