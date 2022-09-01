# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: chen
# data:2020/12/28

import random
from datetime import datetime
from datetime import timedelta

# 语音坐席
AGENT_AUDIO = [
    ("1010", "黎攀登", "语音一组", "推广业务"),
    ("1011", "吴春如", "语音一组", "推广业务"),
    ("1012", "陈保兆", "语音一组", "推广业务"),
    ("1013", "潘启禾", "语音一组", "推广业务"),
    ("1014", "汪小娟", "语音二组", "电销业务"),
    ("1015", "祝玉永", "语音二组", "电销业务"),
    ("1016", "李牧哲", "语音二组", "电销业务"),
    ("1017", "谢鑫鑫", "语音三组", "售后业务"),
    ("1018", "徐栋梁", "语音三组", "售后业务"),
    ("1019", "任旺旺", "语音三组", "售后业务"),
]
# 文本坐席
AGENT_TEXT = [
    ("2020", "张兰霞", "文本一组", "销售业务"),
    ("2021", "陈江渝", "文本一组", "销售业务"),
    ("2022", "董超跃", "文本一组", "销售业务"),
    ("2023", "闫兆琪", "文本一组", "销售业务"),
    ("2024", "杨晶晶", "文本二组", "故障处理"),
    ("2025", "姚影影", "文本二组", "故障处理"),
    ("2026", "何梅梅", "文本二组", "故障处理"),
    ("2027", "王玉洁", "文本三组", "业务续期"),
    ("2028", "杨良琴", "文本三组", "业务续期"),
    ("2029", "刘国倩", "文本三组", "业务续期"),
]
# 客户信息
CUSTOMERS = [
    ("金蒙蒙", "13223654087"), ("宋怀顺", "18585693217"), ("谢怡平", "13049837605"), ("张三健", "13110849657"),
    ("郑宪威", "18539715628"), ("朱章章", "18897168024"), ("濮仁涛", "13304545676"), ("钱生旺", "14701853962"),
    ("张振康", "18539715628"), ("梁荣中", "13324545679"), ("黄勇强", "13304545680"), ("程艳奇", "13958740293"),
    ("闻园杰", "13380726954"), ("潘大超", "13850942168"), ("谭天信", "15956781402"), ("陈家俊", "13505736914"),
    ("邹嘉乐", "15321835497"), ("赵迎康", "15826839145"), ("王学锋", "18224076583"), ("王佳华", "15984059627"),
    ("翁信仰", "13304545690"), ("李景全", "18224076583"), ("许圳庭", "15581640527"), ("丘振华", "14728475691"),
    ("刘志栋", "13637419586"), ("李樟洪", "18852961740"), ("田梅生", "13314545696"), ("吴立鹏", "13304543697"),
    ("刘西西", "13374545698"), ("巫永腾", "13334545693"), ("刁佳林", "18992730148"), ("孙利杨", "13169725138"),
    ("陈晓涛", "15318743509"), ("凡小春", "15532709518"), ("高以鹏", "13304545698"), ("朱富来", "13186345170")
]
# 语音存放地址
AUDIOS = [
    ("http://172.16.20.185:8248/public/audio/200921182.mp3", 734),
    ("http://172.16.20.185:8248/public/audio/20092016514957210001015200036b.mp3", 88),
    ("http://172.16.20.185:8248/public/audio/2009210925442188000101960003e7ec.mp3", 242),
    ("http://172.16.20.185:8248/public/audio/2009210937388828000101530003d71d.mp3", 227),
    ("http://172.16.20.185:8248/public/audio/2009210938215898000104800003e37f.mp3", 163),
    ("http://172.16.20.185:8248/public/audio/2009210938490871000104800003e39b.mp3", 124),
    ("http://172.16.20.185:8248/public/audio/2009210938558492000102480003e538.mp3", 200),
    ("http://172.16.20.185:8248/public/audio/2009210940388446000104800003e3f5.mp3", 93),
    ("http://172.16.20.185:8248/public/audio/2009210942043939000102430003d95a.mp3", 157),
    ("http://172.16.20.185:8248/public/audio/2009210943101694000104800003e459.mp3", 157),
]

ADD_KEYWORD = ["您好", "亲", "亲爱的", "您好啊", "早上好", "下午好", "晚上好", "尊敬的客户", "Hello", "Hi"]
DEL_KEYWORD = ["滚蛋", "滚", "讨厌", "怎么了", "招人烦", "滚滚滚", "又是你", "烦", "烦人", "不行"]


