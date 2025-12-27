"""
Java AST 解析器模块
使用 javalang 库解析 Java 代码并提取语法结构
"""
import javalang
from typing import Dict, List, Any, Optional
from logger import get_logger


class JavaASTParser:
    """Java 代码 AST 解析器"""

    def __init__(self):
        self.ast_tree = None
        self.parsed_structure = {}
        self.logger = get_logger()

    def parse_java_code(self, java_code: str) -> Optional[javalang.tree.CompilationUnit]:
        """
        解析 Java 代码并生成 AST

        Args:
            java_code: Java 源代码字符串

        Returns:
            解析后的 AST 树,如果解析失败则返回 None
        """
        try:
            self.ast_tree = javalang.parse.parse(java_code)
            self.logger.debug("Java 代码解析成功")
            return self.ast_tree
        except javalang.parser.JavaSyntaxError as e:
            self.logger.error(f"Java 代码语法错误: {e}")
            return None
        except Exception as e:
            self.logger.exception("解析 Java 代码时发生未知错误", exc=e)
            return None

    def extract_package(self) -> Optional[str]:
        """提取包名"""
        if self.ast_tree and self.ast_tree.package:
            return self.ast_tree.package.name
        return None

    def extract_imports(self) -> List[str]:
        """提取所有导入语句"""
        imports = []
        if self.ast_tree and self.ast_tree.imports:
            for imp in self.ast_tree.imports:
                imports.append(imp.path)
        return imports

    def extract_classes(self) -> List[Dict[str, Any]]:
        """
        提取所有类的信息

        Returns:
            类信息列表,包含类名、修饰符、父类、接口等
        """
        classes = []
        if not self.ast_tree:
            return classes

        for path, node in self.ast_tree.filter(javalang.tree.ClassDeclaration):
            class_info = {
                'name': node.name,
                'modifiers': node.modifiers or [],
                'extends': node.extends.name if node.extends else None,
                'implements': [impl.name for impl in node.implements] if node.implements else [],
                'fields': self._extract_fields(node),
                'methods': self._extract_methods(node),
                'constructors': self._extract_constructors(node)
            }
            classes.append(class_info)

        return classes

    def _extract_literal_value(self, initializer):
        """
        从 javalang Literal 对象中提取实际值

        Args:
            initializer: javalang AST 初始化器对象

        Returns:
            提取的值（保留原始类型）
        """
        if not initializer:
            return None

        # 如果是 Literal 对象,提取 value 属性
        if hasattr(initializer, 'value'):
            return initializer.value

        # 其他表达式暂时返回字符串表示
        return str(initializer)

    def _extract_fields(self, class_node) -> List[Dict[str, Any]]:
        """提取类的字段信息"""
        fields = []
        for field in class_node.fields:
            for declarator in field.declarators:
                field_info = {
                    'name': declarator.name,
                    'type': field.type.name,
                    'modifiers': field.modifiers or [],
                    'initializer': self._extract_literal_value(declarator.initializer)
                }
                fields.append(field_info)
        return fields

    def _extract_methods(self, class_node) -> List[Dict[str, Any]]:
        """提取类的方法信息"""
        methods = []
        for method in class_node.methods:
            method_info = {
                'name': method.name,
                'modifiers': method.modifiers or [],
                'return_type': method.return_type.name if method.return_type else 'void',
                'parameters': self._extract_parameters(method.parameters),
                'body': method.body
            }
            methods.append(method_info)
        return methods

    def _extract_constructors(self, class_node) -> List[Dict[str, Any]]:
        """提取构造函数信息"""
        constructors = []
        for constructor in class_node.constructors:
            constructor_info = {
                'name': constructor.name,
                'modifiers': constructor.modifiers or [],
                'parameters': self._extract_parameters(constructor.parameters),
                'body': constructor.body
            }
            constructors.append(constructor_info)
        return constructors

    def _extract_parameters(self, parameters) -> List[Dict[str, str]]:
        """提取方法或构造函数的参数信息"""
        params = []
        if parameters:
            for param in parameters:
                param_info = {
                    'name': param.name,
                    'type': param.type.name
                }
                params.append(param_info)
        return params

    def get_full_structure(self, java_code: str) -> Dict[str, Any]:
        """
        获取 Java 代码的完整结构信息

        Args:
            java_code: Java 源代码

        Returns:
            包含包名、导入、类等完整信息的字典
        """
        self.parse_java_code(java_code)

        if not self.ast_tree:
            return {}

        structure = {
            'package': self.extract_package(),
            'imports': self.extract_imports(),
            'classes': self.extract_classes()
        }

        self.parsed_structure = structure
        return structure


# 向后兼容的函数接口
def parse_java_code(java_code: str) -> Optional[javalang.tree.CompilationUnit]:
    """
    解析 Java 代码并生成 AST (兼容旧接口)

    Args:
        java_code: Java 源代码字符串

    Returns:
        解析后的 AST 树
    """
    parser = JavaASTParser()
    return parser.parse_java_code(java_code)


def extract_class_and_methods(ast_tree) -> tuple:
    """
    从 AST 中提取类名和方法名 (兼容旧接口)

    Args:
        ast_tree: Java AST 树

    Returns:
        (类名列表, 方法名列表)
    """
    classes = []
    methods = []

    if ast_tree:
        for _, node in ast_tree.filter(javalang.tree.ClassDeclaration):
            classes.append(node.name)
            for method in node.methods:
                methods.append(method.name)

    return classes, methods
