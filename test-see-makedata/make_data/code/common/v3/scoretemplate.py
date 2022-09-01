# -*- coding: utf-8 -*-
# @Time    : 2020/05/18
# @Author  : jenniferwang

import json, time
import random
import datetime
from code.common.common_request import Request


class Scoretemplate(object):

    def see_add_scoreTemplate(self, base_url, base_head, initname=None):
        '''
        创建随机名称评分模板接口
        '''

        if (initname != None):
            templatename = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            templatename = 'scoreTemplate_%s_%s' % (currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-template/create'

        # 请求体参数
        data = {
            "name": templatename,
            "basicScore": 60,
            "maxScore": 100
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp,templatename

    def see_del_scoreTemplate(self, base_url, base_head, scoreTemplateid):
        '''
        删除评分模板接口
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-template/delete'

        # 请求体参数
        data = {
            "id": scoreTemplateid
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_get_scoreTemplate_list(self, base_url, base_head, keyword=""):
        '''
        获取评分模板列表
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-template/list'

        # 请求体参数
        data = {
            "keyword": keyword
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_find_scoreTemplate_id_byName(self, base_url, base_head, templatename):
        '''
        获取评分模板列表
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-template/list'

        # 请求体参数
        data = {
            "keyword": ""
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        if resp["code"] == 0:
            data = resp["data"]
            for oneTemp in data:
                if oneTemp["name"] == templatename:
                    return oneTemp["id"]
        return -1

    def see_find_scoreClassification_id_byName(self, base_url, base_head, templateId, Classificationname):
        '''
        获取评分模板列表
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-item-category/list?templateId=%s' % templateId


        resp = Request().get_request(url=base_url, cookies=None, header=base_head)
        if resp["code"] == 0:
            data = resp["data"]
            for oneTemp in data:
                if oneTemp["name"] == Classificationname:
                    return oneTemp["id"]
        return -1

    def see_add_scoreClassification(self, base_url, base_head, scoreTemplateid, initname=None):
        '''
        创建评分分类接口
        '''

        if (initname != None):
            classificationname = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            classificationname = 'scoreClassification_%s_%s' % (currentdate, str(random.randint(1000, 9999)))


        # 接口地址
        base_url = base_url + '/gateway/see-management/score-item-category/create'

        # 请求体参数
        data = {
                    "name": classificationname,
                    "templateId": scoreTemplateid
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp,classificationname

    def see_del_scoreClassification(self, base_url, base_head, scoreTemplateid):
        '''
        删除评分分类接口
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-item-category/delete'

        # 请求体参数
        data = {
                    "id": scoreTemplateid,

                }
        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_add_scoreItem(self, base_url, base_head, score, scoreTemplateid, categoryId, ruleId, ruleType=1, name=None, scoreType=1,includeType=1):
        '''
        创建评分项接口
        scoreType:得分类型（0加分，1减分）
        ruleRelation: 0全部 1任一
        nextRelation:  和下一个条件组合的关系， -1代表没有下一个组合
        includeType: 1包含 2不包含
        type: 规则类型  1系统规则  2人工规则  3流程规则
        '''

        if (name != None):
            # currentdate = int(time.time())
            Itemname = 'scoreItem_%s' % name
        else:
            currentdate = int(time.time())
            Itemname = 'scoreItem_%s' % (str(currentdate))

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-item/create'


        # 请求体参数
        data = {
                    "id": "",
                    "templateId": scoreTemplateid,
                    "name": Itemname,
                    "categoryId": str(categoryId),
                    "desc": "评分描述：这是一个自动化创建的评分项",
                    "score": score,
                    "scoreType": scoreType,
                    "conditions": [{
                        "ruleRelation": 0,
                        "nextRelation": -1,
                        "rules": [{
                            "type": ruleType,
                            "includeType": includeType,
                            "id": ruleId
                        }]
                    }],
                    "rules": [ruleId],
                }

        # print(data)
        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        # print(resp)
        return resp


    def see_del_scoreItem(self, base_url, base_head, scoreItemId):
        '''
        删除评分项接口
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/score-item/delete'

        data = {
            "id": scoreItemId,

        }
        resp = Request().del_request(url=base_url, data=None, cookies=None, header=base_head)
        return resp


    # def see_setup(self, base_url, base_head, ruletype, operatortype, context):
    #     # setup:创建评分模板，评分分类，规则分组，规则
    #     envlist = {}
    #
    #     rule_ids=[]
    #     rule_names=[]
    #     random_no = int(time.time())
    #     templatename = 'scoreTemplate_%s' % (str(random_no))
    #     classificationname = 'scoreClassification_%s' % (str(random_no))
    #     ruleGroupname = 'ruleGroup_%s' % (str(random_no))
    #
    #     # 创建评分模板
    #     resp = self.see_add_scoreTemplate(base_url, base_head, templatename)
    #
    #     envlist["scoreTemplateid"] = resp['data']['id']
    #     envlist["templatename"] = templatename
    #     scoreTemplateid = resp['data']['id']
    #
    #     #创建评分模板下的评分分类
    #     resp = self.see_add_scoreClassification(base_url, base_head, scoreTemplateid, templatename, classificationname)
    #     envlist["ruleTypeId"] = resp['data']['rules'][0]['id']
    #     envlist["ruleTypeName"] = classificationname
    #     ruleTypeId = envlist["ruleTypeId"]
    #
    #     # 创建规则分组
    #     resp = Rulesconfig().see_add_ruleGroup(base_url, base_head, ruleGroupname)
    #
    #     envlist["ruleGroupId"] = resp['data']['id']
    #     envlist["ruleGroupname"] = ruleGroupname
    #     ruleGroupId = resp['data']['id']
    #
    #     if (ruletype == 'BusinessRule'):
    #         # 创建业务规则
    #         if (operatortype == 'keyword'):
    #             resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 2, operatortype)
    #             rule_ids.append(resp['id'])
    #             # print(resp)
    #             rule_names.append("env_rule_keyword")
    #         elif (operatortype == 'regularExpression'):
    #             resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 3, operatortype)
    #             rule_ids.append(resp['id'])
    #             rule_names.append("env_rule_regularExpression")
    #         elif (operatortype == 'keywordlib'):
    #             resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 5, operatortype)
    #             rule_ids.append(resp['id'])
    #             rule_names.append("env_rule_keywordlib")
    #         else:
    #             print("operatortype error para")
    #
    #     else:
    #         print("ruletype error para")
    #
    #     envlist["rule_ids"] = rule_ids
    #     envlist["rule_names"] = rule_names
    #
    #     return envlist
    #
    # def see_teardown(self, base_url, base_head, scoreTemplateid, ruleIds, ruleGroupId):
    #
    #     # Teardown： 删除评分模板，删除规则，删除规则分组
    #     # 删除评分模板
    #     values = self.see_del_scoreTemplate(base_url, base_head, scoreTemplateid)
    #
    #     for x in range(len(ruleIds)):
    #         rule_id = ruleIds[x]
    #         # 删除规则
    #         values = Rulesconfig().see_del_rule(base_url, base_head, rule_id)
    #
    #     # 删除规则分组
    #     values = Rulesconfig().see_del_ruleGroup(base_url, base_head, ruleGroupId)
