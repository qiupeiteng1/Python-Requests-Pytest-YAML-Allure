import pytest
import allure
from operation.user import login_user
from testcases.conftest import api_data
from common.logger import logger


@allure.step("步骤1 ==>> 登录用户")
def step_1(username):
    """
    记录用户登录步骤的日志信息
    :param username: 用户名
    """
    logger.info("步骤1 ==>> 登录用户：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("用户登录模块")
class TestUserLogin():
    """用户登录测试类"""

    @allure.story("用例--登录用户")
    @allure.description("该用例是针对用户登录接口的测试")
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试数据：【 {username}，{password}，{except_result}，{except_code}，{except_msg}】")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, except_result, except_code, except_msg",
                             api_data["test_login_user"])  # 读取测试数据
    def test_login_user(self, username, password, except_result, except_code, except_msg):
        """
        用户登录测试用例
        :param username: 用户名
        :param password: 密码
        :param except_result: 预期结果（成功或失败）
        :param except_code: 预期返回码
        :param except_msg: 预期返回消息
        """
        logger.info("*************** 开始执行用例 ***************")
        result = login_user(username, password)  # 调用用户登录接口
        step_1(username)  # 记录测试步骤日志
        assert result.success == except_result, result.error  # 断言返回的 success 值是否符合预期
        assert result.response.status_code == 200  # 断言 HTTP 状态码是否为 200
        assert result.success == except_result, result.error  # 再次断言 success 值
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code  # 断言返回的 code 是否符合预期
        assert except_msg in result.msg  # 断言返回的消息是否包含预期内容
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_login.py"])  # 运行当前测试脚本
