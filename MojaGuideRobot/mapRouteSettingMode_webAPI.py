# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : mapRouteSettingMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger
from httpClass import HttpClass

URL = "http://192.168.1.110/cmd/nav"


def mapRouteSettingMode():
    # 地图路线设置模块：发送目的地位置给底层（底盘）
    logger.info("地图路线设置模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        if globalVariable.get_value("mapRouteSettingFlag") is True:
            logger.info("地图设置向模块底层发送数据")
            httpRequest = HttpClass()
            body = globalVariable.get_position_name()
            httpRequest.move_target(body)
            globalVariable.set_value("positionInformationFromChassisFlag", True)
            globalVariable.set_value("mapRouteSettingFlag", False)
        else:
            # logger.info("什么都不做")
            pass
        # 代码实现部分
        # 代码实现部分
        rLock.release()
        event.clear()
