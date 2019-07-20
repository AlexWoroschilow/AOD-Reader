import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        # info.setHttpHeader("X-Frame-Options", "ALLOWALL")
        print("interceptRequest")
        print(info.requestUrl())


class MyWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        print("acceptNavigationRequest")
        print(url)
        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)


app = QApplication(sys.argv)

container = QtWidgets.QWidget()
container.setLayout(QtWidgets.QVBoxLayout())

browser = QWebEngineView()
interceptor = WebEngineUrlRequestInterceptor()

profile = QWebEngineProfile()
profile.setRequestInterceptor(interceptor)

page = MyWebEnginePage(profile, browser)
# page.setUrl(QUrl("https://stackoverflow.com/questions/50786186/qwebengineurlrequestinterceptor-not-working"))
page.setHtml("<a href='http://google.com'>test</a>")

browser.setPage(page)

container.layout().addWidget(browser)
container.show()

sys.exit(app.exec_())
