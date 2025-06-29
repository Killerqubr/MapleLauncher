from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                            QWidget, QPushButton, QLabel)
from PyQt5.QtCore import (QSize, QPoint, QEasingCurve,
                            QTimer, Qt, QPropertyAnimation)
from PyQt5.QtGui import (QIcon, QBrush, QPen, QColor,
                        QPainter)
from core.event_center import EventCenter
from utils.Animation import AnimationManager
from utils.RButton import MapleButton
import sys

class MapleWindow(QMainWindow):
    '''`Frame`主框架，一切组件的父级'''

    def __init__(self):
        # 类初始化
        super().__init__()
        self.event_center = EventCenter()
        self.anim_manager = AnimationManager()

        # 设置 无边框 | 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint) # type:ignore
        self.setAttribute(Qt.WA_TranslucentBackground) # type:ignore
        
        # 圆角半径
        self.frame_Rad = 20
        
        # VBox主布局
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(20, 20, 20, 20)  # 留出边距
        
        # ? 设置窗口背景状态
        self.splash_fade_animation = None

        # 窗口图标 | 可被调用
        self.Maple_Icon = QIcon("MapleLauncher/Image/MapleLeaf.png")
        self.setWindowIcon(self.Maple_Icon)
        
        # 初始窗口设置
        self.small_window = QSize(826,547)
        self.resize(self.small_window)
        # 展示图标
        self.splash = None
        self._show_splash_icon() 
        # 设置初始透明度为0,等待图标出现后缓速改变
        self.setWindowOpacity(0)
        
        # 创建中央部件并设置圆角背景
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.central_widget.setStyleSheet("""
            #centralWidget {
                background: rgb(255, 255, 255);
                border-radius: 20px;
            }
        """)
        self.setCentralWidget(self.central_widget)

        # 
        self.setStyleSheet(""" * {
        font-family: 'Cascadia Mono', '宋体', sans-serif;
        font-size: 20pt;
        background-color: transparent;
        border: none;
    }""")
        
        btn = MapleButton(
        text="Resize",
        theme_color="#BF514E",
        min_width=100,
        fixed_height=40,
        font_size=18
        )
        btn.clicked.connect(self._toggle_size)

        self.title_bar = QLabel("枫叶启动器 | a1.5\n 目前只有这一个label和\nRisize的RadioButton")
        self.title_bar.setObjectName("FrameTitleBar")
        self.title_bar.setAlignment(Qt.AlignLeft) #type:ignore
        self.title_bar.setStyleSheet("""
            # FrameTitleBar {
                background-color: rgb(191, 81, 78);
                font-family: 'Cascadia Mono', '宋体', sans-serif;
                font-size: 20pt;
            }
        """)

        # 设置主要控件到frame_layout(VBox)
        frame_layout.addWidget(self.title_bar)
        frame_layout.addWidget(btn)

        self.central_widget.setLayout(frame_layout)



    def paintEvent(self, event): #type:ignore
        """重绘窗口，实现圆角效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        
        # 绘制圆角矩形背景
        brush = QBrush(QColor(240, 240, 240, 200))  # 半透明浅灰色背景
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen) #type:ignore
        
        # 绘制圆角矩形
        rect = self.rect()
        painter.drawRoundedRect(rect, self.frame_Rad, self.frame_Rad)

    def mousePressEvent(self, event): #type:ignore
        """实现窗口拖动功能"""
        if event.button() == Qt.LeftButton: #type:ignore
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event): #type:ignore
        """实现窗口拖动功能"""
        if hasattr(self, 'drag_pos') and event.buttons() == Qt.LeftButton: #type:ignore
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def _show_splash_icon(self):
        """显示启动图标（修复淡入动画）"""
        self.splash = QLabel()
        pixmap = self.Maple_Icon.pixmap(200, 200)

        # 窗体属性 -> 图标窗口完全隐形 | 不可选中
        self.splash.setAttribute(Qt.WA_TranslucentBackground) #type:ignore
        self.splash.setWindowFlags(
            Qt.SplashScreen | #type:ignore
            Qt.FramelessWindowHint | #type:ignore
            Qt.WindowStaysOnTopHint #type:ignore
    )
        self.splash.setPixmap(pixmap)
        self.splash.setAlignment(Qt.AlignCenter) #type:ignore

        # 居中显示
        screen = QApplication.primaryScreen().availableGeometry()
        self.splash.move(
            (screen.width() - pixmap.width()) // 2,
            (screen.height() - pixmap.height()) // 2
        )

        # 修复淡入动画（关键修改）
        self.splash.show()

        # 创建并保留动画对象
        self.splash_fade_animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.splash_fade_animation.setDuration(400)
        self.splash_fade_animation.setStartValue(0)
        self.splash_fade_animation.setEndValue(1.0)
        self.splash_fade_animation.start()

        QTimer.singleShot(1700, self._close_splash)

    def _delayed_show(self):
        """ 延迟显示并启动动画 """
        self.resize(self.small_window)
        self.show()
        self.anim_manager.play("resize_large")

    def _close_splash(self):
        """关闭启动图标"""
        if self.splash:
            self.splash.close()
            self.splash = None
        self._setup_animations()
        QTimer.singleShot(250, self._delayed_show)

    def _setup_animations(self):
        # 窗口显示动画
        (self.anim_manager
            .register("window_enter", self, "fade", duration=500)
            .bind_to(self.event_center.window_show, "window_enter"))

        # 窗口缩放动画（注册两种尺寸）
        (self.anim_manager
            .register("resize_small", self, "scale",
                     start_size=self.small_window,
                     end_size=QSize(600, 400),
                     duration=500,
                     easing=QEasingCurve.Type.OutBack)
            .register("resize_large", self, "scale",
                     start_size=QSize(600, 400),
                     end_size=self.small_window,
                     duration=500,
                     easing=QEasingCurve.Type.OutBack))
        
    def _toggle_size(self):
        """ 切换窗口大小（现在直接触发动画） """
        if self.width() > 600:
            self.anim_manager.play("resize_small")
        else:
            self.anim_manager.play("resize_large")

    def showEvent(self, event): #type:ignore
        """ 触发窗口显示事件 """
        self.event_center.window_show.emit()
        super().showEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MapleWindow()
    sys.exit(app.exec_())