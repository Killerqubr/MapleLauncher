from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import Qt, QSize

class MapleIconButton(QPushButton):
    """
    ``Project Maple`` | 按钮类组件
    - 版本 ``alpha 1.0``
    """
    
    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)
        self._icon_path = icon_path
        self._setup_button()
        
    def _setup_button(self):
        """初始化按钮设置"""
        # 设置图标
        if self._icon_path:
            self.setIcon(QIcon(self._icon_path))
            self.setIconSize(QSize(30, 30))  # 设置图标大小
            
        # 设置鼠标悬停和点击效果
        self.setCursor(Qt.PointingHandCursor) #type:ignore
        
        # 基础样式
        base_style = """
            QPushButton {
                background-color: #BF514E;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-family: 'Cascadia Mono', '宋体', sans-serif;
                font-size: 14px;
                border: none;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #A8423F;
            }
            QPushButton:pressed {
                background-color: #8C3330;
                padding-top: 9px;
                padding-bottom: 7px;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """
        self.setStyleSheet(base_style)
        
    def setIcon(self, icon, size=None):
        """设置按钮图标"""
        super().setIcon(icon)
        if size:
            self.setIconSize(QSize(size, size))
            
    def paintEvent(self, event): #type:ignore
        """重绘按钮，确保图标和文本正确对齐"""
        painter = QPainter(self)
        
        # 绘制背景
        if self.isDown():
            painter.setOpacity(0.8)  # 按下时稍微透明
        
        super().paintEvent(event)
        
        # 自定义绘制可以在这里添加
        painter.end()