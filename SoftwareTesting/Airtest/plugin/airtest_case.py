import importlib
import os
import sys
import time
from argparse import Namespace

from airtest.cli.runner import run_script, AirtestCase
from airtest.core.helper import using
from airtest.utils.compat import script_dir_name
from pocounit import run, PocoTestSuite

from utils.Helper import Helper
from utils.LogHelper import LogHelper


class airtest_case:
    def __init__(self):
        self.rs = None
        self.rep = False #终止

    def Run(self, argv):
        self.rep = False
        self.argv = argv
        Helper.InitBase(self.argv)
        self.RunAir()

    def RunAir(self):
        num = self.argv["repeat"]
        self.ImportDir()
        self.RunAirtest(num, self.argv["Air"])
        if self.argv["after"]:
            num = self.argv["afterNum"]
            # 正常跑
            self.argv["connect"] = False
            Helper.UpdateConnect()
            self.RunAirtest(num, self.argv["Air"])

    def ImportDir(self):
        path = self.argv["Directoy"]
        if self.argv["test"]:
            path, fileName = script_dir_name(path)
        sys.path.append(path)

    def RunAirtest(self, num, air):
        if self.rep:
            return
        self.exten = ".py"
        if air:
            self.exten = '.air'
            self.airtest = Helper.GetAirtestPath()

        # 重启循环
        if self.argv["repeatType"] == 0:
            if not self.argv["test"]:
                if not air:
                    self.run_singleAir("a_BC2UI_0.py", 0)
                self.run_air(air, 1)
            else:
                self.run_singleAir(self.argv["FileName"])
        else:
            # 整个文件夹
            if not self.argv["test"]:
                if not air:
                    self.run_singleAir("a_BC2UI_0.py", 0)

                for i in range(0, num):
                    self.run_air(air, i)
            else:  # 单文件
                for i in range(0, num):
                    self.run_singleAir(self.argv["FileName"], i)

    def run_air(self, air, pos):
        diros = os.listdir(self.argv["Directoy"])
        diros.sort()
        for f in diros:
            # 保证任意一个文件报错也能继续执行下一个
            if f.startswith('BC') and f.endswith(self.exten):
                try:
                    self.run_singleAir(f, pos)
                except Exception as e:
                    LogHelper.out_log("", str(e))

    # 执行air文件
    def run_singleAir(self, f, pos=1):
        if self.rep:
            return
        portName = f.replace(self.exten, '')
        self.beforeRun(portName)
        self.callCommand(portName, f, pos)
        self.afterRun()

    def callCommand(self, portName, f, idx):
        if "Directoy" in self.argv:
            if self.argv["repeatType"] == 2 or self.argv["test"]:
                cmd = f
            else:
                cmd = self.argv["Directoy"] + "/" + f
        else:
            cmd = f

        LogHelper.out_log("Run_", f)
        try:
            path, fileName = script_dir_name(portName)
            if self.exten == ".air":
                logfile = "log/" + fileName
                recordingname = portName + "_" + str(idx) + ".mp4"
                args = Namespace(device=self.argv["android"], compress=None, no_image=True, log=logfile,
                                         recording=recordingname, script=f, language="zh")
                run_script(args, AirtestCase)
            else:
                cmd = 'python ' + cmd
                #self.rs = psutil.Popen(cmd, stdout=open("process.out", "w+"), text=True)
                #self.rs.wait()
                module = importlib.import_module(fileName)
                api_class = getattr(module, fileName)
                suit = PocoTestSuite([api_class()])
                run(suit)

        except Exception as e:
            pass

    def beforeRun(self, f):
        # 需要重连
        self.capupr()


    def afterRun(self):
        self.error_report()
        self.capupr()

    # upr截图
    def capupr(self):
        if self.argv["Upr"]:
            from .unityupr import Capupr
            Capupr()
            time.sleep(10)

    # 错误信息
    def error_report(self):
        if not self.argv["Poco"]:
            return
        from utils.unityPocoHelper import unityError
        msg = unityError().GetErrorMsg()
        if msg is None:
            return
        x = msg.split("$")
        for i in x:
            LogHelper.out_error(i)

    def stopTest(self):
        if self.rs is None:
            return
        if self.rs.is_running():
            self.rs.kill()
            self.rs = None
        self.rep = True
