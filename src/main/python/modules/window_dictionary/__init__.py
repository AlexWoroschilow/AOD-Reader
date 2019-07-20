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

from .service import DictionaryManager


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _widget_settings(self, config=None):
        from .gui.settings.widget import SettingsWidget

        widget = SettingsWidget()

        return widget

    @inject.params(config='config')
    def _provider_translator(self, config=None):
        from .gui.widget import Translator

        return Translator()

    @inject.params(config='config')
    def _service(self, config=None):
        return DictionaryManager()

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_provider('window.translator', self._provider_translator)
        binder.bind_to_constructor('dictionary', self._service)
