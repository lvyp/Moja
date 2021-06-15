# -*- coding: utf-8 -*-

import threading
from enum import Enum


def _init():  # 初始化
    global _global_dict
    global event
    global intent
    global slot
    _global_dict = {}
    event = threading.Event()
    intent = IntentEnum.INITIALACTION
    slot = {'position': SlotPositionEnum.ALL, 'direction': SlotDirectionEnum.UP}


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


def get_event():
    return event


class IntentEnum(Enum):
    INITIALACTION = 0  # 初始状态
    HEADACTION = 1  # 头部动作
    EYEACTION = 2  # 眼部动作
    MOUTHACTION = 3  # 嘴部动作
    MAPNAVIGATION = 4  # 地图导览
    TTSBROADCAST = 5  # TTS播报


class SlotPositionEnum(Enum):
    ALL = 0
    LEFT = 1
    RIGHT = 2


class SlotDirectionEnum(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
