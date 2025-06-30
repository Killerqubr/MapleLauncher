from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QComboBox, 
    QCheckBox, QRadioButton, QSpinBox, QDoubleSpinBox,
    QSlider, QProgressBar, QTextEdit, QListWidget,
    QTreeWidget, QTableWidget, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class WidgetAPI:
    """提供快速创建和配置组件的API"""
    
    def __init__(self, window):
        self.window = window
    
    def create_button(self, text, icon=None, tooltip=None, size=None):
        """创建按钮"""
        btn = QPushButton(text)
        if icon:
            btn.setIcon(QIcon(icon))
        if tooltip:
            btn.setToolTip(tooltip)
        if size:
            btn.setFixedSize(QSize(*size))
        return btn
    
    def create_label(self, text, align=Qt.AlignLeft, style=None):
        """创建标签"""
        label = QLabel(text)
        label.setAlignment(align)
        if style:
            label.setStyleSheet(style)
        return label
    
    def create_line_edit(self, placeholder="", default_text="", max_length=None):
        """创建单行文本框"""
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setText(default_text)
        if max_length:
            edit.setMaxLength(max_length)
        return edit
    
    def create_combobox(self, items=None, editable=False):
        """创建下拉框"""
        combo = QComboBox()
        combo.setEditable(editable)
        if items:
            combo.addItems(items)
        return combo
    
    def create_spinbox(self, min_val=0, max_val=100, step=1, default=0):
        """创建数字输入框"""
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setSingleStep(step)
        spin.setValue(default)
        return spin
    
    def create_checkbox(self, text, checked=False, tristate=False):
        """创建复选框"""
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setTristate(tristate)
        return checkbox
    
    def create_progress_bar(self, min_val=0, max_val=100, value=0, text_visible=True):
        """创建进度条"""
        bar = QProgressBar()
        bar.setRange(min_val, max_val)
        bar.setValue(value)
        bar.setTextVisible(text_visible)
        return bar
    
    def create_groupbox(self, title, layout=None, flat=False):
        """创建分组框"""
        group = QGroupBox(title)
        group.setFlat(flat)
        if layout:
            group.setLayout(layout)
        return group
    
    def create_separator(self, orientation=Qt.Horizontal):
        """创建分隔线"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine if orientation == Qt.Horizontal else QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line