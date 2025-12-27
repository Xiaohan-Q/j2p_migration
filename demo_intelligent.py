"""
智能迁移演示
展示规则映射、语义理解和混合模式的对比
"""
import sys
from pathlib import Path

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from intelligent_migrator import IntelligentMigrator, MigrationMode
from llm_providers import create_llm_provider
from logger import get_logger


def demo_simple_pojo():
    """演示 1: 简单 POJO - 使用规则映射"""
    print("="*80)
    print("演示 1: 简单 POJO 类迁移 (自动选择规则映射模式)")
    print("="*80)

    java_code = """
    public class Product {
        private String name;
        private double price;
        private int quantity;

        public Product(String name, double price, int quantity) {
            this.name = name;
            this.price = price;
            this.quantity = quantity;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public double getPrice() {
            return price;
        }

        public double getTotalValue() {
            return price * quantity;
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    # 使用混合模式(会自动选择规则映射)
    migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("mock"),
        mode=MigrationMode.HYBRID
    )

    results = migrator.migrate(java_code, validate=True)
    migrator.print_results(results)

    print("\n" + "="*80)
    print(f"✓ 模式选择: {results['mode_used']} (快速、免费)")
    print("="*80)


def demo_complex_service():
    """演示 2: 复杂业务服务 - 使用语义理解"""
    print("\n\n")
    print("="*80)
    print("演示 2: 复杂业务服务迁移 (自动选择语义理解模式)")
    print("="*80)

    java_code = """
    public class OrderService {
        private OrderRepository orderRepository;
        private PaymentService paymentService;
        private NotificationService notificationService;
        private Logger logger;

        public Order createOrder(User user, List<OrderItem> items) {
            logger.info("Creating order for user: " + user.getEmail());

            // 验证订单
            if (items == null || items.isEmpty()) {
                throw new IllegalArgumentException("Order items cannot be empty");
            }

            double totalAmount = calculateTotal(items);
            if (totalAmount <= 0) {
                throw new IllegalArgumentException("Invalid order amount");
            }

            // 创建订单
            Order order = new Order();
            order.setUser(user);
            order.setItems(items);
            order.setTotalAmount(totalAmount);
            order.setStatus(OrderStatus.PENDING);
            order.setCreatedAt(new Date());

            // 保存订单
            order = orderRepository.save(order);

            // 处理支付
            try {
                Payment payment = paymentService.processPayment(order);
                if (payment.isSuccessful()) {
                    order.setStatus(OrderStatus.CONFIRMED);
                    orderRepository.save(order);

                    // 发送通知
                    notificationService.sendOrderConfirmation(user, order);
                } else {
                    order.setStatus(OrderStatus.FAILED);
                    orderRepository.save(order);
                }
            } catch (PaymentException e) {
                logger.error("Payment failed for order: " + order.getId(), e);
                order.setStatus(OrderStatus.FAILED);
                orderRepository.save(order);
                throw e;
            }

            return order;
        }

        private double calculateTotal(List<OrderItem> items) {
            double total = 0;
            for (OrderItem item : items) {
                total += item.getPrice() * item.getQuantity();
            }
            return total;
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    # 使用混合模式(会自动选择语义理解)
    migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("mock"),
        mode=MigrationMode.HYBRID
    )

    results = migrator.migrate(java_code, validate=True, refactor=True)
    migrator.print_results(results)

    print("\n" + "="*80)
    print(f"✓ 模式选择: {results['mode_used']} (高质量、完整实现)")
    print("="*80)


def demo_forced_semantic():
    """演示 3: 强制使用语义理解模式"""
    print("\n\n")
    print("="*80)
    print("演示 3: 强制语义理解模式 - 简单类也使用 LLM")
    print("="*80)

    java_code = """
    public class Calculator {
        public int add(int a, int b) {
            return a + b;
        }

        public int subtract(int a, int b) {
            return a - b;
        }
    }
    """

    print("\n【原始 Java 代码】")
    print(java_code)

    # 强制使用语义理解模式
    migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("mock"),
        mode=MigrationMode.SEMANTIC  # 强制语义模式
    )

    results = migrator.migrate(java_code, validate=True)
    migrator.print_results(results)


