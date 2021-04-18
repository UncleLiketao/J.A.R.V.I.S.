# test_Pytest.py文件
# coding=utf-8

import pytest


class Test_Pytest():

    @pytest.mark.xfail
    def test_one(self, ):
        print("----start------")
        print("test_one方法执行")
        assert 1 == 1

    def test_two(self):
        print("test_two方法执行")
        assert "o" in "love"

    def test_three(self):
        print("test_three方法执行")
        assert 3 - 2 == 1


if __name__ == "__main__":
    pytest.main(['-s', '-r', 'test_Pytest.py', 'test_Pytest.py'])
