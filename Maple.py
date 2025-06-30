from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                            QWidget, QPushButton, QLabel, QRadioButton)
from PyQt5.QtCore import (QSize, QPoint, QEasingCurve,
                            QTimer, Qt, QPropertyAnimation)
from PyQt5.QtGui import (QIcon, QBrush, QPen, QColor,
                        QPainter)
from core.event_center import EventCenter
from utils.Animation import AnimationManager
from utils.RButton import MapleButton
from utils.RTitleBar import MapleTitleBar
from utils.RCheckBox import MapleCheckBox
import sys

class MapleWindow(QMainWindow):
    """
    ``Project Maple`` | 窗口框架
    - 版本 alpha1.7
    - 改动 : 完全移除烦人的RToast类
    """
    
    __virsion__ = "a1.7"

    def __init__(self):

        # 类初始化
        super().__init__()
        # 初始化 | 事件处理, 动画处理
        self.event_center = EventCenter()
        self.anim_manager = AnimationManager()

        self.is_first_show = True
        self.was_minimized = False

        # * 不可修改的样式 | 默认启动图标, frame边界圆角, 窗口无边框, 边角透明, 全局样式表
        self.Maple_Icon = QIcon("MapleLauncher a1.7/Image/MapleLeaf.png")
        self.setWindowIcon(self.Maple_Icon)

        self.frame_Rad = 20

        self.setWindowFlags(Qt.FramelessWindowHint) # type: ignore
        self.setAttribute(Qt.WA_TranslucentBackground) # type: ignore

        self.setStyleSheet(""" * {
        font-family: 'Cascadia Mono', '方正小标宋简体', sans-serif;
        font-size: 20pt;
        background-color: transparent;
        border: none;
    }""")
        
        # * 可修改的样式 | 主题色, 背景色(CentralWidget), 消息框出现位置
        self.accentColor = QColor(191,81,78)
        self.centralWidgetColor = QColor(100,100,100)
        self.toastAppear = 'top-right'
        
        # 框架布局frameLayout | VBox样式
        frameLayout = QVBoxLayout()
        frameLayout.setContentsMargins(10, 10, 10, 10)  # 留出边距
        
        # ? 设置窗口背景状态
        self.splash_fade_animation = None
        
        # 初始窗口设置
        self.small_window = QSize(826,547)
        self.resize(self.small_window)
        # 展示图标
        self.splash = None
        self._show_splash_icon() 
        # 设置初始透明度为0,等待图标出现后缓速改变
        self.setWindowOpacity(0)
        
        # * Widget-I | 创立中心控件,管理窗体范围: 标题栏,次中心控件 | 窗体VBox
        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setStyleSheet("""
            #centralWidget {
                background: rgb(100,100,100);
                border-radius: 20px;
            }
        """)
        self.setCentralWidget(self.centralWidget)
        
        # II | 创立次中心控件,管理主要内容
        self.content_container = QWidget()
        self.content_container.setObjectName("contentContainer")
        self.content_container.setStyleSheet("""
            #contentContainer {
                background-color: white;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
            }
        """)
        self.contentLayout = QVBoxLayout(self.content_container)
        self.contentLayout.setContentsMargins(20, 20, 20, 20)  # 内容边距
        self.contentLayout.setSpacing(0)

        self.Label = QLabel("Hello World!")


        self.checkbox = MapleCheckBox(
            theme_color=self.accentColor.name(),
            size=35)
        self.contentLayout.addWidget(self.checkbox)

        # III | 创建测试按钮
        self.resizeButton = MapleButton(
            text="Resize | 窗口大小变换",
            frameColor="#BF514E",
            backgroundColor="#EEDDDD",
            min_width=100,
            fixed_height=40,
            font_size=18,
            borderRadius=15
        )

        self.resizeButton.clicked.connect(self._toggle_size)
        self.Title = MapleTitleBar(self, title="Maple | a1.7", height=50)
        self.Title.setObjectName("FrameTitleBar")
       # self.Title.setAlignment(Qt.AlignLeft) #type:ignore
        self.Title.setStyleSheet("""
            # FrameTitleBar {
                background-color: {};
                font-family: 'Cascadia Mono', '宋体', sans-serif;
                font-size: 20pt;
            }
        """)
        # 链接_toggle_size事件
        self.resizeButton.clicked.connect(self._toggle_size)
        
        # 布局self.contentLayout添加组件
        self.contentLayout.addWidget(self.Label)
        self.contentLayout.addWidget(self.resizeButton)
        self.contentLayout.addStretch()

        # 设置主要控件到frameLayout(VBox)
        frameLayout.addWidget(self.Title)
        frameLayout.addWidget(self.content_container)

        self.centralWidget.setLayout(frameLayout)


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

