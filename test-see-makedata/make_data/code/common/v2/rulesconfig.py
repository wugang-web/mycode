# -*- coding: utf-8 -*-
# @Time    : 2020/05/18
# @Author  : jenniferwang

import json, time
import random
import datetime
from code.common.common_request import Request

class Rulesconfig(object):

    def see_add_ruleGroup(self, base_url, base_head, initname=None):
        '''
        创建随机规则分组接口
        '''

        if (initname != None):
            ruleGroupname = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            ruleGroupname = 'ruleGroup_%s_%s' % (currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/api/v1/ruleGroup'

        # 请求体参数
        data = {
                    "name": ruleGroupname
               }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_del_ruleGroup(self, base_url, base_head, ruleGroupId):
        '''
        删除规则分组接口
        '''

        # 接口地址
        base_url = base_url + '/api/v1/ruleGroup/' + '%s'%str(ruleGroupId)

        # 删除操作
        resp = Request().del_request(url=base_url, data=None, cookies=None, header=base_head)

        return resp

    def see_add_BusinessRule(self, base_url, base_head, ruleGroupId, checkType, checkValue, isSerious=0):
        '''
        在初始化规则分组创建普通规则接口，关键字：您好
        '''
        currentdate = int(time.time())
        rulename = 'Businessrule_keyword_%s_%s' % (checkValue, str(currentdate))

        # 接口地址
        base_url = base_url + '/api/v1/checkRule'

        # 请求体参数
        data = {
                    "name": rulename,
                    "desc": "",
                    "score": 0,
                    "useType": 3,
                    "ruleTypeId": -1,
                    "ruleRootType": "1",
                    "isSerious": isSerious,
                    "customerPortraitRule": [],
                    "ruleGroupId": ruleGroupId,
                    "relation": "(g1-ca)",
                    "conditions": [{
                        "name": "g1-ca",
                        "relation": "fa",
                        "violationMode": "matchToViolation",
                        "messageType": 2,
                        "checkScope": 1,
                        "scopeValue": "",
                        "factors": [{
                            "name": "fa",
                            "checkType": checkType,
                            "checkValue": checkValue,
                            "subCheckValue": ""
                        }]
                    }],
                    "rawConditions": [{
                        "conditionRelation": "all",
                        "violationMode": "matchToViolation",
                        "name": "",
                        "relation": "||",
                        "conditions": [{
                            "checkScope": 1,
                            "scopeValue": "",
                            "messageType": 2,
                            "includeType": 1,
                            "relation": "&&",
                            "factors": [{
                                "checkType": checkType,
                                "checkValue": checkValue,
                                "subCheckValue": "",
                                "thresholdValue": "",
                                "checkTag": ""
                            }]
                        }]
                    }]
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_add_ArtificialRule(self, base_url, base_head, rulename, isSerious):
        '''
        在初始化规则分组创建普通人工规则接口
        '''

        # 接口地址
        base_url = base_url + '/api/v1/checkRule'

        # 请求体参数
        data = {
                    "name": rulename,
                    "score": 0,
                    "desc": "这是一个自动化生成的人工规则",
                    "isSerious": isSerious,
                    "scoreType": "minus",
                    "rawConditions": [],
                    "conditions": [],
                    "relation": "artificial",
                    "ruleRootType": 3
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_add_GeneralRule_keyword(self, base_url, base_head, ruleGroupId, keyword, isSerious=0):
        '''
        在初始化规则分组创建普通规则接口，关键字：您好
        '''

        currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
        rulename = 'Generalrule_keyword_%s_%s_%s' % (keyword, currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/api/v1/checkRule'

        # 请求体参数
        data = {
                    "name": rulename,
                    "desc": "",
                    "score": 0,
                    "useType": 3,
                    "ruleTypeId": -1,
                    "ruleRootType": "4",
                    "isSerious": isSerious,
                    "customerPortraitRule": [],
                    "ruleGroupId": ruleGroupId,
                    "relation": "(g1-ca)",
                    "conditions": [{
                        "name": "g1-ca",
                        "relation": "fa",
                        "violationMode": "matchToViolation",
                        "messageType": 2,
                        "checkScope": 1,
                        "scopeValue": "",
                        "factors": [{
                            "name": "fa",
                            "checkType": 2,
                            "checkValue": keyword,
                            "subCheckValue": ""
                        }]
                    }],
                    "rawConditions": [{
                        "conditionRelation": "all",
                        "violationMode": "matchToViolation",
                        "name": "",
                        "relation": "||",
                        "conditions": [{
                            "checkScope": 1,
                            "scopeValue": "",
                            "messageType": 2,
                            "includeType": 1,
                            "relation": "&&",
                            "factors": [{
                                "checkType": 2,
                                "checkValue": keyword,
                                "subCheckValue": "",
                                "thresholdValue": "",
                                "checkTag": ""
                            }]
                        }]
                    }]
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_del_rule(self, base_url, base_head, ruleId):
        '''
        删除规则接口
        '''


        # 接口地址
        base_url = base_url + '/api/v1/checkRule/' + '%s'%str(ruleId)


        resp = Request().del_request(url=base_url, data=None, cookies=None, header=base_head)
        return resp

