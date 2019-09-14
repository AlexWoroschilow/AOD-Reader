import inject
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        # info.setHttpHeader("X-Frame-Options", "ALLOWALL")
        print("interceptRequest")
        print(info.requestUrl())


class MyWebEnginePage(QWebEnginePage):

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        print([url, url.scheme(), url.path(), url.query()])
        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)

    def setUserStylesheet(self, stylesheet=None):
        if stylesheet is None:
            return None

        stylesheet = stylesheet.replace("\n", ' ')
        self.runJavaScript(""" var styleSheet = document.createElement("style");
                        styleSheet.setAttribute('id', 'customstyle');
                        styleSheet.setAttribute('type', 'text/css');
                        styleSheet.setAttribute('type', 'text/css');
                        styleSheet.innerText = '{}';
                        document.head.appendChild(styleSheet);""".format(stylesheet))

    def removeUserStylesheet(self):
        self.runJavaScript(""" document.getElementById('customstyle').outerHTML = ""; """)

    def getScrollPosition(self, callback=None):
        javascript = "(function () { return window.scrollY; })();"
        self.runJavaScript(javascript, callback)  # scrool selected page to the given position

    def setScrollPosition(self, position):
        javascript = "window.scrollTo(0,parseFloat('{}'));".format(position)
        self.runJavaScript(javascript)  # scrool selected page to the given position


class MyWebEngineView(QWebEngineView):
    zoom = 1
    zoomPixelMax = 150

    translate = QtCore.pyqtSignal(object)
    bookPage = QtCore.pyqtSignal(object)
    book = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config):
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.zoom = float(config.get('browser.zoom', 1))
        self.ebook = None

        super(MyWebEngineView, self).__init__()
        self.bookPage.connect(self.pageEvent)
        self.book.connect(self.bookEvent)

    def event(self, QEvent):
        if QEvent.type() in [QtCore.QEvent.Leave]:
            self.clipboard.selectionChanged.disconnect()
        if QEvent.type() in [QtCore.QEvent.Enter]:
            self.clipboard.selectionChanged.connect(self.translateEvent)
        return super(MyWebEngineView, self).event(QEvent)

    def translateEvent(self, event=None):
        text = self.clipboard.text(QtGui.QClipboard.Selection)
        self.translate.emit(text)

    @inject.params(config='config')
    def wheelEvent(self, event, config):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            point = event.pixelDelta()
            self.zoom = self.zoom + (point.y() / self.zoomPixelMax)
            if self.zoom >= 0 and self.zoom <= 5:
                config.set('browser.zoom', self.zoom)
                self.setZoomFactor(self.zoom)

        self.page().getScrollPosition(self.scrollPositionEvent)
        return super(MyWebEngineView, self).wheelEvent(event)

    @inject.params(config='config')
    def scrollPositionEvent(self, position, config):
        book_unique = self.ebook.get_unique()
        if book_unique is None: return None
        config.set('{}.position'.format(book_unique), position)

    @inject.params(config='config')
    def bookEvent(self, book=None, config=None):
        self.loadFinished.connect(self.appendStylesheet)
        self.clipboard.selectionChanged.connect(self.translateEvent)
        self.ebook = book

        self.setZoomFactor(self.zoom)

        for path in self.ebook.get_pages():
            return self.page().load(QtCore.QUrl(path))

    @inject.params(config='config')
    def pageEvent(self, path=None, config=None):
        book_unique = self.ebook.get_unique()
        if book_unique is not None and book_unique:
            config.set('{}.page'.format(book_unique), path)

        url = QtCore.QUrl(path)
        self.page().setUrl(url)

    @inject.params(config='config')
    def appendStylesheet(self, event=None, config=None):

        book_unique = self.ebook.get_unique()
        if book_unique is not None and book_unique:
            position = config.get('{}.position'.format(book_unique), 0)
            # scrool selected page to the given position
            self.page().setScrollPosition(position)

        with open('css/ebook.css', 'r') as stream:
            stylesheet = stream.readlines()
            self.page().setUserStylesheet(' '.join(stylesheet))
