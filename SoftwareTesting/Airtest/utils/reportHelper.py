import sys
import time
import json
import requests
from plugin.unityupr import unityupr
from utils.LogHelper import LogHelper
from utils.Helper import Helper
from prettytable import PrettyTable
from utils.chatPostHelper import chatPostHelper


# 测试结果报告
class ReportHelper(unityupr):

    def RunReport(self):
        sessionid = self.onReadSessionID()
        self.GetSessionReports(sessionid)

    # ------------------------解析json--------------------------------------
    @staticmethod
    def DecodeJson(res, key, count=1):
        index = 0
        data = ""
        if type(res) is dict:
            for (k_1, v_1) in res.items():
                data += ReportHelper.DecodeJson(v_1, k_1, count)
        elif type(res) is list:
            for item in res:
                if index < 10:
                    data += "{\n" + ReportHelper.DecodeJson(item, key, count) + "},\n"
                    index += 1
                else:
                    break
        else:
            if isinstance(res, int):
                res = res / count
            data += "\t" + key + ":" + str(res) + "\n"
        return data

    @staticmethod
    def OverViewCpuText(res):
        data = "\n AverageFrameRate:" + str(res["AverageFrameRate"]) + "ms" + \
               "\n FrameTimeMean:" + str(res["FrameTimeMean"] / 1000) + "ms" + \
               "\n PhysicsTimeMean:" + str(res["PhysicsTimeMean"] / 1000) + "ms" + \
               "\n RendingTimeMean:" + str(res["RendingTimeMean"] / 1000) + "ms" + \
               "\n ScriptTimeMean:" + str(res["ScriptTimeMean"] / 1000) + "ms\n"
        return data

    @staticmethod
    def ReportMsg(res, sessionid):
        temp = json.loads(res.text)
        url = 'https://upr.unity.com/report/%s#summaryHome' % sessionid
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        isSuc = False
        repMsg = 'UPR报告链接： %s' % url
        if "Score" in temp.keys():
            isSuc = True
            repMsg = localtime + \
                     '\n测试评分：%s' % temp["Score"] + \
                     '\n平均帧率：%.2f' % round(temp["OverviewAndCPUPerformance"]["AverageFrameRate"], 2) + \
                     '\n【CPU性能占用均值】' + \
                     '\nFrameTime 耗时有效帧均值(ms): %.2f' % round(temp["OverviewAndCPUPerformance"]["FrameTimeMean"] / 1000,
                                                             2) + \
                     '\nPhysicsTime 耗时有效帧均值(ms): %.2f' % round(
                temp["OverviewAndCPUPerformance"]["PhysicsTimeMean"] / 1000,
                2) + \
                     '\nRenderingTime 耗时有效帧均值(ms): %.2f' % round(
                temp["OverviewAndCPUPerformance"]["RendingTimeMean"] / 1000, 2) + \
                     '\nScriptTime 耗时有效帧均值(ms): %.2f' % round(
                temp["OverviewAndCPUPerformance"]["ScriptTimeMean"] / 1000,
                2) + \
                     '\n【内存占用】' + \
                     '\nReservedUnity峰值(MB)：%.2f' % round(temp["MemoryUsage"]["ReservedUnityPeak"] / 1000000, 2) + \
                     '\nReservedGFX峰值(MB): %.2f' % round(temp["MemoryUsage"]["ReservedGFXPeak"] / 1000000, 2) + \
                     '\nReservedUnity峰值(MB)：%.2f' % round(temp["MemoryUsage"]["ReservedUnityPeak"] / 1000000, 2) + \
                     '\nReservedGFX峰值(MB): %.2f' % round(temp["MemoryUsage"]["ReservedGFXPeak"] / 1000000, 2) + \
                     '\n【资源】' + \
                     '\n纹理资源峰值MB: %.2f' % round(temp["ResourceDetails"]["TexturesSizePeak"] / 1000000, 2) + \
                     '\nMaterialsCount峰值(个): %s' % temp["ResourceDetails"]["MaterialCountPeak"] + \
                     '\n动画资源峰值MB:  %.2f' % round(temp["ResourceDetails"]["AnimationClipsSizePeak"] / 1000000, 2) + \
                     '\n音频资源峰值MB: %.2f' % round(temp["ResourceDetails"]["AudioClipsCountPeak"] / 1000000, 2) + \
                     '\n网格资源峰值MB: %.2f' % round(temp["ResourceDetails"]["MeshesSizePeak"] / 1000000, 2) + \
                     '\n【图形】' + \
                     '\nCamera.Render 耗时有效帧均值(ms): %.2f' % round(
                temp["CPUDetails"]["CameraRenderAverageTimeConsumption"] / 1000, 2) + \
                     '\nSetPassCalls峰值(次): %s' % temp["GraphicOverviewAndGraphicBatching"]["SetPassCallsPeak"] + \
                     '\nSetPassCalls有效帧均值(次): %s' % temp["GraphicOverviewAndGraphicBatching"]["SetPassCallsMean"] + \
                     '\nDrawCall峰值: %s' % temp["GraphicOverviewAndGraphicBatching"]["DrawCallsPeak"] + \
                     '\nDrawCalls有效帧均值(次): %s' % temp["GraphicOverviewAndGraphicBatching"]["DrawCallsMean"] + \
                     '\nDynamicBatched Saved有效帧均值(次)：%.1f' % round(
                temp["GraphicOverviewAndGraphicBatching"]["DynamicBatchedSavedMean"], 1) + \
                     '\nStaticBatched Saved有效帧均值(次): %.1f' % round(
                temp["GraphicOverviewAndGraphicBatching"]["StaticBatchedSavedMean"], 1) + \
                     '\n【CPU详情】' + \
                     '\nGameObject.Activate Call次数: %.2f' % round(temp["CPUDetails"]["GameObjectActivateTotalTimes"],
                                                                  2) + \
                     '\nGameObject.Deactive Call次数 : %.2f' % temp["CPUDetails"]["GameObjectDeactiveTotalTimes"] + \
                     '\nDestroy Call次数: %.2f' % round(temp["CPUDetails"]["DestroyTotalTimes"], 2) + \
                     '\nInstantiate Call总次数: %.2f' % round(temp["CPUDetails"]["InstantiateTotalTimes"], 2) + \
                     '\nUPR报告链接： %s' % url
        return repMsg, isSuc

    @staticmethod
    def DecodeJsonText(res):
        temp = json.loads(res.text)
        data = ""
        for (k_1, v_1) in temp.items():
            data += k_1 + ":"
            if k_1 != "Score":
                data += "\n{"
                if k_1 == "MemoryUsage":
                    data += ReportHelper.DecodeJson(v_1, k_1, 1000000)
                elif k_1 == "OverviewAndCPUPerformance":
                    data += ReportHelper.OverViewCpuText(v_1)
                elif k_1 == "CPUDetails":
                    data += ReportHelper.DecodeJson(v_1, k_1, 1000)
                else:
                    data += ReportHelper.DecodeJson(v_1, k_1)
                data += "},\n"
            else:
                data += v_1 + "\n"
        return data

    # 与上一次的比较结果，这个的检测结果
    @staticmethod
    def CompareSessionWarning(res, nowRes):
        temp = json.loads(res.text)
        now = json.loads(nowRes.text)
        config = Helper.ReadConfig("lib/utils/uprConfig.json")
        data = ""
        confDetail = config["UPRDetail"]
        confDesc = config["UPRDesc"]
        anywarnning = False
        table = PrettyTable(['模块', '当前', '比较结果'])
        if "Score" in temp.keys():
            for (k_1, v_1) in confDetail.items():
                if type(v_1) is dict:
                    for (k_2, v_2) in v_1.items():
                        frt = temp[k_1][k_2]
                        if abs(frt) > v_2:
                            nowValue = now[k_1][k_2]
                            val = confDesc[k_1][k_2]
                            k_2_1 = k_2 + "_Attr"
                            if k_2_1 in confDesc[k_1].keys():
                                val_1 = confDesc[k_1][k_2_1]
                                nowValue = int(nowValue / val_1)
                                frt = int(frt / val_1)
                                v_2 = int(v_2 / val_1)
                            table.add_row([val, nowValue, frt])
                            anywarnning = True
        return table, anywarnning

    # upr测试结果
    def GetSessionReports(self, sessionsid):
        API_ENDPOINT = self.upr["API_ENDPOINT"]
        url = "%s/sessions/%s/report" % (API_ENDPOINT, sessionsid)
        respone = requests.get(url, auth=self.AUTH)
        msg, isSuc = ReportHelper.ReportMsg(respone, sessionsid)
        if not isSuc:
            time.sleep(30)
            self.RunReport()
            return
        LogHelper.out_log("本次Upr测试结果:\n", msg)
        # 与上一次比较结果
        url = "%s/sessions/%s/compare-reports" % (API_ENDPOINT, sessionsid)
        resp = requests.post(url, auth=self.AUTH)
        comWmsg, anywarnning = ReportHelper.CompareSessionWarning(resp, respone)
        if anywarnning is True:
            LogHelper.out_log("有差异:\n", comWmsg)
            msg = msg + "\n与上一次比较结果:\n" + str(comWmsg)
        Send_Channel = Helper.GetSettingData()["Send_Channel"]
        chatPostHelper.PostMessageChannel(msg, Send_Channel, "自动测试结果")

    def onReadSessionID(self):
        path = Helper.GetRootPath() + self.upr["SessionPath"]
        with open(path, 'r+') as f:  # 打开文件
            line = f.readline()
            return line


def SendReport():
    ReportHelper().RunReport()
