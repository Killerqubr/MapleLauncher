import sys
from PyQt5.QtWidgets import QApplication
from .version_check import check_qt_version, verify_imports
from ..utils.logger import setup_logging

class PyQtApp:
    """PyQt应用管理器"""
    
    def __init__(self, app_name="PyQt Application"):
        # 检查版本和导入
        verify_imports()
        check_qt_version()
        
        # 创建QApplication实例
        self.qapp = QApplication(sys.argv)
        self.qapp.setApplicationName(app_name)
        
        # 设置日志
        self.logger = setup_logging("PyQtApp")
        self.logger.info("Application initialized")
    
    def run(self, main_window):
        """运行应用"""
        main_window.show()
        self.logger.info("Application started")
        sys.exit(self.qapp.exec_())