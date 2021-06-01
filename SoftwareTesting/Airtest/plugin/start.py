import argparse
import getopt

from airtest.core.api import *
from airtest.core.android.adb import *
from .unityupr import StartUpr, StopUpr
from utils.LogHelper import LogHelper
from utils.Helper import Helper


# 启动游戏
class start():
    def __init__(self):
        super(start, self).__init__()
        self.data = Helper.GetSettingData()
        self.packageName = self.data["packageName"]

    def Run(self, argv, master):
        self.master = master
        connect_device(argv["android"])
        self.argv = argv
        if not self.CheckDevices():
            LogHelper.out_error("没有设备连接或不存在游戏")
            return
        if self.CheckRunType():
            LogHelper.out_error("没有找到测试文件")
            return
        self.Init(argv)

    # 判断设备
    def CheckDevices(self):
        dev = device()
        try:
            return dev.check_app(self.packageName);
        except Exception as e:
            return False

    # 判断运行类型
    def CheckRunType(self):
        if self.argv["FileName"] is None:
            return True
        file = self.argv["FileName"]
        if self.argv["repeatType"] == 2 or self.argv["test"]:
            if not os.path.exists(file):
                return True
            return not self.CheckFiles(file)
        else:
            if ("Directoy" not in self.argv) or len(self.argv["Directoy"]) <= 0:
                return True
            dir = os.listdir(self.argv["Directoy"])
            bFind = False
            for f in dir:
                if self.CheckFiles(f):
                    bFind = True
                    break
        return not bFind

    # 判断文件
    def CheckFiles(self, f):
        bFind = False
        if self.argv["Air"]:
            if f.endswith(".air"):
                bFind = True
        if self.argv["Poco"]:
            if f.endswith(".py"):
                bFind = True
        return bFind

    def Init(self, argv):
        if not self.argv["test"]:
            self.StartGame()
        if self.argv["Upr"]:
            self.StartUpr()
        self.RunGame()
        LogHelper.out_log("End", "Airtest")

    def Repeat(self, argv):
        repeatType = argv["repeatType"]
        # 重启循环
        if repeatType == 0:
            for i in range(1, argv["repeat"]):
                self.RestartGame()

    def RestartGame(self):
        stop_app(self.packageName)
        start_app(self.packageName)
        time.sleep(20)
        self.RunAirTest()

    def start(self, android):
        connect_device(android)
        self.StartGame(False)

    def stop(self):
        if self.CheckDevices():
            stop_app(self.packageName)

    def RunGame(self):
        try:
            self.RunAirTest()
            self.Repeat(self.argv)
        finally:
            if self.argv["Upr"]:
                StopUpr()
                from utils.reportHelper import SendReport
                SendReport()

    def RunAirTest(self):
        self.master.air.Run(self.argv)

    def StartGame(self, bClear=True):
        # 如果游戏在运行停止运行
        stop_app(self.packageName)
        if bClear:
            # 清除游戏信息
            clear_app(self.packageName)
        wake()
        dev = device()
        # 解锁
        dev.unlock()
        # home界面
        home()
        start_app(self.packageName)
        time.sleep(20)

    def StartUpr(self):
        StartUpr()


def RunStart(argv, master):
    s = start()
    s.Run(argv, master)
