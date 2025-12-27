"""
Python 代码生成模块
根据映射后的结构生成格式化的 Python 代码
"""
from typing import Dict, List, Any, Optional
import textwrap


class PythonCodeGenerator:
    """Python 代码生成器"""

    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.generated_code = []

    def _indent(self, code: str, level: int = 1) -> str:
        """添加缩进"""
        indent = ' ' * (self.indent_size * level)
        return textwrap.indent(code, indent)

    def generate_imports(self, imports: List[str]) -> str:
        """
        生成导入语句

        Args:
            imports: Python 导入列表

        Returns:
            导入语句代码
        """
        if not imports:
            return ""

        # 添加常用的导入
        standard_imports = ["from typing import Dict, List, Any, Optional"]
        all_imports = standard_imports + imports

        # 去重并排序
        unique_imports = sorted(set(all_imports))

        return "\n".join(unique_imports) + "\n\n"

    def generate_field(self, field: Dict[str, Any], is_class_level: bool = False) -> str:
        """
        生成字段/属性代码

        Args:
            field: 字段信息
            is_class_level: 是否是类级别变量

        Returns:
            字段代码
        """
        name = field.get('python_name', field['name'])
        field_type = field.get('type', 'Any')
        initializer = field.get('initializer')

        if is_class_level or field.get('is_class_variable'):
            # 类变量
            if initializer:
                return f"{name}: {field_type} = {initializer}"
            else:
                return f"{name}: {field_type}"
        else:
            # 实例变量 (在 __init__ 中)
            if initializer:
                return f"self.{name}: {field_type} = {initializer}"
            else:
                return f"self.{name}: {field_type} = None"

    def generate_parameter_list(self, parameters: List[Dict[str, Any]],
                               include_self: bool = False) -> str:
        """
        生成参数列表

        Args:
            parameters: 参数信息列表
            include_self: 是否包含 self 参数

        Returns:
            参数列表字符串
        """
        params = []

        if include_self:
            params.append("self")

        for param in parameters:
            annotation = param.get('annotation', param['name'])
            params.append(annotation)

        return ", ".join(params)

    def generate_method(self, method: Dict[str, Any]) -> str:
        """
        生成方法代码

        Args:
            method: 方法信息

        Returns:
            方法代码
        """
        lines = []

        # 添加装饰器
        for decorator in method.get('decorators', []):
            lines.append(decorator)

        # 方法签名
        method_name = method.get('python_name', method['name'])
        is_static = method.get('is_static', False)

        # 参数列表
        params = self.generate_parameter_list(
            method.get('parameters', []),
            include_self=not is_static and method_name != '__init__'
        )

        # 返回类型
        return_type = method.get('return_type', 'None')
        # 总是添加返回类型注解
        signature = f"def {method_name}({params}) -> {return_type}:"

        lines.append(signature)

        # 方法体 (简化处理,实际需要转换 Java AST 节点)
        body = method.get('body')
        if body:
            lines.append(self._indent('"""TODO: 实现方法体"""'))
            lines.append(self._indent('pass'))
        else:
            lines.append(self._indent('"""TODO: 实现方法体"""'))
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_constructor(self, constructor: Dict[str, Any],
                            fields: List[Dict[str, Any]]) -> str:
        """
        生成构造函数 (__init__)

        Args:
            constructor: 构造函数信息
            fields: 字段列表

        Returns:
            __init__ 方法代码
        """
        lines = []

        # 参数列表
        params = ["self"]
        for param in constructor.get('parameters', []):
            params.append(param.get('annotation', param['name']))

        signature = f"def __init__({', '.join(params)}):"
        lines.append(signature)

        # 初始化字段
        has_body = False
        for field in fields:
            if not field.get('is_class_variable') and not field.get('is_constant'):
                field_init = self.generate_field(field, is_class_level=False)
                lines.append(self._indent(field_init))
                has_body = True

        # 如果没有字段,添加 pass
        if not has_body:
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_class(self, class_info: Dict[str, Any]) -> str:
        """
        生成类代码

        Args:
            class_info: 类信息

        Returns:
            类代码
        """
        lines = []

        # 类定义
        class_name = class_info['name']
        base_classes = class_info.get('base_classes', [])

        if base_classes:
            class_def = f"class {class_name}({', '.join(base_classes)}):"
        else:
            class_def = f"class {class_name}:"

        lines.append(class_def)

        # 类文档字符串
        lines.append(self._indent(f'"""Java 类 {class_name} 的 Python 实现"""'))
        lines.append("")

        # 类变量/常量
        class_vars = [f for f in class_info.get('fields', [])
                     if f.get('is_class_variable') or f.get('is_constant')]

        for field in class_vars:
            field_code = self.generate_field(field, is_class_level=True)
            lines.append(self._indent(field_code))

        if class_vars:
            lines.append("")

        # 构造函数
        constructors = class_info.get('constructors', [])
        instance_fields = [f for f in class_info.get('fields', [])
                          if not f.get('is_class_variable') and not f.get('is_constant')]

        if constructors:
            constructor_code = self.generate_constructor(
                constructors[0],  # 只使用第一个构造函数
                instance_fields
            )
            lines.append(self._indent(constructor_code))
            lines.append("")
        elif instance_fields:
            # 没有构造函数但有实例字段,生成默认 __init__
            default_constructor = {'parameters': []}
            constructor_code = self.generate_constructor(
                default_constructor,
                instance_fields
            )
            lines.append(self._indent(constructor_code))
            lines.append("")

        # 方法
        for method in class_info.get('methods', []):
            method_code = self.generate_method(method)
            lines.append(self._indent(method_code))
            lines.append("")

        # 如果类为空,添加 pass
        if len(lines) == 3:  # 只有类定义和文档字符串
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_code(self, python_structure: Dict[str, Any]) -> str:
        """
        生成完整的 Python 代码

        Args:
            python_structure: Python 代码结构 (来自 semantic_mapper)

        Returns:
            完整的 Python 代码
        """
        code_parts = []

        # 文件头部注释
        code_parts.append('"""')
        code_parts.append('自动从 Java 代码迁移生成')
        code_parts.append('Generated by Java to Python Migration Tool')
        code_parts.append('"""')
        code_parts.append('')

        # 导入语句
        imports = self.generate_imports(python_structure.get('imports', []))
        if imports:
            code_parts.append(imports)

        # 生成所有类
        for i, class_info in enumerate(python_structure.get('classes', [])):
            class_code = self.generate_class(class_info)
            code_parts.append(class_code)
            # 类定义后添加两个空行 (最后一个类除外)
            if i < len(python_structure.get('classes', [])) - 1:
                code_parts.append('\n')

        # 主函数检查前添加两个空行
        code_parts.append('\n')
        code_parts.append('if __name__ == "__main__":')
        code_parts.append('    # TODO: 添加主程序入口')
        code_parts.append('    pass')

        return "\n".join(code_parts)

    def format_code(self, code: str) -> str:
        """
        格式化代码 (移除多余空行等)

        Args:
            code: 原始代码

        Returns:
            格式化后的代码
        """
        lines = code.split('\n')
        formatted_lines = []
        prev_blank = False

        for line in lines:
            is_blank = line.strip() == ''

            # 避免连续多个空行
            if is_blank and prev_blank:
                continue

            formatted_lines.append(line)
            prev_blank = is_blank

        # 确保文件末尾有换行符
        result = '\n'.join(formatted_lines)
        if not result.endswith('\n'):
            result += '\n'

        return result

    def save_to_file(self, code: str, filename: str) -> None:
        """
        保存代码到文件

        Args:
            code: Python 代码
            filename: 文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"代码已保存到: {filename}")


# 向后兼容的函数接口
def generate_python_code(mapped_code: str) -> str:
    """
    根据映射后的代码生成 Python 代码 (兼容旧接口)

    Args:
        mapped_code: 映射后的代码

    Returns:
        Python 代码
    """
    # 简单处理,直接返回映射后的代码
    return mapped_code
