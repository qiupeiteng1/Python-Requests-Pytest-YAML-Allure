import requests  # 导入requests库，用于发送HTTP请求
import json as complexjson  # 导入json模块并重命名为complexjson，避免与局部变量json冲突
from common.logger import logger  # 导入日志模块，用于记录HTTP请求日志


class RestClient():
    """
    RestClient类，封装HTTP请求的方法
    """

    def __init__(self, api_root_url):
        """
        初始化RestClient类
        :param api_root_url: API的根URL
        """
        self.api_root_url = api_root_url  # 设置API根URL
        self.session = requests.session()  # 创建一个requests的会话对象，提高请求效率

    def get(self, url, **kwargs):
        """
        发送GET请求
        :param url: API接口路径
        :param kwargs: 其他可选参数（如headers, params等）
        :return: GET请求的响应对象
        """
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        发送POST请求
        :param url: API接口路径
        :param data: 表单数据（可选）
        :param json: JSON格式数据（可选）
        :param kwargs: 其他可选参数（如headers等）
        :return: POST请求的响应对象
        """
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """
        发送PUT请求
        :param url: API接口路径
        :param data: 需要更新的数据
        :param kwargs: 其他可选参数（如headers等）
        :return: PUT请求的响应对象
        """
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        """
        发送DELETE请求
        :param url: API接口路径
        :param kwargs: 其他可选参数（如headers等）
        :return: DELETE请求的响应对象
        """
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        """
        发送PATCH请求
        :param url: API接口路径
        :param data: 需要部分更新的数据
        :param kwargs: 其他可选参数（如headers等）
        :return: PATCH请求的响应对象
        """
        return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        """
        统一的请求方法
        :param url: API接口路径
        :param method: 请求方法（GET, POST, PUT, DELETE, PATCH）
        :param data: 表单数据（可选）
        :param json: JSON格式数据（可选）
        :param kwargs: 其他可选参数（如headers, params等）
        :return: 请求的响应对象
        """
        url = self.api_root_url + url  # 拼接完整的URL
        headers = dict(**kwargs).get("headers")  # 获取请求头
        params = dict(**kwargs).get("params")  # 获取请求参数
        files = dict(**kwargs).get("files")  # 获取文件上传参数
        cookies = dict(**kwargs).get("cookies")  # 获取cookies参数

        # 记录请求日志
        self.request_log(url, method, data, json, params, headers, files, cookies)

        # 根据请求方法调用相应的requests方法
        if method == "GET":
            return self.session.get(url, **kwargs)
        if method == "POST":
            return requests.post(url, data=data, json=json, **kwargs)
        if method == "PUT":
            if json:
                data = complexjson.dumps(json)  # 将json对象转换为字符串
            return self.session.put(url, data=data, **kwargs)
        if method == "DELETE":
            return self.session.delete(url, **kwargs)
        if method == "PATCH":
            if json:
                data = complexjson.dumps(json)  # 将json对象转换为字符串
            return self.session.patch(url, data=data, **kwargs)

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                    **kwargs):
        """
        记录HTTP请求日志，方便调试和问题排查
        :param url: 请求的URL
        :param method: 请求方法（GET, POST, PUT, DELETE, PATCH）
        :param data: 表单数据（可选）
        :param json: JSON格式数据（可选）
        :param params: URL查询参数（可选）
        :param headers: 请求头（可选）
        :param files: 上传的文件（可选）
        :param cookies: 请求的cookies（可选）
        :param kwargs: 其他可选参数
        """
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))
