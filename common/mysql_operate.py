import pymysql  # 导入pymysql库，用于操作MySQL数据库
import os  # 导入os模块，用于路径操作
from common.read_data import data  # 从common模块中导入读取数据的方法
from common.logger import logger  # 从common模块中导入日志记录器

# 获取当前文件的上级目录路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 定义配置文件的路径
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
# 读取配置文件中的 MySQL 配置信息
data = data.load_ini(data_file_path)["mysql"]

# 从配置文件中提取MySQL连接所需的参数，并存储在字典中
DB_CONF = {
    "host": data["MYSQL_HOST"],        # 数据库主机地址
    "port": int(data["MYSQL_PORT"]),   # 数据库端口号
    "user": data["MYSQL_USER"],        # 数据库用户名
    "password": data["MYSQL_PASSWD"],  # 数据库密码
    "db": data["MYSQL_DB"]             # 数据库名称
}


class MysqlDb():
    """
        MysqlDb 类用于封装 MySQL 数据库的连接和操作方法。
        """

    def __init__(self, db_conf=DB_CONF):
        """
        初始化MySQL连接
        :param db_conf: 数据库配置字典，包含连接MySQL所需的配置信息
        """
        # 通过字典拆包传递数据库配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=False)
        # 通过 cursor() 方法创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        """
        释放数据库资源，在对象被删除时自动调用
        """
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """
        执行查询操作
        :param sql: 要执行的SQL查询语句
        :return: 查询结果（列表格式）
        """
        # 检查数据库连接是否断开，如果连接断开则重新建立连接
        self.conn.ping(reconnect=True)
        # 执行SQL查询
        self.cur.execute(sql)
        # 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """
        执行更新、插入或删除操作
        :param sql: 要执行的SQL语句（更新/插入/删除）
        """
        try:
            # 检查数据库连接是否断开，如果连接断开则重新建立连接
            self.conn.ping(reconnect=True)
            # 执行SQL语句
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 捕获异常并记录错误日志
            logger.info("操作MySQL出现错误，错误原因：{}".format(e))
            # 如果发生异常，回滚事务
            self.conn.rollback()


# 创建MysqlDb对象并使用DB_CONF进行初始化
db = MysqlDb(DB_CONF)
