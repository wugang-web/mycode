# -*- coding: utf-8 -*-

"""
管理员账号登录产品页面
"""

import requests
import uuid
import logging
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

class Login_v2(object):

    def crack_pwd(self,pwd):
        """
        对账号密码进行加密
        """
        key = "-----BEGIN PUBLIC KEY-----\n"+"MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlwS6f4FBSHKDgg8Tti2YXW6ic8BGLeoKI8IuXEUy0q2cV53DcJ7ON55oXuuDuBRLE6PanT86gcoRTp1IOTKjI7fga3arIaWjYubEBzCLUlTPQx/jjO0/mWarj4yvKzk6Ulo/uXWumR+dx0dYiGtbJQlClgILvYtxNHQB7uXWPjwIDAQAB"+"\n-----END PUBLIC KEY-----"	
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
        cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
        value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
        return value

    def admin_login(self,account,password,aiforceIP,aiforcePort):
        """
        返回登录cookies
        """
        #定义请求头
        login_header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'http://' + aiforceIP,
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://' + aiforceIP,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'XSRF-TOKEN=b1ea29ee-b38f-4793-8f22-17f236913d1c',
            'X-XSRF-TOKEN': 'b1ea29ee-b38f-4793-8f22-17f236913d1c'
        }


        login_url = 'http://' + aiforceIP + ':' + aiforcePort+ '/aiforce/authentication/v1/sessions'

        pwd = self.crack_pwd(pwd=password)
        login_data = {
            'username':account,
            'password':pwd
        }

        userlogin = requests.post(login_url,data=login_data,headers=login_header,timeout=5)
        cookies = userlogin.cookies.get_dict()

        return cookies

    def admin_logout(self,account,password,hostIP,hostPort,bId,aiforceIP,aiforcePort):
        """
        返回退出状态
        """
        #定义请求头
        login_header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        logout_url = 'http://' + hostIP + ':' + hostPort + '/util/clear-token?businessId='+bId
        cookies = self.admin_login(account=account,password=password,aiforceIP=aiforceIP,aiforcePort=aiforcePort)

        requests.get(logout_url,headers=login_header,cookies=cookies)
        return

    def get_web_cookie(self, hostIP, hostPort, account, password, aiforceIP, aiforcePort):
        '''
        获取前端cookie
        '''
        # 获取aiforce的cookie
        aiforce_cookie = self.admin_login(account, password, aiforceIP, aiforcePort)

        login_header = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://" + aiforceIP,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Cookie": "aiforce=" + aiforce_cookie['aiforce']
        }

        web_cookie = requests.get("http://" + hostIP + ":" + hostPort + "/quality", headers=login_header).cookies.get_dict()

        return web_cookie, aiforce_cookie

if __name__ == '__main__':
    print(Login_v2().get_web_cookie("172.16.20.185", "8248","zjzzcheck@qq.com", "abcd1234", "172.16.20.185", "40080"))


