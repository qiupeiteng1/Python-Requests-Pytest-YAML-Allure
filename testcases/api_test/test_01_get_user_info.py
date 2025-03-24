import pytest
import allure
from operation.user import get_all_user_info, get_one_user_info  # 导入用户信息相关的操作方法
from testcases.conftest import api_data  # 导入测试数据
from common.logger import logger  # 导入日志模块


@allure.step("步骤1 ==>> 获取所有用户信息")
def step_1():
    """日志记录步骤1，获取所有用户信息"""
    logger.info("步骤1 ==>> 获取所有用户信息")


@allure.step("步骤1 ==>> 获取某个用户信息")
def step_2(username):
    """
    日志记录步骤1，获取指定用户信息
    :param username: 要查询的用户名
    """
    logger.info("步骤1 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.TRIVIAL)  # 设置测试用例的重要级别
@allure.epic("针对单个接口的测试")  # 设置测试模块的标题
@allure.feature("获取用户信息模块")  # 设置测试功能模块名称
class TestGetUserInfo():
    """获取用户信息模块的测试用例"""

    @allure.story("用例--获取全部用户信息")  # 定义子模块
    @allure.description("该用例是针对获取所有用户信息接口的测试")  # 用例描述
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")  # 关联Bug链接
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")  # 关联测试用例链接
    @pytest.mark.single  # 打上 single 标记，方便分类执行
    @pytest.mark.parametrize("except_result, except_code, except_msg",
                             api_data["test_get_all_user_info"])  # 参数化测试用例
    def test_get_all_user_info(self, except_result, except_code, except_msg):
        """
        测试获取所有用户信息接口
        :param except_result: 预期的执行结果（布尔值）
        :param except_code: 预期的返回码
        :param except_msg: 预期的返回信息
        """
        logger.info("*************** 开始执行用例 ***************")
        step_1()  # 记录步骤
        result = get_all_user_info()  # 调用获取所有用户信息的接口
        assert result.response.status_code == 200  # 断言 HTTP 状态码是否为 200
        assert result.success == except_result, result.error  #断言 result.success 是否和 except_result 期望值一致.如果不一致，则返回 result.error 详细错误信息
        logger.info("code ==>> 期望结果：{}， 实际结果：{}".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code  # 断言返回码是否符合预期
        assert except_msg in result.msg  # 断言返回信息是否包含预期内容
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--获取某个用户信息")  # 定义子模块
    @allure.description("该用例是针对获取单个用户信息接口的测试")  # 用例描述
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")  # 关联Bug链接
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")  # 关联测试用例链接
    @allure.title("测试数据：【 {username}，{except_result}，{except_code}，{except_msg} 】")  # 设置测试报告标题
    @pytest.mark.single  # 打上 single 标记
    @pytest.mark.parametrize("username, except_result, except_code, except_msg",
                             api_data["test_get_get_one_user_info"])  # 参数化测试用例
    def test_get_get_one_user_info(self, username, except_result, except_code, except_msg):
        """
        测试获取单个用户信息接口
        :param username: 需要查询的用户名
        :param except_result: 预期的执行结果（布尔值）
        :param except_code: 预期的返回码
        :param except_msg: 预期的返回信息
        """
        logger.info("*************** 开始执行用例 ***************")
        step_2(username)  # 记录步骤
        result = get_one_user_info(username)  # 调用获取单个用户信息的接口
        assert result.response.status_code == 200  # 断言 HTTP 状态码是否为 200
        assert result.success == except_result, result.error  # 断言接口是否返回成功
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code  # 断言返回码是否符合预期
        assert except_msg in result.msg  # 断言返回信息是否包含预期内容
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_get_user_info.py"])  # 运行该测试文件
