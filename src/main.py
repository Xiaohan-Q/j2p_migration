"""
Java to Python 迁移工具主程序
整合所有模块,提供完整的迁移流程
"""
import argparse
import sys
from pathlib import Path

from ast_parser import JavaASTParser
from semantic_mapper import SemanticMapper
from migration_planner import MigrationPlanner
from code_generater import PythonCodeGenerator
from validator import MigrationValidator
from logger import get_logger, set_verbose


class JavaToPythonMigrator:
    """Java to Python 迁移器"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = get_logger(verbose=verbose)
        self.parser = JavaASTParser()
        self.mapper = SemanticMapper()
        self.planner = MigrationPlanner()
        self.generator = PythonCodeGenerator()
        self.validator = MigrationValidator()

    def log(self, message: str, level: str = "INFO"):
        """日志输出 (保留向后兼容)"""
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "SUCCESS":
            self.logger.success(message)
        else:
            self.logger.info(message)

    def migrate(self, java_code: str, show_plan: bool = False,
                validate: bool = True) -> dict:
        """
        执行完整的迁移流程

        Args:
            java_code: Java 源代码
            show_plan: 是否显示迁移计划
            validate: 是否验证生成的代码

        Returns:
            包含所有结果的字典
        """
        results = {
            'success': False,
            'java_structure': None,
            'python_structure': None,
            'python_code': None,
            'migration_plan': None,
            'validation_report': None,
            'errors': []
        }

        try:
            # 步骤 1: 解析 Java 代码
            self.logger.section("步骤 1/5: 解析 Java 代码")
            java_structure = self.parser.get_full_structure(java_code)

            if not java_structure:
                results['errors'].append("Java 代码解析失败")
                self.logger.error("Java 代码解析失败")
                return results

            results['java_structure'] = java_structure
            self.logger.success(f"解析成功: 找到 {len(java_structure.get('classes', []))} 个类")

            # 步骤 2: 生成迁移计划
            self.logger.section("步骤 2/5: 生成迁移计划")
            migration_plan = self.planner.plan_migration(java_structure)
            results['migration_plan'] = migration_plan

            if show_plan:
                self.planner.print_plan(migration_plan)

            # 步骤 3: 语义映射
            self.logger.section("步骤 3/5: 执行语义映射")
            python_structure = self.mapper.map_structure(java_structure)
            results['python_structure'] = python_structure
            self.logger.success(f"映射完成: {len(python_structure.get('classes', []))} 个类")

            # 步骤 4: 生成 Python 代码
            self.logger.section("步骤 4/5: 生成 Python 代码")
            python_code = self.generator.generate_code(python_structure)
            python_code = self.generator.format_code(python_code)
            results['python_code'] = python_code
            self.logger.success("代码生成完成")

            # 步骤 5: 验证 (可选)
            if validate:
                self.logger.section("步骤 5/5: 验证生成的代码")
                validation_report = self.validator.validate_migration(
                    java_code,
                    python_code,
                    python_structure
                )
                results['validation_report'] = validation_report

                if validation_report['overall_status'] == 'failed':
                    results['errors'].append("代码验证失败")
                    self.logger.error("验证失败")
                else:
                    self.logger.success(f"验证完成: {validation_report['overall_status']}")

            results['success'] = len(results['errors']) == 0

        except Exception as e:
            results['errors'].append(f"迁移过程中发生错误: {str(e)}")
            self.logger.exception("迁移过程中发生错误", exc=e)

        return results

    def migrate_file(self, input_file: str, output_file: str = None,
                    show_plan: bool = False, validate: bool = True) -> bool:
        """
        从文件读取 Java 代码并迁移

        Args:
            input_file: 输入 Java 文件路径
            output_file: 输出 Python 文件路径 (可选)
            show_plan: 是否显示迁移计划
            validate: 是否验证

        Returns:
            是否成功
        """
        try:
            # 读取 Java 代码
            with open(input_file, 'r', encoding='utf-8') as f:
                java_code = f.read()

            self.logger.info(f"从文件读取 Java 代码: {input_file}")

            # 执行迁移
            results = self.migrate(java_code, show_plan, validate)

            if not results['success']:
                self.logger.error("迁移失败")
                for error in results['errors']:
                    self.logger.error(f"  - {error}")
                return False

            # 保存 Python 代码
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(results['python_code'])
                self.logger.success(f"Python 代码已保存到: {output_file}")
            else:
                # 如果没有指定输出文件,打印到控制台
                print("\n" + "="*60)
                print("生成的 Python 代码:")
                print("="*60)
                print(results['python_code'])

            # 显示验证报告
            if validate and results['validation_report']:
                self.validator.print_report(results['validation_report'])

            return True

        except FileNotFoundError:
            self.logger.error(f"文件未找到: {input_file}")
            return False
        except Exception as e:
            self.logger.exception(f"文件迁移失败", exc=e)
            return False


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Java to Python 代码迁移工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 迁移单个文件
  python main.py -i Example.java -o example.py

  # 显示迁移计划
  python main.py -i Example.java --show-plan

  # 迁移并跳过验证
  python main.py -i Example.java -o example.py --no-validate

  # 详细输出模式
  python main.py -i Example.java -o example.py -v
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入 Java 文件路径'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出 Python 文件路径 (可选,默认输出到控制台)'
    )

    parser.add_argument(
        '--show-plan',
        action='store_true',
        help='显示详细的迁移计划'
    )

    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='跳过代码验证步骤'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出模式'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )

    parser.add_argument(
        '--use-agents',
        action='store_true',
        help='使用 Agent 编排模式执行迁移'
    )

    parser.add_argument(
        '--export-plan',
        metavar='FILE',
        help='导出迁移计划到文件 (支持 .json 和 .md 格式)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Java to Python Migration Tool v1.0.0'
    )

    args = parser.parse_args()

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    # 验证输出文件
    if args.output:
        output_path = Path(args.output)
        if output_path.exists():
            try:
                response = input(f"输出文件已存在: {args.output}\n是否覆盖? (y/N): ")
                if response.lower() != 'y':
                    print("取消操作")
                    sys.exit(0)
            except KeyboardInterrupt:
                print("\n取消操作")
                sys.exit(0)

    # 设置日志
    set_verbose(args.verbose)

    # 使用 Agent 模式或传统模式
    if args.use_agents:
        # Agent 编排模式
        from agents import MigrationOrchestrator
        from logger import get_logger

        logger = get_logger(verbose=args.verbose, use_color=not args.no_color)
        orchestrator = MigrationOrchestrator()
        orchestrator.set_logger(logger)

        # 读取 Java 代码
        with open(args.input, 'r', encoding='utf-8') as f:
            java_code = f.read()

        # 执行迁移
        results = orchestrator.orchestrate_migration(
            java_code,
            validate=not args.no_validate
        )

        if not results['success']:
            logger.error("迁移失败")
            for error in results['errors']:
                logger.error(f"  - {error}")
            sys.exit(1)

        # 保存结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(results['python_code'])
            logger.success(f"Python 代码已保存到: {args.output}")
        else:
            print("\n" + "="*60)
            print("生成的 Python 代码:")
            print("="*60)
            print(results['python_code'])

        sys.exit(0)

    # 传统模式
    migrator = JavaToPythonMigrator(verbose=args.verbose)

    # 导出迁移计划
    if args.export_plan:
        from visualizer import MigrationVisualizer
        visualizer = MigrationVisualizer()

        # 读取并解析 Java 代码
        with open(args.input, 'r', encoding='utf-8') as f:
            java_code = f.read()

        java_structure = migrator.parser.get_full_structure(java_code)
        if java_structure:
            plan = migrator.planner.plan_migration(java_structure)

            export_file = Path(args.export_plan)
            if export_file.suffix == '.json':
                visualizer.export_plan_to_json(plan, str(export_file))
            elif export_file.suffix == '.md':
                visualizer.export_plan_to_markdown(plan, str(export_file))
            else:
                print(f"不支持的导出格式: {export_file.suffix}")
                print("支持的格式: .json, .md")
                sys.exit(1)

    # 执行迁移
    success = migrator.migrate_file(
        input_file=args.input,
        output_file=args.output,
        show_plan=args.show_plan,
        validate=not args.no_validate
    )

    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
