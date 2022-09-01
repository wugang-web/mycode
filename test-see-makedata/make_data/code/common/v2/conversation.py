# !/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import random
from datetime import datetime
from datetime import timedelta

class conversation_v2:
    def __init__(self, agent_list, customer_list, audio_list, content_list):
        '''
        加载会话必要参数
        :param agent_list: 坐席ID、坐席姓名、坐席组、业务线
        :param customer_list: 客户姓名、客户电话
        :param audio_list: 语音存放地址、语音时长
        :param content_list: 文本会话
        '''
        # 会话开始、结束时间
        self.start_time = datetime.now() - timedelta(minutes=85)
        self.end_time = datetime.now() - timedelta(minutes=82)
        # 坐席参数
        agent_id, agent_name, agent_group, business_type = agent_list[random.randint(0, 9)]
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_group = agent_group
        self.agent_business = business_type
        # 客户参数
        customer, phone = customer_list[random.randint(0, 35)]
        self.customer_name = customer
        self.customer_phone = phone
        # 语音会话数据
        audio_add, audio_duration = audio_list[random.randint(0, 9)]
        self.audio_add = audio_add
        self.audio_duration = audio_duration
        # 文本会话数据
        self.content = content_list(self.agent_name, self.customer_name, self.start_time,self.end_time)

    def conversation(self, flag):
        '''
        构造单个会话数据体
        :param flag: 会话的类型
        :return: 会话数据结构
        '''
        conversation = dict()

        conversation["sessionId"] = str(uuid.uuid4())[0:17]
        conversation["agentId"] = self.agent_id
        conversation["agentName"] = self.agent_name
        conversation["agentGroup"] = self.agent_group
        conversation["customName"] = self.customer_name
        conversation["startTime"] = datetime.strftime(self.start_time, "%Y-%m-%d %H:%M:%S")
        conversation["endTime"] = datetime.strftime(self.end_time, "%Y-%m-%d %H:%M:%S")

        if flag == "audio":
            conversation["recordId"] = "1"
            conversation["recordTime"] = self.audio_duration
            conversation["recordAddress"] = self.audio_add
        if flag == "text":
            conversation["conversationList"] = self.content
        # 随路数据，根据客户需求定制
        conversation["associateData"] = {
            # 通用字段
            "testdate": datetime.strftime(self.start_time, "%Y-%m-%d %H:%M:%S"),  # 开始时间
            "testdateEnd": datetime.strftime(self.end_time, "%Y-%m-%d %H:%M:%S"),  # 结束时间
            "testjingzhun": random.choice(["5", "3", "0", "-10"]),
            "testmohu": random.choice(["非常满意", "满意", "一般", "不满意"]),
            "testnum": random.randint(-12, 12)
        }
        # print(conversation)
        return conversation

