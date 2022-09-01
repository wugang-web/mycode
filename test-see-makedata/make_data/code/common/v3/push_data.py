# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
import time
import requests
from code.data.v3 import session_data
from code.common.v3.conversation import conversation_v3
import os

def write_data2txt(data):
    tmpfile = "data"
    # 写之前，先检验文件是否存在，存在就删掉
    if os.path.exists(tmpfile):
        os.remove(tmpfile)

    # 以写的方式打开文件，如果文件不存在，就会自动创建
    with open(tmpfile, "a+", encoding='utf-8') as f:
        f.write(data)

class PushData_v3:
    def __init__(self, send_url, scheduleId):
        '''
        构建推送数据模板
        '''


        self.send_url = send_url
        self.conversation_mode = dict()
        self.conversation_mode["scheduleId"] = scheduleId
        self.conversation_mode["data"] = list()

    def conversation_data(self, flag, num, work_session_number):
        '''
        构造推送的数据结构
        :param num:会话数量
        :return: 要推送的数据
        '''
        if flag == "audio" or flag == "work" :
            agent_list = session_data.AGENT_AUDIO
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3

        elif flag == "text":
            agent_list = session_data.AGENT_TEXT
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3

        elif flag == "bottom":
            agent_list = session_data.AGENT_TEXT
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3_perftest

        if num == 1:
            self.conversation_mode["data"].append(
                getconversation(
                    agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list, work_session_number
                ).conversation(flag)
            )
            return json.dumps(self.conversation_mode)
        elif num > 1:
            for index in range(1, num + 1):
                conversations = \
                    getconversation(
                        agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list, work_session_number
                    ).conversation(flag)
                self.conversation_mode["data"].append(copy.deepcopy(conversations))
            # print(self.conversation_mode)
            # write_data2txt(str(self.conversation_mode))

            return json.dumps(self.conversation_mode)

    def send_data(self, flag, num, busid, work_session_number):
        '''
        数据推送
        :param num: 推送会话的数量
        :return: 推送结果状态
        '''
        header = {'Content-Type': 'application/json; charset=utf-8', 'X-businessId': busid}
        data = self.conversation_data(flag, num, work_session_number)
        print(data)
        try:
            now_begin = time.time()  # 记录开始时间
            print("begin:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 展示开始时间
            # print(header)
            # print(data)

            print(self.send_url)
            response = requests.post(self.send_url, data=data.encode(), headers=header, timeout=36000)
            print(response.text)
            now_end = time.time()  # 记录结束时间
            print("end:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 展示结束时间
            print("dif_time:", now_end - now_begin)  # 展示时间差
        except requests.ReadTimeout as e:
            return -1  # 读超时
        except Exception as e:
            print(e)
            return -2  # 连接错误
        if response.status_code != 200:
            return -3  # 状态码不是200




