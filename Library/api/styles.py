from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

class StyleAPI:
    """提供样式设置的API"""
    
    def __init__(self, window):
        self.window = window
    
    def set_dark_theme(self):
        """设置暗色主题"""
        dark_palette = self.window.palette()
        
        # 基础颜色
        dark_color = QColor(45, 45, 45)
        text_color = QColor(200, 200, 200)
        highlight_color = QColor(42, 130, 218)
        
        # 设置调色板
        dark_palette.setColor(QPalette.Window, dark_color)
        dark_palette.setColor(QPalette.WindowText, text_color)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, dark_color)
        dark_palette.setColor(QPalette.ToolTipBase, text_color)
        dark_palette.setColor(QPalette.ToolTipText, text_color)
        dark_palette.setColor(QPalette.Text, text_color)
        dark_palette.setColor(QPalette.Button, dark_color)
        dark_palette.setColor(QPalette.ButtonText, text_color)
        dark_palette.setColor(QPalette.BrightText, QColor.red)
        dark_palette.setColor(QPalette.Link, highlight_color)
        dark_palette.setColor(QPalette.Highlight, highlight_color)
        dark_palette.setColor(QPalette.HighlightedText, QColor.black)
        
        # 禁用状态颜色
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(100, 100, 100))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(100, 100, 100))
        
        self.window.setPalette(dark_palette)
        self.window.setStyleSheet("""
            QToolTip { 
                color: #ffffff; 
                background-color: #2a82da; 
                border: 1px solid white; 
            }
            QMenu::item:selected { 
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #2a82da, stop:1 #1a62ba);
            }
        """)
    
    def set_light_theme(self):
        """设置亮色主题"""
        pass