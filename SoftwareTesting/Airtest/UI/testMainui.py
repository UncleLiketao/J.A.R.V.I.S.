import subprocess
import sys
import threading
import os

from airtest.core.api import *

from UI.Ui_widget import Ui_widget
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QApplication

from utils.Helper import Helper
from utils.LogHelper import LogHelper


class testMainUI(Ui_widget, QtWidgets.QWidget):
    LogTrigger = pyqtSignal(str, str)

    def __init__(self):
        super(testMainUI, self).__init__()
        self.setupUi(self)
        self.argv = {"android": "Android:///"}
        self.InitUI()
        self.running = False

    def Run(self, master, data):
        self.data = data
        self.master = master
        self.LogTrigger.connect(self.PostLogMsg)
        LogHelper.AddFunctionHandler(self.LogTrigger.emit)
        self.InitUIData()
        self.show()

    def InitUIData(self):
        self.FileTextBrowser.append(self.data["Directoy"])
        self.spinBox.setValue(self.data["repeat"])
        self.comboBox.setCurrentIndex(self.data["repeatType"])
        # self.radioButton_6.setChecked(self.data["test"])
        self.checkBox_5.setChecked(self.data["after"])
        self.argv["after"] = self.checkBox_5.isChecked()
        self.spinBox_2.setValue(self.data["afterNum"])

    def InitUI(self):
        self.BtnEvent()
        self.ComboxEvent()

    # 测试按钮
    def BtnEvent(self):
        # 开始测试
        self.pushButton.clicked.connect(self.RunTestEvent)
        self.pushButton_9.clicked.connect(self.StopTest)
        self.pushButton_9.setVisible(False)
        # 选择文件
        self.pushButton_2.clicked.connect(self.SelectFiles)
        # 默认选中
        self.radioButton.setChecked(True)
        # wifi
        self.pushButton_5.clicked.connect(lambda: self.OpenWifi(False))
        self.pushButton_6.clicked.connect(lambda: self.OpenWifi(True))
        # 启动游戏
        self.pushButton_4.clicked.connect(lambda: self.StartGame(True))
        self.pushButton_3.clicked.connect(lambda: self.StartGame(False))
        # 安装游戏
        self.pushButton_8.clicked.connect(lambda: self.InstallGame())
        self.pushButton_7.clicked.connect(lambda: self.LinkDevice())
        # 日志
        self.adblog.clicked.connect(lambda: self.OpenLogFile())
        self.inputlog.setVisible(False)
        #self.inputlog.clicked.connect(lambda: self.InputLog())

    def SelectFiles(self):
        file = None
        test = self.radioButton_6.isChecked()
        if not test or self.radioButton.isChecked():
            file = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
            self.argv["Directoy"] = file
        else:
            file, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*)")
            self.argv["FileName"] = file
        self.FileTextBrowser.clear()
        self.FileTextBrowser.append(file)

    def OpenWifi(self, bOpen):
        if bOpen:
            cmd = " shell svc wifi enable"
        else:
            cmd = " shell svc wifi disable"
        adbPath = Helper.GetAdbPath()
        cmd = adbPath + cmd
        return subprocess.call(cmd, shell=True) == 0

    def StartGame(self, bOpen):
        if bOpen:
            t = threading.Thread(target=self.OnThreadStartGame, args=(self.argv["android"],))
            t.start()
        else:
            self.StopTest()
            self.master.StopGame()

    def OnThreadStartGame(self, v):
        self.master.StartGame(v)

    def InstallGame(self):
        t = threading.Thread(target=self.OnThreadInstallGame, args=(self.argv["android"],))
        t.start()

    def OnThreadInstallGame(self, v):
        file = self.PkgFile.toPlainText()
        if len(file) < 1:
            return
        idx = self.comboBox_2.currentIndex()
        id = self.deviceId[idx]
        self.argv["android"] = "Android:///" + id
        # 连接设备
        connect_device(self.argv["android"])
        self.CheckApp()
        # 安装
        install(file)

    def CheckApp(self):
        bFind = False
        pkg = Helper.GetPackageName()
        try:
            bFind = device().check_app(pkg)
        except:
            pass
        if bFind:
            # 卸载
            uninstall(pkg)

    def LinkDevice(self):
        # 获取连接设备
        order = Helper.GetAdbPath() + ' devices -l'
        pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
        dev = pi.stdout.read().decode()
        devs = dev.split("\r\n")
        self.deviceId = []
        self.deviceName = []
        for i in range(1, len(devs)):
            dev = devs[i]
            if len(dev) < 1:
                break
            t1 = dev.find("model:")
            t2 = dev.find("device:")
            t3 = dev.find("device")
            if t1 > 0:
                if t2 > 0:
                    d = dev[t1 + 6:t2]
                else:
                    d = dev[t1 + 6:len(dev)]
                self.deviceName.append(d)
            id = dev[0:t3].strip()
            self.deviceId.append(id)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.deviceName)
        self.comboBox_2.setCurrentIndex(0)
        self.GetAndroidid()

    def GetAndroidid(self):
        if len(self.deviceId) > 0:
            id = self.comboBox_2.currentIndex()
            self.argv["android"] = "Android:///" + self.deviceId[id]
        else:
            self.argv["android"] = "Android:///"

    # 下拉框
    def ComboxEvent(self):
        self.comboBox.addItems(["重启循环", "不重启循环"])
        self.comboBox.setCurrentIndex(1)

        # 设备数据
        self.LinkDevice()

    # 点击开始测试
    def RunTestEvent(self):
        # 获取循环次数
        self.argv["repeat"] = self.spinBox.value()
        self.argv["repeatType"] = self.comboBox.currentIndex()
        self.argv["Air"] = self.radioButton.isChecked()
        self.argv["Poco"] = self.radioButton_2.isChecked()
        self.argv["Upr"] = self.checkBox.isChecked()
        self.argv["test"] = self.radioButton_6.isChecked()
        # 断线判断
        self.argv["connect"] = self.checkBox_2.isChecked()
        self.argv["wifi"] = self.checkBox_3.isChecked()
        self.argv["home"] = self.checkBox_4.isChecked()
        # 默认连接设备
        if not "Directoy" in self.argv:
            self.argv["Directoy"] = self.FileTextBrowser.toPlainText()
        self.argv["FileName"] = self.FileTextBrowser.toPlainText()
        # 结束后跑流程
        self.argv["after"] = self.checkBox_5.isChecked()
        self.argv["afterNum"] = self.spinBox_2.value()
        self.argv["Upr"] = False
        self.GetAndroidid()

        # 启动线程执行
        if self.running:
            return
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self._thread = threading.Thread(target=self.OnThreadRun, args=(self.argv,))
        self._thread.start()
        self.running = True

    def StopTest(self):
        if self.running:
            self.master.StopTest()
            self.running = False
        self.pushButton.setVisible(True)
        self.pushButton_9.setVisible(False)

    def OnThreadRun(self, argv, ):
        self.pushButton.setVisible(False)
        self.pushButton_9.setVisible(True)
        self.master.RunGame(argv)

    def PostLogMsg(self, msg, type):
        if type == 'ERROR':
            self.textBrowser_2.append(msg)
        else:
            self.textBrowser.append(msg)

    def OpenLogFile(self):
        self.master.OpenAdbLog()


def ShowtestMainUI(master, data):
    app = QApplication(sys.argv)
    ex = testMainUI()
    ex.Run(master, data)
    app.exec_()
