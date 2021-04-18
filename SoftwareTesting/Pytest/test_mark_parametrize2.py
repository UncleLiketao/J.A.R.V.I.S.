import pytest

test_user_data = ['linda', 'sai', 'tom']


@pytest.fixture(scope='module')
def login(request):
    user = request.param
    print('打开首页登陆%s' % user)
    return user


# indirect=True是把login当作函数去执行
@pytest.mark.parametrize('login', test_user_data, indirect=True)
def test_cart(login):
    usera = login
    print('不同用户添加购物车%s' % usera)
    assert usera != ''
