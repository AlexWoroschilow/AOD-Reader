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
from typing import List, Any, Tuple

import os
import uuid
import zipfile
from collections import OrderedDict
import xmltodict
import logging


class BookReader(object):
    def __init__(self, path=None):
        self.logger = logging.getLogger('reader')

        self.cache = '/tmp/aod-reader/{}'.format(
            self.get_unique(path)
        )

        self.ebook = path

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _get_source_content(self):
        """
        looking for the file "content.opf"
        :return:
        """
        try:

            def parse(stream_dict=None, zipstream=None):
                if stream_dict is None or zipstream is None:
                    return None
                return stream_dict['container']['rootfiles']['rootfile']['@full-path']

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:
                with zipstream.open('META-INF/container.xml') as stream:
                    return parse(xmltodict.parse(stream.read()), zipstream)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def _get_source_content_table(self):
        """
        looking for the file "toc.ncx"
        :return:
        """
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] == 'ncx':
                        if root is None or not len(root):
                            return item['@href']
                        return '{}/{}'.format(root, item['@href'])
                return None

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_unique(self, path=None):
        if path is None:
            path = self.ebook

        if path is None:
            return None

        return uuid.uuid5(uuid.NAMESPACE_URL, path)

    def get_title(self):
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None
                result = stream_dict['package']['metadata']['dc:title']
                if type(result) == OrderedDict:
                    return result.pop()
                return result

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_language(self):
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None
                return stream_dict['package']['metadata']['dc:language']

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_cover_image(self):
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] not in ['cover', 'coverimage', 'cover-image']:
                        continue
                    if item['@media-type'].find('image') == -1:
                        continue

                    href = item['@href']
                    if root is not None and len(root):
                        href = '{}/{}'.format(root, href)

                    return 'file://{}/{}'.format(self.cache, href)

                return None

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_cover_image_content(self):
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] not in ['cover', 'coverimage', 'cover-image']:
                        continue
                    if item['@media-type'].find('image') == -1:
                        continue

                    href = item['@href']
                    if root is not None and len(root):
                        href = '{}/{}'.format(root, href)

                    with zipstream.open(href) as stream:
                        return stream.read()

                return None

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_cover_page(self):

        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@id'] not in ['cover', 'coverpage', 'cover-page']:
                        continue
                    if item['@media-type'].find('application') == -1:
                        continue

                    href = item['@href']
                    if root is not None and len(root):
                        href = '{}/{}'.format(root, href)

                    return 'file://{}/{}'.format(self.cache, href)

                return None

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_stylesheet(self):
        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@media-type'].find('css') == -1:
                        continue

                    href = item['@href']
                    if root is not None and len(root):
                        href = '{}/{}'.format(root, href)

                    yield 'file://{}/{}'.format(self.cache, href)

                return None

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return None

    def get_content_table(self):
        collection = []

        try:

            def parse_recursive(items, root=None):
                collection = []

                try:
                    for item in items:

                        src = item['content']['@src']
                        if root is not None and len(root):
                            src = '{}/{}'.format(root, src)

                        label = item['navLabel']['text']
                        order = int(item['@playOrder'])

                        collection.append((label, 'file://{}/{}'.format(self.cache, src), order))
                        if 'navPoint' not in item.keys():
                            continue

                        children = parse_recursive(item['navPoint'], root)
                        collection = collection + children

                except (Exception, TypeError) as ex:
                    print(ex)

                return collection

            def parse(stream_dict=None, collection=None, root=None):
                navPoint = stream_dict['ncx']['navMap']['navPoint']
                if type(navPoint) == OrderedDict:
                    navPoint = [navPoint]

                children = parse_recursive(navPoint, root)
                return collection + children

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content_table()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), collection, content_folder)

        except (Exception, TypeError) as ex:
            raise ex

        return sorted(collection, key=lambda entity: entity[2])

    def get_pages(self):
        collection = []

        if not os.path.exists(self.cache):
            with zipfile.ZipFile(self.ebook, 'r') as stream:
                stream.extractall(self.cache)

        try:

            def parse(stream_dict=None, root=None):
                if stream_dict is None:
                    return None

                for item in stream_dict['package']['manifest']['item']:
                    if item['@media-type'].find('xhtml') == -1:
                        continue

                    href = item['@href']
                    if root is not None and len(root):
                        href = '{}/{}'.format(root, href)

                    yield 'file://{}/{}'.format(self.cache, href)

            with zipfile.ZipFile(self.ebook, 'r') as zipstream:

                content_file = self._get_source_content()
                content_folder = os.path.dirname(content_file)

                with zipstream.open(content_file) as stream:
                    return parse(xmltodict.parse(stream.read()), content_folder)

        except Exception as ex:
            self.logger.error(ex)
        return sorted(collection, key=lambda entity: entity[0])


class ReaderService(object):

    def book(self, path=None):
        return BookReader(path)


if __name__ == "__main__":
    book = '/home/sensey/Books/18850745.epub'
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
