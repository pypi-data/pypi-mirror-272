"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/5/9 10:26:00
"""
import configparser
import json


def replace_values(json_obj, replace_dict):
    """
    替换json中的内容，替换
    :param json_obj:
    :param replace_dict:
    :return:
    """
    if isinstance(json_obj, dict):
        return {k: replace_values(v, replace_dict) for k, v in json_obj.items()}
    elif isinstance(json_obj, list):
        return [replace_values(element, replace_dict) for element in json_obj]
    else:
        return replace_dict.get(json_obj, json_obj)


def save_conf_var(ini_file):
    """
    根据ini文件，生成一个dict，用于替换json中的变量
    :param ini_file:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(ini_file)


def generate_value_to_jsonpath_map(obj, path='$'):
    value_to_path = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f'{path}.{key}' if path != '$' else f'$.{key}'
            if isinstance(value, (dict, list)):
                nested_paths = generate_value_to_jsonpath_map(value, new_path)
                for val, paths in nested_paths.items():
                    if val not in value_to_path:
                        value_to_path[val] = []
                    if isinstance(paths, list):
                        value_to_path[val].extend(paths)
                    else:
                        value_to_path[val].append(paths)
            else:
                if value not in value_to_path:
                    value_to_path[value] = []
                value_to_path[value].append(new_path)

    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = f'{path}[{index}]'
            if isinstance(value, (dict, list)):
                nested_paths = generate_value_to_jsonpath_map(value, new_path)
                for val, paths in nested_paths.items():
                    if val not in value_to_path:
                        value_to_path[val] = []
                    if isinstance(paths, list):
                        value_to_path[val].extend(paths)
                    else:
                        value_to_path[val].append(paths)
            else:
                if value not in value_to_path:
                    value_to_path[value] = []
                value_to_path[value].append(new_path)

    return value_to_path


if __name__ == '__main__':
    original_dict = [{"url": "https://aiob-open.baidu.com", "path": "/aiob-server/api/v2/getToken", "method": "POST", "headers": {"Content-Type": "application/json"}, "params": {}, "body": {"accessKey": "0600332f717442ae9198e3f39f22594b", "secretKey": "ed81a69cffb849c98f587a4b367a5151"}}, {"url": "https://aiob-open.baidu.com", "path": "/api/v1/did/list", "method": "GET", "headers": {"Authorization": "cc-api-auth-v2/10.D392A0628FDD362CED972BA925DC20D6C08796CA6D5D7FE89465FE3DA050A3EFE89A08C20A05204E939AA902D55BA058"}, "params": {}, "body": {}}]

    new_dict = generate_value_to_jsonpath_map(original_dict)
    print(json.dumps(new_dict))
