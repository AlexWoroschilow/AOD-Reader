import inject
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
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


class MyWebEngineView(QWebEngineView):
    zoom = 1
    zoomPixelMax = 150

    book = QtCore.pyqtSignal(object)
    translate = QtCore.pyqtSignal(object)

    def __init__(self):
        self.clipboard = QtWidgets.QApplication.clipboard()
        super(MyWebEngineView, self).__init__()
        self.book.connect(self.bookEvent)

    def event(self, QEvent):
        if QEvent.type() in [QtCore.QEvent.Leave]:
            self.clipboard.selectionChanged.disconnect()
        if QEvent.type() in [QtCore.QEvent.Enter]:
            self.clipboard.selectionChanged.connect(self.test)
        return super(MyWebEngineView, self).event(QEvent)

    def test(self, event=None):
        text = self.clipboard.text(QtGui.QClipboard.Selection)
        self.translate.emit(text)

    @inject.params(config='config')
    def wheelEvent(self, event, config):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            point = event.pixelDelta()
            self.zoom = self.zoom + (point.y() / self.zoomPixelMax)
            if self.zoom >= 0 and self.zoom <= 5:
                print(self.zoom)
                config.set('browser.zoom', self.zoom)
                self.setZoomFactor(self.zoom)

        return super(MyWebEngineView, self).wheelEvent(event)

    @inject.params(config='config')
    def bookEvent(self, book=None, config=None):
        self.loadFinished.connect(self.appendStylesheet)
        self.clipboard.selectionChanged.connect(self.test)

        self.zoom = float(config.get('browser.zoom', 1))
        self.setZoomFactor(self.zoom)
        for path in book.get_pages():
            self.page().load(QtCore.QUrl(path))
            break

    def appendStylesheet(self, event=None):

        with open('css/ebook.css', 'r') as stream:
            stylesheet = stream.readlines()
            self.page().setUserStylesheet(' '.join(stylesheet))
