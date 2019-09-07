#!/usr/bin/python3

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
import sys

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

sys.path.append(os.path.join(os.getcwd(), 'lib'))
sys.path.append(os.path.join(os.getcwd(), 'modules'))
sys.path.append(os.path.join(os.getcwd(), 'plugins'))

import inject
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

import optparse
import logging

from lib.kernel import Kernel


class Application(QtWidgets.QApplication):
    kernel = None

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)

        from PyQt5.QtCore import QEventLoop
        self.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)

        self.setApplicationName('AOD - EBookReader')
        self.kernel = Kernel(options, args)
        self.kernel.application = self

    @inject.params(window='window')
    def exec_(self, options, args, window):
        if window is None:
            return None

        window.exit.connect(self.exit)
        window.show()

        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--logfile", default='./reader.log', dest="logfile", help="Logfile location")
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    parser.add_option("--config", default='./reader.conf', dest="config", help="Config file location")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_(options, args))
