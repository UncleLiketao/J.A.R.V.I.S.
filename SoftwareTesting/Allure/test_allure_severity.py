import allure
import pytest


@allure.feature('test_module_01')
@allure.story('test_story_01')
@allure.severity('blocker')
def test_case_01():
    """
    用例描述：Test case 01
    """
    assert 0


@allure.feature('test_module_01')
@allure.story('test_story_01')
@allure.severity('critical')
def test_case_02():
    """
    用例描述：Test case 02
    """
    assert 0 == 0


@allure.feature('test_module_01')
@allure.story('test_story_02')
@allure.severity('normal')
def test_case_03():
    """
    用例描述：Test case 03
    """
    assert 0


@allure.feature('test_module_01')
@allure.story('test_story_02')
@allure.severity('minor')
def test_case_04():
    """
    用例描述：Test case 04
    """
    assert 0 == 0


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', './report/xml'])
