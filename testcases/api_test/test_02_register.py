import pytest
import allure
from operation.user import register_user
from testcases.conftest import api_data
from common.logger import logger


@allure.step("步骤1 ==>> 注册用户")
def step_1(username, password, telephone, sex, address):
    """
    记录用户注册步骤的日志信息
    :param username: 用户名
    :param password: 密码
    :param telephone: 手机号
    :param sex: 性别
    :param address: 地址
    """
    logger.info("步骤1 ==>> 注册用户 ==>> {}, {}, {}, {}, {}".format(username, password, telephone, sex, address))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("用户注册模块")
class TestUserRegister():
    """用户注册测试类"""

    @allure.story("用例--注册用户信息")
    @allure.description("该用例是针对获取用户注册接口的测试")
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @allure.title(
        "测试数据：【 {username}，{password}，{telephone}，{sex}，{address}，{except_result}，{except_code}，{except_msg}】")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, telephone, sex, address, except_result, except_code, except_msg",
                             api_data["test_register_user"])  # 读取测试数据
    @pytest.mark.usefixtures("delete_register_user")  # 依赖 delete_register_user 进行数据清理
    def test_register_user(self, username, password, telephone, sex, address, except_result, except_code, except_msg):
        """
        用户注册测试用例
        :param username: 用户名
        :param password: 密码
        :param telephone: 手机号
        :param sex: 性别
        :param address: 地址
        :param except_result: 预期结果（成功或失败）
        :param except_code: 预期返回码
        :param except_msg: 预期返回消息
        """
        logger.info("*************** 开始执行用例 ***************")
        result = register_user(username, password, telephone, sex, address)  # 调用用户注册接口
        step_1(username, password, telephone, sex, address)  # 记录测试步骤日志
        assert result.success == except_result, result.error  # 断言返回的 success 值是否符合预期
        assert result.response.status_code == 200  # 断言 HTTP 状态码是否为 200
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code  # 断言返回的 code 是否符合预期
        assert except_msg in result.msg  # 断言返回的消息是否包含预期内容
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_register.py"])  # 运行当前测试脚本
