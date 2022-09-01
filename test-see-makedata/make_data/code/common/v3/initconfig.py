# -*- coding: utf-8 -*-
# @Time    : 2021/05/02
# @Author  : zhoulingzhi

import json, time, os
import random
import datetime

from code.common.v3.rulesconfig import Rulesconfig
from code.common.common_request_yaml import Common_request_yaml
from code.common.getyamldata import *
from code.common.v3.scoretemplate import Scoretemplate
class InitConfig(object):

    def init_addrule(self, base_url, base_head, list):
        '''
        新增规则
        '''
        ruleIds = dict()
        # 创建系统规则分组
        values = Rulesconfig().see_add_ruleGroup(base_url, base_head, initname="init_rulegroup888", type="1")
        print(values)
        ruleGroupId = values["data"]



        list_params = getyamldata().read_yaml_params_byfilename("init_system_rule.yaml")
        for curdata in list_params:
            http = curdata[1]
            expected = curdata[2]

            # 创建规则
            currentdate = int(time.time())

            http['params']['name'] = '%s_%s' % (http['params']['name'], currentdate)
            http['params']['groupId'] = ruleGroupId
            values = Common_request_yaml().see_post_request(base_url, base_head, http)
            # print(values)
            ruleIds[http['params']['name']] = values["data"]


        list["ruleIds"] = ruleIds
        # print(list)

        return list


    def init_scoreTemplateItems(self, base_url, base_head, list):
        '''
        新增评分模板、评分分类、评分项
        '''

        # 创建评分模板和评分分类
        values, templatename = Scoretemplate().see_add_scoreTemplate(base_url, base_head, initname="init_scoreTemplate888")

        templateId = Scoretemplate().see_find_scoreTemplate_id_byName(base_url, base_head, templatename)
        list["templateId"] = templateId
        if (templateId > 0):
            # 添加评分分类
            values, classificationname = Scoretemplate().see_add_scoreClassification(base_url, base_head, templateId, initname="init_scoreClassification888")
            classificationId = Scoretemplate().see_find_scoreClassification_id_byName(base_url, base_head, templateId,
                                                                                      classificationname)
            scoreItems = []
            for k, v in list['ruleIds'].items():
                values = Scoretemplate().see_add_scoreItem(base_url, base_head, random.randint(1, 10), templateId,
                                                           classificationId, v, ruleType=1, name=k,
                                                           scoreType=random.randint(0, 1), includeType=1)
                scoreItems.append(values["data"])
            list["scoreItems"] = scoreItems

        return list
