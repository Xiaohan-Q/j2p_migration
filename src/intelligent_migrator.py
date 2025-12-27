"""
智能迁移编排器
整合语义理解、规则映射和混合决策
"""
from typing import Dict, List, Any, Optional
from llm_providers import LLMProvider, create_llm_provider
from semantic_agents import SemanticAnalyzer, SemanticCodeGenerator, CodeReviewer
from ast_parser import JavaASTParser
from semantic_mapper import SemanticMapper
from code_generater import PythonCodeGenerator
from validator import MigrationValidator
from logger import get_logger
import json


class MigrationMode:
    """迁移模式"""
    RULE_BASED = "rule_based"      # 规则映射模式
    SEMANTIC = "semantic"            # 语义理解模式
    HYBRID = "hybrid"                # 混合模式(自动选择)


class IntelligentMigrator:
    """智能迁移器 - 支持多种模式"""

    def __init__(self, llm_provider: Optional[LLMProvider] = None,
                 mode: str = MigrationMode.HYBRID):
        """
        初始化智能迁移器

        Args:
            llm_provider: LLM 提供者(如果为 None 且模式需要,会使用 Mock)
            mode: 迁移模式 (rule_based, semantic, hybrid)
        """
        self.mode = mode
        self.logger = get_logger()

        # 规则映射组件(始终可用)
        self.java_parser = JavaASTParser()
        self.semantic_mapper = SemanticMapper()
        self.code_generator = PythonCodeGenerator()
        self.validator = MigrationValidator()

        # LLM 组件(语义模式需要)
        if mode in [MigrationMode.SEMANTIC, MigrationMode.HYBRID]:
            if llm_provider is None:
                self.logger.warning("未提供 LLM,使用 Mock 模式")
                llm_provider = create_llm_provider("mock")

            self.llm = llm_provider
            self.semantic_analyzer = SemanticAnalyzer(llm_provider)
            self.semantic_generator = SemanticCodeGenerator(llm_provider)
            self.code_reviewer = CodeReviewer(llm_provider)
        else:
            self.llm = None
            self.semantic_analyzer = None
            self.semantic_generator = None
            self.code_reviewer = None

    def migrate(self, java_code: str,
                validate: bool = True,
                refactor: bool = False) -> Dict[str, Any]:
        """
        执行智能迁移

        Args:
            java_code: Java 源代码
            validate: 是否验证
            refactor: 是否重构为更 Pythonic 的代码

        Returns:
            迁移结果字典
        """
        self.logger.section(f"开始智能迁移 (模式: {self.mode})")

        results = {
            'success': False,
            'mode_used': None,
            'java_structure': None,
            'python_code': None,
            'business_analysis': None,
            'review_report': None,
            'validation_report': None,
            'errors': [],
            'warnings': []
        }

        try:
            # 决定使用哪种模式
            if self.mode == MigrationMode.HYBRID:
                actual_mode = self._decide_mode(java_code)
            else:
                actual_mode = self.mode

            results['mode_used'] = actual_mode
            self.logger.info(f"使用模式: {actual_mode}")

            # 执行迁移
            if actual_mode == MigrationMode.RULE_BASED:
                python_code = self._migrate_rule_based(java_code, results)
            else:  # SEMANTIC
                python_code = self._migrate_semantic(java_code, results, refactor)

            results['python_code'] = python_code

            # 验证
            if validate:
                self.logger.section("验证代码")
                validation_report = self.validator.validate_migration(
                    java_code,
                    python_code,
                    results.get('python_structure')
                )
                results['validation_report'] = validation_report

                if validation_report['overall_status'] == 'failed':
                    results['warnings'].append("代码验证发现问题")

            results['success'] = len(results['errors']) == 0

        except Exception as e:
            results['errors'].append(f"迁移失败: {str(e)}")
            self.logger.exception("迁移过程出错", exc=e)

        return results

    def _decide_mode(self, java_code: str) -> str:
        """
        决定使用哪种模式

        规则:
        - 简单的 POJO/DTO/实体类 -> 规则映射(快速、免费)
        - 复杂的业务逻辑类 -> 语义理解(高质量)
        """
        # 解析代码
        structure = self.java_parser.get_full_structure(java_code)

        if not structure:
            return MigrationMode.RULE_BASED

        # 计算复杂度分数
        complexity_score = 0

        for cls in structure.get('classes', []):
            # 方法数量
            num_methods = len(cls.get('methods', []))
            if num_methods > 10:
                complexity_score += 3
            elif num_methods > 5:
                complexity_score += 2
            elif num_methods > 2:
                complexity_score += 1

            # 继承和接口
            if cls.get('extends'):
                complexity_score += 2
            if cls.get('implements'):
                complexity_score += 2

            # 检查方法体复杂度
            for method in cls.get('methods', []):
                body = method.get('body')
                if body:
                    # 检查是否有复杂逻辑
                    # (这里简化处理,实际可以更复杂)
                    complexity_score += 1

        # 决策
        if complexity_score <= 3:
            self.logger.info(f"复杂度分数: {complexity_score} -> 使用规则映射")
            return MigrationMode.RULE_BASED
        else:
            self.logger.info(f"复杂度分数: {complexity_score} -> 使用语义理解")
            return MigrationMode.SEMANTIC

    def _migrate_rule_based(self, java_code: str,
                           results: Dict[str, Any]) -> str:
        """
        规则映射模式迁移

        优点: 快速、免费、可预测
        缺点: 不能处理复杂逻辑
        """
        self.logger.info("📋 使用规则映射模式...")

        # 解析
        java_structure = self.java_parser.get_full_structure(java_code)
        results['java_structure'] = java_structure

        # 映射
        python_structure = self.semantic_mapper.map_structure(java_structure)
        results['python_structure'] = python_structure

        # 生成
        python_code = self.code_generator.generate_code(python_structure)
        python_code = self.code_generator.format_code(python_code)

        return python_code

    def _migrate_semantic(self, java_code: str,
                         results: Dict[str, Any],
                         refactor: bool = False) -> str:
        """
        语义理解模式迁移

        优点: 高质量、完整实现、智能重构
        缺点: 需要 LLM API、较慢
        """
        self.logger.info("🧠 使用语义理解模式...")

        # 1. 业务逻辑分析
        business_analysis = self.semantic_analyzer.analyze_business_logic(java_code)
        results['business_analysis'] = business_analysis

        # 2. 生成 Python 代码
        python_code = self.semantic_generator.generate_python_code(
            java_code,
            business_analysis
        )

        # 3. 重构(可选)
        if refactor:
            self.logger.info("🔧 重构为更 Pythonic 的代码...")
            python_code = self.semantic_generator.refactor_to_pythonic(python_code)

        # 4. 审查
        self.logger.info("📝 审查迁移质量...")
        review_report = self.code_reviewer.review_migration(java_code, python_code)
        results['review_report'] = review_report

        # 如果审查发现严重问题,记录警告
        if review_report.get('overall_rating') in ['较差', '一般']:
            results['warnings'].append(
                f"代码质量评级: {review_report.get('overall_rating')}"
            )

        return python_code

    def print_results(self, results: Dict[str, Any]):
        """打印迁移结果"""
        print("\n" + "="*70)
        print("迁移结果")
        print("="*70)

        print(f"\n状态: {'✅ 成功' if results['success'] else '❌ 失败'}")
        print(f"使用模式: {results.get('mode_used', '未知')}")

        # 业务分析
        if results.get('business_analysis'):
            print("\n【业务分析】")
            analysis = results['business_analysis']
            print(f"  目的: {analysis.get('business_purpose', '未知')}")
            print(f"  复杂度: {analysis.get('complexity', '未知')}")
            if analysis.get('design_patterns'):
                print(f"  设计模式: {', '.join(analysis['design_patterns'])}")

        # 审查报告
        if results.get('review_report'):
            print("\n【代码审查】")
            report = results['review_report']
            print(f"  整体评级: {report.get('overall_rating', '未知')}")
            print(f"  Pythonic 评分: {report.get('pythonic_quality', '?')}/10")

            if report.get('issues'):
                print("  问题:")
                for issue in report['issues']:
                    print(f"    - {issue}")

            if report.get('suggestions'):
                print("  建议:")
                for suggestion in report['suggestions']:
                    print(f"    + {suggestion}")

        # 错误和警告
        if results['errors']:
            print("\n【错误】")
            for error in results['errors']:
                print(f"  ❌ {error}")

        if results['warnings']:
            print("\n【警告】")
            for warning in results['warnings']:
                print(f"  ⚠️  {warning}")

        # 生成的代码
        if results['python_code']:
            print("\n【生成的 Python 代码】")
            print("-" * 70)
            print(results['python_code'])
            print("-" * 70)


