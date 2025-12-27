"""
Costrict 风格智能 Agent 系统完整演示
展示严格模式和快速模式的完整工作流
"""
import sys
from pathlib import Path

# 设置编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from costrict_orchestrator import StrictModeOrchestrator
from llm_providers import create_llm_provider
from logger import get_logger


def demo_strict_mode():
    """演示严格模式 - 完整的 6 个阶段"""
    print("="*100)
    print("🔒 演示 1: Costrict 严格模式 (6 个阶段完整流程)")
    print("="*100)
    print("\n参考: https://github.com/zgsm-ai/costrict")
    print("理念: 质量优先、严格流程、系统化分解\n")

    java_code = """
    public class OrderProcessor {
        private PaymentService paymentService;
        private InventoryService inventoryService;
        private NotificationService notificationService;

        public OrderResult processOrder(Order order) {
            // 验证订单
            if (order == null || order.getItems().isEmpty()) {
                throw new IllegalArgumentException("Order cannot be empty");
            }

            // 检查库存
            for (OrderItem item : order.getItems()) {
                if (!inventoryService.checkAvailability(item.getProductId(), item.getQuantity())) {
                    return OrderResult.failed("Insufficient inventory for " + item.getProductId());
                }
            }

            // 计算总金额
            double totalAmount = order.getItems().stream()
                .mapToDouble(item -> item.getPrice() * item.getQuantity())
                .sum();

            // 处理支付
            PaymentResult paymentResult = paymentService.processPayment(
                order.getUserId(),
                totalAmount
            );

            if (!paymentResult.isSuccessful()) {
                return OrderResult.failed("Payment failed: " + paymentResult.getReason());
            }

            // 扣减库存
            for (OrderItem item : order.getItems()) {
                inventoryService.deductInventory(item.getProductId(), item.getQuantity());
            }

            // 发送通知
            notificationService.sendOrderConfirmation(order.getUserId(), order.getId());

            return OrderResult.success(order.getId());
        }
    }
    """

    print("【原始 Java 代码】")
    print(java_code)

    # 创建 LLM (使用 Ollama)
    try:
        provider = create_llm_provider("ollama", model="codellama")
        print("\n✓ 使用 Ollama (codellama) - 本地 LLM")
    except:
        print("\n⚠️ Ollama 连接失败,使用 Mock 模式")
        provider = create_llm_provider("mock")

    # 创建严格模式编排器
    orchestrator = StrictModeOrchestrator(provider, enable_all_phases=True)

    # 执行严格模式迁移
    results = orchestrator.migrate_strict(java_code, skip_tests=False)

    # 显示各阶段结果
    print_phase_results(results)

    # 保存结果
    save_results(results, "strict_mode")

    return results


def demo_fast_mode():
    """演示快速模式 - 仅核心阶段"""
    print("\n\n")
    print("="*100)
    print("⚡ 演示 2: 快速模式 (3 个核心阶段)")
    print("="*100)

    java_code = """
    public class StringUtils {
        public static boolean isEmpty(String str) {
            return str == null || str.trim().isEmpty();
        }

        public static String capitalize(String str) {
            if (isEmpty(str)) {
                return str;
            }
            return str.substring(0, 1).toUpperCase() + str.substring(1);
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    try:
        provider = create_llm_provider("ollama", model="codellama")
    except:
        provider = create_llm_provider("mock")

    orchestrator = StrictModeOrchestrator(provider)

    # 执行快速模式
    results = orchestrator.migrate_fast(java_code)

    print_phase_results(results)
    save_results(results, "fast_mode")

    return results


def demo_comparison():
    """对比严格模式和快速模式"""
    print("\n\n")
    print("="*100)
    print("📊 严格模式 vs 快速模式对比")
    print("="*100)

    comparison_table = """
┌─────────────────────┬────────────────────────┬────────────────────────┐
│ 维度                │ 严格模式 (Strict)      │ 快速模式 (Fast)        │
├─────────────────────┼────────────────────────┼────────────────────────┤
│ 执行阶段            │ 6 个完整阶段           │ 3 个核心阶段           │
│ 执行时间            │ 较长 (2-5分钟)         │ 较短 (30秒-1分钟)      │
│ 代码质量            │ ⭐⭐⭐⭐⭐ 最高        │ ⭐⭐⭐⭐ 良好          │
│ 需求分析            │ ✅ 详细分析            │ ✅ 简要分析            │
│ 架构设计            │ ✅ 完整设计            │ ❌ 跳过                │
│ 任务规划            │ ✅ 详细规划            │ ❌ 跳过                │
│ 代码生成            │ ✅ 高质量生成          │ ✅ 快速生成            │
│ 测试生成            │ ✅ 完整测试套件        │ ❌ 跳过                │
│ 代码审查            │ ✅ 严格审查            │ ✅ 基础审查            │
│ 适用场景            │ 生产级代码             │ 原型开发/快速验证      │
│ 推荐使用            │ 企业项目、关键业务     │ 工具类、简单逻辑       │
└─────────────────────┴────────────────────────┴────────────────────────┘

工作流对比:

严格模式 (Strict):
  需求分析 → 架构设计 → 任务规划 → 代码生成 → 测试生成 → 代码审查
  (完整的质量保证流程)

快速模式 (Fast):
  需求分析 → 代码生成 → 代码审查
  (快速迭代,适合简单场景)
