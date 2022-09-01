# -*- coding: utf-8 -*-
# @Time    : 2020/04/16
# @Author  : evan

"""
封装request

"""


import logging
import json
import requests


LOG = logging.getLogger(__name__)

class Request:
    def __init__(self):
        """
        :param env:
        """
        self.header = {
            'zhuiyi-business-id': '66537',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'private, no-store, max-age=0, no-cache, must-revalidate, post-check=0, pre-check=0',
            'Pragma': 'no-cache'
        }

    def get_request(self,url,cookies,header=None,timeout=10):
        """
        Get请求
        :param url:
        :param data:
        :param header:
        :return:

        """

        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            LOG.debug(url)

        try:
            if header is None:
                result = requests.get(url=url, headers=self.header, cookies=cookies,timeout=timeout)
                response = json.loads(result.text)
            else:
                result = requests.get(url=url, headers=header, cookies=cookies, timeout=timeout)
                response = json.loads(result.text)

        except requests.RequestException as e:
            LOG.debug('%s%s' % ('RequestException url: ', url))
            LOG.debug(e)
            return ()

        except Exception as e:
            LOG.debug('%s%s' % ('Exception url: ', url))
            LOG.debug(e)
            return ()

        return response

    def post_request(self,url,data,cookies,header=None,timeout=180):
        """
        Post请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            LOG.debug(url)
        try:
            if header is None:
                result = requests.post(url=url, data=data, headers=self.header,cookies=cookies, timeout=timeout)
                response = json.loads(result.text)
            else:
                result = requests.post(url=url, data=data, headers=header, cookies=cookies,timeout=timeout)
                response = json.loads(result.text)

        except requests.RequestException as e:
            LOG.debug('%s%s' % ('RequestException url: ', url))
            LOG.debug(e)
            return ()

        except Exception as e:
            LOG.debug('%s%s' % ('Exception url: ', url))
            LOG.debug(e)
            return ()

        return response


    def put_request(self,url,data,cookies,header=None,timeout=20):
        """
        Put请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            LOG.debug(url)
        try:
            if header is None:
                result = requests.put(url=url, data=data, headers=self.header,cookies=cookies, timeout=timeout)
                response = json.loads(result.text)
            else:
                result = requests.put(url=url, data=data, headers=header, cookies=cookies,timeout=timeout)
                response = json.loads(result.text)

        except requests.RequestException as e:
            LOG.debug('%s%s' % ('RequestException url: ', url))
            LOG.debug(e)
            return ()

        except Exception as e:
            LOG.debug('%s%s' % ('Exception url: ', url))
            LOG.debug(e)
            return ()

        return response

    def del_request(self,url,data,cookies,header=None,timeout=20):
        """
        Delete请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            LOG.debug(url)
        try:
            if header is None:
                result = requests.delete(url=url, data=data, headers=self.header,cookies=cookies, timeout=timeout)
                response = json.loads(result.text)
            else:
                result = requests.delete(url=url, data=data, headers=header, cookies=cookies,timeout=timeout)
                response = json.loads(result.text)

        except requests.RequestException as e:
            LOG.debug('%s%s' % ('RequestException url: ', url))
            LOG.debug(e)
            return ()

        except Exception as e:
            LOG.debug('%s%s' % ('Exception url: ', url))
            LOG.debug(e)
            return ()

        return response

if __name__ == '__main__':
    pass
