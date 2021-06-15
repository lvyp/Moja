# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : main.py
# @Software: PyCharm

import threading
from loggerMode import logger
from speechRecognitionMode import speechRecognitionMode
from actionControlMode import actionControlMode
from dualRobotInteractionMode import dualRobotInteractionMode
from mapRouteSettingMode import mapRouteSettingMode
from remoteControlMode import remoteControlMode
from accessSystemUpdateRegularlyMode import accessSystemUpdateRegularlyMode
import globalVariable

if __name__ == '__main__':
    # 墨甲导览机器人启动入口
    logger.info("墨甲导览机器人启动入口")
    globalVariable._init()
    globalVariable.set_value("actionFlag", False)

    # 设置线程组
    threads = []

    # 创建线程：
    speechRecognition = threading.Thread(target=speechRecognitionMode)
    actionControl = threading.Thread(target=actionControlMode)
    # dualRobotInteraction = threading.Thread(target=dualRobotInteractionMode)
    mapRouteSetting = threading.Thread(target=mapRouteSettingMode)
    speechRecognition.setName("speechRecognition")
    actionControl.setName("actionControl")
    # dualRobotInteraction.setName("dualRobotInteraction")
    mapRouteSetting.setName("mapRouteSetting")

    # remoteControl = threading.Thread(target=remoteControlMode)
    # accessSystemUpdateRegularly = threading.Thread(target=accessSystemUpdateRegularlyMode)
    # remoteControl.setName("remoteControl")
    # accessSystemUpdateRegularly.setName("accessSystemUpdateRegularly")

    # 添加到线程组
    threads.append(speechRecognition)
    threads.append(actionControl)
    threads.append(mapRouteSetting)
    # threads.append(dualRobotInteraction)
    # threads.append(remoteControl)
    # threads.append(accessSystemUpdateRegularly)

    # 开启线程
    for thread in threads:
        thread.start()

    # 线程阻塞
    for thread in threads:
        thread.join()
