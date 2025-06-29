from PyQt5.QtCore import QSize, QPoint
from core.event_center import EventCenter
from core.component import AnimatedButton, AnimatedLabel
from PyQt5.QtWidgets import QMainWindow

def create_window_with_animations(event_center):
    """ 创建预配置动画的窗口 """
    window = QMainWindow()
    window.resize(800, 600)
    
    # 添加带动画的按钮
    btn = AnimatedButton("Click Me")
    btn.add_animation(
        name="click_effect",
        anim_type="scale",
        start_size=QSize(100, 40),
        end_size=QSize(120, 50),
        duration=300
    ).on(btn.clicked, "click_effect")
    
    # 绑定窗口显示动画
    window.showEvent = lambda e: event_center.window_show.emit() #type:ignore
    
    return window