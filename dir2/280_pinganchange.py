import threading
import time
import os
import requests
import pymysql, time, random, xlrd, uuid

def att_post(base_url, pubkey, path):
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '123',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://passport.csdn.net',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    workbook = xlrd.open_workbook(path,"rb")
    table = workbook.sheet_by_name('Sheet1')
    dd = 0  # 循环测试测试
    kk = 0  # 累计发送条数
    while True:
        print("~~~~~~~~~~~~开始第%d次发送数据~~~~~~~~~~~" % dd)
        db = pymysql.Connect(host=host2, port=3306, user=user1, passwd=passwd1, db=db1, charset='utf8')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        gg = random.randint(1, 1)  # 选择数据的方式
        gg=1
        ww = random.randint(10, 3000)  # 发送数据条数
        print("查询了%d条数据" % ww)
        time_ss = 1
        if gg == 1:
            # cursor.execute("SELECT question,FaqId  FROM FaqSimilars ORDER BY RAND() limit %s" % str(
            #     ww + 8))  # 查出faq  SELECT question,FaqId  FROM FaqSimilars ORDER BY RAND() limit %s
            cursor.execute("select sim.question,sim.FaqId,la.c_value FROM b132073.faqsimilars as sim\
                inner join b132073.faqlabels as fla on (sim.FaqId = fla.FaqId) inner join t_labels as la on\
                (fla.LabelId = la.id) ORDER BY RAND() limit %s" % str(ww + 8))
            a = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =2 ORDER BY RAND() limit 1")  # 查出用户标签
            # labels = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =1 ORDER BY RAND() limit 1")  # 查出接入渠道
            # client = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =3 ORDER BY RAND() limit 1")  # 查出业务入口
            # eid = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =4 ORDER BY RAND() limit 1")  # 查出使用角色
            # cid = cursor.fetchall()  # 使用 fetchone() 方法获取一条数据
            i = 0
            form_data = {}
            while i < ww:
                dz_type = i + random.randint(1, 4)
                form_data["pubkey"] = pubkey
                # form_data["cid"] = cid[0][0]
                form_data["sessionId"] = "sql_" + str(uuid.uuid1())  # "dcdz_"+str(round(time.time() * 1000))
                form_data["account"] = "Sql@wezhuiyi.com"
                form_data["ip"] = str(table.cell(i, 0).value)
                form_data["client"] = a[i][2]
                # form_data["labels"] = labels[0][0]
                # form_data["client"] = client[0][0]
                # form_data["eid"] = eid[0][0]
                feedback_data = {}
                while i < dz_type:
                    form_data["question"] = a[i][0]
                    # form_data["client"] = a[i][2]
                    r = requests.post(base_url, json=form_data, headers=headers)
                    b_rc = r.json()  # 回包数据
                    try:
                        anser_type = b_rc['type']
                        reject_sign = b_rc['reject_recog']
                        if b_rc['task_status'] == 1:
                            print("[第%d轮]【%d】%s:%s:第%d条流水,类型【%s】,命中【%s_%s】,耗时【%s】,问句:[%s]" % (dd, i, b_rc['sessionId'], b_rc['search_id'], i, anser_type, b_rc['answer_type'], b_rc['feature']['intent'][0]['intent_id'], b_rc['cost_ms'], b_rc['raw_query']))
                            print("[第%d轮]【%d】命中了任务型，不赞不踩下一条" % (dd, i))
                            i = i + 1
                            time.sleep(time_ss)
                        else:
                            print("[第%d轮]【%d】%s:%s:第%d条流水,类型【%s】,命中【%s_%s】,耗时【%s】,问句:[%s]" % (dd, i, b_rc['sessionId'], b_rc['search_id'], i, anser_type, b_rc['answer_type'], b_rc['info'][0]['id'], b_rc['cost_ms'], b_rc['raw_query']))
                            if anser_type == 200 and reject_sign != 1:
                                anser_confidence_01 = b_rc['info'][0]['confidence']
                                anser_confidence = int(float(b_rc['info'][0]['confidence']))
                                corre_water_feedback = b_rc['corre_water_feedback']
                                sessionId = b_rc['sessionId']
                                feedback_data["pubkey"] = pubkey
                                feedback_data["question"] = b_rc['raw_query']
                                feedback_data["docid"] = str(b_rc['info'][0]['id'])
                                feedback_data["op"] = "feedback"
                                if anser_confidence > 100:  # 如果是直接回答，且置信度大于75则进行点赞
                                    feedback_data["type"] = "2"
                                    feedback_data["reason"] = "赞赞赞~~~"
                                    print("[第%d轮]【%d】置信度是: 【%s】,赞一个哟~" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    time.sleep(time_ss)
                                    print("点赞发送数据%r" % feedback_data)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    print("点赞返回数据：%r" % f.json())
                                    i = i + 1
                                # 转人工
                                elif anser_confidence <= 100 and anser_confidence >= 99:  # 如果是直接回答，且置信度小于65则进行转人工
                                    feedback_data["type"] = "11"
                                    feedback_data["reason"] = "我要转人工，机器人解决不了我的问题"
                                    print("[第%d轮]【%d】置信度是: 【%s】,转人工处理！！" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    i = i + 1
                                    time.sleep(time_ss)
                                else:
                                    resons = ['答非所问', '看不明白', '答案方法不可行', '其他']
                                    feedback_data["type"] = "3"
                                    feedback_data["reason"] = resons[random.randint(0, 3)]
                                    print("[第%d轮]【%d】置信度是: 【%s】,踩踩踩！！【%s】" % (dd, i, anser_confidence_01, feedback_data['reason']))
                                 #    print("[第%d轮]【%d】置信度是: 【%s】,赞赞赞！" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    print(feedback_data)
                                    i = i + 1
                                    time.sleep(time_ss)
                            elif anser_type == 300:
                                print("[第%d轮]【%d】出了多个答案，不赞不踩下一条" % (dd, i))
                                print("[第%d轮]【%d】出了多个答案，不赞不踩下一条" % (dd, i))
                                i = i + 1
                                time.sleep(time_ss)
                            elif anser_type == 100:
                                print("[第%d轮]【%d】没有答案，不赞不踩下一条" % (dd, i))
                                i = i + 1
                                time.sleep(time_ss)
                            else:
                                print("[第%d轮]【%d】异常的类型，不点赞也不点踩，异常是：%s" % (dd, i, b_rc))
                                i = i + 1
                                time.sleep(time_ss)
                    except:
                        print("[第%d轮]【%d】返回数据异常，异常是：%s" % (dd, i, b_rc))
                        i = i + 1
                        time.sleep(time_ss)
                        # db.close()

                # a_aaa = r.json()  # 返回的数据
                # time.sleep(time_ss)  # 休息一会避免操作太快
                # try:
                #     corre_water_feedback = a_aaa['corre_water_feedback']
                #     sessionId = a_aaa['sessionId']
                #     feedback_data["pubkey"] = pubkey
                #     feedback_data["docid"] =str(b_rc['info'][0]['id'])
                #     cursor.execute("SELECT question  FROM Faqs where id =%s " %b_rc['info'][0]['id'])  # 查出faq
                #     faq_01 = cursor.fetchall()
                #     feedback_data["faq"] = str(faq_01[0][0])
                #     feedback_data["op"] = "feedback"
                #     feedback_data["type"] = "11"
                #     feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                #     feedback_data["sessionId"] = str(sessionId)
                #     print("发送的转人工数据是：%r"%feedback_data)
                #     print("[第%d轮]【%d】 发送第%d条转人工数据========" % (dd, i, i))
                #     f = requests.post(base_url, json=feedback_data, headers=headers)
                #     i = i + 1
                #     time.sleep(time_ss)
                # except:
                #     print("[第%d轮]【%d】返回异常，直接下一条" % (dd, i))
                #     i = i + 1
                #     time.sleep(time_ss)



        else:
            i = 0
            form_data = {}
            feedback_data = {}
            while i < ww:
                ni = random.randint(0, ww)
                form_data["ip"] = str(table.cell(ni, 0).value)
                form_data["pubkey"] = pubkey
                form_data["sessionId"] = "excl_" + str(uuid.uuid1())
                form_data["account"] = "Excel@wezhuiyi.com"
                j = 0
                while j < 1:
                    j+=1
                    form_data["question"] = table.cell(ni, 1).value
                    r = requests.post(base_url, json=form_data, headers=headers)
                    b_rc = r.json()  # 回包数据
                    try:
                        anser_type = b_rc['type']
                        reject_sign = b_rc['reject_recog']
                        if b_rc['answer_type'] == 'task':
                            print("[第%d轮]【%d】%s:%s:第%d条流水,类型【%s】,命中【%s_%s】,耗时【%s】,问句:[%s]" % (dd, i, b_rc['sessionId'], b_rc['search_id'], i, anser_type, b_rc['answer_type'], b_rc['feature']['intent'][0]['intent_id'], b_rc['cost_ms'], b_rc['raw_query']))
                            print("[第%d轮]【%d】命中了任务型，不赞不踩下一条" % (dd, i))
                            i = i + 1
                            time.sleep(time_ss)
                        else:
                            print("[第%d轮]【%d】%s:%s:第%d条流水,类型【%s】,命中【%s_%s】,耗时【%s】,问句:[%s]" % (dd, i, b_rc['sessionId'], b_rc['search_id'], i, anser_type, b_rc['answer_type'], b_rc['info'][0]['id'], b_rc['cost_ms'], b_rc['raw_query']))
                            if anser_type == 200 and reject_sign != 1:
                                anser_id = b_rc['info'][0]['id']
                                anser_confidence_01 = b_rc['info'][0]['confidence']
                                anser_confidence = int(float(b_rc['info'][0]['confidence']))
                                corre_water_feedback = b_rc['corre_water_feedback']
                                sessionId = b_rc['sessionId']
                                feedback_data["pubkey"] = pubkey
                                feedback_data["question"] = b_rc['raw_query']
                                feedback_data["docid"] = str(b_rc['info'][0]['id'])
                                feedback_data["op"] = "feedback"
                                # if anser_confidence > 73:  # 如果是直接回答，且置信度大于75则进行点赞
                                if anser_confidence > 95:
                                    feedback_data["type"] = "2"
                                    feedback_data["reason"]="赞一个哟~"
                                    print("[第%d轮]【%d】置信度是: 【%s】,赞一个哟~" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    time.sleep(time_ss)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    i = i + 1
                                elif anser_confidence <= 95 and anser_confidence >= 90:  # 如果是直接回答，且置信度小于65则进行点踩
                                    feedback_data["type"] = "11"
                                    feedback_data["reason"] = "什么垃圾回答，转人工，哈哈哈，这只是批跑测试数据"
                                    print("[第%d轮]【%d】置信度是: 【%s】,什么垃圾回答，转人工！！" % (dd, i, anser_confidence_01))
                                 #    print("[第%d轮]【%d】置信度是: 【%s】,赞赞赞！" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    print(feedback_data)
                                    i = i + 1
                                    time.sleep(time_ss)
                                else:
                                    feedback_data["type"] = "3"
                                    feedback_data["reason"] = "什么垃圾回答，点踩"
                                    print("[第%d轮]【%d】置信度是: 【%s】,什么垃圾回答，踩踩踩！！" % (dd, i, anser_confidence_01))
                                 #    print("[第%d轮]【%d】置信度是: 【%s】,赞赞赞！" % (dd, i, anser_confidence_01))
                                    feedback_data["corre_water_feedback"] = str(corre_water_feedback)
                                    feedback_data["sessionId"] = str(sessionId)
                                    f = requests.post(base_url, json=feedback_data, headers=headers)
                                    print(feedback_data)
                                    i = i + 1
                                    time.sleep(time_ss)
                            elif anser_type == 300:
                                print("[第%d轮]【%d】出了多个答案，不赞不踩下一条" % (dd, i))
                                i = i + 1
                                time.sleep(time_ss)
                            elif anser_type == 100:
                                print("[第%d轮]【%d】没有答案，不赞不踩下一条" % (dd, i))
                                i = i + 1
                                time.sleep(time_ss)
                            else:
                                print("[第%d轮]【%d】异常的类型，不点赞也不点踩，异常是：%s" % (dd, i, b_rc))
                                i = i + 1
                                time.sleep(time_ss)
                    except:
                        print("[第%d轮]【%d】返回数据异常，异常是：%s" % (dd, i, b_rc))
                        i = i + 1
                        time.sleep(time_ss)
                        # db.close()
        print("\n\n\n恭喜各位大佬，数据第%d轮已经制作完成，请前往业务检查是否符合心意哟~\n马上要开始下一次的数据发送啦，拜拜┏＾0＾┛" % dd)
        dd = dd + 1
        kk = kk + i
        print("累计发送数据为：%s" % kk)
        time.sleep(30)


if __name__ == "__main__":
    n = 1
    t_list = []
    for i in range(n):
       # base_url = "http://172.18.168.127/:8000/common/query?source="
        base_url = "http://172.18.167.149:8000/common/query?source="
        pubkey = "XFcElUgZshXM7eYadLE5E4xVEjVxMNButsp+XL4kHSg"
        host1 = '172.18.167.149'
        host2 = '172.18.167.149'
        user1 = 'root'  # web端user
        passwd1 = "uWXf87plmQGz8zMM"  # NpzQhB3r
        db1 = "b132073"  # b66538  b131075  b131074  b32964609
        path = 'D:/高灯问句（脚本访问).xls'
        t = threading.Thread(target=att_post, args=(base_url, pubkey, path))
        t.start()
        t_list.append(t)
for t in t_list:
    t.join()

