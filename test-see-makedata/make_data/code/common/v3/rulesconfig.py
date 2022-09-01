# -*- coding: utf-8 -*-
# @Time    : 2021/05/02
# @Author  : zhoulingzhi

import json, time, os
import random
import datetime
from code.common.common_request import Request

class Rulesconfig(object):

    def see_add_ruleGroup(self, base_url, base_head, initname=None, type=None):
        '''
        创建规则分组接口
        type:系统规则-1  人工规则-2  流程规则-3
        '''

        if (initname != None):
            ruleGroupname = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            ruleGroupname = 'ruleGroup_%s_%s' % (currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/gateway/see-management/rule/group/create'

        # 请求体参数
        data = {
                    "name": ruleGroupname,
                    "type": type
               }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_del_ruleGroup(self, base_url, base_head, ruleGroupId):
        '''
        删除规则分组接口
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/rule/group/delete'

        # 请求体参数
        data = {
            "id": ruleGroupId
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_update_ruleGroup(self, base_url, base_head, id, initname=None, type=None):
        '''
        创建规则分组接口
        type:系统规则-1  人工规则-2  流程规则-3
        '''

        if (initname != None):
            ruleGroupname = initname
        else:
            currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
            ruleGroupname = 'u_ruleGroup_%s_%s' % (currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/gateway/see-management/rule/group/update'

        # 请求体参数
        data = {
                    "id": id,
                    "name": ruleGroupname,
                    "type": type
               }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp


    def get_rule_group_list(self, base_url, base_head, type):
        '''
        创建规则分组list接口
        '''

        base_url = base_url + '/gateway/see-management/rule/group/list'

        # 请求体参数
        data = {
            "type": type
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        return resp

    def find_rule_group_byId(self, data, id):
        '''
        创建拉取接口
        '''

        for inf in data:
            if inf["id"] == id:
                return inf["id"]
        return -1

    def see_del_rule(self, base_url, base_head, ruleGroupId):
        '''
        删除规则接口
        '''

        # 接口地址
        base_url = base_url + '/gateway/see-management/rule/delete'

        # 请求体参数
        data = {
            "id": ruleGroupId
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp
