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

from .thread import CollectionThread
from .gui.widget import CollectionWidget


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(window='window')
    def _provider_collection(self, window=None):
        thread = CollectionThread()

        widget = CollectionWidget(window)
        thread.started.connect(lambda x: widget.progress.setVisible(True))
        thread.finished.connect(lambda x: widget.progress.setVisible(False))
        thread.progress.connect(lambda x: widget.progress.setValue(x))
        thread.book.connect(widget.append)

        thread.start()

        return widget

    @inject.params(config='config')
    def _widget_settings(self, config=None):
        from .gui.settings.widget import SettingsWidget

        widget = SettingsWidget()

        return widget

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_provider('window.collection', self._provider_collection)

    @inject.params(window='window', widget='window.collection')
    def boot(self, options, args, window=None, widget=None):
        widget.book.connect(window.reader.emit)

        if window is None:
            return None

        window.collection.connect(self.onWindowCollection)
        window.setCentralWidget(widget)

    @inject.params(window='window', widget='window.collection')
    def onWindowCollection(self, event, window=None, widget=None):
        widget.book.connect(window.reader.emit)

        window.setCentralWidget(widget)
