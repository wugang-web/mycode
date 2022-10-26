# -*- coding: utf-8 -*-#

#-------------------------------——————————————————————————————
# Name:         clear
# Description:  
# Author:       MiKo
# Date:         2022/10/24
#--------------------------------—————————————————————————————

from paramiko.ssh_exception import AuthenticationException
import threading
import time
import os
import requests
import sys
import pymysql, time, random, xlrd, uuid

import paramiko

def clear_caches(host2):
    print("------开始清除清除缓存---")
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    try:
        ssh.connect(host2, username="root", port=22, password="Dl7mdkzbMLwe0FBu")
    except AuthenticationException as e:
        print("账号或密码错误!")
    # ssh.connect(host2, username="ops", port=22, password="zhuiyi")
    # 使用这个连接执行命令
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sync; echo 3 > /proc/sys/vm/drop_caches")
    time.sleep(1)
    # 获取输出
    result = ssh_stdout.read()
    print(result.decode('utf-8'))
    print("------清除缓存成功-------")
    # 关闭连接
    ssh.close()

def clear_taskLine(host2):
    #workbook = xlrd.open_workbook(path,"rb")
    #table = workbook.sheet_by_name('Sheet1')
    print("~~~~~~~~~~~~开始清除排队中任务~~~~~~~~~~~" )
    # db = pymysql.Connect(host=host2, port=3306, user=user1, passwd=passwd1, db=db1, charset='utf8')  # 打开数据库连接
    # cursor = db.cursor()  # 使用cursor()方法获取操作游标

    db2 = "data_platform"
    db1 = pymysql.Connect(host=host2, port=3306, user="root", passwd="uWXf87plmQGz8zMM", db=db2, charset='utf8')
    cursor1 = db1.cursor()
    list = [0,3,4]
    print("status: 0 ---排队中；1--正在执行；2 ---成功完成；3—失败（等待重试）；4—失败状态（不在重试）；5 ---无改动；6---已终止； 99—删除")
    for i in list:
        print("%d" %i)
        cursor1.execute("delete from task where status =%d" % i)
        time.sleep(2)
        db1.commit()
        if db1.affected_rows()==0:
            print("不存在该 %d 类型的任务,无需处理 " % i)
        else:
            assert db1.affected_rows() !=0,"删除失败"
            time.sleep(2)
            db1.commit()
            time.sleep(2)
            print("%d 类型删除成功 " % i)
    print("---0，3，4 类型删除成功,排队中已处理 ---")
    db1.close()
    ''' >>> host2 = '172.16.40.87'
        >>> user1 = 'root'  # web端user
        >>> passwd1 = "uWXf87plmQGz8zMM"  # NpzQhB3r'''




def change_CM(host2):
    print("---仅支持algorithm-platform训练平台  CPU,Memory 调节0.95额度中-----")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host2, username="root", port=22, password="Dl7mdkzbMLwe0FBu")
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("docker cp algorithm-platform:/data/data_platform/soft/backend/conf/admin.conf /tmp/")
    time.sleep(0.5)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sed -i 's/memory_limit=0.*/memory_limit=0.95/g'  /tmp/admin.conf")
    time.sleep(0.5)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sed -i 's/cpu_limit=0.*/cpu_limit=0.95/g'  /tmp/admin.conf")
    time.sleep(0.5)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("docker cp /tmp/admin.conf algorithm-platform:/data/data_platform/soft/backend/conf/admin.conf")
    time.sleep(0.5)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("docker restart algorithm-platform")
    print("重启中：请等待10秒中")
    time.sleep(10)
    print("---训练平台 CPU,Memory 调节0.95额度完成--训练平台重启成功")
        # gg = random.randint(1, 1)  # 选择数据的方式
        # gg=1
        # ww = random.randint(10, 3000)  # 发送数据条数
        # print("查询了%d条数据" % ww)
        # time_ss = 1
        # if gg == 1:
        #     # cursor.execute("SELECT question,FaqId  FROM FaqSimilars ORDER BY RAND() limit %s" % str(
        #     #     ww + 8))  # 查出faq  SELECT question,FaqId  FROM FaqSimilars ORDER BY RAND() limit %s
        #     cursor.execute("select sim.question,sim.FaqId,la.c_value FROM b132073.faqsimilars as sim\
        #         inner join b132073.faqlabels as fla on (sim.FaqId = fla.FaqId) inner join t_labels as la on\
        #         (fla.LabelId = la.id) ORDER BY RAND() limit %s" % str(ww + 8))
        #     a = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =2 ORDER BY RAND() limit 1")  # 查出用户标签
            # labels = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =1 ORDER BY RAND() limit 1")  # 查出接入渠道
            # client = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =3 ORDER BY RAND() limit 1")  # 查出业务入口
            # eid = cursor.fetchall()
            # cursor.execute("SELECT value  FROM Labels where type =4 ORDER BY RAND() limit 1")  # 查出使用角色






if __name__ == "__main__":
    n = 1
    t_list = []
    print("运行需安装threading和paramiko 两个python库")
    host2 = input("请输入需要清理的机器IP地址(训练平台仅支持algorithm-platform):")
    print("请输入需要清理的机器IP地址(训练平台仅支持algorithm-platform")
    #host2 = sys.stdin.readline()
    #host2 = '172.16.50.136'
    print("缓存，排队中，训练平台 CPU,Memory 已调节至0.95 多线程执行中")
    for i in range(n):
        # change_CM(host2)
        # clear_caches(host2)
        # clear_taskLine(host2)

        t1 = threading.Thread(target=change_CM, args=(host2,))
        t1.start()
        t_list.append(t1)
        t2 = threading.Thread(target=clear_caches, args=(host2,))
        t2.start()
        t_list.append(t2)
        print(t_list)
        t3 = threading.Thread(target=clear_taskLine, args=(host2,))
        t3.start()
        t_list.append(t3)
    for t in t_list:
     t.join()
    input("缓存，排队中，训练平台 CPU,Memory 已调节至0.95 均已完成")

