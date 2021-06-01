
import os,sys,time
import logging
from .Helper import Helper
from logging.handlers import TimedRotatingFileHandler
Log = logging.getLogger("make")


class FunctionLoggerHandler(logging.Handler):
    LEVEL_COLORS = {
        'DEBUG': 'gray',
        'INFO': 'white',
        'WARNING': 'yellow',
        'CRITICAL': 'yellow',
        'ERROR': 'red'
    }
    def __init__(self, func):
        super(FunctionLoggerHandler, self).__init__()
        self._func = func

    def emit(self, record):
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = '[%s]%s' % (localtime, str(record.msg))
        self._func(msg, record.levelname)

class LogHelper:
    # 按日期创建文件
    @staticmethod
    def GetDirectoyPath(filename='log', bLastLog=True):
        if sys.platform.startswith("win"):
            fileYear = Helper.GetRootPath() + "\\" + filename + "\\"
        else:
            fileYear = Helper.GetRootPath() + "/" + filename + "/"
        if not os.path.exists(fileYear):
            os.mkdir(fileYear)
        return fileYear

    # 输出文本
    @staticmethod
    def out_log(a, strval=""):
        strtxt = a + str(strval)
        Log.info(strtxt)

    @staticmethod
    def out_error(e):
        Log.error(str(e))

    @staticmethod
    def InitLog():
        logair = logging.getLogger("airtest")
        logair.setLevel(logging.ERROR)
        path = LogHelper.GetDirectoyPath('log', False)
        logger = Log
        logger.setLevel(logging.DEBUG)
        fmtDate = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[%(asctime)s] %(message)s', fmtDate)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        fmt = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s', fmtDate)
        handler = logging.handlers.RotatingFileHandler(os.path.join(path, 'air_log.log'), mode='w', encoding='utf8')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(fmt)
        logger.addHandler(handler)

    @staticmethod
    def AddFunctionHandler(func):
        logger = Log
        logger.addHandler(FunctionLoggerHandler(func))