#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : speechRecognitionMode.py
# @Software: PyCharm
import json
import os

import requests
from aip import AipSpeech, AipNlp
from loggerMode import logger


class Baidu_NLU(object):
    def __init__(self):

        self.API_Key = "EI3cSUrazGNTbeCIU4R4IQ8e"
        self.Secret_Key = "ENbN0tsyS5QnlqeFznp6S5XltZfWkHLp"
        self.AppID = "S53630"
        self.access_token = self.get_access_token()
        self.session_id = ""

    def get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
            self.API_Key, self.Secret_Key)
        response = requests.get(host)
        return (response.json().get("access_token"))

    def get_NLU(self,text):
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + self.access_token
        post_data = "{\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1057\"]}}}"
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        body = {
            "version": "2.0",
            # "skill_ids":"",技能ID列表。我们允许开发者指定调起哪些技能。这个列表是有序的——排在越前面的技能，优先级越高。技能优先级体现在response的排序上。
            "log_id": "UNITTEST_10000",  # 开发者需要在客户端生成的唯一id，用来定位请求，响应中会返回该字段。对话中每轮请求都需要一个log_id
            "session_id": self.session_id,
            # session保存机器人的历史会话信息，由机器人创建，客户端从上轮应答中取出并直接传递，不需要了解其内容。如果为空，则表示清空session（开发者判断用户意图已经切换且下一轮会话不需要继承上一轮会话中的词槽信息时可以把session置空，从而进行新一轮的会话）。session字段内容较多，开发者可以通过传送session_id的方式节约传输流量。
            "bot_id":"1099740",
            "skill_sessions": "",

            "service_id": self.AppID,  # 机器人ID，service_id 与skill_ids不能同时缺失，至少一个有值·
            "request": {"query": text, "user_id": "88888"},
        }
        response = requests.post(url=url, data=json.dumps(body), headers=headers)
        if response:
            json_result = response.json().get("result")
            print(json_result)
            self.session_id = json_result.get("session_id")
            answer = json_result.get("response_list")[0]
            return answer


class BaiduCloud(object):
    def __init__(self):
        self.Cloud_AppID = "24343144"
        self.Cloud_APIKey = "E1GPVi0geOh8ufvROWC7NOz2"
        self.Cloud_Secret_Key = "iCvIBWCrEG2E8OBfmIiVWU3dgGZPT9B9"
        self.AipSpeechclient = AipSpeech(self.Cloud_AppID, self.Cloud_APIKey, self.Cloud_Secret_Key)
        self.NLPclient = AipNlp(self.Cloud_AppID, self.Cloud_APIKey, self.Cloud_Secret_Key)

    def call_asr(self, filePath):
        with open(filePath, "rb") as fp:
            try:
                asr_result = self.AipSpeechclient.asr(fp.read(), "wav", 16000, {
                    "dev_pid": 1537,
                })
                return asr_result.get("result")[0]
            except Exception as e:
                logger.info("Exception Happened: " + str(e))
                return "Exception Happened"

    def call_tts(self, text):
        result = self.AipSpeechclient.synthesis(text, "zh", 1, {
            "vol": 5,
        })
        if not isinstance(result, dict):
            if os.path.exists("./TtsRecording/BaiduCloud/TtsResponse.mp3"):
                os.remove("./TtsRecording/BaiduCloud/TtsResponse.mp3")
            else:
                pass
            with open("./TtsRecording/BaiduCloud/TtsResponse.mp3", "wb") as f:
                f.write(result)