def demo_with_real_llm():
    """演示 4: 使用真实的 LLM (需要 API key)"""
    print("\n\n")
    print("="*80)
    print("演示 4: 使用真实 LLM 的高质量迁移")
    print("="*80)
    print("\n提示: 这需要设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量")
    print("如果没有 API key,请跳过此演示\n")

    import os

    # 检查是否有 API key
    has_openai = os.getenv('OPENAI_API_KEY')
    has_anthropic = os.getenv('ANTHROPIC_API_KEY')
    has_ollama = True  # Ollama 是本地的,总是可用(如果已安装)

    if not (has_openai or has_anthropic or has_ollama):
        print("❌ 未找到任何 LLM 配置,跳过此演示")
        print("\n配置方法:")
        print("  - OpenAI: export OPENAI_API_KEY='sk-...'")
        print("  - Anthropic: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("  - Ollama: 运行 'ollama serve' 启动本地服务")
        return

    # 尝试创建 LLM 提供者
    try:
        if has_openai:
            print("✓ 使用 OpenAI GPT-4")
            provider = create_llm_provider("openai", model="gpt-4-turbo-preview")
        elif has_anthropic:
            print("✓ 使用 Anthropic Claude")
            provider = create_llm_provider("anthropic")
        else:
            print("✓ 使用本地 Ollama (codellama)")
            provider = create_llm_provider("ollama", model="codellama")

        java_code = """
        public class UserValidator {
            public boolean validateEmail(String email) {
                if (email == null || email.trim().isEmpty()) {
                    return false;
                }

                int atIndex = email.indexOf('@');
                if (atIndex <= 0 || atIndex == email.length() - 1) {
                    return false;
                }

                String domain = email.substring(atIndex + 1);
                return domain.contains(".");
            }
        }
        """

        print("\n【原始 Java 代码】")
        print(java_code)

        migrator = IntelligentMigrator(
            llm_provider=provider,
            mode=MigrationMode.SEMANTIC
        )

        results = migrator.migrate(java_code, validate=True, refactor=True)
        migrator.print_results(results)

    except Exception as e:
        print(f"❌ LLM 调用失败: {e}")
        print("请检查 API key 配置或 Ollama 服务状态")


def show_comparison():
    """显示三种模式的对比"""
    print("\n\n")
    print("="*80)
    print("三种迁移模式对比总结")
    print("="*80)

    comparison = """
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ 特性           │ 规则映射模式   │ 语义理解模式   │ 混合模式       │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ 速度           │ ⚡ 非常快      │ 🐢 较慢        │ ⚡🐢 智能选择  │
│ 成本           │ 💰 免费        │ 💰💰 需付费    │ 💰💰 按需付费  │
│ 质量           │ ⭐⭐⭐         │ ⭐⭐⭐⭐⭐      │ ⭐⭐⭐⭐       │
│ 方法体实现     │ ❌ 不支持      │ ✅ 完整实现    │ ✅ 智能处理    │
│ 设计模式识别   │ ❌ 不支持      │ ✅ 支持        │ ✅ 智能处理    │
│ Pythonic重构   │ ❌ 基础        │ ✅ 深度重构    │ ✅ 智能重构    │
│ 适用场景       │ POJO/DTO      │ 业务逻辑       │ 所有场景       │
└────────────────┴────────────────┴────────────────┴────────────────┘

推荐使用策略:
✓ 混合模式 (HYBRID) - 自动选择最佳方案,平衡质量和成本
✓ 简单数据类 -> 自动使用规则映射(快速、免费)
✓ 复杂业务逻辑 -> 自动使用语义理解(高质量)
    """
    print(comparison)


if __name__ == "__main__":
    try:
        # 获取日志器
        logger = get_logger(verbose=False, use_color=True)

        print("🚀 Java to Python 智能迁移工具 - 完整演示\n")

        # 运行演示
        demo_simple_pojo()
        demo_complex_service()
        demo_forced_semantic()

        # 显示对比
        show_comparison()

        # 可选:真实 LLM 演示
        response = input("\n是否尝试使用真实 LLM? (需要 API key) [y/N]: ")
        if response.lower() == 'y':
            demo_with_real_llm()

        print("\n\n")
        print("="*80)
        print("✅ 所有演示完成!")
        print("="*80)
        print("\n下一步:")
        print("  1. 配置真实的 LLM (OpenAI/Anthropic/Ollama)")
        print("  2. 在 main.py 中集成智能迁移器")
        print("  3. 使用: python src/main.py -i Example.java --intelligent")

    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
