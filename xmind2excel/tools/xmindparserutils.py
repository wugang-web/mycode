# -*- coding: utf-8 -*-

import xmindparser
# https://www.5axxw.com/questions/content/5nr1rz

def flatten(d):
    """
    将嵌套字典列表，转换层单个字典列表
    :param d:
    :return:
    """
    try:
        key, lst = next((k, v) for k, v in d.items() if isinstance(v, list))
    except (StopIteration, AttributeError):
        return [d]
    return [{**d, **{key: v}} for record in lst for v in flatten(record)]

def get_case(dict_a):
    """
    获取单条测试用例
    :param dict_a:
    :return:
    """
    case = {"title": [],"note":"","labels":"","makers":"","callout":""}

    def dicts_to_dict(dict_a):
        """
        将多层字典，变成单层
        :param dict_a:
        :return:
        """
        if isinstance(dict_a, dict):
            for k, v in dict_a.items():
                if k=="title" :
                    case[k].append(v)
                    #print(case)
                if isinstance(v,dict) and k=="topics":
                    dicts_to_dict(v)
                if k=="note":
                    case[k]=v
                if k == "makers":
                    if isinstance(v,list):
                        priority=[p for p in v if p.startswith("priority")]
                        case[k]=priority[0]
                    else:
                        case[k] = v
                if k == "labels":
                    case[k] = v
                if k == "callout":
                    case["callout"] = v[0]
                #测试数据是否正常
                #print(case)

    dicts_to_dict(dict_a)
    #if "priority" not in case["makers"]:
    #    return {}
    #print(case)
    return case

def get_cases(xmindfile):
    """
    获取所有测试用例数据
    :param xmindfile:
    :return:
    """
    contentdatas = xmindparser.xmind_to_dict(xmindfile)
    #print(contentdatas)
    casedatas = []
    for contentdata in contentdatas:
        caselists = flatten(contentdata["topic"])
        #print(caselists)
        for caselist in caselists:
            caseDict = get_case(caselist)
            #print(caseDict)
            #print(bool(caseDict))
            #if bool(caseDict)== False:
            casedatas.append(caseDict)
                #print(caselists)
                #print(casedatas)
    #可用于调试
    #print(casedatas)
    return casedatas

if __name__ == '__main__':
    get_cases(r'D:\work\学习记录\定制化\江苏银行\测试\江苏银行.xmind')
    ...
