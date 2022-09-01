# -*- coding: utf-8 -*-
# @Time    : 2020/05/18
# @Author  : jenniferwang

import json, time
import random
import datetime
from code.common.common_request import Request


from code.common.v2.rulesconfig import Rulesconfig

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
        base_url = base_url + '/api/v1/scoreTemplate'

        # 请求体参数
        data = {
            "name": templatename,
            "basicScore": 1,
            "maxScore": 1000
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_del_scoreTemplate(self, base_url, base_head, templateId):
        '''
        删除评分模板接口
        '''

        # 接口地址
        base_url = base_url + '/api/v1/scoreTemplate/' + '%s'%str(templateId)


        resp = Request().del_request(url=base_url, data=None, cookies=None, header=base_head)
        return resp

    def see_add_scoreClassification(self, base_url, base_head, scoreTemplateid, scoretemplatename, initname=None):
        '''
        创建评分分类接口
        '''

        if (initname != None):
            classificationname = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            classificationname = 'scoreClassification_%s_%s' % (currentdate, str(random.randint(1000, 9999)))


        ruleTypeId = int(round(time.time() * 1000))

        # 接口地址
        base_url = base_url + '/api/v1/scoreTemplate/' + '%s'%str(scoreTemplateid)

        # 请求体参数
        data = {
                    "rules": [{
                        "type": classificationname,
                        "id": ruleTypeId,
                        "scoreItemIds": []
                    }],
                    "id": scoreTemplateid,
                    "name": scoretemplatename,
                    "basicScore": 1,
                    "minScore": 0,
                    "maxScore": 110,
                    "status": 0
                }
        resp = Request().put_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_del_scoreClassification(self, base_url, base_head, scoreTemplateid, scoretemplatename):
        '''
        删除评分分类接口
        '''

        # 接口地址
        base_url = base_url + '/api/v1/scoreTemplate/' + '%s'%str(scoreTemplateid)

        # 请求体参数
        data = {
                    "rules": [],
                    "id": scoreTemplateid,
                    "name": scoretemplatename,
                    "basicScore": 1,
                    "minScore": 0,
                    "maxScore": 110,
                    "status": 0
                }
        resp = Request().put_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_add_scoreItem(self, base_url, base_head, scoreTemplateid, ruleTypeId, ruleId, ruleType, scoreType=1, score=10, name=None):
        '''
        创建评分项接口
        '''

        if (name != None):
            currentdate = int(time.time())
            Itemname = 'scoreItem_%s_%s' % (name,str(currentdate))
        else:
            currentdate = int(time.time())
            Itemname = 'scoreItem_%s' % (str(currentdate))

        # 接口地址
        base_url = base_url + '/api/v1/scoreItems'

        # 请求体参数
        data = {
                    "id": "",
                    "templateId": scoreTemplateid,
                    "name": Itemname,
                    "ruleTypeId": str(ruleTypeId),
                    "desc": "评分描述：这是一个自动化创建的评分项",
                    "score": score,
                    "scoreType": scoreType,
                    "conditions": [{
                        "conditionRelation": "all",
                        "relation": "||",
                        "conditions": [{
                            "ruleType": ruleType,
                            "includeType": 1,
                            "ruleId": ruleId
                        }]
                    }],
                    "rules": [ruleId],
                    "oldRuleTypeId": "makedata_scoreClassification"
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def see_add_scoreItem_batch_general(self, base_url, base_head, scoreTemplateid, ruleTypeId, ruleIds, rulenames):
        '''
        批量导入评分项接口
        '''

        # 接口地址
        base_url = base_url + '/api/v1/scoreItems/batchCreate'

        rules=[]
        for x in range(len(ruleIds)):
            rules.append({"id": ruleIds[x],"name": rulenames[x],"score": 0,"ruleRootType": 2})

        print(rules)

        # 请求体参数
        data = {
                    "rules": rules,
                    "typeId": str(ruleTypeId),
                    "templateId": scoreTemplateid
                }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_del_scoreItem(self, base_url, base_head, scoreItemId):
        '''
        删除评分项接口
        '''


        # 接口地址
        base_url = base_url + '/api/v1/scoreItems/' + '%s'%str(scoreItemId)


        resp = Request().del_request(url=base_url, data=None, cookies=None, header=base_head)
        return resp


    def see_setup(self, base_url, base_head, ruletype, operatortype, context):
        # setup:创建评分模板，评分分类，规则分组，规则
        envlist = {}

        rule_ids=[]
        rule_names=[]
        random_no = random.randint(1000, 9999)
        templatename = 'scoreTemplate_%s' % (str(random_no))
        classificationname = 'scoreClassification_%s' % (str(random_no))
        ruleGroupname = 'ruleGroup_%s' % (str(random_no))

        # 创建评分模板
        resp = self.see_add_scoreTemplate(base_url, base_head, templatename)

        envlist["scoreTemplateid"] = resp['data']['id']
        envlist["templatename"] = templatename
        scoreTemplateid = resp['data']['id']

        #创建评分模板下的评分分类
        resp = self.see_add_scoreClassification(base_url, base_head, scoreTemplateid, templatename, classificationname)
        envlist["ruleTypeId"] = resp['data']['rules'][0]['id']
        envlist["ruleTypeName"] = classificationname
        ruleTypeId = envlist["ruleTypeId"]

        # 创建规则分组
        resp = Rulesconfig().see_add_ruleGroup(base_url, base_head, ruleGroupname)

        envlist["ruleGroupId"] = resp['data']['id']
        envlist["ruleGroupname"] = ruleGroupname
        ruleGroupId = resp['data']['id']

        if (ruletype == 'BusinessRule'):
            # 创建业务规则
            if (operatortype == 'keyword'):
                resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 2, context)
                rule_ids.append(resp['id'])
                rule_names.append("env_rule_keyword_hello")
            elif (operatortype == 'regularExpression'):
                resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 3, context)
                rule_ids.append(resp['id'])
                rule_names.append("env_rule_regularExpression_ID")
            elif (operatortype == 'keywordlib'):
                resp = Rulesconfig().see_add_BusinessRule(base_url, base_head, envlist["ruleGroupId"], 5, context)
                rule_ids.append(resp['id'])
                rule_names.append("env_rule_keywordlib_1")
            else:
                print("operatortype error para")

        else:
            print("ruletype error para")

        envlist["rule_ids"] = rule_ids
        envlist["rule_names"] = rule_names

        return envlist

    def see_teardown(self, base_url, base_head, scoreTemplateid, ruleIds, ruleGroupId):

        # Teardown： 删除评分模板，删除规则，删除规则分组
        # 删除评分模板
        values = self.see_del_scoreTemplate(base_url, base_head, scoreTemplateid)

        for x in range(len(ruleIds)):
            rule_id = ruleIds[x]
            # 删除规则
            values = Rulesconfig().see_del_rule(base_url, base_head, rule_id)

        # 删除规则分组
        values = Rulesconfig().see_del_ruleGroup(base_url, base_head, ruleGroupId)