#    def mousePressEvent(self, event): #type:ignore
#        """实现窗口拖动功能"""
#        if event.button() == Qt.LeftButton: #type:ignore
#            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
#            event.accept()
    
#    def mouseMoveEvent(self, event): #type:ignore
#        """实现窗口拖动功能"""
#        if hasattr(self, 'drag_pos') and event.buttons() == Qt.LeftButton: #type:ignore
#            self.move(event.globalPos() - self.drag_pos)
#            event.accept()
    
    # * 启动步骤 I | 显示图标
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

        QTimer.singleShot(1200, self._close_splash)
    
    # * 启动步骤 II | 关闭图标窗口
    def _close_splash(self):
        """关闭启动图标"""
        if self.splash:
            self.splash.close()
            self.splash = None
            self._setup_animations()
        QTimer.singleShot(100, self._delayed_show)

        # * 启动步骤 III | 启用窗口动画
    def _delayed_show(self):
        """ 延迟显示并启动动画 """
        self.resize(self.small_window)
        self.show()
        self.anim_manager.play("resize_large")
      
    def _setup_animations(self):
        # 窗口初始化显示渐入动画
        (self.anim_manager
            .register("window_enter", self, "fade", duration=800)
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
        
        # 连接动画完成信号
        for anim_name in ["resize_small", "resize_large"]:
            anim = self.anim_manager._animations[anim_name]
            anim.finished.connect(lambda: self._on_animation_finished(anim_name))
        
    def on_animation_start(self):
        """动画开始时连接位置更新"""
        if hasattr(self, 'toast') and self.toast.isVisible():
            self.toast.positionChanged.connect(self.update_toast_position)
    
    def _on_animation_finished(self, anim_name):
        """动画完成后的回调"""
        self._is_animating = False
        self.resizeButton.setDisabled(False)  # 恢复按钮原色
    
    def update_toast_position(self):
        """动态更新提示框位置"""
        if hasattr(self, 'toast') and self.toast.isVisible():
            # 使用定时器确保在几何变化完成后更新
            QTimer.singleShot(10, self.toast.update_position)
    
    # * 事件 | 
    def _toggle_size(self):
        """``Project Maple`` | 可触发事件"""
        if hasattr(self, "_is_animating") and self._is_animating:
            return

        # 获取当前实际尺寸而不是动画目标尺寸
        target_small = self.width() >= self.small_window.width()

        self._is_animating = True
        self.resizeButton.setDisabled(True)  # 按钮变灰

        if target_small:
            # 先同步设置尺寸再开始动画
    #        self.resize(self.small_window)
            self.anim_manager.play("resize_small")
        else:
            # 先同步设置尺寸再开始动画
    #        self.resize(QSize(600, 400))
            self.anim_manager.play("resize_large")


    def showEvent(self, event): # type:ignore
        """处理窗口显示事件"""
        if self.is_first_show:
            # 首次显示时触发动画
            self.event_center.window_show.emit()
            self.is_first_show = False
        elif self.was_minimized:
            # 从最小化恢复时不触发动画
            self.was_minimized = False
        super().showEvent(event)