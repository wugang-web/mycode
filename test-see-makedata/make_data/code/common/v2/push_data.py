# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
import time
import requests
from code.data.v2 import session_data
from code.common.v2.conversation import conversation_v2



class SendData_v2:
    def __init__(self, send_url, busId, recordType, taskTemplateId=0):
        '''
        构建推送数据模板
        :param send_url:推送的url地址
        :param busId:推送的客户ID
        :param recordType:推送的数据类型：0语音、1工单、2文本
        :param taskTemplateId:关联的自动质检任务ID,可选
        '''


        self.send_url = send_url
        self.conversation_mode = dict()
        self.conversation_mode["busId"] = int(busId)
        self.conversation_mode["recordType"] = recordType
        if (taskTemplateId != '0'):
            self.conversation_mode["taskTemplateId"] = taskTemplateId
        self.conversation_mode["data"] = list()

    def conversation_data(self, flag, num):
        '''
        构造推送的数据结构
        :param num:会话数量
        :return: 要推送的数据
        '''
        if flag == "audio":
            agent_list = session_data.AGENT_AUDIO
        elif flag == "text":
            agent_list = session_data.AGENT_TEXT

        getconversation = conversation_v2
        data_content_list = session_data.content_list_v2


        if num == 1:
            self.conversation_mode["data"].append(
                getconversation(
                    agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list
                ).conversation(flag)
            )
            return json.dumps(self.conversation_mode)
        elif num > 1:
            for index in range(1, num + 1):
                conversations = \
                    getconversation(
                        agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list
                    ).conversation(flag)
                self.conversation_mode["data"].append(copy.deepcopy(conversations))
            return json.dumps(self.conversation_mode)

    def send_data(self, flag, num):
        '''
        数据推送
        :param num: 推送会话的数量
        :return: 推送结果状态
        '''
        header = {'Content-Type': 'application/json; charset=utf-8'}
        data = self.conversation_data(flag, num)
        try:
            now_begin = time.time()  # 记录开始时间
            print("begin:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 展示开始时间

            response = requests.post(self.send_url, data=data.encode(), headers=header, timeout=36000)
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




