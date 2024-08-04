'''
Usage: python -m src.main
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray, QTimer
from .define import *
from .apis import *
import json

'''
TODO
[ ] Thêm trạng thái 4G và GPS.
[x] Hiển thị trạng thái call API.
[ ] Check và restart service 4G và GPS trong Setting.
[x] Nút getMapImage thủ công trong Setting.
[ ] Hiển thị log
[ ] Đơn vị thực hiện - SETTING
'''

example_lat = 21.046242
example_lng = 105.787002

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(f"{exception}")
    msgBox.setWindowTitle(f"Lỗi nghiêm trọng")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

class MAIN(QMainWindow):
    IMG_W   = 840
    IMG_H   = 470
    MAP_W   = 290
    MAP_H   = 470
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('assets/icon.png'))
        loadUi(MAIN_UI_PATH, self)
        self.connectSignalsSlots()
        self.speedLimit     = 0

    def loadConfigs(self):
        with open(CONFIGS_PATH) as fd:
            self.configs_data = json.load(fd)
    
    def saveConfigs(self):
        with open(CONFIGS_PATH,'w+',encoding='utf-8') as fd:
            fd.write(json.dumps(self.configs_data,indent=4,ensure_ascii=False))

    def setEventOneSec(self):
        # creating a timer object
        self.timer = QTimer(self)
        # adding action to timer
        self.timer.timeout.connect(self.oneSecTask)
        # update the timer every second
        self.timer.start(1000)

    def oneSecTask(self):
        # @TODO: kiểm tra trạng thái GPS

        # @TODO: kiểm tra trạng thái 4G

        pass

    def popup(self, typeMsg: str, title: str, content: str, hint: str):
        msg = QMessageBox()
        if (typeMsg == 'warn'):
            msg.setIcon(QMessageBox.Warning)
        elif (typeMsg == 'error'):
            msg.setIcon(QMessageBox.Critical)
        else:
            msg.setIcon(QMessageBox.Information)
        msg.setText(content)
        msg.setInformativeText(hint)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def connectSignalsSlots(self):
        self.viewSnapshoot(EXAMPLE_IMG_PATH)
        self.viewMap(EXAMPLE_MAP_PATH)
        self.loadConfigs()
        self.loadSetting()
        self.setTextEdit(self.te_speedLimit,'0','red')
        self.loadDefaultDisplay()
        self.btn_getMap.clicked.connect(self.hdl_getMapManual)
        self.te_deviceID.textChanged.connect(self.hdl_changed_deviceID)
        self.btn_checkService.clicked.connect(self.hdl_checkService)
        self.btn_restart4GService.clicked.connect(self.hdl_restart4GService)
        self.btn_restartGpsService.clicked.connect(self.hdl_restartGpsService)
        resp = getMapImage(self.configs_data['deviceID'], example_lat, example_lng, getDate())

        if (resp != None):
            self.speedLimit = resp['speed_limit']
            self.setTextEdit(self.te_speedLimit,f'{self.speedLimit}','green')
        else:
            self.popup('warn',"Lỗi","Lấy ảnh bản đồ thất bại !","Vui lòng thử lại thủ công ở mục Cài đặt")

    # =============================== MÀN HOME
    def setTextEdit(self, TE_Obj, content: str, color: str):
        font = QFont("Arial", 24)
        if (color == 'green'):
            color = 'rgb(0, 255, 0)'
        elif (color == 'red'):
            color = 'rgb(255, 0, 0)'
        elif (color == 'orange'):
            color = 'rgb(255, 140, 0)'
        else:
            color = 'rgb(255, 255, 255)'
        TE_Obj.setStyleSheet(f"background-color: {color};")
        TE_Obj.setText(content)
        TE_Obj.setAlignment(Qt.AlignCenter)
        TE_Obj.setFont(font)

    def loadDefaultDisplay(self):
        self.setTextEdit(self.te_vehicle,"Ô TÔ", None)
        self.setTextEdit(self.te_licensePlate,"51B-25121", None)
        self.setTextEdit(self.te_speed,"71", None)

    def displayDataFromCamera(self, vehicle: str, license_plate: str, speed: int):
        self.setTextEdit(self.te_vehicle,vehicle, None)
        self.setTextEdit(self.te_licensePlate,license_plate, None)
        self.setTextEdit(self.te_speed,f"{speed}", None)

    def viewSnapshoot(self, img_path):
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(MAIN.IMG_W, MAIN.IMG_H, Qt.KeepAspectRatio)
        self.lbl_display.setPixmap(pixmap)
        self.lbl_display.resize(MAIN.IMG_W, MAIN.IMG_H)
        self.show()

    def viewMap(self, img_path):
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(MAIN.MAP_W, MAIN.MAP_H, Qt.KeepAspectRatio)  # zoom 2x
        self.lbl_map.setPixmap(pixmap)
        self.lbl_map.resize(MAIN.MAP_W, MAIN.MAP_H)
        self.show()

    def viewNoSnapShoot(self):
        pixmap = QPixmap(NULL_IMG_PATH)
        pixmap = pixmap.scaled(MAIN.W_DISP, MAIN.H_DISP, Qt.KeepAspectRatio)
        self.lbl_display.setPixmap(pixmap)
        self.lbl_display.resize(MAIN.W_DISP, MAIN.H_DISP)
        self.show()
    # =============================== HẾT MÀN HOME

    # =============================== MÀN SETTING
    def hdl_getMapManual(self):
        self.loadConfigs()
        resp = getMapImage(self.configs_data['deviceID'], example_lat, example_lng, getDate())
        if (resp != None):
            self.speedLimit = resp['speed_limit']
            self.popup(None,"Thành công","Lấy ảnh bản đồ thành công !","")
        else:
            self.popup('warn',"Lỗi","Lấy ảnh bản đồ thất bại !","Vui lòng kiểm tra kết nối 4G và kế hoạch tuần tra.")
    
    def loadSetting(self):
        self.loadConfigs()
        self.te_deviceID.setText(self.configs_data['deviceID'])

    def hdl_changed_deviceID(self):
        self.loadConfigs()
        self.configs_data['deviceID'] = self.te_deviceID.toPlainText()
        self.saveConfigs()

    def hdl_checkService(self):
        pass

    def hdl_restart4GService(self):
        pass

    def hdl_restartGpsService(self):
        pass


    # =============================== HẾT MÀN SETTING

if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    win = MAIN()
    win.show()
    sys.exit(app.exec())
