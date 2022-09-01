# !/usr/bin/env python
# -*- coding: utf-8 -*-
#__author:zhoulingzhi
#data:2021/5/01

import json
import datetime,time
import random
from code.common.common_request import Request

class DataSet():
    '''
    数据集类
    '''

    def see_searchDataSetByName(self, base_url, base_head, dataSetName,sessionType):
        '''
        通过name获取数据集
        sessionType:文本数据集-1  语音数据集-2
        '''

        # 获取任务详情接口地址
        base_url = base_url + '/gateway/see-task/dataset/list'
        data = {
            "keyword":dataSetName,
            "sessionType":sessionType,
            "scheduleIdList":[],
            "pageSize":10,
            "pageNum":1,
            "importType":""
        }
        resp = Request().post_request(url=base_url, data=json.dumps(data), header=base_head, cookies=None)
        return resp

    def toggle_schedule_stage(self, base_url, base_head, scheduleId,stage):
        '''
        切换数据集计划状态
        '''

        # 获取任务详情接口地址
        base_url = base_url + '/gateway/see-task/dataset-schedule/toggle'
        data = {
            "id":scheduleId,
            "stage":stage
        }
        resp = Request().post_request(url=base_url, data=json.dumps(data), header=base_head, cookies=None)
        return resp

    def see_importDataSet_interface(self, base_url, base_head, datasetUrlId, type, initname=None):
        '''
        导入数据集-接口导入
        type:文本数据集-1  语音数据集-2
        '''

        currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
        if (initname != None):
            dataSetName = initname
        else:
            dataSetName = '接口导入数据集_%s_%s' % (currentdate, str(random.randint(1000, 9999)))

        # 接口地址
        base_url = base_url + '/gateway/see-task/dataset/create'

        # 请求体参数
        data = {
            "sessionType": type,
            "datasetName": dataSetName,
            "interfaceId": datasetUrlId,
            "startTime": currentdate + " 00:00:00",
            "endTime": currentdate + " 23:59:59",
            "importType": "2",
            "audioChannel": "1",
            "audioRate": "8000",
            "audioEngine": "zhuiyi",
            "roleWords": [
                "您","请","你好","高兴","服务","先生","女士","不用谢","客气","评价","感谢","来电","抱歉"
            ]
        }

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp

    def see_adddataSetPush_schedule(self, base_url, base_head, type, number, initname=None):
        '''
        创建数据集自动推送计划
        type:文本数据集-1  语音数据集-2
        '''

        if (initname != None):
            scheduleName = initname
        else:
            currentdate = int(time.time())
            name = "textschedule" if type == 1 else "audioschedule"
            scheduleName = name + '_%s_%s' % (currentdate, number)

        # 接口地址
        base_url = base_url + '/gateway/see-task/dataset-schedule/create'

        # 请求体参数
        data = {
              "name": scheduleName,
              "stage": 1,
              "executeType": 2,
              "sessionType": type
        }

        if type == 2:
            data["audioChannel"] = "1"
            data["audioRate"] = "8000"
            data["audioEngine"] = "zhuiyi"
            data["roleWords"] = ["您", "请", "你好", "高兴", "服务", "先生", "女士", "不用谢", "客气", "评价", "感谢", "来电", "抱歉"]

        # print(data)


        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)

        return resp


    def see_edit_dataset(self, base_url, base_head, id, dataSetName,sessionType):
        '''
        编辑数据集名称
        '''

        #接口地址
        base_url = base_url + '/gateway/see-task/dataset/update'

        # 请求体参数
        data = {
            "id": id,
            "name": dataSetName,
            "sessionType": sessionType
        }

        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        return resp

    def see_del_dataset(self, base_url, base_head, id):
        '''
        根据id删除数据集
        '''

        #接口地址
        base_url = base_url + '/gateway/see-task/dataset/delete'

        # 请求体参数
        data = {
            "id": id
        }

        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        return resp

    def see_getDataSetState_ById(self, base_url, base_head, id, sessionType):
        '''
        根据数据集id获取数据集状态
        '''

        #接口地址 查询所有数据集列表
        base_url = base_url + '/gateway/see-task/dataset/list'
        # 当前日期
        currentdate = (datetime.datetime.now()).strftime("%Y-%m-%d")
        # 请求体参数
        data = {
              "keyword": "",
              "sessionType": sessionType,
              "scheduleIdList": [],
              "pageSize": 10,
              "pageNum": 1,
              "importType": "",
              "startTime": currentdate + " 00:00:00",
              "endTime": currentdate + " 23:59:59",
        }

        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        records = resp["data"]["records"]
        stateStr = ""
        for obj in records:
            if obj["id"] == id:
                stateStr = obj["stateStr"]
                break
        return stateStr

    def see_get_listsession(self, base_url, base_head, datasetid, currentdate):
        '''
        获取数据集详情列表
        '''

        #接口地址
        base_url = base_url + '/gateway/see-dataset/dataset/list-session'

        # 请求体参数
        data = {
              "keyword": "",
              "datasetId": datasetid,
              "sessionCreateTime": currentdate,
              "sessionStartTimeMin": "",
              "sessionStartTimeMax": "",
              "pageNum": 1,
              "pageSize": 10
        }

        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        return resp

if __name__ == "__main__":
    pass