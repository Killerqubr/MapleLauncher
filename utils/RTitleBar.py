from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton, QMainWindow,
                            QSpacerItem, QSizePolicy, QVBoxLayout)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QColor, QPainter, QPen, QIcon
from utils.RPushButton import MapleIconButton
    
class MapleTitleBar(QWidget):
    """
    ``Project Maple`` | 特殊组件
    - 版本 ``alpha 1.6``
    """
    
    def __init__(self, parent=None, title="", headIcon="MapleLauncher a1.7/Image/MapleLeaf.png",
                height=40, closeIcon="MapleLauncher a1.7/Image/Strike.ico"):
        super().__init__(parent)

        self.colseIcon = closeIcon
        
        # 确保parent_window正确设置
        self.parent_window = parent if isinstance(parent, QMainWindow) else None
        if self.parent_window is None:
            # 尝试从parent()获取
            self.parent_window = self.parent()
        
        if self.parent_window is None:
            raise ValueError("MapleTitleBar must be created with a valid parent QMainWindow")
        
        # 初始化所有实例属性
        self._title_height = height
        self._separator_height = 2
        self._separator_color = QColor(191, 81, 78)
        self._separator_margin = 0
        self.drag_pos = None
        self.draggable = True  # 初始化draggable属性
        
        self.setFixedHeight(self._title_height + self._separator_height)
        self._setup_ui(title, headIcon)
        self._setup_style()

    def _setup_ui(self, title, icon):
        """初始化UI布局"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 标题栏主体部分
        self.title_widget = QWidget()
        self.title_widget.setFixedHeight(self._title_height)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(15, 0, 15, 0)
        self.title_layout.setSpacing(10)
        
        # 图标和标题
        self.icon_label = QLabel()
        if icon:
            self.setIcon(icon)
            
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) # type:ignore
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.title_label.setStyleSheet("""
            QLabel {
                    color: white
            }
        """)
        
        # 右侧按钮容器
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(5, 5, 5, 5)
        self.button_layout.setSpacing(5)
        
        # 默认按钮 (最小化/最大化/关闭)
        self.btn_minimize = QPushButton("−")
        self.btn_maximize = QPushButton("□")
        self.btn_close = MapleIconButton(parent=self.parent(), icon_path=self.colseIcon)
        
        # 设置按钮大小和样式
        button_size = 40
        for btn in [self.btn_minimize, self.btn_maximize, self.btn_close]:
            btn.setFixedSize(button_size, button_size)
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: %dpx;
                    font-weight: bold;
                    color: white;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: rgb(255, 255, 255);
                }
            """ % (button_size // 2))
        
        # 特殊样式关闭按钮
        self.btn_close.setStyleSheet("""
            QPushButton {
                border-radius: %dpx;
                font-weight: bold;
                color: white;
                background-color: #FF5C5C;
            }
            QPushButton:hover {
                background-color: #FF3B3B;
            }
        """ % (button_size // 2))
        
        # 将组件添加到布局
        self.button_layout.addWidget(self.btn_minimize)
        self.button_layout.addWidget(self.btn_maximize)
        self.button_layout.addWidget(self.btn_close)
        
        self.title_layout.addWidget(self.icon_label)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.button_container)
        
        # 分隔线部件
        self.separator = QWidget()
        self.separator.setFixedHeight(self._separator_height)
        
        self.main_layout.addWidget(self.title_widget)
        self.main_layout.addWidget(self.separator)
        
        # 连接按钮信号
        self.btn_minimize.clicked.connect(self._on_minimize)
        self.btn_maximize.clicked.connect(self._on_maximize)
        self.btn_close.clicked.connect(self._on_close)
    
    def _setup_style(self):
        """设置默认样式"""
        self.setStyleSheet("""
            MapleTitleBar {
                background-color: transparent;
            }
            QWidget {
                background-color: #BF514E;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
    
    def paintEvent(self, event): # type:ignore
        """绘制分隔线"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制分隔线
        pen = QPen(self._separator_color)
        pen.setWidth(self._separator_height)
        painter.setPen(pen)
        
        line_y = self._title_height + self._separator_height / 2
        painter.drawLine(
            self._separator_margin, 
            int(line_y),
            self.width() - self._separator_margin, 
            int(line_y)
        )
    
    def setIcon(self, icon):
        """设置标题栏图标"""
        if isinstance(icon, QIcon):
            self.icon_label.setPixmap(icon.pixmap(24, 24))
        elif isinstance(icon, str):
            self.icon_label.setPixmap(QIcon(icon).pixmap(24, 24))
    
    def setTitle(self, text):
        """设置标题文本"""
        self.title_label.setText(text)
    
    def setSeparatorColor(self, color):
        """设置分隔线颜色"""
        self._separator_color = QColor(color)
        self.update()
    
    def setSeparatorMargin(self, margin):
        """设置分隔线边距"""
        self._separator_margin = margin
        self.update()
    
    def setHeight(self, height):
        """设置标题栏高度(带动画)"""
        anim = QPropertyAnimation(self, b"titleHeight")
        anim.setDuration(300)
        anim.setStartValue(self._title_height)
        anim.setEndValue(height)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
    
    def getTitleHeight(self):
        """获取标题栏高度(用于动画)"""
        return self._title_height
    
    def setTitleHeight(self, height):
        """设置标题栏高度(用于动画)"""
        self._title_height = height
        self.title_widget.setFixedHeight(height)
        self.setFixedHeight(height + self._separator_height)
    
    #titleHeight = pyqtProperty(int, getTitleHeight, setTitleHeight)
    
    def addButton(self, button, position="right"):
        """向标题栏添加自定义按钮"""
        if position == "left":
            self.title_layout.insertWidget(2, button)  # 在图标和标题后插入
        else:
            self.button_layout.insertWidget(0, button)  # 在系统按钮前插入
    
    def addWidget(self, widget, position="left"):
        """向标题栏添加自定义组件"""
        if position == "left":
            self.title_layout.insertWidget(1, widget)  # 在图标后插入
        else:
            self.title_layout.insertWidget(self.title_layout.count() - 1, widget)
    
    # 其余方法与之前相同...
    def mousePressEvent(self, event: QMouseEvent): # type:ignore
        """鼠标按下事件处理"""
        if event.button() == Qt.LeftButton and self.draggable and self.parent_window: # type:ignore
            self.drag_pos = event.globalPos() - self.parent_window.frameGeometry().topLeft() # type:ignore
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent): # type:ignore
        """鼠标移动事件处理"""
        if (self.draggable and self.drag_pos is not None and 
            event.buttons() == Qt.LeftButton and self.parent_window):# type:ignore
            self.parent_window.move(event.globalPos() - self.drag_pos) # type:ignore
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent): # type:ignore
        """鼠标释放事件处理"""
        self.drag_pos = None
        super().mouseReleaseEvent(event)
    
    def _on_minimize(self):
        """最小化窗口"""
        self.parent_window.showMinimized()# type:ignore
    
    def _on_maximize(self):
        """最大化/还原窗口"""
        if self.parent_window.isMaximized(): # type:ignore
            self.parent_window.showNormal() # type:ignore
            self.btn_maximize.setText("□")
        else:
            self.parent_window.showMaximized()# type:ignore
            self.btn_maximize.setText("❐")
    
    def _on_close(self):
        """关闭窗口"""
        self.parent_window.close()# type:ignore