"""
Costrict 风格的 Agent 编排器
实现严格模式的工作流管理

工作流: 需求分析 → 架构设计 → 任务规划 → 代码生成 → 测试生成 → 代码审查
"""
from typing import Dict, List, Any, Optional
from costrict_agents import (
    AgentContext, AgentPhase,
    RequirementsAnalysisAgent,
    ArchitectureDesignAgent,
    TaskPlanningAgent,
    CodeGenerationAgent,
    TestGenerationAgent,
    CodeReviewAgent
)
from llm_providers import LLMProvider
from logger import get_logger
import json
from datetime import datetime


class StrictModeOrchestrator:
    """严格模式编排器 - 质量优先"""

    def __init__(self, llm: LLMProvider, enable_all_phases: bool = True):
        """
        初始化严格模式编排器

        Args:
            llm: LLM 提供者
            enable_all_phases: 是否启用所有阶段
        """
        self.llm = llm
        self.logger = get_logger()

        # 初始化所有 Agent
        self.agents = {
            AgentPhase.REQUIREMENTS_ANALYSIS: RequirementsAnalysisAgent(llm),
            AgentPhase.ARCHITECTURE_DESIGN: ArchitectureDesignAgent(llm),
            AgentPhase.TASK_PLANNING: TaskPlanningAgent(llm),
            AgentPhase.CODE_GENERATION: CodeGenerationAgent(llm),
            AgentPhase.TEST_GENERATION: TestGenerationAgent(llm),
            AgentPhase.CODE_REVIEW: CodeReviewAgent(llm)
        }

        # 定义工作流
        self.workflow = [
            AgentPhase.REQUIREMENTS_ANALYSIS,
            AgentPhase.ARCHITECTURE_DESIGN,
            AgentPhase.TASK_PLANNING,
            AgentPhase.CODE_GENERATION,
            AgentPhase.TEST_GENERATION,
            AgentPhase.CODE_REVIEW
        ]

        self.enable_all_phases = enable_all_phases

    def migrate_strict(self, java_code: str,
                      skip_tests: bool = False) -> Dict[str, Any]:
        """
        严格模式迁移

        Args:
            java_code: Java 源代码
            skip_tests: 是否跳过测试生成

        Returns:
            完整的迁移结果
        """
        self.logger.section("🔒 Costrict 严格模式迁移")

        # 创建上下文
        context = AgentContext(java_code=java_code)

        # 记录开始时间
        start_time = datetime.now()

        # 执行工作流
        for phase in self.workflow:
            # 可选跳过测试生成
            if skip_tests and phase == AgentPhase.TEST_GENERATION:
                self.logger.info(f"⏭️ 跳过阶段: {phase.value}")
                continue

            # 执行 Agent
            agent = self.agents[phase]
            context = agent.execute(context)

            # 检查是否有严重错误
            if context.errors and self._has_critical_error(context):
                self.logger.error("⚠️ 检测到严重错误,终止流程")
                break

        # 记录结束时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 构建结果
        results = self._build_results(context, duration)

        # 打印摘要
        self._print_summary(results)

        return results

    def migrate_fast(self, java_code: str) -> Dict[str, Any]:
        """
        快速模式(跳过部分阶段)

        Args:
            java_code: Java 源代码

        Returns:
            迁移结果
        """
        self.logger.section("⚡ 快速模式迁移")

        context = AgentContext(java_code=java_code)
        start_time = datetime.now()

        # 快速模式只执行核心阶段
        fast_workflow = [
            AgentPhase.REQUIREMENTS_ANALYSIS,
            AgentPhase.CODE_GENERATION,
            AgentPhase.CODE_REVIEW
        ]

        for phase in fast_workflow:
            agent = self.agents[phase]
            context = agent.execute(context)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        results = self._build_results(context, duration)
        self._print_summary(results)

        return results

    def _has_critical_error(self, context: AgentContext) -> bool:
        """检查是否有关键错误"""
        for error in context.errors:
            if any(keyword in error.lower() for keyword in
                   ['critical', 'failed', 'invalid']):
                return True
        return False

    def _build_results(self, context: AgentContext, duration: float) -> Dict[str, Any]:
        """构建结果字典"""
        success = len(context.errors) == 0

        results = {
            'success': success,
            'mode': 'strict' if self.enable_all_phases else 'fast',
            'duration': duration,

            # 各阶段结果
            'requirements': context.requirements,
            'architecture': context.architecture,
            'plan': context.plan,
            'python_code': context.python_code,
            'test_code': context.test_code,
            'review_report': context.review_report,

            # 质量指标
            'quality_metrics': self._calculate_quality_metrics(context),

            # 错误和警告
            'errors': context.errors,
            'warnings': context.warnings,

            # 元数据
            'metadata': context.metadata
        }

        return results

    def _calculate_quality_metrics(self, context: AgentContext) -> Dict[str, Any]:
        """计算质量指标"""
        metrics = {
            'overall_score': 0,
            'phase_scores': {},
            'completeness': 0,
            'quality_level': '未知'
        }

        if context.review_report:
            metrics['overall_score'] = context.review_report.get('overall_score', 0)
            metrics['quality_level'] = context.review_report.get('overall_rating', '未知')

        # 计算完整度
        completed_phases = 0
        total_phases = len(self.workflow)

        if context.requirements:
            completed_phases += 1
        if context.architecture:
            completed_phases += 1
        if context.plan:
            completed_phases += 1
        if context.python_code:
            completed_phases += 1
        if context.test_code:
            completed_phases += 1
        if context.review_report:
            completed_phases += 1

        metrics['completeness'] = int(completed_phases / total_phases * 100)

        return metrics

    def _print_summary(self, results: Dict[str, Any]):
        """打印执行摘要"""
        print("\n" + "="*80)
        print("📊 严格模式执行摘要")
        print("="*80)

        print(f"\n状态: {'✅ 成功' if results['success'] else '❌ 失败'}")
        print(f"模式: {results['mode']}")
        print(f"耗时: {results['duration']:.2f} 秒")

        # 质量指标
        metrics = results['quality_metrics']
        print(f"\n【质量指标】")
        print(f"  总分: {metrics['overall_score']}/100")
        print(f"  完整度: {metrics['completeness']}%")
        print(f"  质量等级: {metrics['quality_level']}")

        # 阶段完成情况
        print(f"\n【阶段完成情况】")
        print(f"  ✓ 需求分析: {'完成' if results['requirements'] else '未完成'}")
        print(f"  ✓ 架构设计: {'完成' if results['architecture'] else '未完成'}")
        print(f"  ✓ 任务规划: {'完成' if results['plan'] else '未完成'}")
        print(f"  ✓ 代码生成: {'完成' if results['python_code'] else '未完成'}")
        print(f"  ✓ 测试生成: {'完成' if results['test_code'] else '未完成'}")
        print(f"  ✓ 代码审查: {'完成' if results['review_report'] else '未完成'}")

        # 审查详情
        if results['review_report']:
            review = results['review_report']
            print(f"\n【代码审查详情】")
            print(f"  审批状态: {review.get('approval_status', '未知')}")

            if review.get('critical_issues'):
                print(f"  关键问题:")
                for issue in review['critical_issues']:
                    print(f"    ❌ {issue}")

            if review.get('suggestions'):
                print(f"  改进建议:")
                for suggestion in review['suggestions'][:3]:  # 只显示前3条
                    print(f"    💡 {suggestion}")

        # 错误和警告
        if results['errors']:
            print(f"\n【错误】")
            for error in results['errors']:
                print(f"  ❌ {error}")

        if results['warnings']:
            print(f"\n【警告】")
            for warning in results['warnings'][:5]:  # 只显示前5条
                print(f"  ⚠️  {warning}")

        print("\n" + "="*80)

    def export_report(self, results: Dict[str, Any], output_file: str):
        """导出完整报告"""
        report = {
            'metadata': {
                'tool': 'Costrict-style Java to Python Migrator',
                'mode': results['mode'],
                'timestamp': datetime.now().isoformat(),
                'duration': results['duration']
            },
            'quality_metrics': results['quality_metrics'],
            'phases': {
                'requirements_analysis': results['requirements'],
                'architecture_design': results['architecture'],
                'task_planning': results['plan'],
                'code_review': results['review_report']
            },
            'outputs': {
                'python_code_lines': results['python_code'].count('\n') if results['python_code'] else 0,
                'test_code_lines': results['test_code'].count('\n') if results['test_code'] else 0,
                'has_python_code': bool(results['python_code']),
                'has_test_code': bool(results['test_code'])
            },
            'errors': results['errors'],
            'warnings': results['warnings']
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"📄 报告已导出: {output_file}")


