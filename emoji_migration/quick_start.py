"""
快速开始示例 - 迁移单个文件
演示如何使用迁移工具
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


def quick_start_demo():
    """快速开始演示"""
    logger = get_logger(verbose=True, use_color=True)

    logger.info("="*80)
    logger.info("emoji-java 迁移工具 - 快速开始示例")
    logger.info("="*80)

    # 读取 Fitzpatrick.java (最简单的枚举类)
    emoji_java_dir = project_root / 'test' / 'emoji-java'
    fitzpatrick_file = emoji_java_dir / 'src' / 'main' / 'java' / 'com' / 'vdurmont' / 'emoji' / 'Fitzpatrick.java'

    logger.info(f"\n示例文件: Fitzpatrick.java")
    logger.info("这是一个简单的枚举类，定义了 Fitzpatrick 肤色修饰符")

    if not fitzpatrick_file.exists():
        logger.error(f"文件不存在: {fitzpatrick_file}")
        return

    # 读取文件
    with open(fitzpatrick_file, 'r', encoding='utf-8') as f:
        java_code = f.read()

    logger.info(f"\n读取成功，代码长度: {len(java_code)} 字符")
    logger.info("\n原始 Java 代码预览:")
    logger.info("-" * 80)
    print(java_code[:500] + "..." if len(java_code) > 500 else java_code)
    logger.info("-" * 80)

    # 创建 LLM Provider
    logger.info("\n创建 LLM Provider...")
    try:
        provider = create_llm_provider("ollama", model="codellama")
        logger.success("使用 Ollama (codellama)")
    except Exception as e:
        logger.warning(f"Ollama 不可用: {e}")
        logger.info("使用 Mock 模式（将生成示例代码）")
        provider = create_llm_provider("mock")

    # 创建编排器 - 使用快速模式演示
    logger.info("\n创建编排器 (快速模式)...")
    orchestrator = StrictModeOrchestrator(provider, enable_all_phases=False)

    # 执行迁移
    logger.info("\n开始迁移...")
    logger.info("="*80)

    try:
        results = orchestrator.migrate_fast(java_code)

        # 保存结果
        output_dir = Path(__file__).parent / 'output' / 'quick_start'
        output_dir.mkdir(exist_ok=True, parents=True)

        # 保存 Python 代码
        if results.get('python_code'):
            python_file = output_dir / 'Fitzpatrick.py'
            with open(python_file, 'w', encoding='utf-8') as f:
                f.write(results['python_code'])

            logger.success(f"\n✓ Python 代码已保存: {python_file}")

            # 显示生成的代码
            logger.info("\n生成的 Python 代码:")
            logger.info("="*80)
            print(results['python_code'])
            logger.info("="*80)

        # 保存报告
        report_file = output_dir / 'migration_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        logger.success(f"✓ 迁移报告已保存: {report_file}")

        # 显示摘要
        logger.info("\n迁移摘要:")
        logger.info("-" * 80)
        if results.get('requirements'):
            logger.info(f"需求分析: ✓")
        if results.get('python_code'):
            logger.info(f"代码生成: ✓")
        if results.get('review_report'):
            review = results['review_report']
            score = review.get('overall_score', 0)
            logger.info(f"代码审查: ✓ (评分: {score}/100)")

        logger.info("\n下一步:")
        logger.info("1. 查看生成的 Python 代码: {}/Fitzpatrick.py".format(output_dir))
        logger.info("2. 查看迁移报告: {}/migration_report.json".format(output_dir))
        logger.info("3. 运行完整迁移: python migrate_emoji_java.py --mode fast")

    except Exception as e:
        logger.error(f"\n迁移失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        quick_start_demo()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
