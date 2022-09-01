# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import copy
import uuid
import time
import requests


upload_post = "http://172.16.20.185:8248/api/v1/audio/dataset/upload?_csrf={}"


# _csrf: r_kVd-o9YtI5zBDUMBrpSJz-
# fileLength: 0

# fileLength: 1470080
# file: (binary)

dataset_post = "http://172.16.20.185:8248/api/v1/audio/dataset"

abc = {
    "audioChannel": {
        "name":  "自动判别",
        "value": "0"
    },
    "audioEngine": {
        "name": "追一",
        "value": "zhuiyi"
    },
    "audioRate": {
        "name": "8K",
        "value": "8000"
    },
    "audioSource": "cos",
    "cosFiles": [
        {"name": ""}
    ],
    "name": "",
    "roleWords": "您，请，你好，高兴，服务，先生，女士，不用谢，客气，评价，感谢，来电，抱歉"
}

upload_185 = "http://172.16.20.185:8248/api/v1/audio/dataset/upload"


def send_data(upload_url,):

    header = {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryJQnAp7Z8t8a6IGgi',
        "Cookie": "aiforce=fcd2e226-0a13-41a2-8e60-785c5c6b5d8f; "
                  "JSESSIONID=0f0a0ba7-fcd5-445b-b922-0df3b138cea8; "
                  "csrfToken=r_kVd-o9YtI5zBDUMBrpSJz-; "
                  "EGG_SESS=L4QCOWBtFfesozqvwXRu-OYCNrHbPCIkkhdRcOBjF4tOejSqDSlhjfp9dRU6MedX",
        "csrfToken": "r_kVd-o9YtI5zBDUMBrpSJz-"
        }

    data = {}
    try:
        response = requests.post(upload_url, data=data.encode(), headers=header, timeout=36000)
    except requests.ReadTimeout as e:
        return -1  # 读超时
    except Exception as e:
        print(e)
        return -2  # 连接错误
    if response.status_code != 200:
        return -3  # 状态码不是200