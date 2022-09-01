# -*- coding: utf-8 -*-
"""
管理员账号登录产品页面
"""
import requests
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from gmssl import sm2

class Login_v3(object):

    def crack_pwd(self,pwd,nodeHost,ingressPort,login_header):
        """
        对账号密码进行加密
        """
        cipherMode = self.get_cipher_mode(nodeHost,ingressPort,login_header)
        if cipherMode == "RSA":
            key = "-----BEGIN PUBLIC KEY-----\n" + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlwS6f4FBSHKDgg8Tti2YXW6ic8BGLeoKI8IuXEUy0q2cV53DcJ7ON55oXuuDuBRLE6PanT86gcoRTp1IOTKjI7fga3arIaWjYubEBzCLUlTPQx/jjO0/mWarj4yvKzk6Ulo/uXWumR+dx0dYiGtbJQlClgILvYtxNHQB7uXWPjwIDAQAB" + "\n-----END PUBLIC KEY-----"
            rsakey = RSA.importKey(key)
            # 生成对象
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            # 对传递进来的用户名或密码字符串加密
            cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))
            # 将加密获取到的bytes类型密文解码成str类型
            value = cipher_text.decode('utf8')
        elif cipherMode == "SM2":
            # SM2公钥
            public_key = "MFkwEwYHKoZIzj0CAQYIKoEcz1UBgi0DQgAEfHNFIiu378956f7iZ8/G4OYwLCiqyPO6ezEjfZs93viGngW1OBteDlSlKupQlGBILCjqK0iSyIFw7C1S5nn31Q=="
            # 将公匙转化为16进制字符串
            public_key = base64.b64decode(public_key).hex()
            public_key = str.upper(public_key)
            if len(public_key) >= 128:
                public_key = public_key[len(public_key) - 128:]
                # 初始化CryptSM2
            sm2_crypt = sm2.CryptSM2(private_key=None, public_key=public_key)
            # 加密数据为bytes类型
            enc_data = sm2_crypt.encrypt(pwd.encode(encoding="utf-8")).hex()
            value = '04' + enc_data
        else:
            value = cipherMode
        return value

    def get_cipher_mode(self,nodeHost,ingressPort,login_header):
        """
        获取aiforce加密方式
        """
        cipherMode = "get cipher mode error!"
        url = 'http://' + nodeHost + ':' + ingressPort + '/ng-aiforce/aiforce/v1/common/publickey'
        res = requests.get(url,headers=login_header, timeout=60)
        data = json.loads(res.text)['data']
        if 'type' in data and data['type'] != None:
            if data['type'] == "SM2":
                cipherMode = "SM2"
            elif data['type'] == "RSA":
                cipherMode = "RSA"
            else:
                pass
        if 'rsaNote' in data:
            cipherMode = "RSA"
        return cipherMode

    def admin_login(self, account, password, nodeHost, ingressPort):
        """
        返回登录aiforce的cookies
        """
        #定义请求头
        login_header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'http://' + nodeHost + ":" + ingressPort,
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://' + nodeHost + ":" + ingressPort + "/ng-aiforce/",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'XSRF-TOKEN=b1ea29ee-b38f-4793-8f22-17f236913d1c',
            'X-XSRF-TOKEN': 'b1ea29ee-b38f-4793-8f22-17f236913d1c'
        }

        login_url = 'http://' + nodeHost + ":" + ingressPort + '/ng-aiforce/aiforce/authentication/v1/sessions'

        pwd = self.crack_pwd(pwd=password, nodeHost=nodeHost, ingressPort=ingressPort,login_header=login_header)
        login_data = {
            'username':account,
            'password':pwd
        }

        userlogin = requests.post(login_url,data=login_data,headers=login_header,timeout=180, verify=False)
        cookies = userlogin.cookies.get_dict()
        return cookies

    def get_web_cookie(self, account, password, nodeHost, ingressPort):
        """
        Learn3.0版本之后获取登陆cookie
        """

        # 1、获取aiforce的cookies
        aiforce_cookie = self.admin_login(account, password, nodeHost, ingressPort)

        # 2、通过aiforce的cookies获取see的cookies
        see_headers = {'cookie': ';'.join(['{}={}'.format(*_) for _ in aiforce_cookie.items()])}
        see_url = "http://" + nodeHost + ":" + ingressPort + "/gateway/user/info"
        see_result = requests.get(see_url, headers=see_headers, allow_redirects=False)
        see_cookies = see_result.cookies.get_dict()

        # 3、通过see的cookies去访问auth鉴权，通过响应体中的Location获取回调url
        headers = {
            'cookie': ';'.join(['{}={}'.format(*_) for _ in aiforce_cookie.items()]) + ";" + ';'.join(['{}={}'.format(*_) for _ in see_cookies.items()])
        }
        aiforce_url = "http://" + nodeHost + ":" + ingressPort + "/ng-aiforce/aiforce/authentication/oauth/authorize?client_id=see&redirect_uri=http://" + nodeHost + ":" + ingressPort + "/gateway/auth/oauth2/callback&response_type=code&state=1230"
        resp = requests.get(url=aiforce_url, headers=headers, allow_redirects=False)
        location = resp.headers['Location']

        # 4、访问回调请求，如果回调成功，说明步骤2中获取到的cookies合法
        callback_url = location
        result = requests.get(url=callback_url,headers=headers, allow_redirects=False)
        if result.status_code == 302:
            return headers
        else:
            print("获取登录的cookie失败")
            exit(1)

    def tansfer_bussiness(self, base_url, base_head, busId):
        """
        通过busId切换业务
        """
        tansfer_url = base_url + "/gateway/user/change-instance/" + str(busId)
        requests.post(tansfer_url,data="",headers=base_head,timeout=5, verify=False)

if __name__ == '__main__':
    print(Login_v3().get_web_cookie("example@wezhuiyi.com", "T2OUI2K8", "172.18.166.97", "80"))
    # print(Login_v3().admin_login("example@wezhuiyi.com", "T2OUI2K8", "172.18.166.97", "80"))
    # pass