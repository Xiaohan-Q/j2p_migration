"""
快速演示 Java to Python 迁移工具
展示传统模式和 Agent 模式
"""
import sys
from pathlib import Path

# 设置控制台编码为 UTF-8 (Windows 兼容)
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ast_parser import JavaASTParser
from semantic_mapper import SemanticMapper
from migration_planner import MigrationPlanner
from code_generater import PythonCodeGenerator
from validator import MigrationValidator
from agents import MigrationOrchestrator
from logger import get_logger
from visualizer import MigrationVisualizer


def demo_traditional_mode():
    """演示传统模式的迁移流程"""
    print("="*70)
    print("模式 1: 传统迁移模式")
    print("="*70)

    # Java 示例代码
    java_code = """
    public class Person {
        private String name;
        private int age;
        private static int count = 0;

        public Person(String name, int age) {
            this.name = name;
            this.age = age;
            count++;
        }

        public String getName() {
            return name;
        }

        public int getAge() {
            return age;
        }

        public static int getCount() {
            return count;
        }

        public void introduce() {
            System.out.println("Hello, I am " + name);
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    # 创建工具实例
    parser = JavaASTParser()
    mapper = SemanticMapper()
    planner = MigrationPlanner()
    generator = PythonCodeGenerator()
    validator = MigrationValidator()

    print("\n" + "="*70)
    print("步骤 1: 解析 Java 代码")
    print("="*70)

    java_structure = parser.get_full_structure(java_code)
    if java_structure:
        print(f"✓ 解析成功!")
        print(f"  - 包名: {java_structure['package'] or '(default)'}")
        print(f"  - 导入数: {len(java_structure['imports'])}")
        print(f"  - 类数: {len(java_structure['classes'])}")

        for cls in java_structure['classes']:
            print(f"\n  类: {cls['name']}")
            print(f"    - 字段: {len(cls['fields'])} 个")
            print(f"    - 构造函数: {len(cls['constructors'])} 个")
            print(f"    - 方法: {len(cls['methods'])} 个")

    print("\n" + "="*70)
    print("步骤 2: 生成迁移计划")
    print("="*70)

    migration_plan = planner.plan_migration(java_structure)
    planner.print_plan(migration_plan)

    print("\n" + "="*70)
    print("步骤 3: 语义映射")
    print("="*70)

    python_structure = mapper.map_structure(java_structure)
    print(f"✓ 映射完成!")
    print(f"  - Python 类数: {len(python_structure['classes'])}")

    print("\n" + "="*70)
    print("步骤 4: 生成 Python 代码")
    print("="*70)

    python_code = generator.generate_code(python_structure)
    python_code = generator.format_code(python_code)

    print("\n【生成的 Python 代码】")
    print(python_code)

    print("\n" + "="*70)
    print("步骤 5: 验证生成的代码")
    print("="*70)

    validation_report = validator.validate_migration(
        java_code,
        python_code,
        python_structure
    )

    validator.print_report(validation_report)

    # 保存生成的代码
    output_file = Path(__file__).parent / 'example' / 'Person.py'
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(python_code)

    print(f"\n✓ Python 代码已保存到: {output_file}")
    print("\n" + "="*70)
    print("传统模式演示完成!")
    print("="*70)


def demo_agent_mode():
    """演示 Agent 编排模式"""
    print("\n\n")
    print("="*70)
    print("模式 2: Agent 编排模式")
    print("="*70)

    # Java 示例代码
    java_code = """
    public class Calculator {
        private static final double PI = 3.14159;

        public int add(int a, int b) {
            return a + b;
        }

        public static double circleArea(double radius) {
            return PI * radius * radius;
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    # 创建日志器和编排器
    logger = get_logger(verbose=False, use_color=True)
    orchestrator = MigrationOrchestrator()
    orchestrator.set_logger(logger)

    # 执行迁移
    logger.section("使用 Agent 编排器执行迁移")

    results = orchestrator.orchestrate_migration(java_code, validate=True)

    if results['success']:
        logger.success("迁移成功!")

        print("\n【生成的 Python 代码】")
        print(results['python_code'])

        # 显示 Agent 状态
        print("\n【Agent 状态】")
        statuses = orchestrator.get_agent_statuses()
        for agent_name, status in statuses.items():
            print(f"  {agent_name}: {status}")

        # 保存代码
        output_file = Path(__file__).parent / 'example' / 'Calculator.py'
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(results['python_code'])

        logger.success(f"Python 代码已保存到: {output_file}")
    else:
        logger.error("迁移失败")
        for error in results['errors']:
            logger.error(f"  - {error}")

    print("\n" + "="*70)
    print("Agent 模式演示完成!")
    print("="*70)


def demo_visualizer():
    """演示迁移计划可视化"""
    print("\n\n")
    print("="*70)
    print("模式 3: 迁移计划可视化")
    print("="*70)

    java_code = """
    public class ComplexExample extends BaseClass implements Interface1, Interface2 {
        private static final String VERSION = "1.0";
        private List<String> items;
        private Map<Integer, String> data;

        public ComplexExample() {
            this.items = new ArrayList<>();
        }

        public void addItem(String item) {
            items.add(item);
        }

        public static String getVersion() {
            return VERSION;
        }
    }
    """

    # 解析和规划
    parser = JavaASTParser()
    planner = MigrationPlanner()
    visualizer = MigrationVisualizer()

    java_structure = parser.get_full_structure(java_code)
    plan = planner.plan_migration(java_structure)

    # 显示计划
    visualizer.print_plan_summary(plan)

    # 导出计划
    json_file = Path(__file__).parent / 'example' / 'migration_plan.json'
    md_file = Path(__file__).parent / 'example' / 'migration_plan.md'

    visualizer.export_plan_to_json(plan, str(json_file))
    visualizer.export_plan_to_markdown(plan, str(md_file))

    print("\n" + "="*70)
    print("可视化演示完成!")
    print("="*70)


if __name__ == "__main__":
    try:
        # 运行所有演示
        demo_traditional_mode()
        demo_agent_mode()
        demo_visualizer()

        print("\n\n")
        print("="*70)
        print("所有演示完成!")
        print("="*70)
        print("\n提示: 查看 example/ 目录下的生成文件")

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
