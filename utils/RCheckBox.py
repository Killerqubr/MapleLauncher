# utils/RCheckBox.py
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import (Qt, QPropertyAnimation, QEasingCurve, 
                         QSize, QPointF)
from PyQt5.QtGui import (QPainter, QColor, QPen, QBrush)
from PyQt5.QtCore import pyqtProperty # type: ignore

class MapleCheckBox(QCheckBox):
    """
    ``Project Maple`` | 复选框类组件
    - 版本 ``alpha1.8``
    - 修复: 
        - 确保点击总能触发动画
        - 优化动画流畅度
    """
    
    def __init__(self, parent=None, theme_color="#BF514E", size=24, outer_color="#665555"):
        super().__init__(parent)
        self._theme_color = QColor(theme_color)
        self._outer_color = QColor(outer_color)
        self._size = size
        self._outer_radius = size / 2
        self._inner_radius = size / 4
        self._anim_scale = 0.0
        self._hover = False
        
        # 动画设置
        self._animation = QPropertyAnimation(self, b"animScale")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.OutBack)
        
        # 确保动画完成后清理
        self._animation.finished.connect(self._cleanup_animation)
        self.setup_ui()
        
    def _cleanup_animation(self):
        """动画完成后的清理工作"""
        if self._animation.state() == QPropertyAnimation.Stopped: # type: ignore
            self._animation.setCurrentTime(0)
        
    def mousePressEvent(self, event): # type: ignore
        """重写鼠标点击事件，确保总是触发状态变化"""
        if event.button() == Qt.LeftButton: # type: ignore
            self.setChecked(not self.isChecked())
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def setup_ui(self):
        self.setCursor(Qt.PointingHandCursor) # type: ignore
        self.setFixedSize(QSize(self._size, self._size))
        self.setMouseTracking(True)
        
    def getAnimScale(self):
        return self._anim_scale
        
    def setAnimScale(self, value):
        self._anim_scale = value
        self.update()
        
    animScale = pyqtProperty(float, getAnimScale, setAnimScale)
    
    def enterEvent(self, event): # type: ignore
        self._hover = True
        self.update()
        super().enterEvent(event)
        
    def leaveEvent(self, event): # type: ignore
        self._hover = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event): # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width()/2, self.height()/2)
        
        # 悬停效果
        if self._hover and not self.isChecked():
            painter.setPen(Qt.NoPen) # type: ignore
            light_color = QColor(self._theme_color)
            light_color.setAlpha(50)
            painter.setBrush(QBrush(light_color))
            painter.drawEllipse(center, self._outer_radius - 2, self._outer_radius - 2)
            
        # 外圆边框
        pen_width = 3.7 if self._hover else 3
        pen = QPen(self._outer_color, pen_width)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush) # type: ignore
        painter.drawEllipse(center, self._outer_radius - pen_width, self._outer_radius - pen_width)
        
        # 内圆动画
        if self.isChecked() or self._anim_scale > 0:
            current_radius = self._inner_radius * self._anim_scale
            painter.setPen(Qt.NoPen) # type: ignore
            painter.setBrush(QBrush(self._theme_color))
            painter.drawEllipse(center, current_radius, current_radius)
    
    def hitButton(self, pos):
        center = QPointF(self.width()/2, self.height()/2)
        distance = ((pos.x() - center.x()) ** 2 + (pos.y() - center.y()) ** 2) ** 0.5
        return distance <= self._outer_radius
    
    def nextCheckState(self):
        """确保动画总是能触发"""
        super().nextCheckState()
        self._start_animation()
    
    def _start_animation(self):
        """启动动画的独立方法"""
        if self._animation.state() == QPropertyAnimation.Running: # type: ignore
            self._animation.stop()
            
        target_value = 1.0 if self.isChecked() else 0.0
        self._animation.setStartValue(self._anim_scale)
        self._animation.setEndValue(target_value)
        self._animation.start()
    
    def setChecked(self, checked): # type: ignore
        """重写setChecked以确保动画同步"""
        super().setChecked(checked)
        self._start_animation()
    
    def setThemeColor(self, color):
        self._theme_color = QColor(color)
        self.update()
    
    def sizeHint(self):
        return QSize(self._size, self._size)