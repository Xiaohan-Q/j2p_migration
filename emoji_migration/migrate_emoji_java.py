"""
emoji-java 项目迁移脚本
将 emoji-java 项目的 Java 代码迁移为 Python 代码
"""
import sys
from pathlib import Path

# 设置编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from costrict_orchestrator import StrictModeOrchestrator
from llm_providers import create_llm_provider
from logger import get_logger
import json


class EmojiJavaMigrator:
    """emoji-java 项目迁移器"""

    def __init__(self, use_strict_mode=True):
        self.project_root = project_root
        self.emoji_java_dir = self.project_root / 'test' / 'emoji-java'
        self.output_dir = Path(__file__).parent / 'output'
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.use_strict_mode = use_strict_mode
        self.logger = get_logger(verbose=True, use_color=True)

        # Java 源文件列表
        self.java_files = [
            'src/main/java/com/vdurmont/emoji/Emoji.java',
            'src/main/java/com/vdurmont/emoji/EmojiLoader.java',
            'src/main/java/com/vdurmont/emoji/EmojiManager.java',
            'src/main/java/com/vdurmont/emoji/EmojiParser.java',
            'src/main/java/com/vdurmont/emoji/EmojiTrie.java',
            'src/main/java/com/vdurmont/emoji/Fitzpatrick.java',
        ]

    def read_java_file(self, relative_path):
        """读取 Java 文件内容"""
        file_path = self.emoji_java_dir / relative_path
        if not file_path.exists():
            self.logger.error(f"文件不存在: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"读取文件: {relative_path}")
            return content
        except Exception as e:
            self.logger.error(f"读取文件失败 {relative_path}: {e}")
            return None

    def migrate_file(self, java_file_path, provider, orchestrator):
        """迁移单个 Java 文件"""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"开始迁移: {java_file_path}")
        self.logger.info(f"{'='*80}")

        # 读取 Java 代码
        java_code = self.read_java_file(java_file_path)
        if not java_code:
            return None

        # 执行迁移
        try:
            if self.use_strict_mode:
                results = orchestrator.migrate_strict(java_code, skip_tests=False)
            else:
                results = orchestrator.migrate_fast(java_code)

            # 保存结果
            output_name = Path(java_file_path).stem
            self.save_migration_results(results, output_name)

            return results
        except Exception as e:
            self.logger.error(f"迁移失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_migration_results(self, results, output_name):
        """保存迁移结果"""
        output_file_dir = self.output_dir / output_name
        output_file_dir.mkdir(exist_ok=True, parents=True)

        # 保存 Python 代码
        if results.get('python_code'):
            python_file = output_file_dir / f"{output_name}.py"
            with open(python_file, 'w', encoding='utf-8') as f:
                f.write(results['python_code'])
            self.logger.success(f"Python 代码已保存: {python_file}")

        # 保存测试代码
        if results.get('test_code'):
            test_file = output_file_dir / f"test_{output_name}.py"
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(results['test_code'])
            self.logger.success(f"测试代码已保存: {test_file}")

        # 保存详细报告
        report_file = output_file_dir / "migration_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        self.logger.success(f"迁移报告已保存: {report_file}")

    def migrate_all(self):
        """迁移所有文件"""
        self.logger.info("="*80)
        self.logger.info("emoji-java 项目迁移工具")
        self.logger.info("="*80)
        self.logger.info(f"源项目目录: {self.emoji_java_dir}")
        self.logger.info(f"输出目录: {self.output_dir}")
        self.logger.info(f"模式: {'严格模式' if self.use_strict_mode else '快速模式'}")
        self.logger.info(f"待迁移文件数: {len(self.java_files)}")
        self.logger.info("")

        # 创建 LLM Provider
        try:
            self.logger.info("尝试连接 Ollama...")
            provider = create_llm_provider("ollama", model="codellama")
            self.logger.success("使用 Ollama (codellama)")
        except Exception as e:
            self.logger.warning(f"Ollama 连接失败: {e}")
            self.logger.info("使用 Mock 模式")
            provider = create_llm_provider("mock")

        # 创建编排器
        orchestrator = StrictModeOrchestrator(
            provider,
            enable_all_phases=self.use_strict_mode
        )

        # 迁移统计
        total = len(self.java_files)
        success = 0
        failed = 0
        results_list = []

        # 逐个迁移文件
        for i, java_file in enumerate(self.java_files, 1):
            self.logger.info(f"\n进度: [{i}/{total}]")

            result = self.migrate_file(java_file, provider, orchestrator)
            if result:
                success += 1
                results_list.append({
                    'file': java_file,
                    'status': 'success',
                    'result': result
                })
            else:
                failed += 1
                results_list.append({
                    'file': java_file,
                    'status': 'failed'
                })

        # 打印总结
        self.print_summary(total, success, failed, results_list)

        # 生成项目级报告
        self.generate_project_report(results_list)

    def print_summary(self, total, success, failed, results_list):
        """打印迁移总结"""
        self.logger.info("\n\n")
        self.logger.info("="*80)
        self.logger.info("迁移完成总结")
        self.logger.info("="*80)
        self.logger.info(f"总文件数: {total}")
        self.logger.success(f"成功: {success}")
        if failed > 0:
            self.logger.error(f"失败: {failed}")

        self.logger.info("\n文件列表:")
        for item in results_list:
            status_icon = "✓" if item['status'] == 'success' else "✗"
            self.logger.info(f"  {status_icon} {item['file']}")

        self.logger.info(f"\n输出目录: {self.output_dir}")

    def generate_project_report(self, results_list):
        """生成项目级别的迁移报告"""
        report = {
            'project': 'emoji-java',
            'total_files': len(results_list),
            'successful': sum(1 for r in results_list if r['status'] == 'success'),
            'failed': sum(1 for r in results_list if r['status'] == 'failed'),
            'mode': 'strict' if self.use_strict_mode else 'fast',
            'files': [
                {
                    'file': r['file'],
                    'status': r['status']
                }
                for r in results_list
            ]
        }

        report_file = self.output_dir / 'project_migration_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.logger.success(f"项目报告已生成: {report_file}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='emoji-java 项目迁移工具')
    parser.add_argument(
        '--mode',
        choices=['strict', 'fast'],
        default='strict',
        help='迁移模式: strict(严格模式) 或 fast(快速模式)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='仅迁移指定的文件 (相对路径)'
    )

    args = parser.parse_args()

    # 创建迁移器
    migrator = EmojiJavaMigrator(use_strict_mode=(args.mode == 'strict'))

    # 如果指定了单个文件
    if args.file:
        # 创建 provider 和 orchestrator
        try:
            provider = create_llm_provider("ollama", model="codellama")
        except:
            provider = create_llm_provider("mock")

        orchestrator = StrictModeOrchestrator(
            provider,
            enable_all_phases=migrator.use_strict_mode
        )

        migrator.migrate_file(args.file, provider, orchestrator)
    else:
        # 迁移所有文件
        migrator.migrate_all()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