# 使用示例
def demo():
    """演示智能迁移"""

    # 简单示例 - 会使用规则映射
    simple_java = """
    public class Person {
        private String name;
        private int age;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }
    """

    # 复杂示例 - 会使用语义理解
    complex_java = """
    public class UserService {
        private UserRepository repository;
        private EmailValidator validator;

        public User createUser(String email, String name) {
            if (!validator.isValid(email)) {
                throw new IllegalArgumentException("Invalid email: " + email);
            }

            User user = new User(email, name);
            user.setCreatedAt(new Date());
            user.setStatus(UserStatus.ACTIVE);

            return repository.save(user);
        }

        public List<User> findActiveUsers() {
            return repository.findByStatus(UserStatus.ACTIVE);
        }
    }
    """

    # 创建迁移器(使用混合模式)
    migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("mock"),  # 替换为真实 LLM
        mode=MigrationMode.HYBRID
    )

    # 测试简单代码
    print("="*70)
    print("测试 1: 简单 POJO")
    print("="*70)
    results1 = migrator.migrate(simple_java)
    migrator.print_results(results1)

    # 测试复杂代码
    print("\n\n")
    print("="*70)
    print("测试 2: 复杂业务逻辑")
    print("="*70)
    results2 = migrator.migrate(complex_java, refactor=True)
    migrator.print_results(results2)


if __name__ == "__main__":
    demo()
