## Project Maple

这个项目使用PyQt5构建一系列我想要的互动效果，算是对现代化窗口构建的*小小尝试*<br>
作者**Killerqubr**, 如果喜欢我的作品， 可以看看[我的B站链接](https://space.bilibili.com/651662573?spm_id_from=333.1007.0.0)

---

#### cd 2025.6开发版本<br>
> ***现在的开发版本***
- 新增``CentralWidget``类, 并创建了可修改的样式表，设置圆角边框 | 此类是所有组件的主框架
- 新增``Animation``类，并创建了一些基本的动画控件 | 此类控制所有的控件动画
- 重命名文件夹*Lib*为*Library*，删除了``base.py, highlighter.py``
- <Library/> 新增*utils*文件夹，并新建logger.py用于测试日志功能 | 此文件夹用于存放工具函数
- <Library/> 新增*core*文件夹，并新建了一些窗体组件和杂项 | ``application.py, virsion_check.py, window.py``
- 修改``frameLayout``的部分内容
- 移除了窗口边框和圆角边框
- 修复部分漏洞

#### cd 2025.5开发版本<br>
> ***最早的开发版本***
- 创建``PyQt5``最基本的窗口框架
- 新增``frameLayout``属性, 继承自``QVBoxLayout`` | 窗口的基本框架
- 新增一些``TextCtrl``组件，用于测试
- 移入了一些之前的项目，用于测试 | ``func.py, Intro.mov, base.py, highlighter.py``
- 储存了一些可用的图标 | ``Strike.ico``
- 试做了一个日志文档，用于测试 | ``log,txt``
