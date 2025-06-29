from PyQt5.QtCore import QObject, pyqtSignal, QSize

class EventCenter(QObject):
    """ 全局事件中心 """
    window_show = pyqtSignal()       # 窗口显示事件
    button_click = pyqtSignal(str)   # 按钮点击事件
    custom = pyqtSignal(dict)        # 自定义事件
    resize_event = pyqtSignal(QSize)
    
    # 示例：添加更多预定义事件
    resize_event = pyqtSignal(int, int)  # 窗口resize事件

    