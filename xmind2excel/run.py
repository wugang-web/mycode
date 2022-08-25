# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 21:41
# @Author  : yuxiaocui
# @FileName: run.py
# @Software: PyCharm
import os

from loguru import logger

from testscript import xlsx2xmind, xmindtoxlsx


def run():
    print()
    logger.info("\n"
                "==================支持xmind转excel、excel转xmind================== \n"
                "--------------------------注意事项如下：--------------------------\n\n"
                "1.excel表格的表头名称必须为以下描述：用例名、前置条件、用例步骤、预期结果、需求ID、用例目录、用例状态、用例等级；其中用例状态可不填，列顺序不限 \n"
                "2.1 xmind版本要求:xmind转excel，xmind无版本要求；\t  excel转xmind后，需要使用xmind8或者xmind9打开，然后新建一个<画布>并保存。即可使用xmind2022打开 \n"
                "2.2 xmind备注里按照以下描述：前置条件、用例步骤、预期结果、需求ID；eg，前置条件 不可写成前提条件来表达\n"
                "3.对于当前未确定的需求的用例，可以在xmind标签设置为待更新\n"
                "4.对于有额外备注信息，可以在xmind的标注里填写，excel里通过备注列填写 \n \n"
                "================================================================="
                "\n"
                "")

    filePath = input(r"请输入要转换的excel或xmind文件名(带目录)：")
    ext = filePath.split(".")[-1]
    ext=ext.rstrip('"')

    filePath=filePath.lstrip('"').rstrip('"')

    if ext in ["xls", "xlsx"]:
        logger.info("开始进行excel转成xmind....")
        xlsx2xmind.excel_xmind(xlsx2xmind.get_case_data(filePath))
        logger.success("excel已成功转换成xmind~~~~")
        if ext=="xls":
            logger.info("xmind文件见:{0}".format(filePath[:-4] +"(1).xmind"))
        else:
            logger.info("xmind文件见:{0}".format(filePath[:-5] + "(1).xmind"))


    elif ext == "xmind":
        filePath = filePath.lstrip('"').rstrip('"')
        logger.info("开始进行xmind转成excel....")
        xmindtoxlsx.xmind_to_excel_file(filePath)
        logger.success("xmind已成功转换成excel")
        logger.info("excel文件见:{0}".format(filePath[:-6] + '(1).xlsx'))
    else:
        logger.error("待转换文件格式不支持；仅支持xlsx、xls、xmind")

    input("执行完成，按任意键退出")


if __name__ == '__main__':
    run()
#     pyinstaller -F -i ico.ico -n run_%date:~0,4%%date:~5,2%%date:~8,2%.exe run.py
