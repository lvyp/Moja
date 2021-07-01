# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : dualRobotInteractionMode.py
# @Software: PyCharm
import math
import time
import datetime
import json
import threading
import globalVariable
from loggerMode import logger
from playsound import playsound

TTS_BY_COMMUNICATION_PATH = "./TtsRecording/dualRobotCommunication/"
TTS_BY_XIANGSHENG_PATH = "./TtsRecording/xiangsheng/"


def PlayVoice(path):
    # print(path)
    playJudge = playsound(path, False)  # 设置为True需要同步进行。否则录音时会将播放的应该回复录入
    if playJudge is False:
        logger.info("音频格式不正确，无法播放！！\n")
    else:
        logger.info("对话应答已回复！！\n")


def timerMachine(startTime=0.000):
    dt_ms = datetime.datetime.now().strftime('%M:%S.%f')
    m, s = dt_ms.strip().split(":")
    s = float(m) + float(s)
    return float('%.3f' % (s - startTime))


def parsePlot(jsonPath):
    with open(jsonPath, "r") as f:
        poltDict = json.load(f)
        plotList = poltDict["MoJa"]
        f.close()

    startTime = timerMachine()
    # 获取列表中所有字典数据
    for plot in plotList:
        # 判断字典数据时间点
        tempDict = {"time": plot["time"],
                    "sub_time_child": plot["sub_time_child"],
                    "sub_time_old": plot["sub_time_old"]}
        timeFlag = 0
        childTimeFlag = 0
        oldTimeFlag = 0
        print(plot["dialogue"])
        while True:
            currentTime = timerMachine(startTime)

            if plot["sub_time_child"] == 0 and childTimeFlag == 0:
                childTimeFlag += 1
                del tempDict["sub_time_child"]
            if plot["sub_time_old"] == 0 and oldTimeFlag == 0:
                oldTimeFlag += 1
                del tempDict["sub_time_old"]

            # print(currentTime)
            if math.isclose(plot["time"], currentTime, abs_tol=0.010) and timeFlag == 0:
            # if plot["time"] == currentTime:
                timeFlag += 1
                del tempDict["time"]
                if plot["dialogue"] != "":
                    PlayVoice(TTS_BY_XIANGSHENG_PATH + plot["dialogue"])
            if math.isclose(plot["sub_time_child"], currentTime, abs_tol=0.010) and childTimeFlag == 0:
            # if plot["sub_time_child"] == currentTime and childTimeFlag == 0:
                childTimeFlag += 1
                del tempDict["sub_time_child"]
                if plot["action_child"] != "":
                    print("action_child")
            if math.isclose(plot["sub_time_old"], currentTime, abs_tol=0.010) and oldTimeFlag == 0:
            # if plot["sub_time_old"] == currentTime and oldTimeFlag == 0:
                oldTimeFlag += 1
                del tempDict["sub_time_old"]
                if plot["action_old"] != "":
                    print("action_old")

            if len(tempDict) == 0:
                print("len(tempDict): " + str(len(tempDict)))
                break
            else:
                print(currentTime)
                print(tempDict)



def switch_if():
    if globalVariable.get_position("positionA"):
        logger.info("到达位置A")
        parsePlot("Plot1.json")
        # PlayVoice(TTS_BY_COMMUNICATION_PATH + "Communication_hug.mp3")
        # PlayVoice(TTS_BY_COMMUNICATION_PATH + "Communication_iSeeYouLikeHug.mp3")
        globalVariable.set_position("positionA", False)
        if globalVariable.get_position_list_len() > 0:
            globalVariable.set_value("mapRouteSettingFlag", True)
        else:
            pass
    elif globalVariable.get_position("positionB"):
        logger.info("到达位置B")
        globalVariable.set_position("positionB", False)
        pass
    elif globalVariable.get_position("positionC"):
        logger.info("到达位置C")
        globalVariable.set_position("positionC", False)
        pass
    elif globalVariable.get_position("positionD"):
        logger.info("到达位置D")
        globalVariable.set_position("positionD", False)
        pass
    else:
        pass


def dualRobotInteractionMode():
    # 双机器人互动模块：设置对话情景，根据机器人对话情景，发送相应的指令到动作模块
    logger.info("双机器人互动模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        # 代码实现部分
        switch_if()
        # 代码实现部分
        rLock.release()
        event.clear()
