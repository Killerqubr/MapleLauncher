from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty # type: ignore
from PyQt5.QtGui import QColor, QFont

class MapleButton(QPushButton):
    """
    ``Project Maple`` | 按钮类组件
    - 版本 ``Beta 2.1.1``
    """
    
    def __init__(self, 
                 text: str = "",
                 frameColor: str = "#4CAF50",
                 backgroundColor: str = "#FFFFFF",
                 min_width: int = None, # type: ignore
                 max_width: int = None, # type: ignore
                 fixed_height: int = 32,
                 font_size: int = 13,
                 borderRadius = 10,
                 parent = None):
        super().__init__(text, parent)

        self.borderRadius = borderRadius
        
        # 保存基础颜色
        self._frame_color = frameColor
        self._bg_color = backgroundColor
        
        # 初始化动画
        self._opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self._setup_animations()
        
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
        
        # 初始样式更新
        self._update_style_sheet()
    
    def _setup_animations(self):
        """配置透明度过渡动画"""
        self._opacity_animation.setDuration(200)
        self._opacity_animation.setEasingCurve(QEasingCurve.OutQuad)
    
    def _update_style_sheet(self):
        """更新样式表定义所有状态"""
        normal_bg = self._bg_color
        normal_frame = self._frame_color
        normal_text = "black" if QColor(normal_bg).lightness() > 127 else "white"
        
        hover_bg = QColor(self._bg_color).lighter(110).name()
        hover_frame = QColor(self._frame_color).lighter(120).name()
        hover_text = "black" if QColor(hover_bg).lightness() > 127 else "white"
        
        pressed_bg = QColor(self._bg_color).darker(110).name()
        pressed_frame = QColor(self._frame_color).darker(150).name()
        pressed_text = "black" if QColor(pressed_bg).lightness() > 127 else "white"
        
        # ?
        normal_frame = "#665555"
        normal_bg = "#FFFFFF"
        
        self.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {normal_frame};
                border-radius: {self.borderRadius}px;
                padding: 0 12px;
                background-color: {normal_bg};
                color: {normal_text};
                font-size: {self.font().pointSize()}pt;
            }}
            QPushButton:hover {{
                border-color: {hover_frame};
                background-color: {hover_bg};
                color: {hover_text};
            }}
            QPushButton:pressed {{
                border-color: {pressed_frame};
                background-color: {pressed_bg};
                color: {pressed_text};
            }}
            QPushButton:disabled {{
                border-color: #cccccc;
                background-color: #f0f0f0;
                color: #999999;
            }}
        """)
    
    # 鼠标事件处理
    def enterEvent(self, event): # type: ignore
        if not self.isEnabled():
            return
            
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self.windowOpacity())
        self._opacity_animation.setEndValue(0.9)
        self._opacity_animation.start()
        
        super().enterEvent(event)
        
    def leaveEvent(self, event): # type: ignore
        if not self.isEnabled():
            return
            
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self.windowOpacity())
        self._opacity_animation.setEndValue(1.0)
        self._opacity_animation.start()
        
        super().leaveEvent(event)
    
    def mousePressEvent(self, event): # type: ignore
        if not self.isEnabled() or event.button() != Qt.LeftButton: # type: ignore
            return super().mousePressEvent(event)
            
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self.windowOpacity())
        self._opacity_animation.setEndValue(0.8)
        self._opacity_animation.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event): # type: ignore
        if not self.isEnabled() or event.button() != Qt.LeftButton or not self.rect().contains(event.pos()): # type: ignore
            return super().mouseReleaseEvent(event)
            
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self.windowOpacity())
        self._opacity_animation.setEndValue(0.9)
        self._opacity_animation.start()
        
        super().mouseReleaseEvent(event)
    
    def setThemeColor(self, frameColor: str, backgroundColor: str = "#FFFFFF"):
        """动态修改主题色"""
        self._frame_color = frameColor
        self._bg_color = backgroundColor
        self._update_style_sheet()
    
    def setEnabled(self, enabled): # type: ignore
        """重写setEnabled以触发状态更新"""
        super().setEnabled(enabled)
        self._opacity_animation.stop()
        self.setWindowOpacity(1.0 if enabled else 0.7)