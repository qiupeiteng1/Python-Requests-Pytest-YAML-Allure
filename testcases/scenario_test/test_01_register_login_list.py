import pytest
import allure
from operation.user import register_user, login_user, get_one_user_info
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


@allure.step("步骤2 ==>> 登录用户")
def step_2(username):
    """
    记录用户登录步骤的日志信息
    :param username: 用户名
    """
    logger.info("步骤2 ==>> 登录用户：{}".format(username))


@allure.step("步骤3 ==>> 获取某个用户信息")
def step_3(username):
    """
    记录获取用户信息步骤的日志信息
    :param username: 用户名
    """
    logger.info("步骤3 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.CRITICAL)  # 设置用例的严重级别为 CRITICAL（关键）
@allure.epic("针对业务场景的测试")  # 标记该测试类属于 "业务场景测试"
@allure.feature("场景：用户注册-用户登录-查看用户")  # 标记该测试类的功能模块
class TestRegLogList():
    """测试用户注册、登录及查看信息的业务流程"""

    @allure.story("用例--注册/登录/查看--预期成功")  # 定义用例所属的测试场景
    @allure.description("该用例是针对 注册-登录-查看 场景的测试")  # 添加用例描述
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")  # 关联缺陷地址
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")  # 关联测试用例地址
    @allure.title("用户注册登录查看-预期成功")  # 设置测试用例的标题
    @pytest.mark.multiple  # 标记该测试用例属于 "multiple" 组，方便分类执行
    @pytest.mark.usefixtures("delete_register_user")  # 预置条件：先删除注册用户数据
    def test_user_register_login_list(self, testcase_data):
        """
        用户注册-登录-查看信息业务流程测试
        :param testcase_data: 测试数据，包括用户名、密码、手机号等
        """
        # 从测试数据中提取参数
        username = testcase_data["username"]  # 用户名
        password = testcase_data["password"]  # 密码
        telephone = testcase_data["telephone"]  # 手机号
        sex = testcase_data["sex"]  # 性别
        address = testcase_data["address"]  # 地址
        except_result = testcase_data["except_result"]  # 预期结果（成功或失败）
        except_code = testcase_data["except_code"]  # 预期返回码
        except_msg = testcase_data["except_msg"]  # 预期返回消息

        logger.info("*************** 开始执行用例 ***************")  # 记录日志，标识用例开始执行

        # 第一步：用户注册
        result = register_user(username, password, telephone, sex, address)  # 调用注册接口
        step_1(username, password, telephone, sex, address)  # 记录日志信息
        assert result.success is True, result.error  # 断言注册成功，否则抛出错误信息

        # 第二步：用户登录
        result = login_user(username, password)  # 调用登录接口
        step_2(username)  # 记录日志信息
        assert result.success is True, result.error  # 断言登录成功，否则抛出错误信息

        # 第三步：获取用户信息
        result = get_one_user_info(username)  # 获取用户信息
        step_3(username)  # 记录日志信息
        assert result.success == except_result, result.error  # 断言获取信息结果是否符合预期

        # 断言接口返回的状态码和消息是否符合预期
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code  # 断言返回的 code 是否符合预期
        assert except_msg in result.msg  # 断言返回的消息是否包含预期内容

        logger.info("*************** 结束执行用例 ***************")  # 记录日志，标识用例执行结束


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_register_login_list.py"])  # 运行当前测试脚本
