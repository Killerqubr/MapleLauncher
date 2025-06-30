from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QObject, pyqtSignal, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget

class AnimationManager(QObject):
    animation_triggered = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._animations = {}
        self._pending_animations = {}  # 新增：待执行动画队列
        self._debounce_timers = {}     # 新增：防抖计时器
        
    def register(self, name, widget, anim_type, **params):
        """ 注册动画并返回管理器自身以支持链式调用 """
        self._animations[name] = self._create_animation(widget, anim_type, **params)
        return self  # 这里返回管理器实例而不是动画对象
        
    def bind_to(self, signal, anim_name):
        """ 绑定信号到动画 """
        if anim_name in self._animations:
            signal.connect(lambda: self.play(anim_name))
        return self
        
    def play(self, name):
        """ 带防抖机制的动画播放 """
        if name not in self._animations:
            return

        # 防抖处理（300ms内重复调用会被忽略）
        if name in self._debounce_timers:
            self._debounce_timers[name].stop()
        
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._real_play_animation(name))
        timer.start(50)  # 50ms防抖阈值
        self._debounce_timers[name] = timer

    def _real_play_animation(self, name):
        """ 实际执行动画 """
        if name in self._animations:
            anim = self._animations[name]
            anim.stop()  # 停止当前正在运行的相同动画
            anim.start()
    
    @staticmethod
    def _create_animation(widget, anim_type, **params):
        anim_types = {
            'fade': ('windowOpacity', 0, 1),
            'slide': ('pos', params.get('start_pos'), params.get('end_pos')),
            'scale': ('size', params.get('start_size'), params.get('end_size'))
        }
        
        prop, start, end = anim_types[anim_type]
        anim = QPropertyAnimation(widget, prop.encode())
        anim.setDuration(params.get('duration', 800))
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(params.get('easing', QEasingCurve.OutQuad))
        return anim