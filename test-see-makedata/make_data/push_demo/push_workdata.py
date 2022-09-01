import requests
import json
import uuid
from datetime import datetime
from datetime import timedelta

def pushTextDemo(url):
    headers = {
        'Content-Type': 'application/json',
        'X-businessId': '5'
    }

    start_time = datetime.now() - timedelta(minutes=85)
    end_time = datetime.now() - timedelta(minutes=82)
    RequestData = {
        "scheduleId": 8,
        "data": [
            {
                "workOrderNo": "123456",
                "sessionCount": 3,
                "agentId": "2031",
                "agentName": "杨晶晶",
                "agentGroup": "文本二组",
                "customName": "张三",
                "workOrderTime": "2021-11-02 10:02:00",
                "dynamicLabel": {},
                "associateData": {},
                "recordList": [
                    {
                        "recordId": "1111",
                        "recordAddress": "http://172.16.20.185:8248/public/audio/20092016514957210001015200036b.mp3",
                        "startTime": datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S"),
                        "closeTime": datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S"),
                        "associateData": {}
                    },
                    {
                        "recordId": "2222",
                        "recordAddress": "http://172.16.20.185:8248/public/audio/2009210925442188000101960003e7ec.mp3",
                        "startTime": datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S"),
                        "closeTime": datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S"),
                        "associateData": {}
                    },
                    {
                        "recordId": "3333",
                        "recordAddress": "http://172.16.20.185:8248/public/audio/2009210937388828000101530003d71d.mp3",
                        "startTime": datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S"),
                        "closeTime": datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S"),
                        "associateData": {}
                    }
                ]
            }
        ]
    }

    request = requests.post(url=url, data=json.dumps(RequestData), headers=headers)
    print(request.text)
    return 0


if __name__ == "__main__":
    url = 'http://172.16.50.79/see-dataset/dataset/work-order/import-by-url'
    pushTextDemo(url)
