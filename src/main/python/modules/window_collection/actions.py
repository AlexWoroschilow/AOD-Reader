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
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .gui.menu import SettingsMenu
from .thread import SearchThread


class TranslatorActions(object):
    thread = SearchThread()

    def __init__(self):
        pass

    def on_action_progress_started(self, event=None, widget=None):
        if widget is None: return None

        try:
            widget.progress.setVisible(True)
        except (RuntimeError, TypeError, NameError) as ex:
            print(ex)

    def on_action_progress_update(self, event=None, widget=None):
        if widget is None: return None

        try:
            widget.progress.setVisible(True)
            widget.progress.setValue(event)
        except (RuntimeError, TypeError, NameError) as ex:
            print(ex)

    def on_action_progress_finished(self, event=None, widget=None):
        if widget is None: return None

        try:
            widget.progress.setVisible(False)
        except (RuntimeError, TypeError, NameError) as ex:
            print(ex)

    @inject.params(search='search')
    def on_action_search(self, text=None, search=None, widget=None):
        if widget is None: return None

        for result in search.search(text):
            print(result)

    def on_action_clean(self, event=None, widget=None):
        if widget is None: return None
        print(event, widget)

    def on_action_settings(self, button=None, widget=None):
        if widget is None: return None

        menu = QtWidgets.QMenu()

        menu_search = SettingsMenu(widget, self.thread)

        menu_search.started.connect(functools.partial(
            self.on_action_progress_started, widget=widget
        ))
        menu_search.progress.connect(functools.partial(
            self.on_action_progress_started, widget=widget
        ))
        menu_search.progress.connect(functools.partial(
            self.on_action_progress_update, widget=widget
        ))
        menu_search.finished.connect(functools.partial(
            self.on_action_progress_finished, widget=widget
        ))

        menu.addAction(menu_search)
        menu.exec_(QtGui.QCursor.pos())
