"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/5/8 16:56:00
"""
import json
from urllib.parse import urlparse, parse_qs


def analysis(har_file_path, res_file_path=None):
    """
    解析har文件，生成测试用例的json格式
    :param har_file_path: har文件路径
    :param res_file_path: 解析结果文件路径，如果为None，返回json格式字符串
    """
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_json = f.read()
    analysis_json(har_json, res_file_path)


def analysis_json(har_json, res_file_path=None):
    """
    解析har文件，生成测试用例的json格式
    :param har_json:
    :param res_file_path:
    :return:
    """
    har_dict = json.loads(har_json)
    json_output = {
        "caseName": "",
        "description": "",
        "priority": 0,
        "testSteps": []
    }

    # 提取 request 信息
    for index, entry in enumerate(har_dict['log']['entries']):
        request = entry['request']
        parsed_url = urlparse(request['url'])
        url = parsed_url.scheme + '://' + parsed_url.netloc
        path = parsed_url.path
        params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        body = request.get('postData', {})
        if 'json' in body.get('mimeType', ''):  # 检查MIME类型是否为JSON
            body = json.loads(body.get('text', '{}'))  # 是则解析
        step = {
            "step": index,
            "request": {
                "url": url,
                "path": path,
                "method": request['method'],
                "headers": {header['name']: header['value'] for header in request['headers']},
                "param": params,
                "body": body
            },
            "action": [],
            "assert": [
                {
                    "expect": "",
                    "actual": "",
                    "operator": ""
                }
            ]
        }
        json_output['testSteps'].append(step)

    # 输出结果
    res_str = json.dumps(json_output, indent=4)
    if res_file_path:
        with open(res_file_path, 'w', encoding='utf-8') as f:
            f.write(res_str)
        return res_str
    else:
        return res_str


if __name__ == '__main__':
    analysis('/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/通知机器人文本测试.har',
             '/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/通知机器人文本测试.json')