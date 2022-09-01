import requests
import json
import uuid
import datetime
import random


# encoding: utf-8

def pushTextDemo(url):
    headers = {
        'Content-Type': 'application/json',
        'X-businessId': '4'
    }

    RequestData = {
        "scheduleId": "6",
        "data": [
            {
                "sessionId": str(uuid.uuid1()),
                "agentName": "小yi",
                "agentId": '123456',
                "agentGroup": "0",
                "customName": "张三11111",
                "startTime": "2021-06-17 03:06:09",
                "endTime": "2021-06-17 03:06:20",
                "conversationList": [
                    {
                        "startTime": "2021-06-17 03:06:09",
                        "endTime": "2021-06-17 03:06:12",
                        "content": "您好，我是追一客服小yi，请问有什么可以帮您。",
                        "messageType": '2'
                    },
                    {
                        "startTime": "2021-06-17 03:06:13",
                        "endTime": "2021-06-17 03:06:14",
                        "content": "追一都有什么产品？",
                        "messageType": '1'
                    },
                    {
                        "startTime": "2021-06-17 03:06:15",
                        "endTime": "2021-06-17 03:06:18",
                        "content": "see,pal,learn",
                        "messageType": '2'
                    },
                    {
                        "startTime": "2021-06-17 03:06:19",
                        "endTime": "2021-06-17 03:06:20",
                        "content": "可以卖给我们吗。",
                        "messageType": 1
                    }
                ],
                "associateData": {
                    "str_10": "1630981113",  # 10位字符串格式  2021-09-07 10:18:33
                    "num_10": 1630981113,  # 10位数字格式
                    "str_13": "1630981037840",  # 13位字符串格式   2021-09-07 10:17:17
                    "num13": 1630981037840,  # 13位数字
                }
            }
        ]
    }

    request = requests.post(url=url, data=json.dumps(RequestData), headers=headers)
    print(request.text)
    return 0


if __name__ == "__main__":
    url = 'http://172.18.166.52/see-dataset/dataset/import-by-url'

    pushTextDemo(url)


