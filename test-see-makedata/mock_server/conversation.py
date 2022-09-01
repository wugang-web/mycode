# !/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import random
from datetime import datetime
from datetime import timedelta


class conversation_v3:
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
        self.content = content_list(self.agent_name, self.customer_name, self.start_time, self.end_time)

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
            conversation["recordTime"] = self.audio_duration
            conversation["recordAddress"] = self.audio_add
        if flag == "text" or flag == "bottom":
            conversation["conversationList"] = self.content
        # 随路数据，根据客户需求定制
        conversation["associateData"] = {
            # 通用字段
            "ad_start_time": datetime.strftime(self.start_time, "%Y-%m-%d %H:%M:%S"),  # 开始时间
            "ad_end_time": datetime.strftime(self.end_time, "%Y-%m-%d %H:%M:%S"),  # 结束时间
            "ad_called_name": self.agent_name,  # 员工名称
            "ad_business_type": self.agent_business,  # 组别名称
            "ad_skillGroup": str(random.randint(1, 2)),  # 技能组
            # 定制字段
            "ad_caller_id": random.choice(["司机", "用户"]),  # 来电身份
            "ad_satisfaction": str(random.randint(1, 5)),  # 满意度
            "ad_remark": random.choice(["已回访", "备注信息", "已下单", "考虑中"]),  # 备注信息
            "false": str(random.randint(0, 2)), # 真假标签修改
            "age": random.randint(0, 100)  # 真假标签修改
        }
        # print(conversation)
        return conversation
