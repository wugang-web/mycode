# -*- coding: utf-8 -*-#

#-------------------------------——————————————————————————————
# Name:         gwg
# Description:  
# Author:       MiKo
# Date:         2022/6/9
#--------------------------------—————————————————————————————


# coding:utf-8



import hashlib
import random
import base64

accout="Botest@wezhuiyi.com"
ip ='127.0.0.1'
question="起飞"
sessionId ="sssdfsef"
time_stamp=str(random.randint(100000,1000000))
pubkey=input("请输入pubkey:")

privateKey=input("请输入privateKey:")

# raw_str = accout+ip+pubkey+question+sessionId+time_stamp+privateKey
raw_str= "132"+pubkey+privateKey
s=raw_str
#s = '18703609115127.0.0.1KVLE+uasdmS2WFAiO5bhK7Ph9YyyWTcJ5JJOhGZiqlM起飞sssdfsef15269931583f5db08824ad94798020a6bb34864ed7'
bs = (base64.b64encode(s.encode('utf-8')))     # 将字符为unicode编码转换为utf-8编码

code = (base64.b64encode(s.encode('utf-8'))).decode('utf-8')    #base64编码

#print(bs)    #-》 b'bmloYW8='

#print(code)   #//-》 bmloYW8=
md5 = hashlib.md5()     # 应用MD5算法
#
data = code
#
md5.update(data.encode('utf-8'))
sign=md5.hexdigest()
#
# print("account",accout)
# print("question",question)
# print("sessionId",sessionId)
# print("time_stamp",time_stamp)
# print("sign:",md5.hexdigest())
# print("pubkey:",pubkey)
all = """
"account":"{0}",
"pubkey":"{1}",
"question":"{2}",
"sessionId":"{3}",
"time_stamp":"{4}",
"sign":"{5}"
""".format(accout,pubkey,question,sessionId,time_stamp,sign)



print("{\n"+all+"}\n")
