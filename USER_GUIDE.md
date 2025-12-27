# Java to Python 迁移工具 - 使用指南

## 📖 目录

1. [快速开始](#快速开始)
2. [功能特性](#功能特性)
3. [安装配置](#安装配置)
4. [使用方式](#使用方式)
5. [高级功能](#高级功能)
6. [API 参考](#api-参考)
7. [常见问题](#常见问题)

---

## 🚀 快速开始

### 基本使用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 迁移单个文件
python src/main.py -i Example.java -o example.py

# 3. 查看帮助
python src/main.py --help
```

### 运行演示

```bash
# 运行完整演示(包括传统模式、Agent 模式和可视化)
python demo.py
```

---

## ✨ 功能特性

### 核心功能

✅ **完整的代码结构转换**
- 类定义和继承关系
- 方法和构造函数
- 字段和属性
- 静态成员和常量

✅ **智能类型映射**
- 基本类型转换 (int, String, boolean → int, str, bool)
- 泛型类型转换 (List<String> → List[str])
- 数组类型转换 (int[] → List[int])

✅ **Python 命名规范**
- 驼峰命名 → snake_case (getUserName → get_user_name)
- 常量大写 (MAX_SIZE)
- 私有方法下划线前缀 (_private_method)

✅ **代码验证**
- 语法检查
- 结构完整性验证
- 命名规范检查
- 类型注解验证

### 新增功能

🆕 **统一日志系统**
- 彩色控制台输出
- 多级别日志 (DEBUG, INFO, WARNING, ERROR, SUCCESS)
- 详细错误追踪

🆕 **配置管理**
- JSON 配置文件支持
- 灵活的配置选项
- 配置合并功能

🆕 **可视化增强**
- 详细的迁移计划展示
- 进度追踪
- 导出为 JSON/Markdown

🆕 **Agent 架构**
- 模块化的 Agent 设计
- 灵活的编排机制
- 状态追踪和错误恢复

---

## 🔧 安装配置

### 系统要求

- Python 3.7+
- 支持 Windows, Linux, macOS

### 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖说明

```
javalang==0.13.0      # Java 代码解析
pytest>=7.3.0         # 测试框架
flake8>=6.0.0         # 代码检查(可选)
pylint>=2.17.0        # 代码分析(可选)
black>=23.0.0         # 代码格式化(可选)
```

---

## 📚 使用方式

### 1. 命令行工具 (CLI)

#### 基本迁移

```bash
# 迁移文件并输出到控制台
python src/main.py -i Example.java

# 迁移文件并保存
python src/main.py -i Example.java -o example.py

# 详细模式
python src/main.py -i Example.java -o example.py -v
```

#### 查看迁移计划

```bash
# 显示迁移计划
python src/main.py -i Example.java --show-plan

# 导出计划为 JSON
python src/main.py -i Example.java --show-plan --export-plan plan.json

# 导出计划为 Markdown
python src/main.py -i Example.java --show-plan --export-plan plan.md
```

#### 使用 Agent 模式

```bash
# 使用 Agent 编排器执行迁移
python src/main.py -i Example.java -o example.py --use-agents
```

#### 其他选项

```bash
# 跳过验证
python src/main.py -i Example.java -o example.py --no-validate

# 禁用彩色输出
python src/main.py -i Example.java --no-color

# 显示版本
python src/main.py --version
```

### 2. Python API

#### 传统模式

```python
from main import JavaToPythonMigrator

# 创建迁移器
migrator = JavaToPythonMigrator(verbose=True)

# 从字符串迁移
java_code = """
public class Example {
    private int value;

    public Example(int value) {
        this.value = value;
    }
}
"""

result = migrator.migrate(java_code, show_plan=True, validate=True)

if result['success']:
    print(result['python_code'])
else:
    print("Errors:", result['errors'])

# 从文件迁移
success = migrator.migrate_file(
    input_file='Example.java',
    output_file='example.py',
    show_plan=True,
    validate=True
)
```

#### Agent 模式

```python
from agents import MigrationOrchestrator
from logger import get_logger

# 创建日志器
logger = get_logger(verbose=True, use_color=True)

# 创建编排器
orchestrator = MigrationOrchestrator()
orchestrator.set_logger(logger)

# 执行迁移
java_code = "public class Test { }"
result = orchestrator.orchestrate_migration(java_code, validate=True)

# 检查结果
if result['success']:
    print(result['python_code'])

    # 查看 Agent 状态
    statuses = orchestrator.get_agent_statuses()
    print("Agent 状态:", statuses)
```

#### 使用单独模块

```python
# 1. 解析
from ast_parser import JavaASTParser

parser = JavaASTParser()
java_structure = parser.get_full_structure(java_code)

# 2. 规划
from migration_planner import MigrationPlanner

planner = MigrationPlanner()
plan = planner.plan_migration(java_structure)
planner.print_plan(plan)

# 3. 映射
from semantic_mapper import SemanticMapper

mapper = SemanticMapper()
python_structure = mapper.map_structure(java_structure)

# 4. 生成
from code_generater import PythonCodeGenerator

generator = PythonCodeGenerator()
python_code = generator.generate_code(python_structure)
python_code = generator.format_code(python_code)

# 5. 验证
from validator import MigrationValidator

validator = MigrationValidator()
report = validator.validate_migration(java_code, python_code, python_structure)
validator.print_report(report)
```

---

## 🎓 高级功能

### 配置文件

创建配置文件 `config.json`:

```json
{
  "verbose": true,
  "use_color": true,
  "indent_size": 4,
  "max_line_length": 100,
  "add_type_hints": true,
  "add_docstrings": true,
  "run_validation": true,
  "run_static_analysis": false,
  "show_plan": true,
  "custom_type_mapping": {
    "BigDecimal": "Decimal"
  }
}
```

使用配置文件:

```python
from config import MigrationConfig

# 从文件加载
config = MigrationConfig.from_file('config.json')

# 或手动创建
config = MigrationConfig(
    verbose=True,
    indent_size=2,
    add_type_hints=True
)

# 保存配置
config.save_to_file('my_config.json')
```

### 可视化工具

```python
from visualizer import MigrationVisualizer, VisualizationOptions

# 创建可视化器
options = VisualizationOptions(
    show_progress_bar=True,
    show_step_details=True,
    use_colors=True
)

visualizer = MigrationVisualizer(options)

# 显示计划
visualizer.print_plan_summary(plan)

# 追踪进度
visualizer.start_migration()
visualizer.print_progress(1, 5, "解析 Java 代码")
# ... 执行迁移步骤
visualizer.end_migration(success=True)

# 导出
visualizer.export_plan_to_json(plan, 'plan.json')
visualizer.export_plan_to_markdown(plan, 'plan.md')
```

### 自定义 Agent

```python
from agents import BaseAgent, AgentResult, AgentStatus

class CustomAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("CustomAgent", config)

    def validate_input(self, input_data):
        # 验证输入
        return True

    def execute(self, input_data):
        self.status = AgentStatus.RUNNING
        self.log_info("执行自定义任务")

        try:
            # 执行任务逻辑
            output = self.process(input_data)

            self.status = AgentStatus.SUCCESS
            return AgentResult(
                status=AgentStatus.SUCCESS,
                output=output,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )
        except Exception as e:
            self.log_error(str(e))
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )

    def process(self, input_data):
        # 实现处理逻辑
        return input_data
```

---

## 📖 API 参考

### JavaASTParser

解析 Java 代码并提取结构信息。

```python
parser = JavaASTParser()

# 解析代码
ast_tree = parser.parse_java_code(java_code)

# 提取结构
structure = parser.get_full_structure(java_code)
```

### SemanticMapper

将 Java 语义映射为 Python 等价语义。

```python
mapper = SemanticMapper()

# 映射类型
python_type = mapper.map_type('String')  # 'str'

# 映射结构
python_structure = mapper.map_structure(java_structure)
```

### MigrationPlanner

生成迁移计划和建议。

```python
planner = MigrationPlanner()

# 生成计划
plan = planner.plan_migration(java_structure)

# 显示计划
planner.print_plan(plan)
```

### PythonCodeGenerator

生成格式化的 Python 代码。

```python
generator = PythonCodeGenerator(indent_size=4)

# 生成代码
code = generator.generate_code(python_structure)

# 格式化
formatted = generator.format_code(code)

# 保存
generator.save_to_file(code, 'output.py')
```

### MigrationValidator

验证迁移结果的质量。

```python
validator = MigrationValidator()

# 验证
report = validator.validate_migration(java_code, python_code, python_structure)

# 显示报告
validator.print_report(report)
```

---

## ❓ 常见问题

### Q1: 如何处理编码问题?

**A:** 在 Windows 上可能遇到 GBK 编码问题,demo.py 已经包含了解决方案:

```python
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

### Q2: 生成的代码需要手动修改吗?

**A:** 是的,当前版本主要转换类结构、方法签名和类型,方法体需要手动实现或进一步开发。

### Q3: 支持批量迁移吗?

**A:** 当前版本支持单文件迁移,批量迁移可以通过脚本实现:

```bash
for file in *.java; do
    python src/main.py -i "$file" -o "${file%.java}.py"
done
```

### Q4: 如何自定义类型映射?

**A:** 使用配置文件或直接修改 SemanticMapper:

```python
mapper = SemanticMapper()
mapper.TYPE_MAPPING['CustomType'] = 'MyPythonType'
```

### Q5: 测试失败怎么办?

**A:** 确保安装了所有依赖:

```bash
pip install -r requirements.txt
pytest test/ -v
```

---

## 📞 获取帮助

- 查看文档: [README.md](README.md)
- 优化总结: [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)
- 提交问题: 在项目 issues 中反馈

---

## 📄 许可证

MIT License - 详见项目根目录 LICENSE 文件

---

**享受使用 Java to Python 迁移工具! 🎉**
