from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QApplication)
from PyQt5.QtCore import (Qt)

class ConsoleApp(QWidget):
    """"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Console Application")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Enter command...")
        
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_field)
        self.setLayout(layout)
    

# 使用示例
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    console = ConsoleApp()
    console.show()
    sys.exit(app.exec_())