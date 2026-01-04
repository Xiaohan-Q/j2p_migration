"""Python 代码生成模块"""
from typing import Dict, List, Any, Optional
import textwrap


class JavaASTTranslator:
    """将 Java AST 节点转换为 Python 代码"""

    def __init__(self, class_name: str = None, is_static_context: bool = False):
        """
        初始化转换器

        Args:
            class_name: 当前类名（用于访问类变量）
            is_static_context: 是否在静态方法中
        """
        self.class_name = class_name
        self.is_static_context = is_static_context

    def translate_expression(self, expr) -> str:
        """转换表达式"""
        expr_type = type(expr).__name__

        if expr_type == 'Literal':
            return str(expr.value)

        if expr_type == 'MemberReference':
            member = expr.member
            if member and member.isupper():
                if self.is_static_context and self.class_name:
                    return f"{self.class_name}._{member}"
                else:
                    return f"self._{member}" if not self.is_static_context else f"_{member}"
            return member

        elif expr_type == 'BinaryOperation':
            left = self.translate_expression(expr.operandl)
            right = self.translate_expression(expr.operandr)
            operator = expr.operator
            return f"{left} {operator} {right}"

        elif expr_type == 'MethodInvocation':
            method_name = expr.member
            args = [self.translate_expression(arg) for arg in (expr.arguments or [])]
            args_str = ", ".join(args)
            return f"{method_name}({args_str})"

        else:
            return f"# TODO: translate {expr_type}"

    def translate_statement(self, stmt) -> str:
        """转换语句"""
        stmt_type = type(stmt).__name__

        if stmt_type == 'ReturnStatement':
            if stmt.expression:
                expr = self.translate_expression(stmt.expression)
                return f"return {expr}"
            else:
                return "return"

        elif stmt_type == 'StatementExpression':
            expr = self.translate_expression(stmt.expression)
            return expr

        else:
            return f"# TODO: translate {stmt_type}"

    def translate_body(self, body_statements: List) -> List[str]:
        """转换方法体"""
        if not body_statements:
            return ["pass"]

        lines = []
        for stmt in body_statements:
            translated = self.translate_statement(stmt)
            lines.append(translated)

        return lines if lines else ["pass"]


