"""
Costrict 风格的智能 Agent 系统
基于严格模式的多 Agent 协作架构

参考: https://github.com/zgsm-ai/costrict
核心理念: 质量优先、严格流程、系统化分解
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from llm_providers import LLMProvider
from logger import get_logger
import json


class AgentPhase(Enum):
    """Agent 执行阶段 (参考 Costrict 严格模式)"""
    REQUIREMENTS_ANALYSIS = "requirements_analysis"  # 需求分析
    ARCHITECTURE_DESIGN = "architecture_design"      # 架构设计
    TASK_PLANNING = "task_planning"                  # 任务规划
    CODE_GENERATION = "code_generation"              # 代码生成
    TEST_GENERATION = "test_generation"              # 测试生成
    CODE_REVIEW = "code_review"                      # 代码审查
    QUALITY_CHECK = "quality_check"                  # 质量检查


@dataclass
class AgentContext:
    """Agent 上下文 - 在各 Agent 间传递的共享信息"""
    # 输入
    java_code: str
    java_structure: Optional[Dict] = None

    # 分析结果
    requirements: Optional[Dict] = None
    architecture: Optional[Dict] = None
    plan: Optional[Dict] = None

    # 生成结果
    python_code: Optional[str] = None
    test_code: Optional[str] = None

    # 审查结果
    review_report: Optional[Dict] = None
    quality_report: Optional[Dict] = None

    # 元数据
    metadata: Dict[str, Any] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class BaseStrictAgent:
    """严格模式 Agent 基类"""

    def __init__(self, name: str, llm: LLMProvider):
        self.name = name
        self.llm = llm
        self.logger = get_logger()
        self.phase = None

    def execute(self, context: AgentContext) -> AgentContext:
        """
        执行 Agent 任务

        Args:
            context: Agent 上下文

        Returns:
            更新后的上下文
        """
        self.logger.section(f"[{self.name}] 开始执行")

        try:
            # 验证前置条件
            if not self.validate_preconditions(context):
                raise ValueError(f"{self.name}: 前置条件验证失败")

            # 执行核心逻辑
            context = self.process(context)

            # 验证输出
            if not self.validate_output(context):
                raise ValueError(f"{self.name}: 输出验证失败")

            self.logger.success(f"[{self.name}] 执行完成")

        except Exception as e:
            self.logger.error(f"[{self.name}] 执行失败: {str(e)}")
            context.errors.append(f"{self.name}: {str(e)}")

        return context

    def validate_preconditions(self, context: AgentContext) -> bool:
        """验证前置条件"""
        return True

    def process(self, context: AgentContext) -> AgentContext:
        """处理逻辑(子类实现)"""
        raise NotImplementedError

    def validate_output(self, context: AgentContext) -> bool:
        """验证输出"""
        return True


class RequirementsAnalysisAgent(BaseStrictAgent):
    """需求分析 Agent - 理解迁移需求和业务逻辑"""

    def __init__(self, llm: LLMProvider):
        super().__init__("RequirementsAnalysis", llm)
        self.phase = AgentPhase.REQUIREMENTS_ANALYSIS

    def validate_preconditions(self, context: AgentContext) -> bool:
        """验证是否有 Java 代码"""
        return bool(context.java_code and context.java_code.strip())

    def process(self, context: AgentContext) -> AgentContext:
        """分析迁移需求"""
        self.logger.info("📋 分析迁移需求...")

        prompt = f"""
作为需求分析专家,请分析以下 Java 代码的迁移需求:

```java
{context.java_code}
```

请分析并以 JSON 格式返回:
{{
  "business_domain": "业务领域(如: 用户管理、订单处理等)",
  "core_functions": ["核心功能1", "核心功能2"],
  "technical_requirements": ["技术要求1", "技术要求2"],
  "data_structures": ["关键数据结构1", "关键数据结构2"],
  "external_dependencies": ["外部依赖1", "外部依赖2"],
  "quality_requirements": ["质量要求1", "质量要求2"],
  "migration_challenges": ["挑战1", "挑战2"],
  "priority": "高/中/低"
}}
"""

        response = self.llm.complete(
            prompt,
            system="你是专业的软件需求分析师。",
            temperature=0.1
        )

        requirements = self._parse_json(response)
        context.requirements = requirements

        self.logger.info(f"  业务领域: {requirements.get('business_domain', '未知')}")
        self.logger.info(f"  优先级: {requirements.get('priority', '中')}")

        return context

    def validate_output(self, context: AgentContext) -> bool:
        """验证需求分析结果"""
        return context.requirements is not None

    def _parse_json(self, text: str) -> Dict:
        """解析 JSON 响应"""
        import re
        try:
            return json.loads(text.strip())
        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {}


class ArchitectureDesignAgent(BaseStrictAgent):
    """架构设计 Agent - 设计 Python 代码架构"""

    def __init__(self, llm: LLMProvider):
        super().__init__("ArchitectureDesign", llm)
        self.phase = AgentPhase.ARCHITECTURE_DESIGN

    def validate_preconditions(self, context: AgentContext) -> bool:
        """需要需求分析结果"""
        return context.requirements is not None

    def process(self, context: AgentContext) -> AgentContext:
        """设计 Python 架构"""
        self.logger.info("🏗️ 设计 Python 架构...")

        requirements = context.requirements

        prompt = f"""
