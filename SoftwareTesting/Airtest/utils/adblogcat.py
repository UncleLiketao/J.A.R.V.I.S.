import os
import signal
import subprocess
import threading
import time

from utils.Helper import Helper
from utils.LogHelper import LogHelper


class adblogcat():
    def __init__(self):
        self.rs = None
        self.bStart = False
        self.list = []

    def startlog(self, a):
        adbPath = Helper.GetAdbPath()
        cmd = "logcat -s Unity "
        localtime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        self.fileName = LogHelper.GetDirectoyPath() + str(localtime) + ".log"
        cmd = adbPath + cmd
        self.rs = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while self.rs.poll() is None:
            if self.rs.stdout is not None:
                try:
                    line = self.rs.stdout.readline()
                    if line:
                        self.decodeLog(line)
                except Exception as e:
                    pass

    def InitLog(self):
        adbPath = Helper.GetAdbPath()
        cmd2 = adbPath + "logcat -c"
        subprocess.Popen(cmd2, shell=True)
        self._thread = threading.Thread(target=self.startlog, args=(cmd2,))
        self._thread.start()

    def endAdbLog(self):
        pass

    def ReadAdblogcatData(self, line):
        with open(self.fileName, "a+", encoding='gbk', errors='ignore') as f:
            f.write(line)

    def decodeLog(self, msg):
        if msg is None:
            return
        self.ReadAdblogcatData(msg)
        pos = msg.find("Unity")
        if pos > 0:
            strcnt = len(msg) - pos - 10
            if strcnt > 5:
                level = msg[pos - 2:pos - 1]
                msg = msg[pos + 10:len(msg)]
                self.FormatColor(msg, level)

    def FormatColor(self, msg, level):
        if level == 'I' or level == 'D':
            #LogHelper.out_log("", msg)
            return
        if level == 'W':  # 黄色
            msg = ("<font color='green'>{0}<font>".format(msg))
        else :
            msg = ("<font color='red'> {0}<font>".format(msg))

        LogHelper.out_error(msg)

    def OpenLogcatFile(self):
        flag = os.path.exists(self.fileName)
        if flag:
            os.startfile(self.fileName)
