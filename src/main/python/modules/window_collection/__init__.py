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

from .thread import CollectionThread
from .thread import SearchThread

from .gui.widget import CollectionWidget
from .actions import TranslatorActions


class Loader(object):
    thread = None
    actions = TranslatorActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self):
        self.thread = CollectionThread()

    @inject.params(window='window')
    def _provider_library(self, window=None):

        try:
            self.thread.started.disconnect()
            self.thread.finished.disconnect()
            self.thread.progress.disconnect()
            self.thread.book.disconnect()
        except (Exception, RuntimeError, TypeError, NameError) as ex:
            logger = logging.getLogger('library')
            logger.error("{}".format(ex))

        widget = CollectionWidget(window)
        widget.settings.connect(functools.partial(
            self.actions.on_action_settings, widget=widget
        ))
        widget.search.connect(functools.partial(
            self.actions.on_action_search, widget=widget
        ))
        widget.clean.connect(functools.partial(
            self.actions.on_action_clean, widget=widget
        ))

        try:

            self.thread.started.connect(functools.partial(
                self.actions.on_action_progress_started, widget=widget
            ))
            self.thread.progress.connect(functools.partial(
                self.actions.on_action_progress_started, widget=widget
            ))
            self.thread.progress.connect(functools.partial(
                self.actions.on_action_progress_update, widget=widget
            ))
            self.thread.finished.connect(functools.partial(
                self.actions.on_action_progress_finished, widget=widget
            ))

            self.thread.book.connect(lambda x: widget.append(x))

        except (Exception, RuntimeError, TypeError, NameError) as ex:
            logger = logging.getLogger('library')
            logger.error("{}".format(ex))

        self.thread.start()

        return widget

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_provider('window.collection', self._provider_library)

    @inject.params(window='window', widget='window.collection')
    def boot(self, options, args, window=None, widget=None):
        if widget is None: return None
        if window is None: return None

        widget.book.connect(window.reader.emit)

        window.collection.connect(self.onWindowCollection)
        window.setCentralWidget(widget)

    @inject.params(window='window', widget='window.collection')
    def onWindowCollection(self, event, window=None, widget=None):
        if widget is None: return None
        if window is None: return None

        widget.book.connect(window.reader.emit)
        window.setCentralWidget(widget)