基于以下需求,设计 Python 代码的架构:

需求分析:
{json.dumps(requirements, indent=2, ensure_ascii=False)}

原始 Java 代码:
```java
{context.java_code}
```

请设计 Python 架构并以 JSON 返回:
{{
  "class_structure": {{
    "class_name": "类名",
    "base_classes": ["基类1", "基类2"],
    "patterns": ["设计模式1", "设计模式2"],
    "responsibilities": ["职责1", "职责2"]
  }},
  "module_organization": ["模块组织建议"],
  "data_models": ["数据模型设计"],
  "interface_design": ["接口设计"],
  "error_handling": ["异常处理策略"],
  "pythonic_improvements": ["Pythonic 改进建议"]
}}
"""

        response = self.llm.complete(
            prompt,
            system="你是资深的软件架构师,擅长 Python 架构设计。",
            temperature=0.2
        )

        architecture = self._parse_json(response)
        context.architecture = architecture

        patterns = architecture.get('class_structure', {}).get('patterns', [])
        if patterns:
            self.logger.info(f"  设计模式: {', '.join(patterns)}")

        return context

    def validate_output(self, context: AgentContext) -> bool:
        """验证架构设计"""
        return context.architecture is not None

    def _parse_json(self, text: str) -> Dict:
        import re
        try:
            return json.loads(text.strip())
        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {}


class TaskPlanningAgent(BaseStrictAgent):
    """任务规划 Agent - 制定详细的实现计划"""

    def __init__(self, llm: LLMProvider):
        super().__init__("TaskPlanning", llm)
        self.phase = AgentPhase.TASK_PLANNING

    def validate_preconditions(self, context: AgentContext) -> bool:
        """需要架构设计"""
        return context.architecture is not None

    def process(self, context: AgentContext) -> AgentContext:
        """制定任务计划"""
        self.logger.info("📝 制定实现计划...")

        prompt = f"""
基于以下信息制定详细的实现计划:

需求:
{json.dumps(context.requirements, indent=2, ensure_ascii=False)}

架构:
{json.dumps(context.architecture, indent=2, ensure_ascii=False)}

请制定实现计划,以 JSON 返回:
{{
  "implementation_steps": [
    {{
      "step_number": 1,
      "description": "步骤描述",
      "tasks": ["任务1", "任务2"],
      "estimated_complexity": "简单/中等/复杂",
      "dependencies": [0]
    }}
  ],
  "code_structure": {{
    "imports": ["导入语句"],
    "classes": ["类定义顺序"],
    "methods": ["方法实现顺序"]
  }},
  "risk_points": ["风险点1", "风险点2"],
  "validation_checklist": ["验证项1", "验证项2"]
}}
"""

        response = self.llm.complete(
            prompt,
            system="你是软件项目管理专家。",
            temperature=0.1
        )

        plan = self._parse_json(response)
        context.plan = plan

        steps = plan.get('implementation_steps', [])
        self.logger.info(f"  实现步骤数: {len(steps)}")

        return context

    def validate_output(self, context: AgentContext) -> bool:
        return context.plan is not None

    def _parse_json(self, text: str) -> Dict:
        import re
        try:
            return json.loads(text.strip())
        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {}


class CodeGenerationAgent(BaseStrictAgent):
    """代码生成 Agent - 生成高质量 Python 代码"""

    def __init__(self, llm: LLMProvider):
        super().__init__("CodeGeneration", llm)
        self.phase = AgentPhase.CODE_GENERATION

    def validate_preconditions(self, context: AgentContext) -> bool:
        """需要至少有需求分析，计划是可选的（快速模式可能没有）"""
        return context.requirements is not None

    def process(self, context: AgentContext) -> AgentContext:
        """生成 Python 代码"""
        self.logger.info("💻 生成 Python 代码...")

        # 构建提示词，根据可用的上下文信息
        prompt_parts = [
            "严格按照以下规范生成高质量的 Python 代码:",
            "",
            "原始 Java 代码:",
            "```java",
            context.java_code,
            "```",
            "",
            "需求分析:",
            json.dumps(context.requirements, indent=2, ensure_ascii=False),
            ""
        ]

        # 如果有架构设计，添加到 prompt
        if context.architecture:
            prompt_parts.extend([
                "架构设计:",
                json.dumps(context.architecture, indent=2, ensure_ascii=False),
                ""
            ])

        # 如果有实现计划，添加到 prompt
        if context.plan:
            prompt_parts.extend([
                "实现计划:",
                json.dumps(context.plan, indent=2, ensure_ascii=False),
                ""
            ])

        prompt_parts.extend([
            "代码质量要求:",
            "1. 完整实现所有方法体(不允许 pass 或 TODO)",
            "2. 添加完整的类型注解(使用 typing 模块)",
            "3. 编写详细的文档字符串(Google 风格)",
            "4. 实现完整的异常处理",
            "5. 使用 Pythonic 惯用法",
            "6. 遵循 PEP 8 规范",
            "7. 添加必要的注释",
            "",
            "只返回完整的 Python 代码,用 ```python 包裹:"
        ])

        prompt = "\n".join(prompt_parts)

        response = self.llm.complete(
            prompt,
            system="你是专业的 Python 开发工程师,严格遵循代码质量标准。",
            temperature=0.2,
            max_tokens=4096
        )

        python_code = self._extract_code(response)
        context.python_code = python_code

        lines = python_code.count('\n')
        self.logger.info(f"  代码行数: {lines}")

        return context

    def validate_output(self, context: AgentContext) -> bool:
        """验证生成的代码"""
        if not context.python_code:
            return False

        # 基本验证
        code = context.python_code

        # 检查是否有实际代码
        if 'pass' in code and code.count('pass') > code.count('def'):
            context.warnings.append("代码包含过多的 pass 语句")

        return True

    def _extract_code(self, text: str) -> str:
        import re
        match = re.search(r'```python\s*\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r'```\s*\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()


class TestGenerationAgent(BaseStrictAgent):
    """测试生成 Agent - 生成单元测试"""

    def __init__(self, llm: LLMProvider):
        super().__init__("TestGeneration", llm)
        self.phase = AgentPhase.TEST_GENERATION

    def validate_preconditions(self, context: AgentContext) -> bool:
        """需要生成的代码"""
        return context.python_code is not None

    def process(self, context: AgentContext) -> AgentContext:
        """生成测试代码"""
        self.logger.info("🧪 生成单元测试...")

        prompt = f"""
