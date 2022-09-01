# -*- coding: utf-8 -*-
# @Time    : 2020/5/26
# @Author  : Amanda

import yaml
import os

class getyamldata():
    def get_yaml_data(self, test_data_path):
        case = []  # 保存测试用例名称
        http = []  # 保存请求对象
        expected = []  # 保存预期结果
        with open(test_data_path, encoding='utf-8') as f:
            dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
            test = dat['tests']
            for it in test:
                case.append(it.get('case', ''))
                http.append(it.get('http', {}))
                expected.append(it.get('expected', {}))
        parameters = zip(case, http, expected)
        return parameters

    def read_yaml_params_byfilename(self, yaml_file_name):
        datapath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/yaml/',
                                yaml_file_name)
        parameters = self.get_yaml_data(datapath)
        list_params = list(parameters)
        return list_params

if __name__ == '__main__':
    pass
