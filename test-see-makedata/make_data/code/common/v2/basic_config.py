# -*- coding: utf-8 -*-
# @Time    : 2020/05/18
# @Author  : jenniferwang

import json, time
import random
import datetime
from code.common.common_request import Request
from code.common.v2.adminlogin import Login_v2
from code.common.v2.rulesconfig import Rulesconfig
from code.common.v2.scoretemplate import Scoretemplate
from code.data.v2 import session_data


class basic_config_v2(object):
    def __init__(self,hostIP,port,account,password,aiforceIP,aiforcePort):
        self.hostIP = hostIP
        self.port = port
        self.account = account
        self.password = password
        self.aiforceIP = aiforceIP
        self.aiforcePort = aiforcePort



    def see_basic_config_v2(self):
        qrules = Rulesconfig()
        template = Scoretemplate()
        # 获取登录信息
        base_cookies = Login_v2().get_web_cookie(hostIP=self.hostIP, hostPort=self.port, account=self.account, password=self.password,
                                              aiforceIP=self.aiforceIP, aiforcePort=self.aiforcePort)
        base_head = {
            "Content-Type": "application/json;charset=UTF-8",
            "Atoken": "aiforce=" + base_cookies[1]['aiforce'] + " ;csrfToken=" + base_cookies[0]["csrfToken"],
            "x-csrf-token": base_cookies[0]["csrfToken"],
            "Cookie": "aiforce=" + base_cookies[1]['aiforce'] + " ;JSESSIONID=" + base_cookies[1][
                'JSESSIONID'] + " ;EGG_SESS=" + base_cookies[0]["EGG_SESS"] + " ;csrfToken=" + base_cookies[0][
                          "csrfToken"]
        }

        base_url = 'http://' + self.hostIP + ':' + self.port

        # 创建评分模板
        resp = template.see_add_scoreTemplate(base_url, base_head, 'makedata_scoreTemplate')
        if resp == ():
            print("评分模板 makedata_scoreTemplate 已初始化完成")
        else:
            scoreTemplateid = resp['data']['id']
            templatename = "makedata_scoreTemplate"
            # 创建评分模板下的评分分类
            resp = template.see_add_scoreClassification(base_url, base_head, scoreTemplateid, templatename,
                                                        'makedata_scoreClassification')
            # print(resp)
            if resp == ():
                # TODO 暂时走不进来
                print("评分分类 makedata_scoreClassification 已初始化完成")
            else:
                ruleTypeId = resp['data']['rules'][0]['id']


                # 创建规则分组
                resp = qrules.see_add_ruleGroup(base_url, base_head, 'makedata_ruleGroup')
                if resp == {'message': 'Internal Server Error'}:
                    print("规则分组 makedata_ruleGroup 已初始化完成")
                else:
                    scoreItemIds = []
                    ruleGroupId = resp['data']['id']
                    # 创建加分规则
                    for i in range(0, len(session_data.ADD_KEYWORD)):
                        resp = qrules.see_add_BusinessRule(base_url, base_head, ruleGroupId, 2, session_data.ADD_KEYWORD[i])
                        resp = template.see_add_scoreItem(base_url, base_head,
                                                          scoreTemplateid,
                                                          ruleTypeId,
                                                          resp['id'], 1, 0, random.randint(1, 20), session_data.ADD_KEYWORD[i])
                        scoreItemIds.append(resp["data"]["id"])


                    # 创建减分规则
                    for i in range(0, len(session_data.DEL_KEYWORD)):
                        resp = qrules.see_add_BusinessRule(base_url, base_head, resp['data']['id'], 2, session_data.DEL_KEYWORD[i], 1)
                        resp = template.see_add_scoreItem(base_url, base_head,
                                                          scoreTemplateid,
                                                          ruleTypeId,
                                                          resp['id'], 1, 1, random.randint(1, 20), session_data.DEL_KEYWORD[i])
                        scoreItemIds.append(resp["data"]["id"])
        return base_url, base_head, scoreTemplateid, scoreItemIds

    def see_add_dataset_schedule_task(self):
        # TODO
        pass

    def see_add_check_schedule_task(self):
        # TODO
        pass
