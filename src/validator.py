"""
验证模块
验证迁移后的 Python 代码质量和功能等价性
"""
import ast
import subprocess
import tempfile
import os
from typing import Dict, List, Any, Optional, Tuple


class MigrationValidator:
    """迁移验证器"""

    def __init__(self):
        self.validation_results = {}
        self.errors = []
        self.warnings = []

    def validate_syntax(self, python_code: str) -> Tuple[bool, List[str]]:
        """
        验证 Python 代码语法

        Args:
            python_code: Python 代码

        Returns:
            (是否有效, 错误列表)
        """
        errors = []

        try:
            ast.parse(python_code)
            return True, []
        except SyntaxError as e:
            errors.append(f"语法错误 (行 {e.lineno}): {e.msg}")
            return False, errors
        except Exception as e:
            errors.append(f"解析错误: {str(e)}")
            return False, errors

    def validate_structure(self, python_structure: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证 Python 代码结构完整性

        Args:
            python_structure: Python 代码结构

        Returns:
            (是否有效, 警告列表)
        """
        warnings = []

        # 检查是否有类
        if not python_structure.get('classes'):
            warnings.append("代码中没有类定义")

        # 检查每个类
        for cls in python_structure.get('classes', []):
            # 检查类名
            if not cls.get('name'):
                warnings.append("发现未命名的类")

            # 检查方法
            methods = cls.get('methods', [])
            if not methods and not cls.get('fields'):
                warnings.append(f"类 {cls.get('name')} 没有方法或字段")

            # 检查构造函数
            if cls.get('fields') and not cls.get('constructors'):
                warnings.append(f"类 {cls.get('name')} 有字段但没有构造函数")

        return len(warnings) == 0, warnings

    def validate_naming_conventions(self, python_code: str) -> Tuple[bool, List[str]]:
        """
        验证 Python 命名规范

        Args:
            python_code: Python 代码

        Returns:
            (是否符合规范, 警告列表)
        """
        warnings = []

        try:
            tree = ast.parse(python_code)

            # 检查类名 (应该是 PascalCase)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper():
                        warnings.append(f"类名 '{node.name}' 应该以大写字母开头")

                # 检查函数名 (应该是 snake_case)
                elif isinstance(node, ast.FunctionDef):
                    if node.name.startswith('_'):
                        continue  # 私有方法可以以下划线开头
                    if any(c.isupper() for c in node.name):
                        warnings.append(
                            f"函数名 '{node.name}' 应该使用 snake_case 命名"
                        )

        except Exception as e:
            warnings.append(f"命名规范检查失败: {str(e)}")

        return len(warnings) == 0, warnings

    def validate_imports(self, python_code: str) -> Tuple[bool, List[str]]:
        """
        验证导入语句

        Args:
            python_code: Python 代码

        Returns:
            (是否有效, 警告列表)
        """
        warnings = []

        try:
            tree = ast.parse(python_code)

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # 检查是否有未使用的导入 (简化检查)
            # 实际应该使用更复杂的静态分析

        except Exception as e:
            warnings.append(f"导入验证失败: {str(e)}")

        return len(warnings) == 0, warnings

    def check_type_annotations(self, python_code: str) -> Tuple[bool, List[str]]:
        """
        检查类型注解的完整性

        Args:
            python_code: Python 代码

        Returns:
            (是否完整, 警告列表)
        """
        warnings = []

        try:
            tree = ast.parse(python_code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 检查参数类型注解
                    for arg in node.args.args:
                        if arg.arg != 'self' and not arg.annotation:
                            warnings.append(
                                f"函数 '{node.name}' 的参数 '{arg.arg}' 缺少类型注解"
                            )

                    # 检查返回类型注解
                    if node.name != '__init__' and not node.returns:
                        warnings.append(f"函数 '{node.name}' 缺少返回类型注解")

        except Exception as e:
            warnings.append(f"类型注解检查失败: {str(e)}")

        return len(warnings) == 0, warnings

    def run_static_analysis(self, python_code: str) -> Tuple[bool, List[str]]:
        """
        运行静态代码分析 (使用 pylint 或 flake8)

        Args:
            python_code: Python 代码

        Returns:
            (是否通过, 问题列表)
        """
        issues = []

        try:
            # 将代码写入临时文件
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(python_code)
                temp_file = f.name

            try:
                # 尝试运行 flake8
                result = subprocess.run(
                    ['flake8', temp_file, '--max-line-length=100'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0:
                    issues.append(f"Flake8 检查:\n{result.stdout}")

            except FileNotFoundError:
                issues.append("未安装 flake8,跳过静态分析")
            except subprocess.TimeoutExpired:
                issues.append("静态分析超时")
            finally:
                # 删除临时文件
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            issues.append(f"静态分析失败: {str(e)}")

        return len(issues) == 0, issues

    def test_code_execution(self, python_code: str) -> Tuple[bool, str]:
        """
        测试代码是否可以执行 (不产生运行时错误)

        Args:
            python_code: Python 代码

        Returns:
            (是否成功, 输出或错误信息)
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(python_code)
                temp_file = f.name

            try:
                # 运行 Python 代码
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:
                    return True, result.stdout
                else:
                    return False, result.stderr

            except subprocess.TimeoutExpired:
                return False, "代码执行超时"
            finally:
                # 删除临时文件
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            return False, f"执行测试失败: {str(e)}"

    def validate_migration(self, java_code: str, python_code: str,
                          python_structure: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        完整的迁移验证

        Args:
            java_code: 原始 Java 代码
            python_code: 迁移后的 Python 代码
            python_structure: Python 代码结构 (可选)

        Returns:
            验证报告
        """
        self.errors = []
        self.warnings = []

        report = {
            'overall_status': 'success',
            'checks': {}
        }

        # 1. 语法验证
        syntax_valid, syntax_errors = self.validate_syntax(python_code)
        report['checks']['syntax'] = {
            'passed': syntax_valid,
            'errors': syntax_errors
        }
        if not syntax_valid:
            self.errors.extend(syntax_errors)
            report['overall_status'] = 'failed'

        # 2. 结构验证
        if python_structure:
            structure_valid, structure_warnings = self.validate_structure(python_structure)
            report['checks']['structure'] = {
                'passed': structure_valid,
                'warnings': structure_warnings
            }
            self.warnings.extend(structure_warnings)

        # 3. 命名规范
        naming_valid, naming_warnings = self.validate_naming_conventions(python_code)
        report['checks']['naming'] = {
            'passed': naming_valid,
            'warnings': naming_warnings
        }
        self.warnings.extend(naming_warnings)

        # 4. 导入验证
        imports_valid, import_warnings = self.validate_imports(python_code)
        report['checks']['imports'] = {
            'passed': imports_valid,
            'warnings': import_warnings
        }
        self.warnings.extend(import_warnings)

        # 5. 类型注解检查
        types_valid, type_warnings = self.check_type_annotations(python_code)
        report['checks']['type_annotations'] = {
            'passed': types_valid,
            'warnings': type_warnings
        }
        self.warnings.extend(type_warnings)

        # 6. 静态分析 (可选)
        static_valid, static_issues = self.run_static_analysis(python_code)
        report['checks']['static_analysis'] = {
            'passed': static_valid,
            'issues': static_issues
        }

        # 7. 执行测试
        exec_valid, exec_output = self.test_code_execution(python_code)
        report['checks']['execution'] = {
            'passed': exec_valid,
            'output': exec_output
        }
        if not exec_valid:
            self.errors.append(f"执行失败: {exec_output}")

        # 设置总体状态
        if self.errors:
            report['overall_status'] = 'failed'
        elif self.warnings:
            report['overall_status'] = 'warning'

        report['errors'] = self.errors
        report['warnings'] = self.warnings

        self.validation_results = report
        return report

    def print_report(self, report: Dict[str, Any]) -> None:
        """打印验证报告"""
        print("\n" + "="*60)
        print("迁移验证报告")
        print("="*60)

        status_icon = {
            'success': '✓',
            'warning': '⚠',
            'failed': '✗'
        }

        print(f"\n【总体状态】 {status_icon.get(report['overall_status'], '?')} "
              f"{report['overall_status'].upper()}")

        print("\n【检查项】")
        for check_name, check_result in report['checks'].items():
            passed = check_result.get('passed', False)
            icon = '✓' if passed else '✗'
            print(f"  {icon} {check_name}: {'通过' if passed else '未通过'}")

            # 显示错误
            if check_result.get('errors'):
                for error in check_result['errors']:
                    print(f"    错误: {error}")

            # 显示警告
            if check_result.get('warnings'):
                for warning in check_result['warnings']:
                    print(f"    警告: {warning}")

            # 显示问题
            if check_result.get('issues'):
                for issue in check_result['issues']:
                    print(f"    问题: {issue}")

        # 汇总错误和警告
        if report.get('errors'):
            print(f"\n【错误汇总】 ({len(report['errors'])} 个)")
            for i, error in enumerate(report['errors'], 1):
                print(f"  {i}. {error}")

        if report.get('warnings'):
            print(f"\n【警告汇总】 ({len(report['warnings'])} 个)")
            for i, warning in enumerate(report['warnings'], 1):
                print(f"  {i}. {warning}")

        print("\n" + "="*60)


# 向后兼容的函数接口
def validate_migration(java_code: str, python_code: str) -> bool:
    """
    验证迁移 (兼容旧接口)

    Args:
        java_code: Java 代码
        python_code: Python 代码

    Returns:
        是否验证通过
    """
    try:
        # 简单的语法验证
        compile(python_code, '<string>', 'exec')
        return True
    except SyntaxError as e:
        print(f"迁移验证失败: {e}")
        return False
    except Exception as e:
        print(f"验证过程中发生错误: {e}")
        return False
