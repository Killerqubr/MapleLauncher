import PyQt5
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
import warnings

def check_qt_version(required_version='5.15.0'):
    """
    检查Qt和PyQt版本兼容性
    :param required_version: 要求的最低版本号
    """
    from distutils.version import LooseVersion
    
    if LooseVersion(QT_VERSION_STR) < LooseVersion(required_version):
        warnings.warn(
            f"Qt版本 {QT_VERSION_STR} 低于推荐版本 {required_version}. "
            "某些功能可能不可用。",
            RuntimeWarning
        )
    
    if LooseVersion(PYQT_VERSION_STR) < LooseVersion(required_version):
        warnings.warn(
            f"PyQt版本 {PYQT_VERSION_STR} 低于推荐版本 {required_version}. "
            "某些功能可能不可用。",
            RuntimeWarning
        )

def verify_imports():
    """验证所有必需的导入是否可用"""
    required_modules = [
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
    ]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError as e:
            raise ImportError(
                f"必需模块 {module} 不可用。请确保安装了完整版本的PyQt5。"
            ) from e