import os
from sys import platform
from utils.Helper import Helper


class upr_lib:
    execcmd=""
    def __init__(self):
        data = Helper.GetSettingData()
        if data is None:
            return
        self.InitData(data)
        self.upr = data["upr"]
        self.packagename = data["packageName"]

    def InitData(self, data):
        path = Helper.GetRootPath()
        if platform.startswith("win"):
            execcmd = data["win"]["execcmd"]
            self.adbpath = data["win"]["adbpath"]
        else:
            execcmd = data["ios"]["execcmd"]
            self.adbpath = data["ios"]["adbpath"]

        execcmd = path + self.execcmd
        self.adbpath = path + self.adbpath

    def start(self, sessionId):
        cmd = self.execcmd + '-p {0} -s {1} -n {2} -adb={3} '.format("127.0.0.1", sessionId, self.packagename,
                                                                     self.adbpath)
        print(cmd)
        res = os.popen(cmd)

    @staticmethod
    def cap_object():
        cmd = upr_lib.execcmd + "--c"
        res = os.popen(cmd)

    @staticmethod
    def cap_tag():
        cmd = upr_lib.execcmd + "--t"
        res = os.popen(cmd)

    @staticmethod
    def cap_memory():
        cmd = upr_lib.execcmd + "--m"
        res = os.popen(cmd)

    @staticmethod
    def stop():
        cmd = upr_lib.execcmd + "--stop"
        res = os.popen(cmd)
