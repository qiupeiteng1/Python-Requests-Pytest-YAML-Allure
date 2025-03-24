import pytest  # 导入 pytest 进行测试框架管理
import allure  # 导入 allure 进行测试报告的生成
from operation.user import register_user  # 从 user 操作模块导入注册用户的方法
from common.logger import logger  # 从 common 模块导入日志记录器


@allure.step("步骤1 ==>> 注册用户")
def step_1(username, password, telephone, sex, address):
    """
    记录注册用户的操作步骤
    :param username: 注册用户名
    :param password: 注册密码
    :param telephone: 注册手机号
    :param sex: 注册用户性别
    :param address: 注册用户地址
    """
    logger.info("步骤1 ==>> 注册用户 ==>> {}, {}, {}, {}, {}".format(username, password, telephone, sex, address))


@allure.step("步骤2 ==>> 重复注册用户")
def step_2(username, password, telephone, sex, address):
    """
    记录重复注册用户的操作步骤
    :param username: 注册用户名
    :param password: 注册密码
    :param telephone: 注册手机号
    :param sex: 注册用户性别
    :param address: 注册用户地址
    """
    logger.info("步骤2 ==>> 重复注册用户 ==>> {}, {}, {}, {}, {}".format(username, password, telephone, sex, address))


@allure.severity(allure.severity_level.CRITICAL)  # 标记该测试用例的严重级别为关键
@allure.epic("针对业务场景的测试")  # 设置测试 Epic（史诗），表示该测试属于业务场景测试
@allure.feature("场景：用户注册-重复注册")  # 设置测试 Feature（功能模块），表示该测试属于用户注册-重复注册场景
class TestRepeatReg:
    """
    用户重复注册测试类
    该测试类用于验证用户注册功能的正常性，包括首次注册和重复注册的情况
    """

    @allure.story("用例--注册/重复注册--预期成功")  # 设置测试用例的 story，表示具体测试场景
    @allure.description("该用例是针对 注册-重复注册 场景的测试")  # 用例描述
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")  # 关联缺陷地址
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")  # 关联测试用例地址
    @allure.title("用户注册/重复注册-预期成功")  # 设置用例标题
    @pytest.mark.single  # 标记该测试为单一测试
    @pytest.mark.usefixtures("delete_register_user")  # 运行测试前执行 delete_register_user 清理操作，确保测试数据一致性
    def test_user_repeat_register(self, testcase_data):
        """
        用户重复注册测试用例
        测试用户首次注册成功后，再次使用相同信息进行注册，验证系统是否正确返回错误信息
        :param testcase_data: 传入的测试数据，包含用户名、密码、手机号、性别、地址以及预期结果
        """
        # 从测试数据中提取用户注册相关信息
        username = testcase_data["username"]
        password = testcase_data["password"]
        telephone = testcase_data["telephone"]
        sex = testcase_data["sex"]
        address = testcase_data["address"]
        except_result = testcase_data["except_result"]  # 预期结果（成功/失败）
        except_code = testcase_data["except_code"]  # 预期返回码
        except_msg = testcase_data["except_msg"]  # 预期返回信息

        logger.info("*************** 开始执行用例 ***************")

        # 第一次注册用户
        result = register_user(username, password, telephone, sex, address)
        step_1(username, password, telephone, sex, address)  # 记录步骤1
        assert result.success is True, result.error  # 断言注册成功

        # 第二次重复注册相同用户
        result = register_user(username, password, telephone, sex, address)
        step_2(username, password, telephone, sex, address)  # 记录步骤2
        assert result.success == except_result, result.error  # 断言结果是否符合预期

        # 验证返回码是否正确
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code

        # 验证返回消息是否符合预期
        assert except_msg in result.msg

        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    # 运行 pytest 测试，并输出详细信息
    pytest.main(["-q", "-s", "test_04_repeat_register.py"])
