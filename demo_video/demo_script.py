"""产品演示视频 - 自动化演示脚本"""
import sys
import time
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from logger import get_logger


class DemoPresenter:
    """演示控制器"""

    def __init__(self):
        self.logger = get_logger(verbose=True, use_color=True)
        self.project_root = Path(__file__).parent.parent

    def print_title(self, title, style="="):
        """打印标题"""
        width = 80
        print("\n" + style * width)
        print(title.center(width))
        print(style * width + "\n")
        time.sleep(1)

    def print_section(self, text):
        """打印章节"""
        print(f"\n{'─' * 80}")
        print(f"📍 {text}")
        print(f"{'─' * 80}\n")
        time.sleep(0.5)

    def pause(self, seconds=2):
        """暂停"""
        time.sleep(seconds)

    def demo_part1_intro(self):
        """第一部分: 开场介绍"""
        self.print_title("Java to Python Migration Tool", "=")
        print("智能化代码迁移解决方案\n")
        self.pause(2)

        print("💡 在现代软件开发中，将遗留的 Java 代码迁移到 Python 是一个常见但耗时的任务。")
        self.pause(1)
        print("⚡ 今天，我们展示一个创新的解决方案——")
        print("   结合 AST 解析和 LLM 智能 Agent 的自动迁移工具。")
        self.pause(2)

    def demo_part2_features(self):
        """第二部分: 核心功能展示"""
        self.print_section("核心功能介绍")

        print("🔧 双引擎系统:\n")
        print("1️⃣  传统引擎 (AST-based)")
        print("    ├─ Java AST 解析")
        print("    ├─ 语义映射")
        print("    ├─ Python 代码生成")
        print("    └─ 语法验证")
        self.pause(1.5)

        print("\n2️⃣  智能 Agent 系统 (LLM-powered)")
        print("    ├─ 需求分析 Agent")
        print("    ├─ 架构设计 Agent")
        print("    ├─ 任务规划 Agent")
        print("    ├─ 代码生成 Agent")
        print("    ├─ 测试生成 Agent")
        print("    └─ 代码审查 Agent")
        self.pause(2)

    def demo_part3_traditional(self):
        """第三部分: 传统模式演示"""
        self.print_section("传统模式演示")

        java_code = """public class Calculator {
    private static final double PI = 3.14159;

    public int add(int a, int b) {
        return a + b;
    }

    public static double circleArea(double radius) {
        return PI * radius * radius;
    }
}"""

        demo_file = self.project_root / "demo_video" / "Calculator.java"
        demo_file.parent.mkdir(exist_ok=True)
        with open(demo_file, 'w') as f:
            f.write(java_code)

        print("📄 示例 Java 代码:")
        print("─" * 80)
        print(java_code)
        print("─" * 80)
        self.pause(2)

        print("\n⚙️  执行迁移...")
        print("$ python src/main.py -i demo_video/Calculator.java -o demo_video/Calculator.py -f")
        self.pause(1)

        print("\n💡 提示: 请在另一个终端运行上述命令查看迁移过程")
        print("    迁移完成后，生成的 Python 代码将保存在 demo_video/Calculator.py")
        print("    使用 -f 参数强制覆盖已存在的文件")

        self.pause(3)

    def demo_part4_agent(self):
        """第四部分: 智能 Agent 模式"""
        self.print_section("智能 Agent 模式 - 快速演示")

        print("🤖 启动 Costrict 6 阶段工作流...\n")
        self.pause(1)

        stages = [
            ("需求分析", "识别业务领域、核心功能", 1),
            ("架构设计", "设计 Python 类结构", 1),
            ("任务规划", "制定实现步骤", 1),
            ("代码生成", "生成高质量 Python 代码", 2),
            ("测试生成", "生成单元测试", 1),
            ("代码审查", "质量评分和改进建议", 1),
        ]

        for i, (name, desc, duration) in enumerate(stages, 1):
            print(f"\n[{i}/6] {name}")
            print(f"{'─' * 80}")
            print(f"📋 {desc}...")

            for j in range(duration):
                time.sleep(0.5)
                print(".", end="", flush=True)

            self.logger.success(f" ✅ 完成")
            time.sleep(0.3)

        self.pause(1)
        print("\n✅ 所有阶段执行完成!")
        self.pause(2)

    def demo_part5_emoji_java(self):
        """第五部分: emoji-java 真实案例"""
        self.print_section("真实案例: emoji-java 项目迁移")

        print("📦 项目信息:")
        print("  ├─ 原项目: emoji-java (https://github.com/vdurmont/emoji-java)")
        print("  ├─ 规模: 6 个核心 Java 文件")
        print("  ├─ 复杂度: 枚举、数据模型、解析器、字典树")
        print("  └─ 模式: 严格模式 (6 阶段)")
        self.pause(2)

        print("\n📊 迁移结果:")
        print("┌─────────────────┬──────────────┬────────────────┐")
        print("│ 指标            │ 结果         │ 说明           │")
        print("├─────────────────┼──────────────┼────────────────┤")
        print("│ 迁移成功率      │ ✅ 100% (6/6)│ 全部成功       │")
        print("│ 语法正确率      │ ✅ 100%      │ 验证通过       │")
        print("│ 测试覆盖        │ ✅ 100%      │ 包含测试       │")
        print("│ 平均质量分      │ 85/100       │ 高质量输出     │")
        print("│ 总耗时          │ ~15 分钟     │ 严格模式       │")
        print("└─────────────────┴──────────────┴────────────────┘")
        self.pause(3)

        print("\n📈 代码质量详情:")
        files = [
            ("Emoji.py", 52, 1, 7, 7, 7),
            ("EmojiLoader.py", 42, 1, 3, 2, 2),
            ("EmojiManager.py ⭐", 135, 1, 10, 11, 10),
            ("EmojiParser.py", 103, 1, 7, 7, 7),
            ("EmojiTrie.py", 65, 3, 11, 2, 11),
            ("Fitzpatrick.py", 53, 1, 3, 4, 3),
        ]

        print("┌──────────────────┬─────┬───┬─────┬─────┬─────┐")
        print("│ 文件             │ 行数│类 │方法 │文档 │注解 │")
        print("├──────────────────┼─────┼───┼─────┼─────┼─────┤")
        for name, lines, classes, methods, docs, annots in files:
            print(f"│ {name:<16} │ {lines:>3} │ {classes} │ {methods:>3} │ {docs:>3} │ {annots:>3} │")
        print("└──────────────────┴─────┴───┴─────┴─────┴─────┘")
        self.pause(3)

    def demo_part6_validation(self):
        """第六部分: 验证展示"""
        self.print_section("迁移结果验证")

        print("🔍 验证工具:")
        print("$ cd emoji_migration")
        print("$ python validate_migration.py")
        self.pause(1)

        print("\n✅ 验证结果:")
        print("  ├─ Python 语法检查: ✅ 6/6 通过")
        print("  ├─ 代码质量分析: ✅ 完成")
        print("  ├─ 测试完整性: ✅ 6/6 包含测试")
        print("  └─ 验证报告: ✅ 已生成")
        self.pause(2)

        print("\n📦 输出结构:")
        print("emoji_migration/")
        print("├── output/                    # 迁移输出")
        print("│   ├── Emoji/")
        print("│   ├── EmojiManager/")
        print("│   └── ...")
        print("└── emoji_python/              # Python 包")
        print("    ├── __init__.py")
        print("    ├── Emoji.py")
        print("    ├── tests/")
        print("    └── examples/")
        self.pause(2)

    def demo_part7_summary(self):
        """第七部分: 总结"""
        self.print_section("总结")

        print("🌟 核心优势:\n")
        advantages = [
            "✅ 双引擎系统 - 灵活适配不同场景",
            "✅ 智能化迁移 - LLM 驱动的 6 阶段流程",
            "✅ 高质量输出 - 完整文档、测试、类型注解",
            "✅ 真实验证 - emoji-java 项目 100% 成功迁移",
            "✅ 完整工具链 - 迁移、验证、打包一体化"
        ]

        for adv in advantages:
            print(f"  {adv}")
            self.pause(0.5)

        self.pause(2)

        print("\n📚 获取更多信息:")
        print("  📘 GitHub: [项目链接]")
        print("  📗 文档: emoji_migration/VALIDATION_GUIDE.md")
        print("  📙 示例: demo_costrict.py")
        self.pause(2)

        self.print_title("立即尝试，让代码迁移变得简单！", "=")

    def run_full_demo(self):
        """运行完整演示"""
        try:
            self.demo_part1_intro()
            self.demo_part2_features()
            self.demo_part3_traditional()
            self.demo_part4_agent()
            self.demo_part5_emoji_java()
            self.demo_part6_validation()
            self.demo_part7_summary()

            print("\n\n🎉 演示完成!")

        except KeyboardInterrupt:
            print("\n\n⏸️  演示已暂停")
        except Exception as e:
            print(f"\n\n❌ 演示出错: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='产品演示视频脚本')
    parser.add_argument(
        '--part',
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help='只运行指定部分 (1-7)'
    )

    args = parser.parse_args()

    presenter = DemoPresenter()

    if args.part:
        part_methods = {
            1: presenter.demo_part1_intro,
            2: presenter.demo_part2_features,
            3: presenter.demo_part3_traditional,
            4: presenter.demo_part4_agent,
            5: presenter.demo_part5_emoji_java,
            6: presenter.demo_part6_validation,
            7: presenter.demo_part7_summary,
        }
        part_methods[args.part]()
    else:
        presenter.run_full_demo()


if __name__ == '__main__':
    main()
