import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def open_url(url):
    # 前置
    driver = webdriver.Chrome()
    driver.get(url)  # url为链接地址
    yield driver  # yield之前代码是前置，之后的代码就是后置。
    # 后置
    driver.quit()

@pytest.fixture()
def refresh_page(open_url):
    yield
    open_url.refresh()
