"""
基于 LLM 的智能代码迁移 Agent
实现真正的语义理解和上下文推理
"""
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import json


class LLMProvider(ABC):
    """LLM 提供者抽象基类"""

    @abstractmethod
    def complete(self, prompt: str, system: str = None) -> str:
        """调用 LLM 生成补全"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API 提供者"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    def complete(self, prompt: str, system: str = None) -> str:
        """调用 OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.2  # 降低随机性,提高一致性
            )

            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM 调用失败: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API 提供者"""

    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model

    def complete(self, prompt: str, system: str = None) -> str:
        """调用 Anthropic API"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system if system else "You are a code migration expert.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"LLM 调用失败: {str(e)}")


class SemanticUnderstandingAgent:
    """基于 LLM 的语义理解 Agent"""

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def understand_business_logic(self, java_code: str) -> Dict[str, Any]:
        """理解代码的业务逻辑"""

        system_prompt = """你是一个代码语义分析专家。
分析给定的 Java 代码,理解其业务逻辑、设计意图和功能目的。
以 JSON 格式返回分析结果。"""

        user_prompt = f"""
请分析以下 Java 代码的业务逻辑:

```java
{java_code}
```

请以 JSON 格式返回分析结果,包含:
1. business_purpose: 代码的业务目的
2. key_concepts: 核心概念和领域术语
3. design_patterns: 使用的设计模式
4. dependencies: 依赖的外部资源或库
5. side_effects: 副作用(IO、状态修改等)
6. complexity: 复杂度评估(简单/中等/复杂)
"""

        response = self.llm.complete(user_prompt, system_prompt)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果 LLM 返回的不是纯 JSON,尝试提取
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("LLM 返回格式错误")

    def generate_semantic_equivalent(self, java_code: str,
                                    business_context: Dict[str, Any]) -> str:
        """生成语义等价的 Python 代码"""

        system_prompt = """你是一个 Java 到 Python 代码迁移专家。
你需要生成语义等价的 Python 代码,不仅仅是语法转换,而是要:
1. 保持业务逻辑完全一致
2. 使用 Pythonic 的惯用法
3. 保留设计模式的核心思想
4. 添加适当的类型注解和文档字符串
"""

        user_prompt = f"""
请将以下 Java 代码迁移为 Python 代码:

原始 Java 代码:
```java
{java_code}
```

业务上下文:
{json.dumps(business_context, indent=2, ensure_ascii=False)}

要求:
1. 保持业务逻辑完全一致
2. 使用 Python 的惯用法(如属性、上下文管理器等)
3. 添加类型注解
4. 添加清晰的文档字符串
5. 如果有设计模式,保留其核心思想
6. 只返回 Python 代码,不要额外解释

请生成 Python 代码:
"""

        response = self.llm.complete(user_prompt, system_prompt)

        # 提取代码块
        import re
        code_match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_match:
            return code_match.group(1)
        else:
            # 如果没有代码块标记,返回整个响应
            return response.strip()

    def analyze_method_body(self, method_code: str) -> Dict[str, Any]:
        """分析方法体的语义"""

        system_prompt = """你是代码逻辑分析专家。
分析方法体的执行逻辑,识别关键步骤和数据流。"""

        user_prompt = f"""
分析以下方法的执行逻辑:

```java
{method_code}
```

以 JSON 格式返回:
1. steps: 执行步骤列表
2. variables: 关键变量及其用途
3. control_flow: 控制流分析
4. return_value: 返回值的含义
"""

        response = self.llm.complete(user_prompt, system_prompt)

        try:
            return json.loads(response)
        except:
            return {"raw_response": response}

    def suggest_improvements(self, python_code: str) -> List[str]:
        """建议代码改进"""

        system_prompt = """你是 Python 代码审查专家。
提供代码改进建议,使其更加 Pythonic 和高效。"""

        user_prompt = f"""
审查以下 Python 代码并提供改进建议:

```python
{python_code}
```

请以列表形式返回具体的改进建议。
"""

        response = self.llm.complete(user_prompt, system_prompt)

        # 简单解析建议列表
        suggestions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or
                        line[0].isdigit() and '.' in line[:3]):
                suggestions.append(line.lstrip('-•0123456789. '))

        return suggestions if suggestions else [response]


class IntelligentMigrationAgent:
    """智能迁移 Agent - 整合语义理解"""

    def __init__(self, llm_provider: LLMProvider):
        self.semantic_agent = SemanticUnderstandingAgent(llm_provider)

    def migrate_with_understanding(self, java_code: str) -> Dict[str, Any]:
        """
        带语义理解的智能迁移

        Returns:
            包含迁移结果和分析信息的字典
        """
        results = {
            'success': False,
            'business_analysis': None,
            'python_code': None,
            'suggestions': [],
            'errors': []
        }

        try:
            # 步骤 1: 理解业务逻辑
            print("🔍 分析业务逻辑...")
            business_context = self.semantic_agent.understand_business_logic(java_code)
            results['business_analysis'] = business_context

            print(f"✓ 业务目的: {business_context.get('business_purpose', '未知')}")
            print(f"✓ 复杂度: {business_context.get('complexity', '未知')}")

            # 步骤 2: 生成语义等价的 Python 代码
            print("\n🔄 生成 Python 代码...")
            python_code = self.semantic_agent.generate_semantic_equivalent(
                java_code,
                business_context
            )
            results['python_code'] = python_code

            # 步骤 3: 提供改进建议
            print("\n💡 分析改进建议...")
            suggestions = self.semantic_agent.suggest_improvements(python_code)
            results['suggestions'] = suggestions

            results['success'] = True

        except Exception as e:
            results['errors'].append(str(e))

        return results


# 使用示例
def demo_intelligent_migration():
    """演示智能迁移"""

    # 配置 LLM (二选一)
    # provider = OpenAIProvider(api_key="your-openai-key")
    provider = AnthropicProvider(api_key="your-anthropic-key")

    # 创建智能 Agent
    agent = IntelligentMigrationAgent(provider)

    # Java 示例代码
    java_code = """
    public class UserService {
        private UserRepository repository;

        public User createUser(String email, String name) {
            if (!isValidEmail(email)) {
                throw new IllegalArgumentException("Invalid email");
            }

            User user = new User(email, name);
            user.setCreatedAt(new Date());

            return repository.save(user);
        }

        private boolean isValidEmail(String email) {
            return email != null && email.contains("@");
        }
    }
    """

    # 执行智能迁移
    result = agent.migrate_with_understanding(java_code)

    if result['success']:
        print("\n" + "="*70)
        print("迁移成功!")
        print("="*70)

        print("\n【业务分析】")
        print(json.dumps(result['business_analysis'], indent=2, ensure_ascii=False))

        print("\n【生成的 Python 代码】")
        print(result['python_code'])

        print("\n【改进建议】")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    else:
        print("迁移失败:", result['errors'])


if __name__ == "__main__":
    demo_intelligent_migration()
