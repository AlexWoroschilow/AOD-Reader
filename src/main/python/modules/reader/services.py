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
import uuid
import zipfile
from collections import OrderedDict
import xmltodict
import logging


class BookReader(object):
    def __init__(self, path=None):
        self.logger = logging.getLogger('reader')

        self.cache = '/tmp/ebook/{}'.format(
            self.get_unique(path)
        )

        self.path = path

        if not os.path.exists(self.cache):
            with zipfile.ZipFile(self.path, 'r') as stream:
                stream.extractall(self.cache)

    def _get_source_content(self):
        """
        looking for the file "content.opf"
        :return:
        """
        with open('{}/META-INF/container.xml'.format(self.cache), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                href = stream_dict['container']['rootfiles']['rootfile']['@full-path']
                source = '{}/{}'.format(self.cache, href)
                if os.path.exists(source):
                    return source
                source = '{}/OEBPS/{}'.format(self.cache, href)
                if os.path.exists(source):
                    return source

                return None

            except Exception as ex:
                self.logger.error(ex)
        return None

    def _get_source_content_table(self):
        """
        looking for the file "toc.ncx"
        :return:
        """
        with open(self._get_source_content(), 'rb') as stream:
            stream_dict = xmltodict.parse(stream.read())
            for item in stream_dict['package']['manifest']['item']:
                if item['@id'] == 'ncx':
                    href = item['@href']
                    source = '{}/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return source
                    source = '{}/OEBPS/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return source
                    return None
        return None

    def get_unique(self, path=None):
        if path is None:
            path = self.path

        if path is None:
            return None

        return uuid.uuid5(uuid.NAMESPACE_URL, path)

    def get_title(self):
        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                return stream_dict['package']['metadata']['dc:title']
            except Exception as ex:
                self.logger.error(ex)
        return None

    def get_language(self):
        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                return stream_dict['package']['metadata']['dc:language']
            except Exception as ex:
                self.logger.error(ex)
        return None

    def get_cover_image(self):
        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] not in ['cover', 'coverimage', 'cover-image']:
                        continue
                    if item['@media-type'].find('image') == -1:
                        continue

                    href = item['@href']
                    source = '{}/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return source
                    source = '{}/OEBPS/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return source
                return None
            except Exception as ex:
                self.logger.error(ex)
        return None

    def get_cover_page(self):
        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] not in ['cover', 'coverpage', 'cover-page']:
                        continue
                    if item['@media-type'].find('application') == -1:
                        continue

                    href = item['@href']
                    source = '{}/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return 'file://{}'.format(source)
                    source = '{}/OEBPS/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        return 'file://{}'.format(source)
                return None
            except Exception as ex:
                self.logger.error(ex)
        return None

    def get_stylesheet(self):
        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                for item in stream_dict['package']['manifest']['item']:
                    if item['@media-type'].find('css') == -1:
                        continue

                    href = item['@href']
                    source = '{}/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        yield 'file://{}'.format(source)
                    source = '{}/OEBPS/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        yield 'file://{}'.format(source)
                return None
            except Exception as ex:
                self.logger.error(ex)
        return None

    def _get_content_table_recursive(self, items):

        collection = []
        for item in items:

            src = item['content']['@src']
            source = '{}/OEBPS/{}'.format(self.cache, src)
            if not os.path.exists(source):
                source = '{}/{}'.format(self.cache, src)

            label = item['navLabel']['text']
            order = int(item['@playOrder'])

            collection.append((label, 'file://{}'.format(source), order))
            if 'navPoint' not in item.keys():
                continue

            children = self._get_content_table_recursive(item['navPoint'])
            collection = collection + children

        return collection

    def get_content_table(self):
        collection = []

        with open(self._get_source_content_table(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                navPoint = stream_dict['ncx']['navMap']['navPoint']
                if type(navPoint) == OrderedDict:
                    navPoint = [navPoint]

                children = self._get_content_table_recursive(navPoint)
                return collection + children

            except Exception as ex:
                raise ex
        return sorted(collection, key=lambda entity: entity[2])

    def get_pages(self):
        collection = []

        with open(self._get_source_content(), 'rb') as stream:
            try:
                stream_dict = xmltodict.parse(stream.read())
                for item in stream_dict['package']['manifest']['item']:
                    if item['@media-type'].find('xhtml') == -1:
                        continue

                    href = item['@href']
                    source = '{}/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        yield 'file://{}'.format(source)

                    source = '{}/OEBPS/{}'.format(self.cache, href)
                    if os.path.exists(source):
                        yield 'file://{}'.format(source)

            except Exception as ex:
                self.logger.error(ex)
        return sorted(collection, key=lambda entity: entity[0])


class ReaderService(object):

    def book(self, path=None):
        return BookReader(path)


if __name__ == "__main__":
    book = '/home/sensey/Books/[Philip_Reeve]_Night_Flights(z-lib.org).epub'
    reader = BookReader(book)
    print(reader.get_title())
    print(reader.get_language())
    print(reader.get_cover_image())
    print(reader.get_cover_page())
    print(reader.get_content_table())
    for page in reader.get_pages():
        print(page)
    for stylesheet in reader.get_stylesheet():
        print(stylesheet)
