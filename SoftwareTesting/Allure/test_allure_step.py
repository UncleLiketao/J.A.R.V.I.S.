﻿import allure
import pytest

@allure.step("字符串相加：{0}，{1}")
# 测试步骤，可通过format机制自动获取函数参数
def str_add(str1, str2):
    if not isinstance(str1, str):
        return "%s is not a string" % str1
    if not isinstance(str2, str):
        return "%s is not a string" % str2
    return str1 + str2

@allure.feature('test_module_01')
@allure.story('test_story_01')
@allure.severity('blocker')
def test_case():
    str1 = 'hello'
    str2 = 'world'
    assert str_add(str1, str2) == 'helloworld'


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', './report/xml'])
