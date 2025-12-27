"""
语义映射模块
将 Java 代码结构映射为 Python 等价语义
"""
from typing import Dict, List, Any, Optional


class SemanticMapper:
    """Java 到 Python 的语义映射器"""

    # Java 类型到 Python 类型映射
    TYPE_MAPPING = {
        'int': 'int',
        'long': 'int',
        'short': 'int',
        'byte': 'int',
        'float': 'float',
        'double': 'float',
        'boolean': 'bool',
        'char': 'str',
        'String': 'str',
        'void': 'None',
        'Integer': 'int',
        'Long': 'int',
        'Float': 'float',
        'Double': 'float',
        'Boolean': 'bool',
        'Character': 'str',
        'List': 'list',
        'ArrayList': 'list',
        'Set': 'set',
        'HashSet': 'set',
        'Map': 'dict',
        'HashMap': 'dict',
    }

    # Java 导入到 Python 导入映射
    IMPORT_MAPPING = {
        'java.util.List': 'from typing import List',
        'java.util.ArrayList': '',  # Python 使用内置 list
        'java.util.Set': 'from typing import Set',
        'java.util.HashSet': '',  # Python 使用内置 set
        'java.util.Map': 'from typing import Dict',
        'java.util.HashMap': '',  # Python 使用内置 dict
        'java.io.IOException': '',  # Python 使用内置异常
        'java.lang.String': '',  # Python 内置
    }

    def __init__(self):
        self.mapped_structure = {}

    def _to_snake_case(self, name: str) -> str:
        """
        将驼峰命名转换为 snake_case

        Args:
            name: 驼峰命名字符串

        Returns:
            snake_case 命名字符串
        """
        import re
        # 在大写字母前插入下划线
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # 处理连续大写字母
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def map_type(self, java_type: str) -> str:
        """
        映射 Java 类型到 Python 类型

        Args:
            java_type: Java 类型名

        Returns:
            对应的 Python 类型
        """
        # 处理泛型类型,如 List<String>
        if '<' in java_type:
            base_type = java_type.split('<')[0]
            generic_type = java_type.split('<')[1].rstrip('>')

            mapped_base = self.TYPE_MAPPING.get(base_type, base_type)
            mapped_generic = self.TYPE_MAPPING.get(generic_type, generic_type)

            if mapped_base in ['list', 'set']:
                return f'{mapped_base.capitalize()}[{mapped_generic}]'
            elif mapped_base == 'dict':
                return f'Dict[str, {mapped_generic}]'

        # 处理数组类型,如 int[]
        if java_type.endswith('[]'):
            base_type = java_type[:-2]
            mapped_base = self.TYPE_MAPPING.get(base_type, base_type)
            return f'List[{mapped_base}]'

        return self.TYPE_MAPPING.get(java_type, java_type)

    def map_imports(self, java_imports: List[str]) -> List[str]:
        """
        映射 Java 导入到 Python 导入

        Args:
            java_imports: Java 导入列表

        Returns:
            Python 导入语句列表
        """
        python_imports = set()

        for java_import in java_imports:
            mapped = self.IMPORT_MAPPING.get(java_import, '')
            if mapped:
                python_imports.add(mapped)

        return sorted(list(python_imports))

    def map_modifiers(self, modifiers: List[str]) -> Dict[str, Any]:
        """
        映射 Java 修饰符

        Args:
            modifiers: Java 修饰符列表 (public, private, static, final 等)

        Returns:
            Python 修饰符信息字典
        """
        modifier_info = {
            'is_private': 'private' in modifiers,
            'is_static': 'static' in modifiers,
            'is_final': 'final' in modifiers,
            'is_abstract': 'abstract' in modifiers,
        }
        return modifier_info

    def _extract_initializer_value(self, initializer: Any) -> Optional[str]:
        """
        从 Java AST 初始化器中提取实际值

        Args:
            initializer: Java AST 初始化器对象

        Returns:
            Python 可用的初始化值字符串
        """
        if initializer is None:
            return None

        # 如果是字符串,尝试解析为数字或布尔值
        if isinstance(initializer, str):
            # 尝试解析为整数
            try:
                int_val = int(initializer)
                return str(int_val)
            except ValueError:
                pass

            # 尝试解析为浮点数
            try:
                float_val = float(initializer)
                return str(float_val)
            except ValueError:
                pass

            # 检查布尔值
            if initializer.lower() == 'true':
                return 'True'
            elif initializer.lower() == 'false':
                return 'False'

            # 字符串字面量 (需要加引号)
            return f'"{initializer}"'

        # 如果是字典(Literal对象),提取value字段
        if isinstance(initializer, dict):
            value = initializer.get('value')
            if value is None:
                return None
            # 递归处理
            return self._extract_initializer_value(value)

        # 如果是其他基本类型
        if isinstance(initializer, bool):
            return 'True' if initializer else 'False'
        if isinstance(initializer, (int, float)):
            return str(initializer)

        # 如果是对象,尝试获取value属性
        if hasattr(initializer, 'value'):
            value = initializer.value
            # 递归处理
            return self._extract_initializer_value(value)

        return None

    def map_field(self, field_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射 Java 字段到 Python 属性

        Args:
            field_info: Java 字段信息

        Returns:
            Python 属性信息
        """
        modifiers = self.map_modifiers(field_info.get('modifiers', []))

        # 提取初始化值
        initializer = self._extract_initializer_value(field_info.get('initializer'))

        python_field = {
            'name': field_info['name'],
            'type': self.map_type(field_info['type']),
            'is_class_variable': modifiers['is_static'],
            'is_constant': modifiers['is_final'] and modifiers['is_static'],
            'is_private': modifiers['is_private'],
            'initializer': initializer,
            'annotation': f": {self.map_type(field_info['type'])}"
        }

        # Python 命名约定
        if python_field['is_private']:
            python_field['python_name'] = f"_{field_info['name']}"
        elif python_field['is_constant']:
            python_field['python_name'] = field_info['name'].upper()
        else:
            python_field['python_name'] = field_info['name']

        return python_field

    def map_method(self, method_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射 Java 方法到 Python 方法

        Args:
            method_info: Java 方法信息

        Returns:
            Python 方法信息
        """
        modifiers = self.map_modifiers(method_info.get('modifiers', []))

        # 映射参数
        params = []
        for param in method_info.get('parameters', []):
            params.append({
                'name': param['name'],
                'type': self.map_type(param['type']),
                'annotation': f"{param['name']}: {self.map_type(param['type'])}"
            })

        # 映射返回类型
        return_type = self.map_type(method_info.get('return_type', 'void'))

        python_method = {
            'name': method_info['name'],
            'parameters': params,
            'return_type': return_type,
            'is_static': modifiers['is_static'],
            'is_abstract': modifiers['is_abstract'],
            'is_private': modifiers['is_private'],
            'body': method_info.get('body')
        }

        # Python 命名约定
        method_name = method_info['name']
        if python_method['is_private']:
            python_method['python_name'] = f"_{self._to_snake_case(method_name)}"
        else:
            # 转换为 snake_case
            python_method['python_name'] = self._to_snake_case(method_name)

        # 确定装饰器
        decorators = []
        if python_method['is_static']:
            decorators.append('@staticmethod')
        if python_method['is_abstract']:
            decorators.append('@abstractmethod')

        python_method['decorators'] = decorators

        return python_method

    def map_class(self, class_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射 Java 类到 Python 类

        Args:
            class_info: Java 类信息

        Returns:
            Python 类信息
        """
        # 映射继承
        base_classes = []
        if class_info.get('extends'):
            base_classes.append(class_info['extends'])
        if class_info.get('implements'):
            base_classes.extend(class_info['implements'])

        # 映射字段
        fields = [self.map_field(field) for field in class_info.get('fields', [])]

        # 映射方法
        methods = [self.map_method(method) for method in class_info.get('methods', [])]

        # 映射构造函数
        constructors = []
        for constructor in class_info.get('constructors', []):
            constructors.append(self.map_constructor(constructor))

        python_class = {
            'name': class_info['name'],
            'base_classes': base_classes,
            'fields': fields,
            'methods': methods,
            'constructors': constructors,
            'is_abstract': 'abstract' in class_info.get('modifiers', [])
        }

        return python_class

    def map_constructor(self, constructor_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射 Java 构造函数到 Python __init__ 方法

        Args:
            constructor_info: Java 构造函数信息

        Returns:
            Python __init__ 方法信息
        """
        params = []
        for param in constructor_info.get('parameters', []):
            params.append({
                'name': param['name'],
                'type': self.map_type(param['type']),
                'annotation': f"{param['name']}: {self.map_type(param['type'])}"
            })

        return {
            'name': '__init__',
            'parameters': params,
            'body': constructor_info.get('body')
        }

    def map_structure(self, java_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        映射完整的 Java 代码结构到 Python

        Args:
            java_structure: Java 代码结构(来自 ast_parser)

        Returns:
            Python 代码结构
        """
        python_structure = {
            'imports': self.map_imports(java_structure.get('imports', [])),
            'classes': []
        }

        # 映射所有类
        for java_class in java_structure.get('classes', []):
            python_class = self.map_class(java_class)
            python_structure['classes'].append(python_class)

        self.mapped_structure = python_structure
        return python_structure


# 向后兼容的函数接口
def map_java_to_python(java_code: str) -> str:
    """
    映射 Java 代码到 Python 代码 (兼容旧接口)

    Args:
        java_code: Java 源代码

    Returns:
        简单映射后的 Python 代码
    """
    # 基本的字符串替换
    python_code = java_code.replace("System.out.println", "print")
    python_code = python_code.replace("public class", "class")
    python_code = python_code.replace("String[] args", "args")
    python_code = python_code.replace("public static void main", "def main")
    python_code = python_code.replace("{", ":")
    python_code = python_code.replace("}", "")
    python_code = python_code.replace(";", "")

    return python_code
