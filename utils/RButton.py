from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

class MapleButton(QPushButton):
    """
    带主题色的多功能按钮
    Features:
    - 可设置主题色边框/白底黑字
    - 支持尺寸弹性控制
    - 自动悬停/按压效果
    - 圆角支持
    """
    
    def __init__(self, 
                 text: str = "",
                 theme_color: str = "#4CAF50",
                 min_width: int = None, #type:ignore
                 max_width: int = None, #type:ignore
                 fixed_height: int = 32,
                 font_size: int = 13,
                 parent=None):
        super().__init__(text, parent)
        
        # 尺寸控制
        if min_width:
            self.setMinimumWidth(min_width)
        if max_width:
            self.setMaximumWidth(max_width)
        self.setFixedHeight(fixed_height)
        
        # 字体设置
        font = QFont()
        font.setFamilies(['Microsoft YaHei', 'PingFang SC', 'sans-serif'])
        font.setPointSize(font_size)
        self.setFont(font)
        
        # 应用样式
        self._update_style(theme_color)
    
    def _update_style(self, theme_color: str):
        """动态更新按钮样式"""
        lighter = QColor(theme_color).lighter(115).name()
        darker = QColor(theme_color).darker(115).name()
        darkest = QColor(theme_color).darker(130).name()
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: white;
                color: black;
                border: 2px solid {theme_color};
                border-radius: 10px;
                padding: 0 12px;
                font-size: {self.font().pointSize()}pt;
                {f'min-width: {self.minimumWidth()}px;' if self.minimumWidth() > 0 else ''}
                {f'max-width: {self.maximumWidth()}px;' if self.maximumWidth() < 16777215 else ''}
            }}
            QPushButton:hover {{
                background: {lighter};
                border-color: {lighter};
            }}
            QPushButton:pressed {{
                background: #f0f0f0;
                border-color: {darkest};
            }}
            QPushButton:disabled {{
                background: #f0f0f0;
                border-color: #cccccc;
                color: #999999;
            }}
        """)
    
    def setThemeColor(self, color: str):
        """动态修改主题色"""
        self._update_style(color)
    
    def setFixedSize(self, w: int, h: int): #type:ignore
        """重写设置固定尺寸"""
        super().setFixedSize(w, h)
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)