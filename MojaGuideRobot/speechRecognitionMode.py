# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : speechRecognitionMode.py
# @Software: PyCharm

import ctypes
import threading

import win32api

import globalVariable
from loggerMode import logger
from ctypes import *


def micGenerateRocord():
    pass


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
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        # 判断是否被唤醒
        cppDll = CDLL("awaken_sample")
        cppDll.CFunction.restype = ctypes.c_uint64  # 修改lib.bar返回类型
        returnValue = str(cppDll.CFunction())
        win32api.FreeLibrary(cppDll._handle)  # 释放DLL资源否则线程再次运行会直接返回上次结果
        if returnValue == "202":
            logger.info("唤醒成功！！\n")
            # 进行麦克风收音，生成音频文件
            micGenerateRocord()
            # 将音频发送给百度云进行ASR解析

            # 将ASR识别结果发送给NLU进行自然语言处理

            # 根据NLU返回的intent和slot进行判断控制相应的线程

        elif returnValue == "201":
            logger.info("登录失败！！\n")


        globalVariable.set_value("actionFlag", True)
        globalVariable.set_value("mapRouteSettingFlag", True)
        event.set()
        rLock.release()
