"""
emoji-java 迁移结果验证工具
验证生成的 Python 代码的正确性和质量
"""
import sys
from pathlib import Path
import json
import ast
import subprocess

# 设置编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from logger import get_logger


class MigrationValidator:
    """迁移结果验证器"""

    def __init__(self):
        self.logger = get_logger(verbose=True, use_color=True)
        self.output_dir = Path(__file__).parent / 'output'
        self.validation_results = {
            'files': [],
            'summary': {
                'total': 0,
                'syntax_valid': 0,
                'syntax_invalid': 0,
                'has_tests': 0,
                'tests_passed': 0,
                'tests_failed': 0
            }
        }

    def validate_all(self):
        """验证所有迁移结果"""
        self.logger.info("="*80)
        self.logger.info("emoji-java 迁移结果验证")
        self.logger.info("="*80)

        # 读取项目报告
        project_report_file = self.output_dir / 'project_migration_report.json'
        if not project_report_file.exists():
            self.logger.error("未找到项目迁移报告")
            return

        with open(project_report_file, 'r', encoding='utf-8') as f:
            project_report = json.load(f)

        self.logger.info(f"\n项目: {project_report['project']}")
        self.logger.info(f"模式: {project_report['mode']}")
        self.logger.info(f"总文件数: {project_report['total_files']}")
        self.logger.success(f"成功: {project_report['successful']}")
        if project_report['failed'] > 0:
            self.logger.error(f"失败: {project_report['failed']}")

        # 获取所有输出目录
        output_dirs = [d for d in self.output_dir.iterdir()
                      if d.is_dir() and d.name != 'quick_start']

        self.logger.info(f"\n找到 {len(output_dirs)} 个迁移结果目录")
        self.logger.info("")

        # 验证每个文件
        for i, output_dir in enumerate(sorted(output_dirs), 1):
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"[{i}/{len(output_dirs)}] 验证: {output_dir.name}")
            self.logger.info(f"{'='*80}")

            result = self.validate_single(output_dir)
            self.validation_results['files'].append(result)

        # 打印总结
        self.print_summary()

        # 保存验证报告
        self.save_report()

    def validate_single(self, output_dir: Path) -> dict:
        """验证单个迁移结果"""
        result = {
            'name': output_dir.name,
            'python_file': None,
            'test_file': None,
            'syntax_valid': False,
            'syntax_errors': [],
            'test_exists': False,
            'test_valid': False,
            'test_results': None,
            'quality_score': 0,
            'metrics': {}
        }

        # 1. 查找 Python 文件
        python_file = output_dir / f"{output_dir.name}.py"
        if not python_file.exists():
            self.logger.error(f"  ✗ Python 文件不存在: {python_file.name}")
            return result

        result['python_file'] = str(python_file)
        self.logger.info(f"  ✓ 找到 Python 文件: {python_file.name}")

        # 2. 验证语法
        syntax_valid, syntax_errors = self.validate_syntax(python_file)
        result['syntax_valid'] = syntax_valid
        result['syntax_errors'] = syntax_errors

        if syntax_valid:
            self.logger.success(f"  ✓ 语法验证通过")
            self.validation_results['summary']['syntax_valid'] += 1
        else:
            self.logger.error(f"  ✗ 语法验证失败:")
            for error in syntax_errors:
                self.logger.error(f"    - {error}")
            self.validation_results['summary']['syntax_invalid'] += 1

        # 3. 分析代码质量
        metrics = self.analyze_code_quality(python_file)
        result['metrics'] = metrics
        self.print_metrics(metrics)

        # 4. 查找测试文件
        test_file = output_dir / f"test_{output_dir.name}.py"
        if test_file.exists():
            result['test_file'] = str(test_file)
            result['test_exists'] = True
            self.logger.info(f"  ✓ 找到测试文件: {test_file.name}")
            self.validation_results['summary']['has_tests'] += 1

            # 验证测试语法
            test_syntax_valid, test_errors = self.validate_syntax(test_file)
            result['test_valid'] = test_syntax_valid

            if test_syntax_valid:
                self.logger.success(f"  ✓ 测试文件语法验证通过")

                # 尝试运行测试（可选）
                # test_results = self.run_tests(test_file)
                # result['test_results'] = test_results
            else:
                self.logger.error(f"  ✗ 测试文件语法验证失败")

        else:
            self.logger.warning(f"  ! 未找到测试文件")

        # 5. 读取迁移报告
        report_file = output_dir / 'migration_report.json'
        if report_file.exists():
            with open(report_file, 'r', encoding='utf-8') as f:
                migration_report = json.load(f)

            if migration_report.get('review_report'):
                review = migration_report['review_report']
                score = review.get('overall_score', 0)
                result['quality_score'] = score
                self.logger.info(f"  质量评分: {score}/100")

        self.validation_results['summary']['total'] += 1
        return result

    def validate_syntax(self, file_path: Path) -> tuple:
        """验证 Python 文件语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # 使用 ast.parse 验证语法
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            return False, [f"第 {e.lineno} 行: {e.msg}"]
        except Exception as e:
            return False, [str(e)]

    def analyze_code_quality(self, file_path: Path) -> dict:
        """分析代码质量指标"""
        metrics = {
            'lines': 0,
            'classes': 0,
            'functions': 0,
            'methods': 0,
            'docstrings': 0,
            'type_hints': 0,
            'comments': 0
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # 基本统计
            lines = code.split('\n')
            metrics['lines'] = len(lines)

            # 使用 AST 分析
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    metrics['classes'] += 1
                    if ast.get_docstring(node):
                        metrics['docstrings'] += 1
                elif isinstance(node, ast.FunctionDef):
                    if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
                        metrics['methods'] += 1
                    else:
                        metrics['functions'] += 1

                    if ast.get_docstring(node):
                        metrics['docstrings'] += 1

                    # 检查类型注解
                    if node.returns or any(arg.annotation for arg in node.args.args):
                        metrics['type_hints'] += 1

            # 统计注释
            metrics['comments'] = sum(1 for line in lines if line.strip().startswith('#'))

        except Exception as e:
            self.logger.warning(f"  代码分析失败: {e}")

        return metrics

    def print_metrics(self, metrics: dict):
        """打印代码指标"""
        self.logger.info(f"  代码指标:")
        self.logger.info(f"    - 总行数: {metrics['lines']}")
        self.logger.info(f"    - 类: {metrics['classes']}")
        self.logger.info(f"    - 函数/方法: {metrics['functions'] + metrics['methods']}")
        self.logger.info(f"    - 文档字符串: {metrics['docstrings']}")
        self.logger.info(f"    - 类型注解: {metrics['type_hints']}")
        self.logger.info(f"    - 注释行: {metrics['comments']}")

    def run_tests(self, test_file: Path) -> dict:
        """运行测试用例（使用 pytest）"""
        try:
            result = subprocess.run(
                ['python', '-m', 'pytest', str(test_file), '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                'exit_code': result.returncode,
                'passed': result.returncode == 0,
                'output': result.stdout,
                'errors': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'exit_code': -1,
                'passed': False,
                'output': '',
                'errors': 'Timeout'
            }
        except Exception as e:
            return {
                'exit_code': -1,
                'passed': False,
                'output': '',
                'errors': str(e)
            }

    def print_summary(self):
        """打印验证总结"""
        summary = self.validation_results['summary']

        self.logger.info("\n\n")
        self.logger.info("="*80)
        self.logger.info("验证总结")
        self.logger.info("="*80)

        self.logger.info(f"\n总文件数: {summary['total']}")

        self.logger.info(f"\n【语法验证】")
        self.logger.success(f"  通过: {summary['syntax_valid']}")
        if summary['syntax_invalid'] > 0:
            self.logger.error(f"  失败: {summary['syntax_invalid']}")

        self.logger.info(f"\n【测试文件】")
        self.logger.info(f"  包含测试: {summary['has_tests']}/{summary['total']}")

        # 计算成功率
        if summary['total'] > 0:
            success_rate = (summary['syntax_valid'] / summary['total']) * 100
            self.logger.info(f"\n语法验证成功率: {success_rate:.1f}%")

        # 详细文件列表
        self.logger.info(f"\n【详细结果】")
        for file_result in self.validation_results['files']:
            status = "✓" if file_result['syntax_valid'] else "✗"
            score = file_result.get('quality_score', 0)
            self.logger.info(f"  {status} {file_result['name']:<20} (质量分: {score}/100)")

    def save_report(self):
        """保存验证报告"""
        report_file = self.output_dir / 'validation_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)

        self.logger.success(f"\n验证报告已保存: {report_file}")


def main():
    """主函数"""
    validator = MigrationValidator()
    validator.validate_all()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
