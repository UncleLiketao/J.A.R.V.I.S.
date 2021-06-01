import json

import requests

from .upr_lib import upr_lib
from utils.Helper import Helper


class unityupr(upr_lib):
    AUTH = (
        '',  # 请填写项目的 App ID
        ''  # 请填写项目的 App Secret
    )

    def CreateSession(self):
        # 创建session
        session_request = {
            "ProjectId": self.upr["PROJECT_ID"],
            "SessionName": "bc0",  # 测试名称
            "GameName": "BC",  # 游戏名称
            "GameVersion": "",  # 游戏版本号
            "PackageName": self.packagename,  # 游戏包名
            "UnityVersion": "2019.4",  # Unity版本号
            "screenshotEnabled": True,  # 屏幕截图是否开启
            "screenshotFrequency": 4,  # 屏幕截图频率 (单位秒）
            "frameLockEnabled": False,  # 游戏是否有锁帧
            "frameLockFrequency": 60,  # 游戏锁定帧率
            "enableDeepLua": False,  # 是否开启Lua Profiling代码 (需要搭配UPR Package一起使用）
            "enableDeepMono": False,  # 是否开启Mono C#代码Profiling (需要搭配UPR Package一起使用）
            "monitor": False,  # 是否需要手机UPR App性能数据 （对UPR Desktop无效）
            "ShareReport": False,  # 是否允许Project外的人员通过sessionId直接访问报表
            "gpuprofileEnabled": True,  # 是否开启GPU profiling
            "GCCallStackEnabled": True,
        }
        resp = requests.post('%s/sessions' % self.upr["API_ENDPOINT"], auth=self.AUTH, json=session_request)
        temp = json.loads(resp.text)
        if "SessionId" in temp:
            global SessionId
            SessionId = temp["SessionId"]
            return SessionId
        return SessionId



    # 存储SessionID
    def onSaveSessionID(self, id):
        path = Helper.GetRootPath() + self.upr["SessionPath"]
        with open(path, "w+") as f:
            f.seek(0)
            f.truncate()
            f.write(id)

    # 启动upr
    def startupr(self):
        session = self.CreateSession()
        self.onSaveSessionID(session)
        self.start(session)


def StartUpr():
    upr = unityupr()
    upr.startupr()


def Capupr():
    if Helper.IsOpenUpr():
        upr_lib.cap_memory()
        upr_lib.cap_tag()
        upr_lib.cap_object()


def StopUpr():
    upr_lib.stop()