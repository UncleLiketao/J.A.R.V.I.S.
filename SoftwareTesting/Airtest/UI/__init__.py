import argparse

from utils.Helper import Helper
from plugin.airtest_case import airtest_case
from utils.LogHelper import LogHelper
from utils.adblogcat import adblogcat


class ui():
    def __init__(self):
        self.air = None
        self.adblogcat = None
        LogHelper.InitLog()
        self.air = airtest_case()
        self.adblogcat = adblogcat()
        self.adblogcat.InitLog()

    def Run(self):
        data = Helper.GetData()
        from .testMainui import ShowtestMainUI
        ShowtestMainUI(self, data)
        # parser = argparse.ArgumentParser()
        # self.ArgumentParser(parser)
        # args = parser.parse_args()
        # argv = Helper.GetData()
        # if j:
        #     from plugin.start import RunStart
        #    RunStart(argv)
        # else:
        #    from .testMainui import ShowtestMainUI
        #    ShowtestMainUI(self)

    def RunGame(self, argv):
        from plugin.start import RunStart
        RunStart(argv, self)

    def StartGame(self, android):
        from plugin.start import start
        start().start(android)

    def StopGame(self):
        from plugin.start import start
        start().stop()

    def StopTest(self):
        if self.air is not None:
            self.air.stopTest()
        if self.air is not None:
            self.adblogcat.endAdbLog()

    def StartAbdlog(self):
        self.adblogcat = adblogcat()
        self.adblogcat.InitLog()

    def OpenAdbLog(self):
        if self.adblogcat:
            self.adblogcat.OpenLogcatFile()

    def ArgumentParser(self, parse):
        pass
