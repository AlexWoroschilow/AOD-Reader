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


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(window='window')
    def _provider_browser(self, window):
        from PyQt5.QtWebEngineWidgets import QWebEngineProfile

        from .gui.browser.webview import WebEngineUrlRequestInterceptor
        from .gui.browser.webview import MyWebEnginePage
        from .gui.browser.webview import MyWebEngineView

        browser = MyWebEngineView()
        profile = QWebEngineProfile(window)
        interceptor = WebEngineUrlRequestInterceptor(window)
        profile.setRequestInterceptor(interceptor)
        page = MyWebEnginePage(profile, window)
        browser.setPage(page)

        return browser

    @inject.params(window='window')
    def _provider_reader(self, window=None):
        from .gui.widget import ReaderWidget
        return ReaderWidget(window)

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_provider('window.reader', self._provider_reader)
        binder.bind_to_provider('window.browser', self._provider_browser)

    @inject.params(window='window')
    def boot(self, options, args, window=None):
        window.reader.connect(self.onWindowReader)

    @inject.params(window='window', reader='window.reader')
    def onWindowReader(self, book, window=None, reader=None):
        if reader is None:
            return None

        reader.back.connect(window.collection.emit)
        reader.translate.connect(window.translate.emit)
        reader.open(book)

        window.setCentralWidget(reader)
