# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
import time
import requests
from code.data.v3 import session_data
from code.common.v3.conversation import conversation_v3
from code.common.v3.adminlogin import Login_v3
from code.common.common_request import Request

class PullData_v3:
    def __init__(self, pull_url, hostIP, port, account, password, busId):
        '''
        初始化函数
        '''

        self.pull_url = pull_url
        self.hostIP = hostIP
        self.hostPort = port
        self.account = account
        self.password = password
        self.busId = busId
        self.infname = "探底测试拉取接口_see_autotest"

    def see_login(self):
        # 获取登录信息
        base_cookies = \
            Login_v3().get_web_cookie(
                account=self.account,
                password=self.password,
                nodeHost=self.hostIP,
                ingressPort=self.hostPort
            )

        # 登录See的base_url
        base_url = 'http://' + self.hostIP + ':' + self.hostPort
        # 登录AIForce的base_url
        aiforce_base_url = "http://" + self.hostIP + ':' + self.hostPort + "/ng-aiforce"

        # # 获取busId
        # busId = Login_v3().get_busId(base_url, base_cookies, productId, bussinessName)

        # 登录See的base_head
        base_head = {
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": base_cookies["cookie"],
            "X-businessId": str(self.busId)
        }

        return base_url, base_head, aiforce_base_url

    def create_pull_intf_id(self, base_url, base_head, data):
        '''
        创建拉取接口
        type： 1-文本 ； 2-语音
        '''

        base_url = base_url + '/gateway/see-management/system/data-interface/create'
        newdata = [{
            "name": self.infname,
            "type": 1,
            "url": self.pull_url
        }]
        data = data + newdata

        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        return resp

    def get_pull_intf_list(self, base_url, base_head):
        '''
        创建拉取接口
        type： 1-文本 ； 2-语音
        '''

        base_url = base_url + '/gateway/see-management/system/data-interface/list'

        resp = Request().get_request(url=base_url,header=base_head,cookies=None)

        return resp

    def find_pull_intfid_byname(self, data, name):
        '''
        创建拉取接口
        type： 1-文本 ； 2-语音
        '''

        for inf in data:
            if inf["name"] == name and inf["url"] == self.pull_url:
                return inf["id"]
        return -1

    def get_infid(self, base_url, base_head):

        # 获取已经配置的文本拉取接口
        resp = self.get_pull_intf_list(base_url, base_head)
        data = resp['data']

        # 查找是否配置了探底接口
        id = self.find_pull_intfid_byname(data, self.infname)
        if (id != -1):
            return id

        self.create_pull_intf_id(base_url,base_head, data)

        # 再次获取已经配置的文本拉取接口
        resp = self.get_pull_intf_list(base_url, base_head)
        data = resp['data']

        # 返回探底接口id
        id = self.find_pull_intfid_byname(data, self.infname)

        return id

    def create_pull_dataset(self, base_url, base_head, id):
        '''
        创建手工拉取接口的数据集
        sessionType： 会话类型（1文本，2语音，3工单）
        importType: 本地导入1，接口导入2，计划导入3
        '''

        datasetName = 'pulldataset_%s' % (str(int(time.time())))
        currentdate = time.strftime("%Y-%m-%d", time.localtime())


        base_url = base_url + '/gateway/see-task/dataset/create'
        data = {
                    "sessionType": 1,
                    "datasetName": datasetName,
                    "interfaceId": id,
                    "startTime": "%s 00:00:00" % currentdate,
                    "endTime": "%s 23:59:59" % currentdate,
                    "importType": "2"
                }

        print(data)
        resp = Request().post_request(url=base_url,data=json.dumps(data),header=base_head,cookies=None)
        return resp

    def pull_data(self, flag, num):
        '''
        手工数据拉取
        '''

        # 获取登录信息
        see_login = self.see_login()

        id = self.get_infid(see_login[0],see_login[1])
        if (id == -1):
            print("Error:未获取到拉取接口id")
            return -1

        resp = self.create_pull_dataset(see_login[0], see_login[1], id)
        print(resp)

        # header = {'Content-Type': 'application/json; charset=utf-8'}
        # data = self.conversation_data(flag, num)
        # print(data)
        # try:
        #     now_begin = time.time()  # 记录开始时间
        #     print("begin:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 展示开始时间
        #     # print(header)
        #     # print(data)
        #     # print(self.send_url)
        #     response = requests.post(self.send_url, data=data.encode(), headers=header, timeout=36000)
        #     # print(response.text)
        #     now_end = time.time()  # 记录结束时间
        #     print("end:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 展示结束时间
        #     print("dif_time:", now_end - now_begin)  # 展示时间差
        # except requests.ReadTimeout as e:
        #     return -1  # 读超时
        # except Exception as e:
        #     print(e)
        #     return -2  # 连接错误
        # if response.status_code != 200:
        #     return -3  # 状态码不是200



