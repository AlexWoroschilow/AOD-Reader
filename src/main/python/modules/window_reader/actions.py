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
import shutil

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ReaderActions(object):

    def __init__(self):
        pass

    def on_action_export(self, ebook=None, widget=None):
        if widget is None: return None

        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if os.path.exists(path):

                button_1 = QtWidgets.QMessageBox.Yes
                button_2 = QtWidgets.QMessageBox.No
                message = "Are you sure you want to overwrite the file '{}' ?".format(path)
                reply = QtWidgets.QMessageBox.question(widget, 'Are you sure?', message, button_1, button_2)
                if reply == QtWidgets.QMessageBox.No:
                    break

            if not os.path.exists(ebook.get_path()): return None
            shutil.copyfile(ebook.get_path(), '{}.epub'.format(path.replace('.epub', '')))
