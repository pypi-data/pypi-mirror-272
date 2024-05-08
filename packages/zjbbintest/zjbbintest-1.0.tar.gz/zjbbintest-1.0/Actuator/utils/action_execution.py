"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/20 19:02:00
"""
from Actuator.utils.string_dynamic_run import StringDynamicRun


class BatchActionExecutor:
    """
    Batch action executor.
    批量动作执行器
    """

    def __init__(self, action_list):
        """
        Init batch action executor.
        初始化批量动作执行器
        :param action_list: 动作列表
        :type action_list: list
        """
        self.__action_list = action_list

    def execute(self, case_var_dict, req_list, resp_list):
        """
        Execute batch action.
        执行批量动作
        :return: 返回结果
        :rtype: list
        """
        for action in self.__action_list:
            _, case_var_dict = StringDynamicRun(action, case_var_dict, req_list, resp_list).run()
        return case_var_dict
