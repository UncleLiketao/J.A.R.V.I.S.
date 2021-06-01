import json
import os
import sys


class Helper:
    """docstring for Helper"""

    # 根目录
    @staticmethod
    def GetRootPath():
        if len(sys.argv) > 1:
            path = os.path.dirname(sys.argv[1])
            if not os.path.exists(path):
                path = os.getcwd()
        else:
            path = os.getcwd()
        return path

    @staticmethod
    def GetFullPath(path):
        return os.path.normpath(os.path.join(Helper.GetRootPath(), path))

    # -------------------------------------------------------------------------------------
    @staticmethod
    def ReadConfig(path):
        if not os.path.exists(path):
            fullpath = Helper.GetFullPath(path)
            if not os.path.exists(fullpath):
                return None

            path = fullpath
        if not os.path.isfile(path):
            return None

        with open(path, 'r', -1, "utf8") as f:
            data = f.read()
            config = json.loads(data)
        return config

    @staticmethod
    def dumpJson(path, val):
        # res = [val]
        if not os.path.exists(path):
            fullpath = Helper.GetFullPath(path)
            if not os.path.exists(fullpath):
                return None

            path = fullpath
        if not os.path.isfile(path):
            return None
        with open(path, 'w', -1, "utf8") as f:
            json.dump(val, f)

    @staticmethod
    def GetSettingData():
        return Helper.ReadConfig("config/setting.json")

    @staticmethod
    def GetData():
        return Helper.ReadConfig("config/data.json")

    @staticmethod
    def GetAdbPath():
        data = Helper.GetSettingData()
        if sys.platform.startswith("win"):
            adbPath = data["win"]["adbpath"]
        else:
            adbPath = data["ios"]["adbpath"]

        return Helper.GetRootPath() + adbPath

    @staticmethod
    def GetAirtestPath():
        data = Helper.GetSettingData()
        if sys.platform.startswith("win"):
            airPath = data["win"]["airtest"]
        else:
            airPath = data["ios"]["airtest"]

        return Helper.GetRootPath() + airPath

    @staticmethod
    def InitBase(argv):
        data = Helper.GetData()
        for i in data.keys():
            data[i] = argv[i]

        if "Directoy" in argv:
            data["Directoy"] = argv["Directoy"]
        else:
            data["Directoy"] = argv["FileName"]
        Helper.dumpJson("config/data.json", data)

    @staticmethod
    def UpdateConnect():
        data = Helper.GetData()
        data["connect"] = False

    @staticmethod
    def GetConnectState():
        data = Helper.GetData()
        return data["connect"]

    @staticmethod
    def GetConnectWifiState():
        data = Helper.GetData()
        v = data["wifi"]
        return v

    @staticmethod
    def GetConnectHomeState():
        data = Helper.GetData()
        return data["home"]

    @staticmethod
    def GetDirectory():
        data = Helper.GetData()
        return data["Directoy"]

    @staticmethod
    def GetPackageName():
        data = Helper.GetSettingData()
        return data["packageName"]

    @staticmethod
    def IsOpenUpr():
        data = Helper.GetData()
        return data["Upr"]