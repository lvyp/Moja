# -*- coding: utf-8 -*-
# @Time : 2021/6/18 16:12
# @Author :
# @Site : Beijing
# @File : positionInformationFromChassisMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger


def positionInformationFromChassisMode():
    # 底盘交互模块：底盘实时交互获取位置信息。到达固定地点则进行剧本表演
    logger.info("底盘交互模块模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        rLock.acquire()
        # 从底层获取当前位置信息
        if globalVariable.get_value("mapRouteSettingFlag") is True:
            globalVariable.set_position("positionA", True)
            logger.info("底盘交互模块底层发送数据")
            globalVariable.set_value("mapRouteSettingFlag", False)
        else:
            # logger.info("什么都不做")
            pass
        # 代码实现部分
        # 代码实现部分
        event.set()
        rLock.release()
