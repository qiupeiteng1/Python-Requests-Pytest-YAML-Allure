import os  # 导入os模块，用于文件和目录操作
from core.rest_client import RestClient  # 从core模块导入RestClient类
from common.read_data import data  # 从common模块导入data类，用于读取数据

# 获取当前文件所在的目录的上一级目录路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 构造配置文件setting.ini的完整路径
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
# 读取配置文件中的API根URL
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]


class User(RestClient):  # 继承RestClient类，封装用户相关的接口

    def __init__(self, api_root_url, **kwargs):
        """
        初始化User类，调用父类的构造方法
        :param api_root_url: API的根URL
        :param kwargs: 其他可选参数
        """
        super(User, self).__init__(api_root_url, **kwargs)

    def list_all_users(self, **kwargs):
        """
        获取所有用户列表
        :param kwargs: 其他可选参数
        :return: GET请求返回的响应结果
        """
        return self.get("/users", **kwargs)

    def list_one_user(self, username, **kwargs):
        """
        获取指定用户名的用户信息
        :param username: 用户名
        :param kwargs: 其他可选参数
        :return: GET请求返回的响应结果
        """
        return self.get("/users/{}".format(username), **kwargs)

    def register(self, **kwargs):
        """
        用户注册
        :param kwargs: 包含注册所需参数
        :return: POST请求返回的响应结果
        """
        return self.post("/register", **kwargs)

    def login(self, **kwargs):
        """
        用户登录
        :param kwargs: 包含登录所需参数
        :return: POST请求返回的响应结果
        """
        return self.post("/login", **kwargs)

    def update(self, user_id, **kwargs):
        """
        更新用户信息
        :param user_id: 需要更新的用户ID
        :param kwargs: 包含更新内容
        :return: PUT请求返回的响应结果
        """
        return self.put("/update/user/{}".format(user_id), **kwargs)

    def delete(self, name, **kwargs):
        """
        删除用户
        :param name: 需要删除的用户名
        :param kwargs: 其他可选参数
        :return: POST请求返回的响应结果
        """
        return self.post("/delete/user/{}".format(name), **kwargs)


user = User(api_root_url)  # 创建User类的实例，并传入API根URL