from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QSize, QRectF, QRect
from ..api.animation import AnimationAPI
from ..api.styles import StyleAPI
from ..api.widgets import WidgetAPI
from ..utils.logger import setup_logging

from PyQt5.QtWidgets import QGraphicsBlurEffect, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QScreen, QPixmap, QPainter, QColor, QPainterPath

from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QCursor

class AcrylicWindow(QMainWindow):
    def __init__(self, title="Maple Leaf Launcher"):
        super().__init__()
        # 窗口基础设置
        self.setWindowTitle(title)
        self.resize(826, 547)
        
        # 启用无边框和透明背景
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) #type:ignore
        self.setAttribute(Qt.WA_TranslucentBackground) #type:ignore
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        
        
        # 创建自定义标题栏
        self._setup_title_bar()
        
        # 设置默认样式
        self.setStyleSheet("""
            * {
                font-family: 'Cascadia Mono', '宋体', sans-serif;
                font-size: 18pt;
            }
            #centralWidget {
                background-color: rgb(255, 255, 255);
                border-radius: 15px;
            }
            #titleBar {
                background-color: rgb(191, 81, 78);
                font-family: 'Cascadia Mono', '宋体', sans-serif;
                font-size: 20pt;
                border-radius: 15px 15px 0 0;
                padding: 5px;
            }
            #titleLabel {
                color: white;
                font-size: 12px;
                padding-left: 10px;
            }
            #windowButtons {
                spacing: 5px;
            }
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                min-width: 30px;
                min-height: 30px;
                border-radius: 20;
            }
            QPushButton:hover {
                background: rgba(52, 255, 7, 0.75);
                border-radius: 4px;
                border-radius: 20;
            }
        """)

    def _setup_title_bar(self):
        """创建自定义标题栏"""
        # 标题栏容器
        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(30)
        
        # 标题栏布局
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 5, 0)
        title_layout.setSpacing(0)
        
        # 标题标签
        self.title_label = QLabel("Maple Leaf Launcher")
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        
        # 添加弹簧
        title_layout.addStretch()
        
        # 窗口控制按钮
        self.window_buttons = QWidget()
        self.window_buttons.setObjectName("windowButtons")
        buttons_layout = QHBoxLayout(self.window_buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        
        # 最小化按钮
        self.minimize_button = QPushButton("—")
        self.minimize_button.clicked.connect(self.showMinimized)
        buttons_layout.addWidget(self.minimize_button)
        
        # 关闭按钮
        self.close_button = QPushButton("×")
        self.close_button.clicked.connect(self.close) # type: ignore
        buttons_layout.addWidget(self.close_button)
        
        title_layout.addWidget(self.window_buttons)
        
        # 将标题栏添加到主布局
        self.central_layout = QVBoxLayout(self.central_widget)
        self.title_bar.setFixedHeight(48)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_layout.addWidget(self.title_bar)

    def toggle_maximize(self):
        """切换最大化/正常状态"""
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText("□")
        else:
            self.showMaximized()
            self.maximize_button.setText("❐")

    # 以下方法实现窗口拖动功能
    def mousePressEvent(self, event): #type:ignore
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton: #type:ignore
            self.drag_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event): #type:ignore
        """鼠标移动事件"""
        if hasattr(self, 'drag_pos'):
            if event.buttons() == Qt.LeftButton: #type:ignore
                # 计算窗口移动距离
                move_pos = event.globalPos() - self.drag_pos
                self.move(self.pos() + move_pos)
                self.drag_pos = event.globalPos()
                event.accept()

    def mouseReleaseEvent(self, event): #type:ignore
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton and hasattr(self, 'drag_pos'): #type:ignore
            del self.drag_pos
            event.accept()

    def paintEvent(self, event): # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. 绘制标题栏（直角）
        title_bar_rect = QRect(0, 0, self.width(), self.title_bar.height())
        title_bar_path = QPainterPath()
        painter.fillRect(title_bar_rect, QColor(59, 66, 82, 230))  # 标题栏颜色
#        title_bar_path.addRoundedRect(title_bar_rect, 15, 15,0 ,0)

        # 2. 绘制内容区域背景（圆角仅作用于底部）
        path = QPainterPath()
        content_rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(content_rect, 15, 15)  # 仅底部圆角

        painter.setClipPath(path)
        painter.fillPath(path, QColor(46, 52, 64, 180))  # 内容区域背景色

        # 3. 绘制分隔线（可选，增强标题栏与内容区的视觉分割）
        line_y = self.title_bar.height()
        painter.setPen(QColor(255, 255, 255, 30))
        painter.drawLine(0, line_y, self.width(), line_y)

        painter.end()

class BaseWindow(AcrylicWindow):
    """可复用的基础窗口类"""
    
    def __init__(self, title="PyQt Application", size=(800, 600), parent=None):
        super().__init__()
        self._title = title
        self._size = QSize(*size)
        
        # 初始化API
        self.animation = AnimationAPI(self)
        self.style = StyleAPI(self) # type: ignore
        self.widgets = WidgetAPI(self)
        
        # 设置日志
        self.logger = setup_logging(self.__class__.__name__)
        
        # 设置窗口标题
        self.title_label.setText(title)  # 更新标题栏文本
        
        self._setup_ui()
        self._connect_signals()
        
        self.logger.info(f"Window '{title}' initialized")
    
    def _setup_ui(self):
        """初始化UI界面"""
        self.setWindowTitle(self._title)
        self.setMinimumSize(self._size)
        
        # 不再重新创建 central_widget，而是使用父类创建的
        # 获取父类创建的内容区域（标题栏下方的区域）
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        
        # 主布局
        self.main_layout = QVBoxLayout(self.content_area)
        self.main_layout.setAlignment(Qt.AlignTop) # type: ignore
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 将内容区域添加到父类的 central_layout 中
        self.central_layout.addWidget(self.content_area)
        
        # 更新样式表
        self.setStyleSheet(self.styleSheet() + """
            #contentArea {
                background-color: transparent;
                border-radius: 0 0 15px 15px;
            }
        """)
    
    def _connect_signals(self):
        """连接信号与槽"""
        pass
    
    def add_widget(self, widget, stretch=0, alignment=Qt.AlignTop): # type: ignore
        """向主布局添加组件"""
        self.main_layout.addWidget(widget, stretch, alignment)
    
    def add_layout(self, layout):
        """向主布局添加子布局"""
        self.main_layout.addLayout(layout)
    
    def clear_layout(self, layout=None):
        """清空布局中的所有组件"""
        target_layout = layout or self.main_layout
        while target_layout.count():
            item = target_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())