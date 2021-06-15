# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : speechRecognitionMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger


def speechRecognitionMode():
    # 语音识别模块:
    # 1.获取麦克风数据生成音频文件
    # 2.将音频文件推送到百度云，获取ASR、NLU以及TTS音频
    # 3.播放TTS音频并解析NLU，根据相应的意图与槽值发送指令给相应模块
    logger.info("语音识别模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        rLock.acquire()
        logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        globalVariable.set_value("actionFlag", True)
        event.set()
        rLock.release()
