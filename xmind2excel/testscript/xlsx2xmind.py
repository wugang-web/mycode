import csv
import os
import re

import pandas as pd

import xmind

# http://www.javashuo.com/article/p-rgivewak-nh.html
# https://zhuanlan.zhihu.com/p/47835857
# http://t.zoukankan.com/baby123-p-15615673.html

def xlsx_to_csv(xlsxPath):
    """
    利用pandas将xlsx格式的文件转换成csv
    :param xlsxPath: xlsx文件的路径
    :return:
    """
    # 设置生成csv文件的路径
    toCSVPath = xlsxPath[:-5] + '.csv'
    # 使用index_col=0，直接将第一列作为索引，不额外添加列。
    data = pd.read_excel(xlsxPath)
    new_columns = ['用例名称', '前置条件', '用例步骤', '预期结果', '需求ID', '用例目录', '用例状态', '用例等级',"备注"]
    # 重建索引
    data_new = data.reindex(columns=new_columns)

    # index=False,直接将第一列作为索引，不额外添加列
    data_new.to_csv(toCSVPath, encoding="utf-8",index = False)

    return toCSVPath


def get_case_data(xlsxPath):
    csv_path=xlsx_to_csv(xlsxPath)
    data = []
    with open(csv_path, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return  data,csv_path

def excel_xmind(case_data):
    """
    将excel文件转换成xmind
    :param datas:
    :param filePath:
    :return:
    """
    datas, filePath=case_data[0],case_data[1]
    # 创建xmind文件
    xmindPath = filePath[:-4] + "(1).xmind"
    if os.path.exists(xmindPath):
        os.remove(xmindPath)
    titleName = os.path.basename(xmindPath).split(".")[0]

    workbook = xmind.load(xmindPath)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle(titleName)


    # 创建根节点并设置主题名称
    root = sheet.getRootTopic()
    root.setTitle(datas[1][5].split(" - ")[0])


    for data in datas[1:]:
        caseTitle=data[0]
        pre_step=re.sub("\n+","\n",data[1].strip())
        case_step=re.sub("\n+","\n",data[2].strip())
        result=re.sub("\n+","\n",data[3].strip())
        demand_ID=re.sub("\n+","\n",data[4].strip())
        try:
            demand_ID=demand_ID.split(".")[0]
        except:
            demand_ID=demand_ID
        case_module=data[5]
        case_status=data[6]
        case_level=data[7]
        callout=data[8]
        f=case_module.split(" - ")
        f.append(caseTitle)

        # pointer为当前节点的位置
        pointer = root

        for i in range(1, len(f)):
            # 判断当前节点所有节点是否存在这个路径值，不存在则创建节点，然后更改pointer位置为创建节点的位置
            # 如果存在，则把pointer节点位置赋值到存在节点位置处

            if f[i] not in [Topic.getTitle() for Topic in  pointer.getSubTopics()]:
                node = pointer.addSubTopic()
                node.setTitle(f[i])
                pointer=node

            else:
                subTopic=pointer
                for Topic in  pointer.getSubTopics():
                    if Topic.getTitle()==f[i]:
                        subTopic=Topic
                        break
                pointer = subTopic

        # 为节点添加备注
        nodes = '前置条件\r\n{0}\r\n\r\n用例步骤\r\n{1}\r\n\r\n预期结果\r\n{2}\r\n\r\n需求ID\r\n{3}'.format(pre_step,case_step, result, demand_ID)
        pointer.setPlainNotes(nodes)

        # 如果用例的状态为待更新，则添加一个红旗做标记
        if case_status == "待更新":
            pointer.addLabel("待更新")

        # 添加后，在xmind新版本异常
        # # 把备注信息添加到批注那里
        # if len(callout) != 0:
        #     pointer.addComment(callout)

        if len(case_level) != 0:
            pointer.addMarker("priority-" + str(int(case_level[-1]) + 1))


    xmind.save(workbook)


if __name__ == '__main__':
    xlsx_path = r'"D:\project\bot3.0\第二次用例\导入导出任务管理.xlsx"'
    xlsx_path= xlsx_path.lstrip('"').rstrip('"')
    excel_xmind(get_case_data(xlsx_path))
