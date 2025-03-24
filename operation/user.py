from core.result_base import ResultBase
from api.user import user
from common.logger import logger

def get_all_user_info():
    """
    获取全部用户信息
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象，存储返回结果
    res = user.list_all_users()  # 调用API获取全部用户信息
    result.success = False  # 默认成功标志为False
    if res.json()["code"] == 0:  # 判断返回码是否为0
        result.success = True  # 如果返回码为0，表示成功
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]  # 记录返回消息
    result.response = res  # 记录完整的响应
    return result  # 返回封装的结果

def get_one_user_info(username):
    """
    获取单个用户信息
    :param username:  用户名
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象
    res = user.list_one_user(username)  # 获取单个用户信息
    result.success = False  # 默认成功标志为False
    if res.json()["code"] == 0:
        result.success = True  # 成功时设置为True
    else:
        result.error = "查询用户 ==>> 接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("查看单个用户 ==>> 返回结果 ==>> {}".format(result.response.text))  # 记录日志
    return result

def register_user(username, password, telephone, sex="", address=""):
    """
    注册用户信息
    :param username: 用户名
    :param password: 密码
    :param telephone: 手机号
    :param sex: 性别
    :param address: 联系地址
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象
    json_data = {  # 请求体内容
        "username": username,
        "password": password,
        "sex": sex,
        "telephone": telephone,
        "address": address
    }
    header = {  # 请求头
        "Content-Type": "application/json"
    }
    res = user.register(json=json_data, headers=header)  # 调用API进行注册
    result.success = False  # 默认失败
    if res.json()["code"] == 0:
        result.success = True  # 注册成功时标记为True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("注册用户 ==>> 返回结果 ==>> {}".format(result.response.text))  # 记录日志
    return result

def login_user(username, password):
    """
    登录用户
    :param username: 用户名
    :param password: 密码
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象
    payload = {  # 登录请求参数
        "username": username,
        "password": password
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = user.login(data=payload, headers=header)  # 调用API进行登录
    result.success = False  # 默认失败
    if res.json()["code"] == 0:
        result.success = True  # 登录成功时标记为True
        # result.token = res.json()["login_info"]["token"]  # 存储登录令牌
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("登录用户 ==>> 返回结果 ==>> {}".format(result.response.text))  # 记录日志
    return result

def update_user(id, admin_user, new_password, new_telephone, token, new_sex="", new_address=""):
    """
    根据用户ID，修改用户信息
    :param id: 用户ID
    :param admin_user: 当前操作的管理员用户
    :param new_password: 新密码
    :param new_telephone: 新手机号
    :param token: 当前管理员用户的token
    :param new_sex: 新性别
    :param new_address: 新联系地址
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象
    header = {
        "Content-Type": "application/json"
    }
    json_data = {  # 请求体内容
        "admin_user": admin_user,
        "password": new_password,
        "token": token,
        "sex": new_sex,
        "telephone": new_telephone,
        "address": new_address
    }
    res = user.update(id, json=json_data, headers=header)  # 调用API进行用户信息更新
    result.success = False  # 默认失败
    if res.json()["code"] == 0:
        result.success = True  # 更新成功时标记为True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("修改用户 ==>> 返回结果 ==>> {}".format(result.response.text))  # 记录日志
    return result

def delete_user(username, admin_user, token):
    """
    根据用户名，删除用户信息
    :param username: 用户名
    :param admin_user: 当前操作的管理员用户
    :param token: 当前管理员用户的token
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()  # 创建ResultBase对象
    json_data = {  # 请求体内容
        "admin_user": admin_user,
        "token": token,
    }
    header = {
        "Content-Type": "application/json"
    }
    res = user.delete(username, json=json_data, headers=header)  # 调用API进行用户删除
    result.success = False  # 默认失败
    if res.json()["code"] == 0:
        result.success = True  # 删除成功时标记为True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])  # 错误信息
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("删除用户 ==>> 返回结果 ==>> {}".format(result.response.text))  # 记录日志
    return result