# 文本会话信息
def content_list_v2(agent_name, customer, start_time, end_time):
    return random.choice([
        [
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(0, 3))), "%Y-%m-%d %H:%M:%S"),
                "content": "%s，很高兴为您服务，请问有什么可以帮您的?"%random.choice(ADD_KEYWORD),
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(4, 5))), "%Y-%m-%d %H:%M:%S"),
                "content": "哦，你好，我想处理下我的违章",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(5, 7))), "%Y-%m-%d %H:%M:%S"),
                "content": "我是人工客服，麻烦您提供下咨询的车牌号，谢谢，为了不耽误您的时间，麻烦简单说下问题的",
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(7, 8))), "%Y-%m-%d %H:%M:%S"),
                "content": "陕A2Q65T",
                "messageType": 1
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(8, 10))), "%Y-%m-%d %H:%M:%S"),
                "content": "9月24号从西安曲江上高速去咸阳，发票开出来通行明细是从杨凌上的，公司无法报销",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(11, 12))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "怎么无法报销呢",
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(12, 13))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "上高速的地方不对啊",
                "messageType": 1
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(12, 13))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "通行明细上是杨凌 我从曲江上的怎么报销",
                "messageType": 1
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(13, 14))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "你搞笑的很",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(15, 18))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "尊敬的用户您好，您反馈的ETC开票的问题，申办由各发行机构处理发行，但通行费发票开具"
                           "工作现统一由交通部，财政部，国家税务总局三部委联合开发的票根发票平台处理完成，"
                           "很抱歉无法为您处理此问题，请您谅解，烦请您进入中国ETC服务小程序 - ETC发票（跳转至票"
                           "根小程序）- 联系客服 - 回复人工客服 - 转人工进行反馈处理，或者进入中国ETC服务小程序 "
                           "- 添加车辆 - 我要投 诉进行反馈处理，给您带来的不便敬请谅解~感谢您对ETC助手的支持。",
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(21, 23))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "好的，你给我发个短信吧，我按照这个流程处理一下",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(24, 25))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "好的，那请问还有什么可以帮您",
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(25, 26))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "暂时没有了，谢谢",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(27, 28))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "不客气，稍后请对我的服务进行打分，感谢您的来电，再见",
                "messageType": 2
            },
            {
                "name": customer,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(28, 29))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "嗯，再见",
                "messageType": 1
            },
            {
                "name": agent_name,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(29, 30))),
                                          "%Y-%m-%d %H:%M:%S"),
                "content": "再见",
                "messageType": 2
            }
        ],
        [
            {
                "name": agent_name,
                "content": "会话已开始",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(0, 2))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "%s，很高兴为您服务，请问有什么可以帮您的?"%random.choice(ADD_KEYWORD),
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(0, 3))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "如何注销ETC？",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(3, 4))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "这里是人工客服，您好，请您提供车牌号",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(4, 5))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "messageType": 1,
                "content": "陕A 8888",
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(5, 6))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "messageType": 2,
                "content": "[图片]",
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(7, 8))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问还有什么其他可以帮您",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(13, 14))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问还有什么可以帮您的吗？如果您没有其他问题了，这边即将结束会话，麻烦您稍后对我个人的服务"
                           "进行评价，祝您生活愉快。再见",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(17, 22))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "已发送评价请求",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(19, 24))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "当前会话已结束",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(28, 29))),
                                          "%Y-%m-%d %H:%M:%S"),
            }
        ],
        [
            {
                "name": agent_name,
                "content": "会话已开始",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(0, 2))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "%s，很高兴为您服务，请问有什么可以帮您的?"%random.choice(DEL_KEYWORD),
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(1, 4))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": " 发票少开",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(3, 5))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "已为您接入人工服务，请问您在票根上面看到通行记录了吗？",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(8, 9))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "看了。",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(9, 10))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "勾选需要开票的通行记录去开票就可以的",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(12, 15))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "[图片]",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(12, 13))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "[图片]",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(13, 14))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "有三笔扣款，但票根里面没有",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(15, 16))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "为什么",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(16, 18))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问是什么时候扣费成功的呢？",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(21, 24))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "第一个图片有时间啊",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(24, 27))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "是十月份扣费成功的吗？",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(28, 33))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "是的",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(33, 34))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "确认已扣费超7个自然日未在票根查询到通行记录\n您可登录票根官网www.txffp.com/票根APP/票根微信公众号/"
                           "点击在线客服，自助工单-填写相关情况-上报后会有相关工作人员给您处理您可以随时查询工单进度。",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(38, 42))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "10.8/10.14/10.16",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(44, 45))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "登录票根官网www.txffp.com/票根APP/票根微信公众号填写自助工单上报之后会有相关工作人员给您处理的",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(46, 49))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "用手机号登陆吗",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(52, 54))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "首次登录票根平台需凭手机号码注册并设置密码",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(55, 58))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "后面用手机号+密码登录即可",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(60, 62))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问还有其它可以帮您的吗？",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(68, 71))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "如果没有其它可以帮您麻烦稍后对我服务进行评价，稍后如果您还有疑问，可以继续接入人工在线客服"
                           "（客服上班时间：周一到周日09:00--21:00），祝您生活愉快，再见！",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(74, 78))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "已发送评价请求",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(80, 82))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "哪里有自助工单",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(83, 84))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "票根官网www.txffp.com/票根APP/票根微信公众号都可以填写自助工单",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(85, 88))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问还有其它可以帮您的吗？",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(90, 92))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "如果没有其它可以帮您麻烦稍后对我服务进行评价，稍后如果您还有疑问，可以继续接入人工在线客服（客服"
                           "上班时间：周一到周日09:00--21:00），祝您生活愉快，再见！",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(96, 98))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "已发送评价请求",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(99, 102))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "当前会话已结束",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(102, 107))),
                                          "%Y-%m-%d %H:%M:%S"),
            }
        ],
        [
            {
                "name": agent_name,
                "content": "会话已开始",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(0, 2))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "%s，很高兴为您服务，请问有什么可以帮您的?"%random.choice(DEL_KEYWORD),
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(1, 4))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "我反映的问题什么时候能处理好",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(3, 5))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "欢迎进入追一人工服务，稍等我看下",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(6, 8))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "发票一直在开票中是么",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(13, 16))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "是的",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(15, 17))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您这边自己传了分机号了么",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(19, 21))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "什么意思",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(24, 26))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "分机号是对的呀",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(26, 27))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "你们怎么一会一个花样精",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(27, 29))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "因为您是接口开票的，切到云平台的，门店管理没有关联税盘，您传分机号了么，如果传了就按照实际的 2号分机"
                           "传个 2 就好了，如果没传用的云平台的，就直接重新申请一单试试",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(30, 35))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "一会让我这个截图，一会又是那样截图",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(34, 42))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您可以看下",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(40, 44))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "[图片]",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(44, 45))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "上午我有发截图给你们",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(44, 45))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "重试了很多次了",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(45, 47))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "稍等",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(48, 52))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "你们要的所有的截图我都给你们发了，不要兜兜转转老是说那几个问题，到底能不能解决",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(50, 54))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "稍等帮您核实",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(55, 58))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您这边重新开一张试一下",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(58, 62))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "我这边都是客户在手机上直接开的",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(62, 63))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "而且也有今天早上",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(63, 64))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "因为您这边点击重试开票是开不出来的",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(67, 70))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "也是一直在开票中",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(70, 74))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您这边需要重新开",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(80, 82))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "那就是说以后客户手机上申请都不行了吗",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(82, 85))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "都是需要我手工开吗",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(87, 92))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您这边是接口开票的",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(92, 93))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您可以重新开一张试一下，如果可以，那么就可以正常开了",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(93, 95))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "那我现在开票中怎么办呢",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(97, 102))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "开票中他是开不出来的呢",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(100, 104))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "请问还有什么可以帮到您吗",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(104, 105))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "您好！如果没有其他的疑问，这边将结束会话，麻烦对本次服务进行评价，祝您生活愉快。再见！",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(105, 109))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": customer,
                "content": "已发送评价请求",
                "messageType": 1,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(109, 110))),
                                          "%Y-%m-%d %H:%M:%S"),
            },
            {
                "name": agent_name,
                "content": "当前会话已结束",
                "messageType": 2,
                "time": datetime.strftime((start_time + timedelta(seconds=random.randint(114, 115))),
                                          "%Y-%m-%d %H:%M:%S"),
            }],
    ])


