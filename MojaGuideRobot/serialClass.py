# -*- coding: utf-8 -*-
# @Time : 2021/6/29 16:21
# @Author :
# @Site : Beijing
# @File : serialClass.py
# @Software: PyCharm
import json
import threading
import binascii
import serial
import globalVariable
import serial.tools.list_ports
from loggerMode import logger


def parityBit(Data):
    bytesData = bytes(Data, encoding="ascii")
    HexData = binascii.b2a_hex(bytesData)
    hexStrNumber = len(HexData)
    HexData = HexData.decode("utf-8")
    parity = int(hex(int(hexStrNumber/2)), 16)
    step = 2
    for i in range(int(hexStrNumber/2)):
        parity = parity ^ int(HexData[i*2:i*2+step], 16)
    return parity


class Serial(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialFd = 0
        self.targetList = {}
        self.availableDataList = []
        self.getAbailableSerialList()
        self.recvMessage()
        self.connectWifi()
        self.recvMessage()
        self.wifiIp()
        self.recvMessage()
        with open("targetList.txt", "r", encoding='UTF-8') as f:
            self.target = json.load(f)
            print(self.target)
        self.set_target_List()

    def set_target_List(self):
        head = "nav:set_flag_point"
        tail = "]"
        for key in self.target:
            message = ""
            for i in range(len(self.target[key])):
                self.target[key][i] = str(self.target[key][i])
                if i == 0:
                    symbol = '['
                    message = symbol + message + self.target[key][i]
                elif i == len(self.target[key]):
                    symbol = ']'
                    message = message + self.target[key][i] + symbol
                else:
                    symbol = ","
                    message = message + symbol + self.target[key][i]

            self.targetList[key] = message + tail
            message = head + message + "," + key + tail
            self.sendMessage(message)

    def get_target_list(self):
        logger.info(self.targetList)
        return self.targetList

    def __new__(cls, *args, **kwargs):
        if not hasattr(Serial, "_instance"):
            with Serial._instance_lock:
                if not hasattr(Serial, "_instance"):
                    Serial._instance = object.__new__(cls)
        return Serial._instance

    def reboot_machine(self):
        logger.info("??????????????? -----> ????????????")
        self.sendMessage('sys:reboot_machine')

    def wifiIp(self):
        self.sendMessage('ip:request')

    def lanIp(self):
        self.sendMessage("ip_lan:request")

    def connectWifi(self):
        self.sendMessage('connect_wifi[moja-5G{0}moja1122]'.format(chr(0x7f)))

    def getAbailableSerialList(self):
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            logger.info("The Serial port can't find!")
        else:
            plist_0 = list(plist[0])
            serialName = plist_0[0]
            self.serialFd = serial.Serial(serialName, 115200, timeout=60)
            logger.info("check which port was really used >" + self.serialFd.name)

    def sendMessage(self, Data):
        # ???????????????????????????bytes??????
        # ????????????
        frameHead = "AA54"
        # ???????????????
        dataLen = "{0:02x}".format(len(Data))
        # ?????????
        dataBody = bytes(Data, encoding="ascii")
        # ?????????
        parity = "{0:02x}".format(parityBit(Data))
        # ??????????????????
        message = binascii.a2b_hex(frameHead + dataLen) + dataBody + binascii.a2b_hex(parity)
        serStr = self.serialFd.write(message)
        print(serStr)

    def recvMessage(self):
        if self.serialFd.in_waiting:
            with open("serialLog.txt", "a") as f:
                serStr = str(self.serialFd.read(self.serialFd.in_waiting)) + "\r\n"
                f.write(serStr)
                if "move_status" in serStr:
                    print("move_status")
            serStr = serStr.replace("\\xaaT", "0xaaT")
            serStr = serStr.replace("\\", "0")
            serStrList = serStr.split("0xaaT")
            serStr = ""
            # del serStrList[0]
            # ??????????????????
            for tempStr in serStrList:
                # ??????????????????
                if "move_status" in tempStr:
                    logger.info("move_status: " + tempStr[-2])
                    globalVariable.set_nav_status(tempStr[-2])

                if "nav:pose" in tempStr:
                    logger.info("nav:pose: " + tempStr[7:-2])
                    globalVariable.initPoint.append(tempStr[7:-2])

                if "ip:" in tempStr:
                    logger.info("WIFI IP: " + tempStr[-2])

                if len(tempStr) >= 4 and tempStr[:2] == '0x':
                    dataAvailableLen = int(tempStr[:4], 16)

                    if "lase" not in tempStr and "ver:" not in tempStr:
                        self.availableDataList.append(tempStr[4:4+dataAvailableLen])
                        logger.info(tempStr[4:4+dataAvailableLen])
                    else:
                        pass

                    if "nav:pose" in tempStr:
                        logger.info("??????????????????: " + self.availableDataList[-1])
                        return self.availableDataList[-1]
                    elif "point" in tempStr:
                        logger.info("???????????????????????????: " + self.availableDataList[-1])
                    elif "set_flag_point" in tempStr:
                        logger.info("???????????????: " + self.availableDataList[-1])
                    elif "wifi" in tempStr:
                        logger.info("??????????????????WIFI: " + self.availableDataList[-1])
                    elif "ip_lan" in tempStr:
                        logger.info("?????? IP: " + self.availableDataList[-1])
                    elif "move_status" in tempStr:
                        logger.info("?????????????????????: " + self.availableDataList[-1])
                    else:
                        print("???????????????????????????")
                else:
                    pass
            del serStrList

    def serialClose(self):
        self.serialFd.close()

    # ???????????????????????????
    def getPose(self):
        self.sendMessage("get_pose")
