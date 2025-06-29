from PyQt5.QtWidgets import QPushButton, QLabel
from utils.animation import AnimationManager

class Animatable:
    """ 为组件添加动画能力的混入类 """
    def __init__(self):
        self.anim_manager = AnimationManager()
        
    def add_animation(self, name, anim_type, **params):
        """ 添加动画配置 """
        self.anim_manager.register(name, self, anim_type, **params)
        return self  # 支持链式调用
        
    def on(self, signal, anim_name):
        """ 当信号触发时播放动画 """
        self.anim_manager.bind_to(signal, anim_name)
        return self

class AnimatedButton(QPushButton, Animatable):
    """ 带动画效果的按钮 """
    def __init__(self, text=""):
        QPushButton.__init__(self, text)
        Animatable.__init__(self)
        
class AnimatedLabel(QLabel, Animatable):
    """ 带动画效果的标签 """
    def __init__(self, text=""):
        QLabel.__init__(self, text)
        Animatable.__init__(self)