"""
    print(comparison_table)


def print_phase_results(results: Dict):
    """打印各阶段结果详情"""
    print("\n" + "="*100)
    print("📋 各阶段输出详情")
    print("="*100)

    # 1. 需求分析
    if results.get('requirements'):
        print("\n【1️⃣ 需求分析阶段】")
        req = results['requirements']
        print(f"  业务领域: {req.get('business_domain', '未知')}")
        print(f"  优先级: {req.get('priority', '未知')}")
        if req.get('core_functions'):
            print(f"  核心功能: {', '.join(req['core_functions'][:3])}")
        if req.get('migration_challenges'):
            print(f"  迁移挑战: {', '.join(req['migration_challenges'][:2])}")

    # 2. 架构设计
    if results.get('architecture'):
        print("\n【2️⃣ 架构设计阶段】")
        arch = results['architecture']
        if arch.get('class_structure'):
            cs = arch['class_structure']
            print(f"  类名: {cs.get('class_name', '未知')}")
            if cs.get('patterns'):
                print(f"  设计模式: {', '.join(cs['patterns'])}")

    # 3. 任务规划
    if results.get('plan'):
        print("\n【3️⃣ 任务规划阶段】")
        plan = results['plan']
        steps = plan.get('implementation_steps', [])
        print(f"  实现步骤: {len(steps)} 个")
        if steps:
            print(f"  第一步: {steps[0].get('description', '未知')}")

    # 4. 代码生成
    if results.get('python_code'):
        print("\n【4️⃣ 代码生成阶段】")
        code = results['python_code']
        lines = code.count('\n')
        classes = code.count('class ')
        methods = code.count('def ')
        print(f"  代码行数: {lines}")
        print(f"  类数量: {classes}")
        print(f"  方法数量: {methods}")

    # 5. 测试生成
    if results.get('test_code'):
        print("\n【5️⃣ 测试生成阶段】")
        test = results['test_code']
        test_count = test.count('def test_')
        print(f"  测试用例: {test_count} 个")

    # 6. 代码审查
    if results.get('review_report'):
        print("\n【6️⃣ 代码审查阶段】")
        review = results['review_report']
        print(f"  总分: {review.get('overall_score', 0)}/100")
        print(f"  审批状态: {review.get('approval_status', '未知')}")

        # 详细评分
        if review.get('semantic_correctness'):
            print(f"  语义正确性: {review['semantic_correctness'].get('score', 0)}/100")
        if review.get('code_quality'):
            print(f"  代码质量: {review['code_quality'].get('score', 0)}/100")


def save_results(results: Dict, mode: str):
    """保存结果到文件"""
    output_dir = Path("output") / mode
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存 Python 代码
    if results.get('python_code'):
        with open(output_dir / "generated.py", "w", encoding="utf-8") as f:
            f.write(results['python_code'])
        print(f"\n✓ Python 代码已保存: {output_dir / 'generated.py'}")

    # 保存测试代码
    if results.get('test_code'):
        with open(output_dir / "test_generated.py", "w", encoding="utf-8") as f:
            f.write(results['test_code'])
        print(f"✓ 测试代码已保存: {output_dir / 'test_generated.py'}")

    # 保存报告
    from costrict_orchestrator import StrictModeOrchestrator
    from llm_providers import create_llm_provider

    provider = create_llm_provider("mock")  # 只用于导出
    orch = StrictModeOrchestrator(provider)
    orch.export_report(results, str(output_dir / "report.json"))


def show_architecture():
    """显示系统架构"""
    print("\n\n")
    print("="*100)
    print("🏗️ Costrict 风格 Agent 系统架构")
    print("="*100)

    architecture = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                      StrictModeOrchestrator (编排器)                        │
│                                                                              │
│  工作流:                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                   │
│  │ 需求分析 Agent│──>│ 架构设计 Agent│──>│ 任务规划 Agent│                   │
│  └──────────────┘   └──────────────┘   └──────────────┘                   │
│         │                   │                   │                          │
│         └───────────────────┴───────────────────┘                          │
│                             │                                              │
│  ┌──────────────┐   ┌──────▼──────┐   ┌──────────────┐                   │
│  │ 测试生成 Agent│<──│ 代码生成 Agent│──>│代码审查 Agent │                   │
│  └──────────────┘   └─────────────┘   └──────────────┘                   │
│                                                                              │
│  共享数据: AgentContext                                                      │
│  ├─ java_code: 原始代码                                                      │
│  ├─ requirements: 需求分析结果                                               │
│  ├─ architecture: 架构设计                                                   │
│  ├─ plan: 实现计划                                                          │
│  ├─ python_code: 生成的代码                                                  │
│  ├─ test_code: 测试代码                                                      │
│  └─ review_report: 审查报告                                                  │
│                                                                              │
│  质量保证:                                                                   │
│  • 每个 Agent 都有前置条件验证                                                │
│  • 每个 Agent 都有输出验证                                                   │
│  • 严格的错误处理和回滚机制                                                  │
│  • 完整的审查和质量检查                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(architecture)


if __name__ == "__main__":
    try:
        logger = get_logger(verbose=False, use_color=True)

        print("🚀 Costrict 风格智能 Agent 系统 - 完整演示")
        print("参考项目: https://github.com/zgsm-ai/costrict")
        print("核心理念: 质量优先、严格流程、系统化分解\n")

        # 显示架构
        show_architecture()

        # 演示1: 严格模式
        strict_results = demo_strict_mode()

        # 演示2: 快速模式
        fast_results = demo_fast_mode()

        # 对比分析
        demo_comparison()

        print("\n\n")
        print("="*100)
        print("✅ 所有演示完成!")
        print("="*100)
        print("\n生成的文件:")
        print("  📁 output/strict_mode/  - 严格模式输出")
        print("  📁 output/fast_mode/    - 快速模式输出")
        print("\n每个目录包含:")
        print("  📄 generated.py        - 生成的 Python 代码")
        print("  📄 test_generated.py   - 生成的测试代码")
        print("  📄 report.json         - 详细的迁移报告")

    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
