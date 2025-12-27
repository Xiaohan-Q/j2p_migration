"""
LLM 提供者实现
支持多种 LLM 后端: OpenAI, Anthropic, 本地 Ollama
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
import json
import re


class LLMProvider(ABC):
    """LLM 提供者抽象基类"""

    @abstractmethod
    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """
        调用 LLM 生成补全

        Args:
            prompt: 用户提示
            system: 系统提示
            temperature: 温度参数 (0-1, 越低越确定)
            max_tokens: 最大生成 token 数

        Returns:
            LLM 生成的文本
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API 提供者"""

    def __init__(self, api_key: Optional[str] = None,
                 model: str = "gpt-4-turbo-preview",
                 base_url: Optional[str] = None):
        """
        初始化 OpenAI 提供者

        Args:
            api_key: API 密钥 (可从环境变量 OPENAI_API_KEY 读取)
            model: 模型名称
            base_url: API 基础 URL (可用于代理)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("需要提供 OpenAI API key 或设置 OPENAI_API_KEY 环境变量")

        self.model = model
        self.base_url = base_url

    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """调用 OpenAI API"""
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except ImportError:
            raise ImportError("请安装 OpenAI SDK: pip install openai")
        except Exception as e:
            raise RuntimeError(f"OpenAI API 调用失败: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API 提供者"""

    def __init__(self, api_key: Optional[str] = None,
                 model: str = "claude-3-5-sonnet-20241022"):
        """
        初始化 Anthropic 提供者

        Args:
            api_key: API 密钥 (可从环境变量 ANTHROPIC_API_KEY 读取)
            model: 模型名称
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("需要提供 Anthropic API key 或设置 ANTHROPIC_API_KEY 环境变量")

        self.model = model

    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """调用 Anthropic API"""
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system if system else "You are a helpful assistant.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except ImportError:
            raise ImportError("请安装 Anthropic SDK: pip install anthropic")
        except Exception as e:
            raise RuntimeError(f"Anthropic API 调用失败: {str(e)}")


class OllamaProvider(LLMProvider):
    """Ollama 本地模型提供者 (免费)"""

    def __init__(self, model: str = "codellama",
                 base_url: str = "http://localhost:11434"):
        """
        初始化 Ollama 提供者

        Args:
            model: 模型名称 (如 codellama, llama2, mistral)
            base_url: Ollama 服务地址
        """
        self.model = model
        self.base_url = base_url

    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """调用 Ollama API"""
        try:
            import requests

            # 构建完整提示
            full_prompt = prompt
            if system:
                full_prompt = f"{system}\n\n{prompt}"

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()
            return response.json()['response']

        except ImportError:
            raise ImportError("请安装 requests: pip install requests")
        except Exception as e:
            raise RuntimeError(f"Ollama API 调用失败: {str(e)}\n"
                             f"请确保 Ollama 已启动: ollama serve")


class MockLLMProvider(LLMProvider):
    """模拟 LLM 提供者 (用于测试,不需要 API key)"""

    def complete(self, prompt: str, system: Optional[str] = None,
                 temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """返回模拟响应"""

        # 简单的模拟逻辑
        if "业务逻辑" in prompt or "business" in prompt.lower():
            return json.dumps({
                "business_purpose": "用户管理和验证",
                "key_concepts": ["User", "Email validation", "Repository pattern"],
                "design_patterns": ["Repository Pattern"],
                "dependencies": ["UserRepository", "Date"],
                "side_effects": ["Database write"],
                "complexity": "中等"
            }, ensure_ascii=False)

        elif "```java" in prompt and "Python" in prompt:
            # 提取 Java 代码
            java_match = re.search(r'```java\n(.*?)\n```', prompt, re.DOTALL)
            if java_match:
                return '''```python
from datetime import datetime
from typing import Optional

class UserService:
    """用户服务类 - 处理用户创建和验证"""

    def __init__(self, repository):
        self._repository = repository

    def create_user(self, email: str, name: str):
        """创建新用户"""
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")

        user = User(email=email, name=name)
        user.created_at = datetime.now()

        return self._repository.save(user)

    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        return email is not None and '@' in email
```'''

        else:
            return "模拟 LLM 响应"


def create_llm_provider(provider_type: str = "mock", **kwargs) -> LLMProvider:
    """
    工厂方法创建 LLM 提供者

    Args:
        provider_type: 提供者类型 (openai, anthropic, ollama, mock)
        **kwargs: 传递给提供者的参数

    Returns:
        LLM 提供者实例

    Examples:
        >>> # 使用 OpenAI
        >>> provider = create_llm_provider("openai", api_key="sk-...")

        >>> # 使用 Anthropic
        >>> provider = create_llm_provider("anthropic", api_key="sk-ant-...")

        >>> # 使用本地 Ollama (免费)
        >>> provider = create_llm_provider("ollama", model="codellama")

        >>> # 使用 Mock (测试)
        >>> provider = create_llm_provider("mock")
    """
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
        "mock": MockLLMProvider
    }

    if provider_type not in providers:
        raise ValueError(f"未知的提供者类型: {provider_type}")

    return providers[provider_type](**kwargs)


# 使用示例
if __name__ == "__main__":
    # 测试 Mock 提供者
    provider = create_llm_provider("mock")

    response = provider.complete(
        prompt="分析这段 Java 代码的业务逻辑",
        system="你是代码分析专家"
    )

    print("响应:", response)
