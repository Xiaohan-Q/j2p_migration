# ❓ Costrict 风格 Agent 系统常见问题解答 (FAQ)

本文档回答关于 Costrict 风格智能 Agent 系统的常见问题。

---

## 📋 目录

1. [这是单一主控agent还是多agent组？](#1-这是单一主控agent还是多agent组)
2. [现在效果的评判标准是什么？由什么来评判的？有什么依据？](#2-现在效果的评判标准是什么由什么来评判的有什么依据)
3. [如果我想更改测试案例，我应该调整哪个文件里的代码？](#3-如果我想更改测试案例我应该调整哪个文件里的代码)
4. [如果我想更改LLM，我应该调整哪个文件里的代码？](#4-如果我想更改llm我应该调整哪个文件里的代码)
5. [项目文件清单](#5-项目文件清单)

---

## 1. 这是单一主控agent还是多agent组？

### ✅ 答案：多 Agent 组（Multi-Agent System）

本系统采用**多 Agent 协作架构**，而不是单一主控 Agent。

### 🏗️ 系统架构

```
┌────────────────────────────────────────────┐
│    StrictModeOrchestrator (编排器/协调者)   │  ← 单一协调者
│                                            │
│  管理 6 个专业 Agent:                       │
│  ┌──────────────────────────────────────┐ │
│  │ 1. RequirementsAnalysisAgent         │ │  ← 独立 Agent
│  │ 2. ArchitectureDesignAgent           │ │  ← 独立 Agent
│  │ 3. TaskPlanningAgent                 │ │  ← 独立 Agent
│  │ 4. CodeGenerationAgent               │ │  ← 独立 Agent
│  │ 5. TestGenerationAgent               │ │  ← 独立 Agent
│  │ 6. CodeReviewAgent                   │ │  ← 独立 Agent
│  └──────────────────────────────────────┘ │
│                                            │
│  共享: AgentContext (上下文数据)           │
└────────────────────────────────────────────┘
```

### 📊 组成部分

| 组件 | 数量 | 角色 | 文件位置 |
|------|------|------|---------|
| **编排器 (Orchestrator)** | 1 | 协调和调度工作流 | [src/costrict_orchestrator.py](src/costrict_orchestrator.py) |
| **专业 Agent** | 6 | 各自负责特定任务 | [src/costrict_agents.py](src/costrict_agents.py) |
| **共享上下文** | 1 | 数据传递载体 | `AgentContext` 类 |

### 🔄 工作流程

```python
# src/costrict_orchestrator.py

class StrictModeOrchestrator:
    def __init__(self, llm: LLMProvider):
        # 初始化所有 Agent
        self.agents = {
            AgentPhase.REQUIREMENTS_ANALYSIS: RequirementsAnalysisAgent(llm),
            AgentPhase.ARCHITECTURE_DESIGN: ArchitectureDesignAgent(llm),
            AgentPhase.TASK_PLANNING: TaskPlanningAgent(llm),
            AgentPhase.CODE_GENERATION: CodeGenerationAgent(llm),
            AgentPhase.TEST_GENERATION: TestGenerationAgent(llm),
            AgentPhase.CODE_REVIEW: CodeReviewAgent(llm)
        }

        # 定义工作流顺序
        self.workflow = [
            AgentPhase.REQUIREMENTS_ANALYSIS,
            AgentPhase.ARCHITECTURE_DESIGN,
            AgentPhase.TASK_PLANNING,
            AgentPhase.CODE_GENERATION,
            AgentPhase.TEST_GENERATION,
            AgentPhase.CODE_REVIEW
        ]

    def migrate_strict(self, java_code: str) -> Dict:
        # 创建共享上下文
        context = AgentContext(java_code=java_code)

        # 顺序执行各个 Agent
        for phase in self.workflow:
            agent = self.agents[phase]
            context = agent.execute(context)  # 数据流式传递

        return context
```

### 🎯 关键特点

1. **编排器职责**：
   - ✅ 管理 Agent 的执行顺序
   - ✅ 协调 Agent 间的数据传递
   - ✅ 处理错误和异常
   - ✅ 生成最终报告

2. **Agent 职责**：
   - ✅ 每个 Agent 负责单一、明确的任务
   - ✅ 读取共享上下文中的输入数据
   - ✅ 执行专业化处理
   - ✅ 将结果写回共享上下文

3. **协作模式**：
   - **共享上下文模式 (Shared Context Pattern)**
   - Agent 之间松耦合，通过上下文传递数据
   - 支持顺序执行（当前）和并行执行（未来可扩展）

### 📝 6 个 Agent 详细说明

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **1. RequirementsAnalysisAgent** | 分析业务需求 | `java_code` | `requirements` |
| **2. ArchitectureDesignAgent** | 设计 Python 架构 | `requirements` | `architecture` |
| **3. TaskPlanningAgent** | 制定实现计划 | `architecture` | `plan` |
| **4. CodeGenerationAgent** | 生成 Python 代码 | `plan` | `python_code` |
| **5. TestGenerationAgent** | 生成单元测试 | `python_code` | `test_code` |
| **6. CodeReviewAgent** | 审查代码质量 | `java_code` + `python_code` | `review_report` |

### 🔗 数据流示意

```
java_code (输入)
    ↓
[需求分析] → requirements
    ↓
[架构设计] → architecture
    ↓
[任务规划] → plan
    ↓
[代码生成] → python_code
    ↓
[测试生成] → test_code
    ↓
[代码审查] → review_report
    ↓
完整结果 (输出)
```

---

## 2. 现在效果的评判标准是什么？由什么来评判的？有什么依据？

### ✅ 答案：由 LLM 驱动的多维度评分系统

效果评判由 **CodeReviewAgent** 负责，使用 **LLM (如 Ollama codellama)** 进行智能评审。

### 📊 评判标准（7 个维度）

| 维度 | 权重 | 评判内容 | 分数范围 |
|------|------|---------|---------|
| **1. 语义正确性** | 40% | Java 和 Python 代码的业务逻辑是否一致 | 0-100 |
| **2. 代码完整性** | 15% | 所有方法是否都实现（不是空 pass） | 0-100 |
| **3. 代码质量** | 20% | 是否符合 PEP8、最佳实践 | 0-100 |
| **4. 性能** | 5% | 是否有明显性能问题 | 0-100 |
| **5. 安全性** | 10% | 是否有安全隐患 (SQL注入、XSS等) | 0-100 |
| **6. 可维护性** | 5% | 代码可读性、注释、文档 | 0-100 |
| **7. Pythonic 程度** | 5% | 是否使用 Python 特性和惯用法 | 0-100 |

**总分计算公式**：
```
总分 = Σ (各维度分数 × 权重)
    = 语义正确性×0.4 + 代码完整性×0.15 + 代码质量×0.2
      + 性能×0.05 + 安全性×0.1 + 可维护性×0.05 + Pythonic×0.05
```

### 🤖 评判者：CodeReviewAgent

**文件位置**：[src/costrict_agents.py:468-560](src/costrict_agents.py#L468-L560)

```python
class CodeReviewAgent(BaseStrictAgent):
    """代码审查 Agent - 严格的质量审查"""

    def process(self, context: AgentContext) -> AgentContext:
        """执行代码审查"""

        # 构建审查 Prompt
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
  "semantic_correctness": {{"score": 85, "issues": []}},
  "code_completeness": {{"score": 90, "missing_features": []}},
  "code_quality": {{"score": 80, "violations": []}},
  "security": {{"score": 95, "vulnerabilities": []}},
  "overall_score": 85,
  "overall_rating": "优秀/良好/一般/需改进",
  "critical_issues": [],
  "suggestions": ["建议1", "建议2"],
  "approval_status": "通过/需修改/拒绝"
}}
"""

        # 调用 LLM 进行评审
        response = self.llm.complete(
            prompt,
            system="你是代码审查专家,标准严格,注重质量。",
            temperature=0.1  # 低温度确保评审的一致性
        )

        # 解析评审结果
        review = self._parse_json(response)
        context.review_report = review

        return context
```

### 📝 评审报告示例

参考 [output/strict_mode/report.json](output/strict_mode/report.json):

```json
{
  "code_review": {
    "semantic_correctness": {
      "score": 85,
      "issues": []
    },
    "code_completeness": {
      "score": 90,
      "missing_features": []
    },
    "code_quality": {
      "score": 80,
      "violations": ["某些变量命名不够清晰"]
    },
    "security": {
      "score": 95,
      "vulnerabilities": []
    },
    "performance": {
      "score": 88,
      "bottlenecks": []
    },
    "maintainability": {
      "score": 82,
      "issues": []
    },
    "pythonic_quality": {
      "score": 75,
      "suggestions": ["可以使用列表推导式", "建议使用上下文管理器"]
    },
    "overall_score": 85,
    "overall_rating": "良好",
    "critical_issues": [],
    "suggestions": [
      "考虑添加类型注解",
      "部分方法可以提取为辅助函数"
    ],
    "approval_status": "通过"
  }
}
```

### 🎯 评判依据

评判基于以下几个方面：

#### 1. **LLM 的语义理解能力**
- 使用 Ollama codellama（或其他 LLM）的代码理解能力
- LLM 可以理解业务逻辑的深层含义
- 对比原始 Java 和生成的 Python 的语义等价性

#### 2. **专家规则（嵌入在 Prompt 中）**
- **PEP8 规范**：Python 代码风格指南
- **最佳实践**：SOLID 原则、设计模式等
- **安全规范**：OWASP Top 10 等
- **性能准则**：算法复杂度、资源使用等

#### 3. **对比分析**
```
原始 Java 代码的功能 = 生成的 Python 代码的功能 ?
├─ 业务逻辑是否一致
├─ 边界条件是否处理
├─ 异常处理是否完整
└─ 数据流是否正确
```

#### 4. **静态检查（程序化验证）**
```python
# 代码完整性检查
def validate_output(self, context: AgentContext) -> bool:
    """验证输出结果"""
    if not context.review_report:
        return False

    # 检查必须的字段
    required_fields = [
        'overall_score',
        'approval_status'
    ]

    return all(
        field in context.review_report
        for field in required_fields
    )
```

### 📊 审批状态

根据总分自动判定审批状态：

| 总分范围 | 评级 | 审批状态 | 说明 |
|---------|------|---------|------|
| **90-100** | 优秀 | ✅ **通过** | 可直接使用 |
| **75-89** | 良好 | ✅ **通过** | 可使用，建议小优化 |
| **60-74** | 一般 | ⚠️ **需修改** | 需要改进后使用 |
| **0-59** | 较差 | ❌ **拒绝** | 不建议使用，需重新生成 |

### 🔍 评判流程

```
1. CodeReviewAgent 接收上下文
   ├─ 输入: java_code (原始)
   └─ 输入: python_code (生成的)

2. 构建详细的审查 Prompt
   ├─ 包含 7 个评审维度
   ├─ 包含具体的评分标准
   └─ 要求返回 JSON 格式

3. 调用 LLM 进行评审
   ├─ 使用低温度 (0.1) 确保一致性
   └─ 系统提示: "你是代码审查专家"

4. 解析 LLM 返回的 JSON
   ├─ 提取各维度分数
   ├─ 提取问题列表
   └─ 提取改进建议

5. 计算加权总分
   └─ overall_score = Σ(维度分数 × 权重)

6. 判定审批状态
   └─ approval_status = f(overall_score)

7. 记录到上下文
   └─ context.review_report = {...}
```

### 💡 为什么这样评判？

**优点**：

1. **智能化**：LLM 可以理解深层语义，不只是语法检查
2. **全面性**：涵盖 7 个维度，不遗漏重要方面
3. **客观性**：基于明确的评分标准，减少主观性
4. **可追溯**：详细的报告说明每个问题和建议
5. **可定制**：可以通过修改 Prompt 调整评审标准

**局限性**：

1. **依赖 LLM 质量**：不同 LLM 的评审能力差异大
2. **可能不稳定**：同样的代码可能得到略有不同的分数
3. **无法检测运行时问题**：静态分析的局限性

---

## 3. 如果我想更改测试案例，我应该调整哪个文件里的代码？

### ✅ 答案：修改 [src/costrict_agents.py](src/costrict_agents.py) 中的 `TestGenerationAgent` 类

### 📍 具体位置

**文件**：[src/costrict_agents.py:398-466](src/costrict_agents.py#L398-L466)

**类名**：`TestGenerationAgent`

### 🔧 修改方法

```python
class TestGenerationAgent(BaseStrictAgent):
    """测试生成 Agent"""

    def process(self, context: AgentContext) -> AgentContext:
        """生成测试代码"""
        self.logger.info("🧪 生成单元测试...")

        # 🎯 修改这里的 prompt 来调整测试生成策略
        prompt = f"""
为以下 Python 代码生成完整的单元测试:

```python
{context.python_code}
```

要求:
1. 使用 pytest 框架            # ← 可改为 unittest
2. 测试所有public方法           # ← 可调整覆盖范围
3. 包含正常情况和边界情况       # ← 可增加异常测试
4. 包含异常处理测试
5. 使用 fixtures 管理测试数据  # ← 可改为其他方式
6. 添加清晰的测试文档
7. 确保测试覆盖率 > 80%         # ← 可调整覆盖率要求

只返回测试代码,用 ```python 包裹:
"""

        response = self.llm.complete(
            prompt,
            system="你是测试工程师,精通 pytest 和 TDD。",  # ← 可调整角色
            temperature=0.2  # ← 可调整创造性 (0=确定, 1=随机)
        )

        test_code = self._extract_code(response)
        context.test_code = test_code

        # 统计测试数量
        test_count = test_code.count('def test_')
        self.logger.info(f"  测试用例数: {test_count}")

        return context
```

### 📝 修改示例

#### 示例 1: 改用 unittest 框架

```python
prompt = f"""
为以下 Python 代码生成完整的单元测试:

```python
{context.python_code}
```

要求:
1. 使用 unittest 框架  # ← 改这里
2. 创建 TestCase 子类
3. 使用 setUp 和 tearDown 方法
4. 测试所有 public 方法
5. 包含正常情况和异常情况
6. 添加详细的 docstring
7. 确保测试覆盖率 > 80%

只返回测试代码,用 ```python 包裹:
"""

# 同时修改系统提示
response = self.llm.complete(
    prompt,
    system="你是测试工程师,精通 unittest 框架。",
    temperature=0.2
)
```

#### 示例 2: 增加集成测试和端到端测试

```python
prompt = f"""
为以下 Python 代码生成完整的测试套件:

```python
{context.python_code}
```

要求:
1. 使用 pytest 框架
2. 生成三种测试:
   - 单元测试 (test_unit_*.py) - 测试单个方法
   - 集成测试 (test_integration_*.py) - 测试模块间交互
   - 端到端测试 (test_e2e_*.py) - 测试完整流程
3. 使用 fixtures 管理测试数据
4. 使用 parametrize 进行参数化测试
5. 包含性能测试 (使用 pytest-benchmark)
6. 添加详细的测试文档
7. 确保总测试覆盖率 > 90%

返回格式:
```python
# test_unit_xxx.py
[单元测试代码]

# test_integration_xxx.py
[集成测试代码]

# test_e2e_xxx.py
[端到端测试代码]
```
"""
```

#### 示例 3: 调整覆盖率和测试深度

```python
prompt = f"""
为以下 Python 代码生成**全面的**单元测试:

```python
{context.python_code}
```

要求:
1. 使用 pytest 框架
2. 测试所有方法（包括 private 方法）  # ← 扩大覆盖范围
3. 每个方法至少 5 个测试用例:
   - 正常情况 (Happy Path)
   - 边界条件 (Boundary Cases)
   - 异常情况 (Exception Cases)
   - 空值/None 处理
   - 并发安全性（如适用）
4. 使用 mock/patch 隔离外部依赖
5. 使用 fixtures 管理复杂测试数据
6. 添加性能基准测试
7. 确保测试覆盖率 > 95%  # ← 提高覆盖率要求
8. 每个测试都有详细的文档字符串

只返回测试代码,用 ```python 包裹:
"""

response = self.llm.complete(
    prompt,
    system="你是资深测试工程师,精通 TDD、BDD 和测试金字塔理论。",
    temperature=0.15  # ← 降低温度提高质量
)
```

#### 示例 4: 添加特定测试类型

```python
prompt = f"""
为以下 Python 代码生成全面的测试:

```python
{context.python_code}
```

要求:
1. 单元测试 (pytest):
   - 测试所有 public 方法
   - 使用 fixtures 和 parametrize

2. 属性测试 (Hypothesis):
   - 使用 property-based testing
   - 自动生成测试数据

3. 突变测试 (mutmut):
   - 确保测试能发现代码变异

4. 安全测试:
   - SQL 注入测试
   - XSS 测试
   - 输入验证测试

5. 性能测试:
   - 使用 pytest-benchmark
   - 设置性能基线

6. 覆盖率: > 90%

只返回测试代码,用 ```python 包裹:
"""
```

### 🎛️ 可调整参数

| 参数 | 位置 | 作用 | 推荐值 |
|------|------|------|--------|
| **temperature** | `llm.complete()` | 控制输出随机性 | 0.1-0.3（测试生成需要确定性） |
| **system prompt** | `llm.complete()` | 设定 LLM 角色 | "你是测试工程师..." |
| **测试框架** | prompt 第 1 条 | 选择测试框架 | pytest / unittest / nose2 |
| **覆盖率要求** | prompt 最后 | 测试覆盖率目标 | 80% / 90% / 95% |
| **测试类型** | prompt 内容 | 测试的种类 | 单元/集成/端到端/性能 |

### 💡 高级技巧

#### 1. 根据代码类型定制测试策略

```python
def process(self, context: AgentContext) -> AgentContext:
    """生成测试代码"""

    # 分析代码类型
    code_type = self._analyze_code_type(context.python_code)

    if code_type == "data_class":
        # 数据类：简单测试
        requirements = "测试属性访问、相等性、序列化"
        coverage = 80
    elif code_type == "service_class":
        # 服务类：全面测试
        requirements = "测试业务逻辑、异常处理、边界条件、mock 依赖"
        coverage = 95
    elif code_type == "util_class":
        # 工具类：属性测试
        requirements = "使用 Hypothesis 进行属性测试、边界条件"
        coverage = 90

    prompt = f"""
为以下 {code_type} 生成测试:

代码:
```python
{context.python_code}
```

测试要求: {requirements}
覆盖率: > {coverage}%
"""
```

#### 2. 动态调整测试数量

```python
# 根据代码行数调整测试详细程度
code_lines = context.python_code.count('\n')

if code_lines < 50:
    test_detail = "每个方法 2-3 个测试用例"
elif code_lines < 200:
    test_detail = "每个方法 3-5 个测试用例"
else:
    test_detail = "每个方法 5-10 个测试用例，包含复杂场景"

prompt = f"""
生成测试，测试详细程度: {test_detail}
"""
```

### 📂 修改后的测试输出位置

生成的测试代码会保存到：
- **上下文中**：`context.test_code`
- **文件输出**：`output/strict_mode/test_generated.py`（通过 demo_costrict.py）

---

## 4. 如果我想更改LLM，我应该调整哪个文件里的代码？

### ✅ 答案：有两个地方可以修改

### 方法 1: 在演示文件中修改（推荐）⭐

**适用场景**：临时切换 LLM、测试不同模型

**文件位置**：[demo_costrict.py:80-85](demo_costrict.py#L80-L85)

```python
def demo_strict_mode():
    """演示严格模式"""

    # 创建 LLM (使用 Ollama)
    try:
        # 🎯 修改这里 - 切换 LLM

        # 【当前配置】使用 Ollama codellama
        provider = create_llm_provider("ollama", model="codellama")

        # 【选项 1】改为 OpenAI GPT-4
        # provider = create_llm_provider(
        #     "openai",
        #     model="gpt-4-turbo-preview"
        # )

        # 【选项 2】改为 Anthropic Claude
        # provider = create_llm_provider(
        #     "anthropic",
        #     model="claude-3-5-sonnet-20241022"
        # )

        # 【选项 3】改为其他 Ollama 模型
        # provider = create_llm_provider("ollama", model="llama2")
        # provider = create_llm_provider("ollama", model="mistral")
        # provider = create_llm_provider("ollama", model="qwen2.5-coder")

        # 【选项 4】使用 Mock（测试用，不调用真实 LLM）
        # provider = create_llm_provider("mock")

        print("\n✓ 使用 Ollama (codellama) - 本地 LLM")

    except Exception as e:
        print(f"\n⚠️ LLM 连接失败: {e}")
        print("使用 Mock 模式")
        provider = create_llm_provider("mock")

    # 创建编排器
    orchestrator = StrictModeOrchestrator(provider, enable_all_phases=True)

    # 执行迁移
    results = orchestrator.migrate_strict(java_code, skip_tests=False)
```

### 方法 2: 在 LLM 提供者文件中添加新 LLM

**适用场景**：永久添加新的 LLM 支持

**文件位置**：[src/llm_providers.py](src/llm_providers.py)

#### 步骤 1: 创建新的 LLM 提供者类

```python
# src/llm_providers.py

class YourCustomLLMProvider(LLMProvider):
    """自定义 LLM 提供者"""

    def __init__(self, api_key: str, model: str = "your-model",
                 base_url: Optional[str] = None):
        """
        初始化自定义 LLM

        Args:
            api_key: API 密钥
            model: 模型名称
            base_url: API 基础 URL
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://api.yourllm.com/v1"

    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """调用你的 LLM API"""
        try:
            import requests

            # 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system or "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # 发送请求
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )

            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']

        except Exception as e:
            raise RuntimeError(f"自定义 LLM API 调用失败: {str(e)}")
```

#### 步骤 2: 在工厂函数中注册

```python
# src/llm_providers.py

def create_llm_provider(provider_type: str, **kwargs) -> LLMProvider:
    """
    工厂函数 - 创建 LLM 提供者

    支持的类型:
    - "openai": OpenAI GPT-4
    - "anthropic": Anthropic Claude
    - "ollama": 本地 Ollama
    - "mock": 模拟 LLM (测试用)
    - "custom": 自定义 LLM  # ← 新增

    Args:
        provider_type: 提供者类型
        **kwargs: 传递给提供者的参数

    Returns:
        LLMProvider 实例
    """
    if provider_type == "openai":
        return OpenAIProvider(**kwargs)

    elif provider_type == "anthropic":
        return AnthropicProvider(**kwargs)

    elif provider_type == "ollama":
        return OllamaProvider(**kwargs)

    elif provider_type == "mock":
        return MockLLMProvider()

    elif provider_type == "custom":  # ← 新增
        return YourCustomLLMProvider(**kwargs)

    else:
        raise ValueError(f"未知的 LLM 提供者类型: {provider_type}")
```

#### 步骤 3: 使用新的 LLM

```python
# demo_costrict.py

# 使用自定义 LLM
provider = create_llm_provider(
    "custom",
    api_key="your-api-key",
    model="your-model-name",
    base_url="https://api.yourllm.com/v1"  # 可选
)

orchestrator = StrictModeOrchestrator(provider)
```

### 📋 已支持的 LLM 列表

当前无需修改代码即可使用的 LLM：

| 提供者 | 模型示例 | 使用方式 | 成本 | 质量 |
|--------|---------|---------|------|------|
| **OpenAI** | gpt-4-turbo-preview<br>gpt-4<br>gpt-3.5-turbo | `create_llm_provider("openai", model="gpt-4-turbo-preview")` | $$ 高 | ⭐⭐⭐⭐⭐ |
| **Anthropic** | claude-3-5-sonnet-20241022<br>claude-3-opus<br>claude-3-sonnet | `create_llm_provider("anthropic", model="claude-3-5-sonnet-20241022")` | $$ 中高 | ⭐⭐⭐⭐⭐ |
| **Ollama** | codellama<br>llama2<br>mistral<br>qwen2.5-coder | `create_llm_provider("ollama", model="codellama")` | 💰 **免费** | ⭐⭐⭐⭐ |
| **Mock** | 模拟 LLM | `create_llm_provider("mock")` | 💰 **免费** | ⭐⭐ (仅测试) |

### 🔧 配置示例

#### OpenAI GPT-4（最高质量）

```python
import os

# 方式 1: 从环境变量读取
os.environ['OPENAI_API_KEY'] = 'sk-...'
provider = create_llm_provider("openai", model="gpt-4-turbo-preview")

# 方式 2: 直接传入
provider = create_llm_provider(
    "openai",
    api_key="sk-...",
    model="gpt-4-turbo-preview",
    base_url="https://api.openai.com/v1"  # 可选，用于代理
)
```

#### Anthropic Claude（高质量，上下文长）

```python
import os

# 方式 1: 从环境变量读取
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'
provider = create_llm_provider("anthropic")

# 方式 2: 直接传入
provider = create_llm_provider(
    "anthropic",
    api_key="sk-ant-...",
    model="claude-3-5-sonnet-20241022"
)
```

#### Ollama（本地免费）

```bash
# 1. 安装 Ollama
curl https://ollama.ai/install.sh | sh

# 2. 下载模型
ollama pull codellama      # 代码专用，最推荐
ollama pull llama2         # 通用模型
ollama pull mistral        # 轻量高效
ollama pull qwen2.5-coder  # 中文友好的代码模型

# 3. 启动服务
ollama serve
```

```python
# 使用 Ollama
provider = create_llm_provider(
    "ollama",
    model="codellama",
    base_url="http://localhost:11434"  # 默认值
)
```

### 🎯 选择建议

| 场景 | 推荐 LLM | 理由 |
|------|---------|------|
| **企业生产环境** | GPT-4 Turbo | 质量最高、稳定性好 |
| **成本敏感** | Ollama (codellama) | 完全免费、本地运行 |
| **长文本处理** | Claude 3.5 Sonnet | 上下文窗口大（200K tokens） |
| **快速原型** | GPT-3.5 Turbo | 速度快、成本低 |
| **数据隐私** | Ollama (本地) | 数据不出本地 |
| **中文友好** | Qwen2.5-Coder (Ollama) | 专为中文优化 |
| **测试调试** | Mock | 无需 API、即时响应 |

### ⚙️ 高级配置

#### 1. 使用代理

```python
# OpenAI with proxy
provider = create_llm_provider(
    "openai",
    api_key="sk-...",
    base_url="https://your-proxy.com/v1"  # 代理地址
)
```

#### 2. 调整温度参数

```python
# 在 Agent 中调整
response = self.llm.complete(
    prompt,
    system="...",
    temperature=0.1  # 0=确定性, 1=创造性
)

# 代码生成: 0.2-0.3
# 测试生成: 0.1-0.2
# 代码审查: 0.1
# 创意任务: 0.7-0.9
```

#### 3. 切换不同阶段使用不同 LLM

```python
class StrictModeOrchestrator:
    def __init__(self, primary_llm: LLMProvider,
                 review_llm: Optional[LLMProvider] = None):
        """
        Args:
            primary_llm: 主要 LLM (用于生成)
            review_llm: 审查 LLM (用于审查，可以用更强的模型)
        """
        self.primary_llm = primary_llm
        self.review_llm = review_llm or primary_llm

        # 大多数 Agent 用主要 LLM
        self.agents = {
            AgentPhase.CODE_GENERATION: CodeGenerationAgent(primary_llm),
            # ...

            # 审查 Agent 用更强的 LLM
            AgentPhase.CODE_REVIEW: CodeReviewAgent(self.review_llm)
        }

# 使用示例
primary = create_llm_provider("ollama", model="codellama")  # 免费
review = create_llm_provider("openai", model="gpt-4")       # 高质量

orchestrator = StrictModeOrchestrator(primary, review)
```

---

## 5. 项目文件清单

### 📁 完整文件列表（按目录组织）

#### 📂 根目录文件 (13个)

**Python 演示文件 (3个)**
1. [demo.py](demo.py) - 基础演示（传统模式 + Agent 模式）
2. [demo_intelligent.py](demo_intelligent.py) - 智能迁移演示（规则 vs 语义 vs 混合）
3. **[demo_costrict.py](demo_costrict.py)** - **Costrict 严格模式演示** ⭐

**Python 辅助文件 (2个)**
4. [debug_init.py](debug_init.py) - 调试初始化脚本
5. [test_fix.py](test_fix.py) - 测试修复脚本

**文档文件 (7个)**
6. [README.md](README.md) - 项目主文档
7. [USER_GUIDE.md](USER_GUIDE.md) - 用户使用指南
8. [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - 优化总结
9. [SEMANTIC_IMPLEMENTATION_SUMMARY.md](SEMANTIC_IMPLEMENTATION_SUMMARY.md) - 语义理解实现总结
10. [INTELLIGENT_MIGRATION_GUIDE.md](INTELLIGENT_MIGRATION_GUIDE.md) - 智能迁移指南
11. [AGENT_COMPARISON.md](AGENT_COMPARISON.md) - Agent 方案对比
12. **[COSTRICT_IMPLEMENTATION_SUMMARY.md](COSTRICT_IMPLEMENTATION_SUMMARY.md)** - **Costrict 实现总结** ⭐
13. **[FAQ.md](FAQ.md)** - **本文档（常见问题解答）** ⭐

**配置文件 (1个)**
14. [requirements.txt](requirements.txt) - Python 依赖清单

---

#### 📂 src/ 目录 (17个核心源代码)

**基础模块 (6个)**
15. [src/__init__.py](src/__init__.py) - 包初始化
16. [src/logger.py](src/logger.py) - 统一日志系统
17. [src/config.py](src/config.py) - 配置管理
18. [src/ast_parser.py](src/ast_parser.py) - Java AST 解析器
19. [src/semantic_mapper.py](src/semantic_mapper.py) - 语义映射器
20. [src/code_generater.py](src/code_generater.py) - Python 代码生成器

**规划和验证 (3个)**
21. [src/migration_planner.py](src/migration_planner.py) - 迁移计划器
22. [src/validator.py](src/validator.py) - 迁移验证器
23. [src/visualizer.py](src/visualizer.py) - 可视化工具

**主程序 (1个)**
24. [src/main.py](src/main.py) - CLI 命令行入口程序

**Agent 系统 - 旧版 (3个)**
25. [src/agents.py](src/agents.py) - 基础 Agent 框架（工作流编排）
26. [src/semantic_agents.py](src/semantic_agents.py) - 语义理解 Agent（3阶段）
27. [src/intelligent_migrator.py](src/intelligent_migrator.py) - 智能迁移器（混合模式）

**Costrict Agent 系统 - 新版 (2个) ⭐**
28. **[src/costrict_agents.py](src/costrict_agents.py)** - **6个专业 Agent（520行）** ⭐
29. **[src/costrict_orchestrator.py](src/costrict_orchestrator.py)** - **严格模式编排器（260行）** ⭐

**LLM 支持 (1个)**
30. [src/llm_providers.py](src/llm_providers.py) - LLM 提供者抽象层

---

#### 📂 test/ 目录 (2个测试文件)
31. [test/test_conversion.py](test/test_conversion.py) - 基础转换测试
32. [test/test_advanced.py](test/test_advanced.py) - 高级功能测试

---

#### 📂 example/ 目录 (4个示例文件)
33. [example/Calculator.java](example/Calculator.java) - 示例 Java 代码
34. [example/Calculator.py](example/Calculator.py) - 转换后的 Python 代码
35. [example/Person.py](example/Person.py) - 另一个 Python 示例
36. [example/migration_plan.md](example/migration_plan.md) - 迁移计划示例

---

#### 📂 output/ 目录 (3个输出文件)
37. [output/strict_mode/generated.py](output/strict_mode/generated.py) - Costrict 生成的 Python 代码
38. [output/strict_mode/test_generated.py](output/strict_mode/test_generated.py) - Costrict 生成的测试代码
39. `output/strict_mode/report.json` - 详细迁移报告（JSON格式）

---

### 📊 文件统计汇总

| 类别 | 数量 | 说明 |
|------|------|------|
| **Python 源代码** | 17 | src/ 目录下的核心模块 |
| **演示脚本** | 3 | demo.py, demo_intelligent.py, demo_costrict.py |
| **测试文件** | 2 | test/ 目录 |
| **文档** | 7 | Markdown 文档 |
| **示例** | 4 | example/ 目录 |
| **输出** | 3 | output/strict_mode/ 目录 |
| **配置** | 1 | requirements.txt |
| **总计** | **39** | 所有项目文件（含本文档） |

---

### 🌟 核心文件重点说明

#### Costrict 风格核心文件（最新实现）⭐
- **[src/costrict_agents.py](src/costrict_agents.py)** - 6个专业Agent（520行）
  - RequirementsAnalysisAgent（需求分析）
  - ArchitectureDesignAgent（架构设计）
  - TaskPlanningAgent（任务规划）
  - CodeGenerationAgent（代码生成）
  - TestGenerationAgent（测试生成）
  - CodeReviewAgent（代码审查）

- **[src/costrict_orchestrator.py](src/costrict_orchestrator.py)** - 编排器（260行）
  - 严格模式（6阶段）
  - 快速模式（3阶段）
  - 质量评分系统
  - 报告导出

- **[demo_costrict.py](demo_costrict.py)** - 完整演示（340行）
  - 严格模式演示
  - 快速模式演示
  - 两种模式对比

- **[COSTRICT_IMPLEMENTATION_SUMMARY.md](COSTRICT_IMPLEMENTATION_SUMMARY.md)** - 详细文档（28KB）
  - 完整实现说明
  - 架构设计
  - 使用指南

#### 智能迁移核心文件（前期实现）
- **[src/intelligent_migrator.py](src/intelligent_migrator.py)** - 混合模式迁移器
- **[src/semantic_agents.py](src/semantic_agents.py)** - 语义理解Agent（3阶段）
- **[src/llm_providers.py](src/llm_providers.py)** - LLM抽象层（支持4种LLM）

#### 基础设施文件
- **[src/main.py](src/main.py)** - CLI 入口程序
- **[src/logger.py](src/logger.py)** - 统一日志系统
- **[src/ast_parser.py](src/ast_parser.py)** - Java AST 解析器
- **[src/config.py](src/config.py)** - 配置管理
- **[src/validator.py](src/validator.py)** - 迁移验证器

---

### 📂 目录结构树

```
j2p_migration/
│
├─── 📄 README.md                               # 项目主文档
├─── 📄 USER_GUIDE.md                           # 用户指南
├─── 📄 OPTIMIZATION_SUMMARY.md                 # 优化总结
├─── 📄 SEMANTIC_IMPLEMENTATION_SUMMARY.md      # 语义实现总结
├─── 📄 INTELLIGENT_MIGRATION_GUIDE.md          # 智能迁移指南
├─── 📄 AGENT_COMPARISON.md                     # Agent 对比
├─── 📄 COSTRICT_IMPLEMENTATION_SUMMARY.md      # Costrict 实现总结 ⭐
├─── 📄 FAQ.md                                  # 本文档 ⭐
│
├─── 🐍 demo.py                                 # 基础演示
├─── 🐍 demo_intelligent.py                     # 智能迁移演示
├─── 🐍 demo_costrict.py                        # Costrict 演示 ⭐
├─── 🐍 debug_init.py                           # 调试脚本
├─── 🐍 test_fix.py                             # 测试修复
│
├─── ⚙️ requirements.txt                         # 依赖清单
│
├─── 📂 src/                                    # 核心源代码
│    ├─── __init__.py
│    ├─── logger.py                            # 日志系统
│    ├─── config.py                            # 配置管理
│    ├─── ast_parser.py                        # Java 解析
│    ├─── semantic_mapper.py                   # 语义映射
│    ├─── code_generater.py                    # 代码生成
│    ├─── migration_planner.py                 # 迁移规划
│    ├─── validator.py                         # 验证器
│    ├─── visualizer.py                        # 可视化
│    ├─── main.py                              # CLI 入口
│    │
│    ├─── agents.py                            # 基础 Agent
│    ├─── semantic_agents.py                   # 语义 Agent
│    ├─── intelligent_migrator.py              # 智能迁移器
│    │
│    ├─── costrict_agents.py                   # 6个专业 Agent ⭐
│    ├─── costrict_orchestrator.py             # 编排器 ⭐
│    └─── llm_providers.py                     # LLM 抽象层
│
├─── 📂 test/                                   # 测试文件
│    ├─── test_conversion.py                   # 基础测试
│    └─── test_advanced.py                     # 高级测试
│
├─── 📂 example/                                # 示例文件
│    ├─── Calculator.java                      # Java 示例
│    ├─── Calculator.py                        # Python 示例
│    ├─── Person.py                            # 另一个示例
│    └─── migration_plan.md                    # 计划示例
│
└─── 📂 output/                                 # 输出目录
     └─── strict_mode/
          ├─── generated.py                    # 生成的代码 ⭐
          ├─── test_generated.py               # 生成的测试 ⭐
          └─── report.json                     # 迁移报告
```

---

### 🔍 快速查找指南

| 我想... | 查看这个文件 |
|---------|-------------|
| 了解项目概况 | [README.md](README.md) |
| 学习如何使用 | [USER_GUIDE.md](USER_GUIDE.md) |
| 了解 Costrict 实现 | [COSTRICT_IMPLEMENTATION_SUMMARY.md](COSTRICT_IMPLEMENTATION_SUMMARY.md) ⭐ |
| 查看常见问题 | [FAQ.md](FAQ.md) ⭐ |
| 运行演示 | [demo_costrict.py](demo_costrict.py) ⭐ |
| 修改测试生成策略 | [src/costrict_agents.py](src/costrict_agents.py) |
| 切换 LLM | [demo_costrict.py](demo_costrict.py) 或 [src/llm_providers.py](src/llm_providers.py) |
| 查看生成的代码 | [output/strict_mode/generated.py](output/strict_mode/generated.py) |
| 查看生成的测试 | [output/strict_mode/test_generated.py](output/strict_mode/test_generated.py) |
| 查看迁移报告 | `output/strict_mode/report.json` |
| 修改日志输出 | [src/logger.py](src/logger.py) |
| 修改配置 | [src/config.py](src/config.py) |
| 添加新功能 | [src/costrict_agents.py](src/costrict_agents.py) 或 [src/costrict_orchestrator.py](src/costrict_orchestrator.py) |

---

## 📚 相关文档链接

- [README.md](README.md) - 项目总览
- [COSTRICT_IMPLEMENTATION_SUMMARY.md](COSTRICT_IMPLEMENTATION_SUMMARY.md) - Costrict 详细实现 ⭐
- [INTELLIGENT_MIGRATION_GUIDE.md](INTELLIGENT_MIGRATION_GUIDE.md) - 智能迁移使用指南
- [AGENT_COMPARISON.md](AGENT_COMPARISON.md) - Agent 方案技术对比
- [USER_GUIDE.md](USER_GUIDE.md) - 通用用户指南

---

## ❓ 还有其他问题？

如果本文档没有回答您的问题，请：

1. 查看 [COSTRICT_IMPLEMENTATION_SUMMARY.md](COSTRICT_IMPLEMENTATION_SUMMARY.md) 了解详细实现
2. 查看源代码注释（代码中有详细的 docstring）
3. 运行 `python demo_costrict.py` 查看实际效果
4. 查看生成的报告 `output/strict_mode/report.json`

---

**文档版本**: 1.0
**最后更新**: 2025-12-27
**维护者**: Costrict 风格 Agent 系统开发团队

**享受智能代码迁移! 🎉**
