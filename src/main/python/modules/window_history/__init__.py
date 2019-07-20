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
import inject
import functools

from .gui.widget import HistoryWidget
from .service import SQLiteHistory
from .actions import HistoryActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _constructor(self, config=None):
        database = config.get('history.database')
        database = os.path.expanduser(database)
        return SQLiteHistory(database)

    @inject.params(history='history', window='window', factory="history.factory")
    def _provider(self, history=None, window=None, factory=None):
        actions = HistoryActions()

        widget = HistoryWidget()
        widget.exportCsv.connect(functools.partial(
            actions.exportCsvEvent, widget=widget
        ))
        widget.exportAnki.connect(functools.partial(
            actions.exportAnkiEvent, widget=widget
        ))
        return widget

    @inject.params(config='config')
    def _provider_factory(self, book=None, config=None):
        if book is None:
            return None
        database = config.get('history.location', '~/.config/AOD-Reader')
        database = '{}/{}'.format(os.path.expanduser(database), book.get_unique())
        if not os.path.exists(database):
            os.makedirs(database, exist_ok=True)
        return SQLiteHistory('{}/history.dhf'.format(database))

    @inject.params(config='config')
    def _widget_settings(self, config=None):
        from .gui.settings.widget import SettingsWidget
        return SettingsWidget()

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind('history.factory', self._provider_factory)
        binder.bind_to_constructor('history', self._constructor)
        binder.bind_to_provider('widget.history', self._provider)
