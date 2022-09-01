# -*- coding: utf-8 -*-
# @Time    : 2020/05/18
# @Author  : jenniferwang

import json, time
import random
import datetime
from code.common.common_request import Request
from code.common.v3.adminlogin import Login_v3
from code.common.v3.initconfig import InitConfig
from code.common.v3.rulesconfig import Rulesconfig
from code.common.v3.scoretemplate import Scoretemplate
from code.data.v3 import session_data
from code.common.v3.dataSet import DataSet

class basic_config_v3(object):

    def __init__(self,hostIP,port,account,password,busId):
        self.hostIP = hostIP
        self.port = port
        self.account = account
        self.password = password
        self.busId = busId

    def login(self,hostIP,hostPort,account,password,busId):

        # 获取登录信息
        base_cookies = \
            Login_v3().get_web_cookie(
                account=account,
                password=password,
                nodeHost=hostIP,
                ingressPort=hostPort
            )

        # 登录See的base_head
        base_head = {
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": base_cookies["cookie"],
        }

        # 登录See的base_url
        base_url = 'http://' + hostIP + ':' + hostPort
        # 登录AIForce的base_url
        aiforce_base_url = "http://" + hostIP + ':' + hostPort + "/ng-aiforce"

        # 通过busId切换业务
        Login_v3().tansfer_bussiness(base_url, base_head, busId)

        return base_url, base_head, aiforce_base_url


    def see_basic_config_v3(self):
        # 获取登录信息
        print(self.busId)
        base_url, base_head, aiforce_base_url = self.login(self.hostIP,self.port,self.account,self.password,self.busId)
        print(base_head)

        templateId = Scoretemplate().see_find_scoreTemplate_id_byName(base_url, base_head, "init_scoreTemplate888")
        if templateId > 0:
            print("请确认，现有环境已经配置了初始化的评分模板及评分项")
            return templateId

        # 配置系统规则
        envlist = {}
        envlist = InitConfig().init_addrule(base_url, base_head, envlist)

        # 创建评分模板和评分分类
        envlist = InitConfig().init_scoreTemplateItems(base_url, base_head, envlist)
        print(envlist)
        return envlist["templateId"]

    def see_create_dataset_push_schedule(self, number, type):
        # 获取登录信息
        base_url, base_head, aiforce_base_url = self.login(self.hostIP, self.port, self.account, self.password,
                                                           self.busId)

        values = DataSet().see_adddataSetPush_schedule(base_url,base_head, type, number)
        return values['data']



