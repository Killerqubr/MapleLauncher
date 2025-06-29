import logging
from logging.handlers import RotatingFileHandler
import os
from PyQt5.QtCore import QStandardPaths

def setup_logging(name, log_level=logging.INFO):
    """
    配置日志系统
    :param name: 日志名称(通常是模块或类名)
    :param log_level: 日志级别
    :return: 配置好的logger对象
    """
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # 防止重复添加handler
    if logger.handlers:
        return logger
    
    # 创建日志目录(在用户的应用数据目录下)
    log_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    log_dir = os.path.join(log_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志文件路径
    log_file = os.path.join(log_dir, f'{name}.log')
    
    # 创建formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件handler(滚动日志)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger