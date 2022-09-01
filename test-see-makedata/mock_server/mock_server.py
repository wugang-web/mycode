# -*- coding:utf-8 -*-

import sys
import urllib
import json
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse
import uuid
import time
import copy
import session_data
from conversation import conversation_v3

class ServerRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    server_version = "PSHS/0.1"
    sys_version = "Python/3.6.x"

    def create_conversation(self, session_number):
        # 随机生成会话id
        uid = uuid.uuid1()
        suid = ''.join(str(uid).split('-'))
        conversation_list = dict()
        conversation_list["code"] = 0
        conversation_list["dataLength"] = session_number
        conversation_list["message"] = ""
        conversation_list["data"] = list()


        return conversation_list

    def conversation_data(self, flag, conversation_list, num):
        '''
        构造推送的数据结构
        :param num:会话数量
        :return: 要推送的数据
        '''

        if flag == "audio":
            agent_list = session_data.AGENT_AUDIO
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3

        elif flag == "text":
            agent_list = session_data.AGENT_TEXT
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3
        elif flag == "bottom":
            agent_list = session_data.AGENT_TEXT
            getconversation = conversation_v3
            data_content_list = session_data.content_list_v3_perftest

        if num == 1:
            conversation_list["data"].append(
                getconversation(
                    agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list
                ).conversation(flag)
            )
            return json.dumps(conversation_list)
        elif num > 1:
            for index in range(1, num + 1):
                conversations = \
                    getconversation(
                        agent_list, session_data.CUSTOMERS, session_data.AUDIOS, data_content_list
                    ).conversation(flag)
                conversation_list["data"].append(copy.deepcopy(conversations))
            return json.dumps(conversation_list)

    def do_POST(self):
        print(self.path)


    def do_GET(self):

            time1 = time.time()  # 记录开始时间
            print("开始接受Get请求:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            parsed_result = urlparse(self.path)
            query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))
            # print(parsed_result)
            # print(query)

            conversation_list = self.create_conversation(9000)
            self.conversation_data("bottom",conversation_list,1000)
            # print(conversation_list)

            time2 = time.time()  # 记录开始时间
            print("1000会话响应数据准备完毕:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(conversation_list).encode())
                time3 = time.time()  # 记录开始时间
                print("完成写入socket时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            except IOError:
                print("socket.error : Connection broke. ")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # set the target where to mkdir, and default "D:/web"
        ServerRequestHandler.target = sys.argv[1]
    try:
        server = HTTPServer(("", 1769), ServerRequestHandler)
        print("HTTPServer started, serving at http://localhost:1769")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
