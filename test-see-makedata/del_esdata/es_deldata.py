# -*- coding: utf-8 -*-
# @Time    : 2021/10/22
# @Author  : chenshuhua

import requests
import json

class Elasticsearch(object):
# 注意 busid 不要删除 ！！样例业务！！
# 注意 busid 不要删除 ！！样例业务！！
# 注意 busid 不要删除 ！！样例业务！！
    def __init__(self):
        self.hostIp = "172.18.166.52"
        self.busId = "10"
        self.date = "202110"
        self.port1 = "9201"
        self.port2 = "9202"
        self.port3 = "9203"

    def search_bydate(self):
        '''
        根据_202109格式进行搜索索引的_index
        '''

        url = 'http://' + self.hostIp + ':' + self.port1 + '/_cluster/state'
        header = {
            'content-type' : "application/json; charset=UTF-8"
        }

        res = requests.get(url,headers = header).json()['routing_table']['indices']
        tables,estb_bid = [],[]
        for i in res:
            tables.append(i)

        for i in range(len(tables)):
            t1 = tables[i].find('_'+ str(self.busId) +'_')
            t2 = tables[i].find('_'+ str(self.date))
            if t1 > 0 and t2 > 0:
                estb_bid.append(tables[i])
        print(estb_bid)

        return estb_bid

    def search_tb(self,search_tb):
        '''
        查找要删除的索引值的_type
        '''
        url = 'http://' + self.hostIp+ ':' + self.port1+ '/'+ search_tb +'/_search'
        data = {
            "query": {"bool": {"must": [{"match_all": {}}], "must_not": [], "should": []}}, "from": 0, "size": 10,
             "sort": [], "aggs": {}
        }

        header ={
            'content-type': "application/json; charset=UTF-8"
        }
        res = requests.post(url=url,data=json.dumps(data),headers=header)
        return res

    def deldata(self,index,type):
        '''
        删除es内数据（不删除索引结构）
        '''

        list = [self.port1,self.port2,self.port3]
        for i in list:
            print(i)
            url = 'http://' + str(self.hostIp) + ':' + str(i) +'/'+ index +'/'+ type + '/_delete_by_query?pretty'
            print(url)
            data = {
                 "query": {
                  "match_all": {}
                             }
                    }
            header={
                'content-type': "application/json; charset=UTF-8"
            }
            res = requests.post(url, data=json.dumps(data),headers =header).json()
        return res
