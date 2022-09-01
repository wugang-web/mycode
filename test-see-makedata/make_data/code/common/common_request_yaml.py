# -*- coding: utf-8 -*-
# @Time    : 2021/05/01
# @Author  : zhoulingzhi

import json
from code.common.common_request import Request

class Common_request_yaml(object):

    def see_post_request(self, base_url, base_head, http):
        '''
        Post请求
        '''

        # 替换端口号，拼接请求url
        base_url = base_url + http['path']

        # 请求体参数
        data = http['params']

        resp = Request().post_request(url=base_url, data=json.dumps(data), cookies=None, header=base_head)
        # print(resp)

        return resp    

    def see_get_request(self, base_url, base_head):
        '''
        GET请求
        '''

        resp = Request().get_request(url=base_url, header=base_head)
        return resp


if __name__ == '__main__':
    pass