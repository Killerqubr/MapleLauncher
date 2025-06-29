from PyQt5.QtGui import QColor

class AdvancedCommandHighlighter:
    def __init__(self):
        self.command_structure = {}
        self.error_color = "#FF5555"
    
    def parse_command(self, text: str) -> list:
        """解析命令并返回高亮信息"""
        # 实现高亮逻辑...