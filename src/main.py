'''
Usage: python -m src.main
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray
from .define import *
from .apis import *
import json


'''
TODO
[ ] Thêm trạng thái 4G và GPS.
[ ] Hiển thị trạng thái call API.
[ ] Restart server 4G và GPS trong Setting.
[ ] Nút getMapImage thủ công trong Setting.
'''

example_lat = 21.046242
example_lng = 105.787002

class MAIN(QMainWindow):
    IMG_W   = 525
    IMG_H   = 290
    MAP_W   = 180
    MAP_H   = 290
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(MAIN_UI_PATH, self)
        self.connectSignalsSlots()
        self.speedLimit     = 0
        self.configs_data   = None
    def loadConfigs(self):
        with open(CONFIGS_PATH) as fd:
            self.configs_data = json.load(fd)

    def connectSignalsSlots(self):
        # self.viewSnapshoot()
        self.viewMap()
        self.loadConfigs()

        resp = getMapImage(self.configs_data['deviceID'], example_lat, example_lng, getDate())
        if (resp != None):
            self.speedLimit = resp['speed_limit']
            # thành công -> set viền text edit màu xanh
            # mới load UI thì màu cam.
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Lấy ảnh từ server thất bại !")
            msg.setInformativeText("Bạn có muốn thử lại không?")
            msg.setWindowTitle("Lỗi")
            retry_btn = msg.addButton("Thử lại", QMessageBox.AcceptRole)
            reject_btn = msg.addButton("Bỏ qua", QMessageBox.RejectRole)
            # Hiển thị hộp thoại và đợi người dùng tương tác
            if msg.clickedButton() == retry_btn:
                print("Thử lại")
                # Call lại lần nữa
            elif msg.clickedButton() == reject_btn:
                print("Bỏ qua")

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
