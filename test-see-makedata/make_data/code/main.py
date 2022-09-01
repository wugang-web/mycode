# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: chen
# data:2020/12/29

import os
import sys
import configparser,json,random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SYS_PATH)  # 添加运行环境路径
config_file_name = 'conf.ini'


from code.common.v2.basic_config import basic_config_v2
from code.common.v3.push_data import PushData_v3
from code.common.v3.pull_data import PullData_v3
from code.common.v3.basic_config import basic_config_v3



class Exec(object):
    def __init__(self):
        # 读取配置文件信息
        self.get_config()

    def get_config(self):
        CONFIG_PATH = SYS_PATH
        filePath = os.path.join(CONFIG_PATH, config_file_name)
        print(filePath)

        conf = configparser.ConfigParser()
        conf.read(filePath, encoding='utf-8')
        self.text_enable = conf.get('common', 'text_enable')
        self.voice_enable = conf.get('common', 'voice_enable')
        self.work_enable = conf.get('common', 'work_enable')
        self.init_conf_enable = conf.get('common', 'init_conf_enable')
        self.bottom_push_enable = conf.get('common', 'bottom_push_enable')
        self.bottom_pull_enable = conf.get('common', 'bottom_pull_enable')
        self.branch = conf.get('common', 'branch')

        self.text_session_number = json.loads(conf.get('common', 'text_session_number'))
        self.voice_session_number = json.loads(conf.get('common', 'voice_session_number'))
        self.work_number = json.loads(conf.get('common', 'work_number'))
        self.work_session_number = json.loads(conf.get('common', 'work_session_number'))

        self.account = conf.get('login', 'account')
        self.password = conf.get('login', 'password')

        if self.branch >= '300':
            # 读取v3版本配置
            self.hostIP = conf.get('v3', 'host')
            self.port = conf.get('v3', 'port')
            self.busid = conf.get('v3', 'busId')
            pushurl = ':9005/see-dataset/dataset/import-by-url'
            self.pullurl = conf.get('v3', 'pullurl')
            self.scheduleId = conf.get('v3', 'scheduleId')
        else:
            # 读取v2版本配置
            self.hostIP = conf.get('v2', 'host')
            self.port = conf.get('v2', 'port')
            self.aiforceIP = conf.get('v2', 'aiforceIP')
            self.aiforcePort = conf.get('v2', 'aiforcePort')
            self.busid = conf.get('v2', 'busId')

            self.text_task_templateId = conf.get('v2', 'text_task_templateId')
            self.voice_task_templateId = conf.get('v2', 'voice_task_templateId')
            pushurl = ':8248/api/v1/external/workOrder/sendExternalData'


        self.pushurl = 'http://' + self.hostIP + pushurl


    def run(self):
        if (self.branch < '300'):
            # v2 推送数据类型：0语音，1工单，2文本
            if '1' == self.init_conf_enable:
                basic_config_v2(self.hostIP,self.port,self.account,self.password,self.aiforceIP,self.aiforcePort).see_basic_config_v2()

            if '1' == self.text_enable:
                print("Text Run")
                for number in self.text_session_number:
                    recordType = 2
                    SendData_v2(self.pushurl, self.busid, recordType, self.text_task_templateId).send_data("text", number)

            if '1' == self.voice_enable:
                print("Voice Run")
                for number in self.voice_session_number:
                    recordType = 0
                    SendData_v2(self.pushurl, self.busid, recordType, self.voice_task_templateId).send_data("audio", number)


        else:
            # v3 会话类型（1文本，2语音，3工单）
            if '1' == self.init_conf_enable:
                basic_config_v3(self.hostIP, self.port, self.account, self.password, self.busid).see_basic_config_v3()

            if ('1' == self.text_enable):
                print("Text Run")
                for number in self.text_session_number:
                    print(number)
                    # scheduleId = basic_config_v3(self.hostIP, self.port, self.account, self.password,
                    #                              self.busid).see_create_dataset_push_schedule(number, 1)
                    PushData_v3(self.pushurl, self.scheduleId).send_data("text", number, self.busid, self.work_session_number)


            if ('1' == self.voice_enable):
                print("Voice Run")
                for number in self.voice_session_number:
                    print(number)
                    # scheduleId = basic_config_v3(self.hostIP, self.port, self.account, self.password,
                    #                              self.busid).see_create_dataset_push_schedule(number, 2)
                    PushData_v3(self.pushurl, self.scheduleId).send_data("audio", number, self.busid, self.work_session_number)

            if ('1' == self.work_enable):
                print("Voice Run")
                for workNumber in self.work_number:
                    print(workNumber)
                    pushurl = 'http://' + self.hostIP + ':9005/see-dataset/dataset/work-order/import-by-url'
                    PushData_v3(pushurl, self.scheduleId).send_data("work", workNumber, self.busid, self.work_session_number)

            if ('1' == self.bottom_push_enable):
                print("Bottom Push Test Run")
                for number in self.text_session_number:
                    print(number)
                    scheduleId = basic_config_v3(self.hostIP, self.port, self.account, self.password, self.busid).see_create_dataset_push_schedule(number,1)
                    print(scheduleId)
                    PushData_v3(self.pushurl, scheduleId).send_data("bottom", number, self.busid)

            if ('1' == self.bottom_pull_enable):
                print("Bottom Pull Test Run")
                for number in self.text_session_number:
                    print(number)
                    PullData_v3(self.pullurl, self.hostIP, self.port, self.account, self.password, self.busid).pull_data("bottom", number)




if __name__ == '__main__':
    exec = Exec()
    # 执行构造数据
    exec.run()