为以下 Python 代码生成完整的单元测试:

```python
{context.python_code}
```

要求:
1. 使用 pytest 框架
2. 测试所有public方法
3. 包含正常情况和边界情况
4. 包含异常处理测试
5. 使用 fixtures 管理测试数据
6. 添加清晰的测试文档
7. 确保测试覆盖率 > 80%

只返回测试代码,用 ```python 包裹:
"""

        response = self.llm.complete(
            prompt,
            system="你是测试工程师,精通 pytest 和 TDD。",
            temperature=0.2
        )

        test_code = self._extract_code(response)
        context.test_code = test_code

        # 统计测试数量
        test_count = test_code.count('def test_')
        self.logger.info(f"  测试用例数: {test_count}")

        return context

    def _extract_code(self, text: str) -> str:
        import re
        match = re.search(r'```python\s*\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()


class CodeReviewAgent(BaseStrictAgent):
    """代码审查 Agent - 严格的质量审查"""

    def __init__(self, llm: LLMProvider):
        super().__init__("CodeReview", llm)
        self.phase = AgentPhase.CODE_REVIEW

    def validate_preconditions(self, context: AgentContext) -> bool:
        """需要代码和测试"""
        return context.python_code is not None

    def process(self, context: AgentContext) -> AgentContext:
        """执行代码审查"""
        self.logger.info("🔍 执行严格代码审查...")

        prompt = f"""
作为资深代码审查专家,请严格审查以下代码:

原始 Java 代码:
```java
{context.java_code}
```

生成的 Python 代码:
```python
{context.python_code}
```

审查维度:
1. 语义正确性 - 是否保持了原始逻辑
2. 代码完整性 - 是否所有功能都实现
3. 代码质量 - 是否符合最佳实践
4. 性能 - 是否有性能问题
5. 安全性 - 是否有安全隐患
6. 可维护性 - 是否易于维护
7. Pythonic - 是否符合 Python 风格

以 JSON 格式返回审查报告:
{{
  "semantic_correctness": {{
    "score": 85,
    "issues": ["问题1", "问题2"]
  }},
  "code_completeness": {{
    "score": 90,
    "missing_features": []
  }},
  "code_quality": {{
    "score": 80,
    "violations": ["违规1"]
  }},
  "security": {{
    "score": 95,
    "vulnerabilities": []
  }},
  "overall_score": 85,
  "overall_rating": "优秀/良好/一般/需改进",
  "critical_issues": [],
  "suggestions": ["建议1", "建议2"],
  "approval_status": "通过/需修改/拒绝"
}}
"""

        response = self.llm.complete(
            prompt,
            system="你是代码审查专家,标准严格,注重质量。",
            temperature=0.1
        )

        review = self._parse_json(response)
        context.review_report = review

        score = review.get('overall_score', 0)
        status = review.get('approval_status', '未知')
        self.logger.info(f"  总分: {score}/100")
        self.logger.info(f"  状态: {status}")

        # 记录关键问题
        critical = review.get('critical_issues', [])
        for issue in critical:
            context.warnings.append(f"Critical: {issue}")

        return context

    def _parse_json(self, text: str) -> Dict:
        import re
        try:
            return json.loads(text.strip())
        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"overall_score": 0, "approval_status": "未知"}


# 使用示例在下一个文件
