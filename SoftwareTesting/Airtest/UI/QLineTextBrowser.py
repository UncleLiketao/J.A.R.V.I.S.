from PyQt5 import QtWidgets, QtGui


class QLineTextBrowser(QtWidgets.QTextBrowser):
    def __init__(self, parent=None):
        super(QLineTextBrowser, self).__init__(parent)

    def dropEvent(self, e: QtGui.QDropEvent):
        self.clear()
        filePath = (e.mimeData().urls())[0].toLocalFile()
        self.append(filePath)