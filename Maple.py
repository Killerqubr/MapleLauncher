from Library.core.application import PyQtApp
from Library.core.window import BaseWindow
from Library.core.application import PyQtApp
from Library.core.window import BaseWindow

from PyQt5.QtWidgets import QPushButton, QLabel

class MapleWindow(BaseWindow):
    """``MapleLauncher``启动器的基本窗口框架"""
    def __init__(self):
        super().__init__(title="Maple Launcher", size=(826, 547))
        self._setup_custom_ui()
    
    def _setup_custom_ui(self):
        # 添加标签
        self.label = QLabel("Welcome to PyQt Framework!")
        self.add_widget(self.label)
        
        # 添加按钮
        self.button = QPushButton("Click Me!")
        self.add_widget(self.button)
        
        # 连接信号
        self.button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        """按钮点击事件处理"""
        self.label.setText("Button was clicked!")
        # 使用动画API
        self.animation.fade_out(self.label, duration=1000)
        self.animation.fade_in(self.label, duration=1000)

if __name__ == "__main__":
    app = PyQtApp("MapleLauncher")
    window = MapleWindow()
    app.run(window)