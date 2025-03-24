import logging  # 导入logging模块，用于记录日志
import time  # 导入time模块，用于获取当前时间
import os  # 导入os模块，用于文件和目录操作

# 获取当前文件所在的目录的上一级目录路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 定义日志文件存放的目录路径
LOG_PATH = os.path.join(BASE_PATH, "log")

# 如果日志目录不存在，则创建日志目录
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger:
    """
    Logger类用于配置和管理日志记录
    """

    def __init__(self):
        """
        初始化Logger类，创建日志记录器
        """
        # 定义日志文件的完整路径，文件名为当前日期.log
        self.logname = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
        # 创建一个日志记录器实例，名称为"log"
        self.logger = logging.getLogger("log")

        # 设置日志记录器的级别为DEBUG，表示记录所有级别的日志
        self.logger.setLevel(logging.DEBUG)

        # 定义日志格式
        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s'
        )

        # 创建一个日志文件处理器，用于将日志写入文件
        self.filelogger = logging.FileHandler(self.logname, mode='a', encoding="UTF-8")

        # 创建一个控制台处理器，用于在控制台输出日志
        self.console = logging.StreamHandler()

        # 设置控制台日志级别为DEBUG
        self.console.setLevel(logging.DEBUG)

        # 设置文件日志级别为DEBUG
        self.filelogger.setLevel(logging.DEBUG)

        # 为文件日志处理器和控制台日志处理器设置相同的日志格式
        self.filelogger.setFormatter(self.formater)

        # 设置控制台日志的格式
        self.console.setFormatter(self.formater)

        # 将文件日志处理器添加到日志记录器
        self.logger.addHandler(self.filelogger)

        # 将控制台日志处理器添加到日志记录器
        self.logger.addHandler(self.console)


# 创建Logger类的实例，并获取日志记录器
logger = Logger().logger

if __name__ == '__main__':
    logger.info("---测试开始---")  # 记录INFO级别日志
    logger.debug("---测试结束---")  # 记录DEBUG级别日志