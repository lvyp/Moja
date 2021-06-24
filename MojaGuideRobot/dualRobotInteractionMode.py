# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : dualRobotInteractionMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger
from playsound import playsound

TTS_BY_COMMUNICATION_PATH = "./TtsRecording/dualRobotCommunication/"


def PlayVoice(path):
    # print(path)
    playJudge = playsound(path, True)  # 设置为True需要同步进行。否则录音时会将播放的应该回复录入
    if playJudge is False:
        logger.info("音频格式不正确，无法播放！！\n")
    else:
        logger.info("对话应答已回复！！\n")


def switch_if():
    if globalVariable.get_position("positionA"):
        logger.info("到达位置A")
        PlayVoice(TTS_BY_COMMUNICATION_PATH + "Communication_hug.mp3")
        PlayVoice(TTS_BY_COMMUNICATION_PATH + "Communication_iSeeYouLikeHug.mp3")
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
