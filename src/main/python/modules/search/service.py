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

from bs4 import BeautifulSoup
from whoosh.fields import Schema, TEXT, ID
from whoosh import qparser
from whoosh import scoring
from whoosh import index
import urllib


class Search(object):

    def __init__(self, destination=None):
        super(Search, self).__init__()

        self.destination = destination
        self.writer = None
        self.ix = None

        self.schema = Schema(
            title=TEXT(stored=True),
            path=TEXT(stored=True),
            page=TEXT(stored=True),
            content=TEXT(stored=True),
            unique=ID(stored=True)
        )

        if not os.path.exists(self.destination):
            os.mkdir(self.destination)

        if not self.exists(self.destination):
            return self.create(self.destination)

        return self.previous(self.destination)

    def _strip_tags(self, html=None):
        if html is None:
            return None

        soup = BeautifulSoup(html, "html5lib")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('iframe')]
        return soup.text

    def create(self, destination=None):
        if self.schema is None:
            return None

        if destination is None:
            return None

        self.ix = index.create_in(destination, self.schema)

    def exists(self, destination=None):
        if destination is None:
            return False

        if not os.path.exists(destination):
            return False

        return index.exists_in(destination)

    def previous(self, destination=None):
        if destination is None:
            return None

        if not self.exists(destination):
            return None

        self.ix = index.open_dir(destination)
        return None

    def append_book_page(self, path=None, title=None, unique=None, page=None):
        if path is None: return None
        if title is None: return None
        if unique is None: return None
        if page is None: return None

        data = urllib.request.urlopen(page)
        title = u"{}".format(title)
        unique = u"{}".format(unique)
        path = u"{}".format(path)
        text = u"{}".format(data.read())

        content = self._strip_tags(text)
        if content is None or not len(content):
            return

        self.writer = self.ix.writer()
        self.writer.add_document(
            title=title, content=content,
            path=path, page=page,
            unique=unique,
        )
        self.writer.commit()

    def has_in_index(self, string=None):
        """
        Check if the document already exists in the index.
        This method does not check if all the pages of the document are in the index.
        If the indexation was cancelled the part of the document still may be in the index
        and this method will return the positive result
        :param string:
        :return:
        """
        query_parser = qparser.QueryParser("unique", self.ix.schema)
        with self.ix.searcher() as searcher:
            pattern = query_parser.parse(u'{}'.format(string))
            return len(searcher.search(pattern)) > 0
        return False

    def search(self, string=None, fields=["title", "content"]):
        query_parser = qparser.MultifieldParser(fields, self.ix.schema, group=qparser.OrGroup)
        query_parser.remove_plugin_class(qparser.PhrasePlugin)
        query_parser.add_plugin(qparser.FuzzyTermPlugin())
        query_parser.add_plugin(qparser.SequencePlugin())

        with self.ix.searcher(weighting=scoring.BM25F) as searcher:
            pattern = query_parser.parse(u'"{}"'.format(string))
            for result in searcher.search(pattern, limit=None):
                yield result

    def clean(self):
        if self.destination is None: return None
        self.create(self.destination)
        return True
