"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/5/9 10:26:00
"""
import configparser


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
