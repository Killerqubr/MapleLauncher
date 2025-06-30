from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget

class AnimationAPI:
    """提供动画效果的API接口"""
    
    def __init__(self, window):
        self.window = window
        self.animations = {}
    
    def fade_in(self, widget, duration=500):
        """淡入动画"""
        if isinstance(widget, QWidget):
            widget.setGraphicsEffect(None)  # type:ignore
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(duration)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()
            return animation
        return None
    
    def fade_out(self, widget, duration=500):
        """淡出动画"""
        if isinstance(widget, QWidget):
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(duration)
            animation.setStartValue(1)
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.finished.connect(lambda: widget.hide())
            animation.start()
            return animation
        return None
    
    def slide(self, widget, start_pos, end_pos, duration=500):
        """滑动动画"""
        if isinstance(widget, QWidget):
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(duration)
            animation.setStartValue(start_pos)
            animation.setEndValue(end_pos)
            animation.setEasingCurve(QEasingCurve.OutBack)
            animation.start()
            return animation
        return None