class PythonCodeGenerator:
    """Python 代码生成器"""

    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.generated_code = []
        self.current_class_name = None  # 当前处理的类名

    def _indent(self, code: str, level: int = 1) -> str:
        """添加缩进"""
        indent = ' ' * (self.indent_size * level)
        return textwrap.indent(code, indent)

    def generate_imports(self, imports: List[str]) -> str:
        """生成导入语句"""
        if not imports:
            return ""

        standard_imports = ["from typing import Dict, List, Any, Optional"]
        all_imports = standard_imports + imports

        unique_imports = sorted(set(all_imports))

        return "\n".join(unique_imports) + "\n\n"

    def generate_field(self, field: Dict[str, Any], is_class_level: bool = False) -> str:
        """生成字段/属性代码"""
        name = field.get('python_name', field['name'])
        field_type = field.get('type', 'Any')
        initializer = field.get('initializer')

        if is_class_level or field.get('is_class_variable'):
            if initializer:
                return f"{name}: {field_type} = {initializer}"
            else:
                return f"{name}: {field_type}"
        else:
            if initializer:
                return f"self.{name}: {field_type} = {initializer}"
            else:
                return f"self.{name}: {field_type} = None"

    def generate_parameter_list(self, parameters: List[Dict[str, Any]],
                               include_self: bool = False) -> str:
        """生成参数列表"""
        params = []

        if include_self:
            params.append("self")

        for param in parameters:
            annotation = param.get('annotation', param['name'])
            params.append(annotation)

        return ", ".join(params)

    def generate_method(self, method: Dict[str, Any]) -> str:
        """生成方法代码"""
        lines = []

        for decorator in method.get('decorators', []):
            lines.append(decorator)

        method_name = method.get('python_name', method['name'])
        is_static = method.get('is_static', False)

        params = self.generate_parameter_list(
            method.get('parameters', []),
            include_self=not is_static and method_name != '__init__'
        )

        return_type = method.get('return_type', 'None')
        signature = f"def {method_name}({params}) -> {return_type}:"

        lines.append(signature)

        body = method.get('body')
        if body and isinstance(body, list):
            try:
                translator = JavaASTTranslator(
                    class_name=self.current_class_name,
                    is_static_context=is_static
                )
                body_lines = translator.translate_body(body)
                for line in body_lines:
                    lines.append(self._indent(line))
            except Exception as e:
                lines.append(self._indent(f'# 方法体转换失败: {e}'))
                lines.append(self._indent('pass'))
        else:
            lines.append(self._indent('"""TODO: 实现方法体"""'))
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_constructor(self, constructor: Dict[str, Any],
                            fields: List[Dict[str, Any]]) -> str:
        """生成构造函数 (__init__)"""
        lines = []

        params = ["self"]
        for param in constructor.get('parameters', []):
            params.append(param.get('annotation', param['name']))

        signature = f"def __init__({', '.join(params)}):"
        lines.append(signature)

        has_body = False
        for field in fields:
            if not field.get('is_class_variable') and not field.get('is_constant'):
                field_init = self.generate_field(field, is_class_level=False)
                lines.append(self._indent(field_init))
                has_body = True

        if not has_body:
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_class(self, class_info: Dict[str, Any]) -> str:
        """生成类代码"""
        lines = []

        class_name = class_info['name']
        base_classes = class_info.get('base_classes', [])

        if base_classes:
            class_def = f"class {class_name}({', '.join(base_classes)}):"
        else:
            class_def = f"class {class_name}:"

        lines.append(class_def)

        lines.append(self._indent(f'"""Java 类 {class_name} 的 Python 实现"""'))
        lines.append("")

        class_vars = [f for f in class_info.get('fields', [])
                     if f.get('is_class_variable') or f.get('is_constant')]

        for field in class_vars:
            field_code = self.generate_field(field, is_class_level=True)
            lines.append(self._indent(field_code))

        if class_vars:
            lines.append("")

        constructors = class_info.get('constructors', [])
        instance_fields = [f for f in class_info.get('fields', [])
                          if not f.get('is_class_variable') and not f.get('is_constant')]

        if constructors:
            constructor_code = self.generate_constructor(
                constructors[0],
                instance_fields
            )
            lines.append(self._indent(constructor_code))
            lines.append("")
        elif instance_fields:
            default_constructor = {'parameters': []}
            constructor_code = self.generate_constructor(
                default_constructor,
                instance_fields
            )
            lines.append(self._indent(constructor_code))
            lines.append("")

        for method in class_info.get('methods', []):
            method_code = self.generate_method(method)
            lines.append(self._indent(method_code))
            lines.append("")

        if len(lines) == 3:
            lines.append(self._indent('pass'))

        return "\n".join(lines)

    def generate_code(self, python_structure: Dict[str, Any]) -> str:
        """生成完整的 Python 代码"""
        code_parts = []

        code_parts.append('"""')
        code_parts.append('自动从 Java 代码迁移生成')
        code_parts.append('Generated by Java to Python Migration Tool')
        code_parts.append('"""')
        code_parts.append('')

        imports = self.generate_imports(python_structure.get('imports', []))
        if imports:
            code_parts.append(imports)

        for i, class_info in enumerate(python_structure.get('classes', [])):
            class_code = self.generate_class(class_info)
            code_parts.append(class_code)
            if i < len(python_structure.get('classes', [])) - 1:
                code_parts.append('\n')

        code_parts.append('\n')
        code_parts.append('if __name__ == "__main__":')
        code_parts.append('    # TODO: 添加主程序入口')
        code_parts.append('    pass')

        return "\n".join(code_parts)

    def format_code(self, code: str) -> str:
        """格式化代码"""
        lines = code.split('\n')
        formatted_lines = []
        prev_blank = False

        for line in lines:
            is_blank = line.strip() == ''

            if is_blank and prev_blank:
                continue

            formatted_lines.append(line)
            prev_blank = is_blank

        result = '\n'.join(formatted_lines)
        if not result.endswith('\n'):
            result += '\n'

        return result

    def save_to_file(self, code: str, filename: str) -> None:
        """保存代码到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"代码已保存到: {filename}")


def generate_python_code(mapped_code: str) -> str:
    """根据映射后的代码生成 Python 代码 (兼容旧接口)"""
    return mapped_code
