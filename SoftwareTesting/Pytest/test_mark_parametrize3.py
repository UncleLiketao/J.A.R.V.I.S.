import pytest

test_user_data = [
    {'user': 'linda', 'password': '8888'},
    {'user': 'servenruby', 'password': '123456'},
    {'user': 'test01', 'password': ''}
]


@pytest.fixture(scope='module')
def login_r(request):
    # 可以通过dict形式,虽然传递一个参数，但通过key的方式可以达到累死传入多个参数的效果
    user = request.param['user']
    pwd = request.param['password']
    print('\n打开首页准备登陆，登陆用户%s,密码%s' % (user, pwd))
    if pwd:
        return True
    else:
        return False


# 这是pytest参数化驱动,indeirect=True是把login_r当作函数去执行
@pytest.mark.parametrize('login_r', test_user_data, indirect=True)
def test_cart(login_r):
    # 登陆用例
    a = login_r
    print('测试用例中login_r的返回值%s' % a)
    assert a, '失败原因，密码为空'
