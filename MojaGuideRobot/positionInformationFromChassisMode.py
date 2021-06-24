# -*- coding: utf-8 -*-
# @Time : 2021/6/18 16:12
# @Author :
# @Site : Beijing
# @File : positionInformationFromChassisMode.py
# @Software: PyCharm

import math
import threading
import globalVariable
from loggerMode import logger
from httpClass import HttpClass

URL = "http://192.168.1.110/reeman/pose"


def positionInformationFromChassisMode():
    # 底盘交互模块：底盘实时交互获取位置信息。到达固定地点则进行剧本表演
    logger.info("底盘交互模块模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        rLock.acquire()
        # 从底层获取当前位置信息
        if globalVariable.get_value("positionInformationFromChassisFlag") is True:
            #logger.info("底盘交互模块底层发送数据：实时获取位置信息")
            httpRequest = HttpClass()
            x, y, theta = httpRequest.get_pose()
            webSetPosition = globalVariable.get_position_list().get(globalVariable.position_name)
            if math.isclose(x, float(webSetPosition[0]), abs_tol=0.2) \
                    and math.isclose(y, float(webSetPosition[1]), abs_tol=0.2):
                # 控制剧本表演
                globalVariable.set_position("positionA", True)
                globalVariable.set_value("positionInformationFromChassisFlag", False)
            else:
                pass
        else:
            # logger.info("什么都不做")
            pass
        event.set()
        rLock.release()