def demo():
    """演示 Costrict 风格的迁移"""
    from llm_providers import create_llm_provider

    # 创建 LLM
    provider = create_llm_provider("ollama", model="codellama")

    # 创建编排器
    orchestrator = StrictModeOrchestrator(provider)

    # 测试代码
    java_code = """
    public class UserValidator {
        private static final int MIN_AGE = 18;
        private EmailService emailService;

        public ValidationResult validateUser(User user) {
            ValidationResult result = new ValidationResult();

            // 验证年龄
            if (user.getAge() < MIN_AGE) {
                result.addError("User must be at least 18 years old");
                return result;
            }

            // 验证邮箱
            if (!emailService.isValidEmail(user.getEmail())) {
                result.addError("Invalid email format");
                return result;
            }

            // 验证用户名
            String username = user.getUsername();
            if (username == null || username.length() < 3) {
                result.addError("Username must be at least 3 characters");
                return result;
            }

            result.setValid(true);
            return result;
        }
    }
    """

    print("="*80)
    print("Costrict 风格智能 Agent 系统演示")
    print("="*80)

    # 执行严格模式迁移
    results = orchestrator.migrate_strict(java_code)

    # 显示生成的代码
    if results['python_code']:
        print("\n" + "="*80)
        print("生成的 Python 代码")
        print("="*80)
        print(results['python_code'])

    # 显示测试代码
    if results['test_code']:
        print("\n" + "="*80)
        print("生成的测试代码")
        print("="*80)
        print(results['test_code'])

    # 导出报告
    orchestrator.export_report(results, 'migration_report.json')


if __name__ == "__main__":
    demo()
