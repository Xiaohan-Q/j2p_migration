"""
语义理解 Agent
使用 LLM 进行深度代码理解和智能转换
"""
from typing import Dict, List, Any, Optional
import json
import re
from llm_providers import LLMProvider
from logger import get_logger


class SemanticAnalyzer:
    """代码语义分析器"""

    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.logger = get_logger()

    def analyze_business_logic(self, java_code: str) -> Dict[str, Any]:
        """
        分析 Java 代码的业务逻辑

        Args:
            java_code: Java 源代码

        Returns:
            业务分析结果字典
        """
        self.logger.info("🔍 分析业务逻辑...")

        system_prompt = """你是一个资深的代码语义分析专家。
你的任务是深入理解 Java 代码的业务逻辑、设计意图和功能目的。
请以 JSON 格式返回分析结果,确保 JSON 格式正确。"""

        user_prompt = f"""
请分析以下 Java 代码的业务逻辑和语义:

```java
{java_code}
```

请严格按照以下 JSON 格式返回分析结果:
{{
  "business_purpose": "代码的主要业务目的",
  "key_concepts": ["核心概念1", "核心概念2"],
  "design_patterns": ["设计模式1", "设计模式2"],
  "dependencies": ["依赖的类或服务1", "依赖的类或服务2"],
  "side_effects": ["副作用1", "副作用2"],
  "complexity": "简单/中等/复杂",
  "main_operations": ["主要操作1", "主要操作2"]
}}

只返回 JSON,不要有其他文字。
"""

        try:
            response = self.llm.complete(user_prompt, system_prompt, temperature=0.1)

            # 提取 JSON
            analysis = self._extract_json(response)

            self.logger.success(f"✓ 业务目的: {analysis.get('business_purpose', '未知')}")
            self.logger.info(f"  复杂度: {analysis.get('complexity', '未知')}")

            return analysis

        except Exception as e:
            self.logger.error(f"业务逻辑分析失败: {str(e)}")
            return self._default_analysis()

    def analyze_method_semantics(self, method_code: str, method_name: str) -> Dict[str, Any]:
        """
        分析单个方法的语义

        Args:
            method_code: 方法代码
            method_name: 方法名称

        Returns:
            方法语义分析结果
        """
        system_prompt = """你是方法级代码分析专家。
分析方法的执行逻辑、数据流和业务含义。"""

        user_prompt = f"""
分析方法 `{method_name}` 的语义:

```java
{method_code}
```

返回 JSON 格式:
{{
  "purpose": "方法目的",
  "steps": ["步骤1", "步骤2"],
  "key_variables": {{"var1": "用途"}},
  "return_meaning": "返回值含义",
  "exceptions": ["可能的异常"]
}}
"""

        try:
            response = self.llm.complete(user_prompt, system_prompt, temperature=0.1)
            return self._extract_json(response)
        except:
            return {"purpose": "未知", "steps": []}

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """从文本中提取 JSON"""
        # 尝试直接解析
        try:
            return json.loads(text.strip())
        except:
            pass

        # 查找 JSON 代码块
        json_match = re.search(r'```json\s*\n(.*?)\n```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass

        # 查找大括号内容
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        raise ValueError("无法从响应中提取有效的 JSON")

    def _default_analysis(self) -> Dict[str, Any]:
        """返回默认分析结果"""
        return {
            "business_purpose": "未知",
            "key_concepts": [],
            "design_patterns": [],
            "dependencies": [],
            "side_effects": [],
            "complexity": "中等",
            "main_operations": []
        }


class SemanticCodeGenerator:
    """基于语义的代码生成器"""

    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.logger = get_logger()

    def generate_python_code(self, java_code: str,
                            business_context: Dict[str, Any]) -> str:
        """
        生成语义等价的 Python 代码

        Args:
            java_code: Java 源代码
            business_context: 业务上下文分析结果

        Returns:
            生成的 Python 代码
        """
        self.logger.info("🔄 生成语义等价的 Python 代码...")

        system_prompt = """你是一个资深的 Java 到 Python 代码迁移专家。

你的任务是生成语义等价的 Python 代码,而不仅仅是语法转换。

核心原则:
1. 保持业务逻辑完全一致
2. 使用 Pythonic 的惯用法
3. 添加完整的类型注解
4. 编写清晰的文档字符串
5. 实现完整的方法体逻辑
6. 保留设计模式的核心思想
7. 使用合适的 Python 标准库

Pythonic 惯用法示例:
- 使用 @property 而不是 getter/setter
- 使用 with 语句管理资源
- 使用列表推导式和生成器
- 使用 dataclass 简化数据类
- 使用 __init__ 而不是多个构造函数
"""

        user_prompt = f"""
请将以下 Java 代码迁移为高质量的 Python 代码:

原始 Java 代码:
```java
{java_code}
```

业务上下文:
{json.dumps(business_context, indent=2, ensure_ascii=False)}

要求:
1. 生成完整的、可运行的 Python 代码
2. 实现所有方法体的逻辑(不要留 pass 或 TODO)
3. 添加完整的类型注解
4. 添加详细的文档字符串
5. 使用 Python 最佳实践
6. 如果有异常处理,转换为 Python 的异常类型
7. 只返回 Python 代码,用 ```python 包裹

生成 Python 代码:
"""

        try:
            response = self.llm.complete(user_prompt, system_prompt, temperature=0.2)

            # 提取代码
            python_code = self._extract_code(response)

            self.logger.success("✓ Python 代码生成完成")
            return python_code

        except Exception as e:
            self.logger.error(f"代码生成失败: {str(e)}")
            return f"# 代码生成失败: {str(e)}\npass"

    def refactor_to_pythonic(self, python_code: str) -> str:
        """
        将 Python 代码重构为更 Pythonic 的风格

        Args:
            python_code: 原始 Python 代码

        Returns:
            重构后的代码
        """
        system_prompt = """你是 Python 代码重构专家。
将代码重构为更 Pythonic、更优雅的风格。"""

        user_prompt = f"""
将以下 Python 代码重构为更 Pythonic 的风格:

```python
{python_code}
```

重构建议:
1. 使用 @property 替代 getter/setter
2. 使用 dataclass 简化数据类
3. 使用列表推导式
4. 使用 f-string
5. 使用上下文管理器
6. 简化逻辑表达式

只返回重构后的代码:
"""

        try:
            response = self.llm.complete(user_prompt, system_prompt, temperature=0.3)
            return self._extract_code(response)
        except:
            return python_code

    def _extract_code(self, text: str) -> str:
        """从文本中提取代码"""
        # 查找 Python 代码块
        code_match = re.search(r'```python\s*\n(.*?)\n```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # 查找任意代码块
        code_match = re.search(r'```\s*\n(.*?)\n```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # 如果没有代码块标记,返回整个响应
        return text.strip()


class CodeReviewer:
    """代码审查器"""

    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.logger = get_logger()

    def review_migration(self, java_code: str, python_code: str) -> Dict[str, Any]:
        """
        审查迁移结果

        Args:
            java_code: 原始 Java 代码
            python_code: 生成的 Python 代码

        Returns:
            审查报告
        """
        self.logger.info("🔍 审查迁移质量...")

        system_prompt = """你是代码审查专家。
检查 Python 代码是否正确迁移了 Java 代码的语义和逻辑。"""

        user_prompt = f"""
审查代码迁移质量:

原始 Java 代码:
```java
{java_code}
```

生成的 Python 代码:
```python
{python_code}
```

返回 JSON 格式的审查报告:
{{
  "semantic_correctness": "语义是否正确(是/否)",
  "logic_completeness": "逻辑是否完整(是/否)",
  "pythonic_quality": "评分(1-10)",
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"],
  "overall_rating": "评级(优秀/良好/一般/较差)"
}}
"""

        try:
            response = self.llm.complete(user_prompt, system_prompt, temperature=0.1)
            report = self._extract_json(response)

            rating = report.get('overall_rating', '一般')
            self.logger.success(f"✓ 审查完成: {rating}")

            return report

        except Exception as e:
            self.logger.error(f"审查失败: {str(e)}")
            return {
                "semantic_correctness": "未知",
                "logic_completeness": "未知",
                "pythonic_quality": 5,
                "issues": [],
                "suggestions": [],
                "overall_rating": "未知"
            }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """从文本中提取 JSON"""
        try:
            return json.loads(text.strip())
        except:
            pass

        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        return {}


# 使用示例
if __name__ == "__main__":
    from llm_providers import create_llm_provider

    # 使用 Mock 提供者测试
    llm = create_llm_provider("mock")

    # 测试语义分析
    analyzer = SemanticAnalyzer(llm)

    java_code = """
    public class UserService {
        public User createUser(String email, String name) {
            if (!isValidEmail(email)) {
                throw new IllegalArgumentException("Invalid email");
            }
            return new User(email, name);
        }
    }
    """

    analysis = analyzer.analyze_business_logic(java_code)
    print("业务分析:", json.dumps(analysis, indent=2, ensure_ascii=False))
