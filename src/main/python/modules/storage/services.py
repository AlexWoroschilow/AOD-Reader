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
import configparser
import glob


class StorageService(object):

    def __init__(self, location=None):
        self.location = []
        self.location.append(location)

    def collection(self):
        sources = self.location.copy()
        if sources.__len__() == 0:
            return []

        collection = []
        while len(sources):
            source = sources.pop()
            for path in glob.glob('{}/*'.format(source)):
                if os.path.isdir(path):
                    sources.append(path)
                    continue
                if path.rfind('epub') != -1:
                    collection.append(path)
        return collection
