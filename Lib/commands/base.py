from typing import Callable, Tuple

class CommandNode:
    """表示命令树中的一个节点"""
    def __init__(self, name: str, validator: Callable = None, children: list = None, optional: bool = False): # type: ignore
        self.name = name
        self.validator = validator if validator else (lambda x: (True, ""))
        self.children = children if children else []
        self.optional = optional
    
    def validate(self, value: str) -> Tuple[bool, str]:
        return self.validator(value)

class CommandSystem:
    """灵活的命令系统，支持父子层级参数验证"""
    def __init__(self):
        self.command_tree = self._build_command_tree()
    
    def _build_command_tree(self):
        """构建命令树结构"""
        return {
            "/var": CommandNode("var", children=[
                CommandNode("<var_name>", str),
                CommandNode("<operation>", str),
                CommandNode("[value]", optional=True)
            ]),
            "/logger": CommandNode("logger", children=[
                CommandNode("<message>", str)
            ])
        }
    
    def parse(self, text: str) -> Tuple[bool, str]:
        """解析并执行命令"""
        # 实现解析逻辑...
        return None # type: ignore