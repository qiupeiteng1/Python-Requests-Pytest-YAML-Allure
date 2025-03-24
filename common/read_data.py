import yaml  # 用于处理 YAML 文件
import json  # 用于处理 JSON 文件
from configparser import ConfigParser  # 用于处理 INI 配置文件
from common.logger import logger  # 导入日志记录器


class MyConfigParser(ConfigParser):
    """
    自定义的 ConfigParser 类，继承自 Python 内置的 ConfigParser。
    主要用于解决 .ini 文件中的键（option）自动转为小写的问题。
    """
    def __init__(self, defaults=None):
        # 调用父类 ConfigParser 的构造方法
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        # 重写 optionxform 方法，使选项名称保持大小写不变
        return optionstr


class ReadFileData():
    """
    该类用于读取不同格式的文件数据，包括 YAML、JSON 和 INI 配置文件。
    """
    def __init__(self):
        pass  # 该类的构造方法无特殊初始化操作

    def load_yaml(self, file_path):
        """
        读取 YAML 文件并解析数据。
        :param file_path: YAML 文件的路径
        :return: 解析后的 YAML 数据
        """
        logger.info("加载 {} 文件......".format(file_path))  # 记录日志，指示正在加载 YAML 文件
        with open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)  # 使用 safe_load 方法解析 YAML 文件
        logger.info("读到数据 ==>>  {} ".format(data))  # 记录日志，输出读取的数据
        return data

    def load_json(self, file_path):
        """
        读取 JSON 文件并解析数据。
        :param file_path: JSON 文件的路径
        :return: 解析后的 JSON 数据
        """
        logger.info("加载 {} 文件......".format(file_path))  # 记录日志，指示正在加载 JSON 文件
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)  # 解析 JSON 文件
        logger.info("读到数据 ==>>  {} ".format(data))  # 记录日志，输出读取的数据
        return data

    def load_ini(self, file_path):
        """
        读取 INI 配置文件并解析数据。
        :param file_path: INI 配置文件的路径
        :return: 解析后的 INI 数据，转换为字典格式
        """
        logger.info("加载 {} 文件......".format(file_path))  # 记录日志，指示正在加载 INI 文件
        config = MyConfigParser()  # 创建 MyConfigParser 实例
        config.read(file_path, encoding="UTF-8")  # 读取 INI 配置文件
        data = dict(config._sections)  # 将配置文件的 sections 转换为字典格式
        # print("读到数据 ==>>  {} ".format(data))  # 该行被注释掉，避免调试输出
        return data


# 创建 ReadFileData 类的实例，以便在其他模块中直接使用 data 变量进行文件读取操作
data = ReadFileData()
