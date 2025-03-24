import time

import pytest
import os
import allure
from api.user import user
from common.mysql_operate import db
from common.read_data import data
from common.logger import logger

# 获取当前文件所在目录的上一级目录，即项目的根目录
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_data(yaml_file_name):
    """
    读取 YAML 文件数据
    :param yaml_file_name: YAML 文件名称
    :return: 解析后的 YAML 数据
    """
    try:
        data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))  # 如果读取 YAML 失败，则跳过测试
    else:
        return yaml_data


# 读取基础数据、API 测试数据和场景测试数据
base_data = get_data("base_data.yml")
api_data = get_data("api_test_data.yml")
scenario_data = get_data("scenario_test_data.yml")


@allure.step("前置步骤 ==>> 清理数据")
def step_first():
    """测试前的前置步骤：清理数据"""
    logger.info("******************************")
    logger.info("前置步骤开始 ==>> 清理数据")


@allure.step("后置步骤 ==>> 清理数据")
def step_last():
    """测试后的后置步骤：清理数据"""
    logger.info("后置步骤开始 ==>> 清理数据")


@allure.step("前置步骤 ==>> 管理员用户登录")
def step_login(username, password):
    """
    记录管理员用户登录步骤
    :param username: 管理员用户名
    :param password: 管理员密码
    """
    logger.info("前置步骤 ==>> 管理员 {} 登录，返回信息 为：{}".format(username, password))


@pytest.fixture(scope="session")
def login_fixture():
    """
    测试会话级别的前置步骤：
    - 读取管理员账户信息
    - 执行管理员用户登录
    - 生成登录会话数据
    """
    username = base_data["init_admin_user"]["username"]
    password = base_data["init_admin_user"]["password"]
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "username": username,
        "password": password
    }
    loginInfo = user.login(data=payload, headers=header)  # 调用用户登录接口
    step_login(username, password)  # 记录登录步骤
    yield loginInfo.json()  # 生成登录会话数据


@pytest.fixture(scope="function")
def insert_delete_user():
    """
    用例前置步骤：
    - 在数据库插入一条用户数据（用于后续删除测试）
    - 执行后，在测试结束后删除该数据
    """
    insert_sql = base_data["init_sql"]["insert_delete_user"][0]  # 获取插入用户的 SQL 语句
    db.execute_db(insert_sql)  # 执行插入 SQL
    step_first()  # 记录前置步骤
    logger.info("删除用户操作：插入新用户--准备用于删除用户")
    logger.info("执行前置SQL：{}".format(insert_sql))
    yield
    # 测试执行后，进行数据清理
    del_sql = base_data["init_sql"]["insert_delete_user"][1]  # 获取删除用户的 SQL 语句
    db.execute_db(del_sql)  # 执行删除 SQL
    step_last()  # 记录后置步骤
    logger.info("删除用户操作：手工清理处理失败的数据")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def delete_register_user():
    """
    用例前置步骤：
    - 在注册新用户前，先删除数据库中可能存在的相同用户
    - 执行后，在测试结束后再删除一次，确保环境干净
    """
    del_sql = base_data["init_sql"]["delete_register_user"]  # 获取删除用户的 SQL 语句
    db.execute_db(del_sql)  # 执行删除 SQL
    step_first()  # 记录前置步骤
    logger.info("注册用户操作：清理用户--准备注册新用户")
    logger.info("执行前置SQL：{}".format(del_sql))
    yield
    # 测试执行后，进行数据清理
    db.execute_db(del_sql)  # 重新执行删除 SQL
    step_last()  # 记录后置步骤
    logger.info("注册用户操作：删除注册的用户")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def update_user_telephone():
    """
    用例前置步骤：
    - 由于手机号是唯一的，因此每次测试前需要修改手机号，以便测试用例可重复执行
    """
    update_sql = base_data["init_sql"]["update_user_telephone"]  # 获取更新手机号的 SQL 语句
    db.execute_db(update_sql)  # 执行更新 SQL
    step_first()  # 记录前置步骤
    logger.info("修改用户操作：手工修改用户的手机号，以便用例重复执行")
    logger.info("执行SQL：{}".format(update_sql))
