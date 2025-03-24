import pytest
from testcases.conftest import api_data  # 导入 api_data 模块，通常是自定义的，负责获取测试数据

@pytest.fixture(scope="function")  # 定义一个fixture，作用范围是函数级别（每个测试用例都会调用）
def testcase_data(request):
    testcase_name = request.function.__name__  # 获取当前测试用例的名称
    return api_data.get(testcase_name)  # 获取与测试用例名对应的数据，并返回
