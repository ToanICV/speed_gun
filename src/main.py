'''
Usage: python -m src.main
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray
from .define import *


class MAIN(QMainWindow):
    IMG_W   = 525
    IMG_H   = 290
    MAP_W   = 180
    MAP_H   = 290
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(MAIN_UI_PATH, self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.viewSnapshoot()
        self.viewMap()

    def viewSnapshoot(self):
        pixmap = QPixmap(EXAMPLE_IMG_PATH)
        pixmap = pixmap.scaled(MAIN.IMG_W, MAIN.IMG_H, Qt.KeepAspectRatio)
        self.lbl_display.setPixmap(pixmap)
        self.lbl_display.resize(MAIN.IMG_W, MAIN.IMG_H)
        self.show()

    def viewMap(self):
        pixmap = QPixmap(EXAMPLE_MAP_PATH)
        pixmap = pixmap.scaled(MAIN.MAP_W, MAIN.MAP_H, Qt.KeepAspectRatio)
        self.lbl_map.setPixmap(pixmap)
        self.lbl_map.resize(MAIN.MAP_W, MAIN.MAP_H)
        self.show()

    def viewNoSnapShoot(self):
        pixmap = QPixmap(NULL_IMG_PATH)
        pixmap = pixmap.scaled(MAIN.W_DISP, MAIN.H_DISP, Qt.KeepAspectRatio)
        self.lbl_display.setPixmap(pixmap)
        self.lbl_display.resize(MAIN.W_DISP, MAIN.H_DISP)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MAIN()
    win.show()
    sys.exit(app.exec())
