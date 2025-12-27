# 智能语义理解迁移指南

## 🎯 概述

现在你的项目已经支持**真正的智能代码迁移**,具备以下能力:

✅ **语义理解** - 理解代码的业务含义和设计意图
✅ **完整实现** - 自动生成方法体逻辑,不只是签名
✅ **智能重构** - 自动转换为 Pythonic 风格
✅ **设计模式识别** - 识别并保留设计模式
✅ **混合模式** - 自动选择最佳迁移策略

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 基础依赖(已有)
pip install -r requirements.txt

# LLM 依赖(选择一个)
pip install openai        # OpenAI GPT-4
pip install anthropic     # Anthropic Claude
pip install requests      # Ollama (本地免费)
```

### 2. 配置 LLM

#### 方案 A: OpenAI (推荐)
```bash
export OPENAI_API_KEY="sk-..."
```

#### 方案 B: Anthropic Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### 方案 C: Ollama (本地免费)
```bash
# 安装 Ollama
curl https://ollama.ai/install.sh | sh

# 下载模型
ollama pull codellama

# 启动服务
ollama serve
```

### 3. 运行演示

```bash
# 运行完整演示(使用 Mock LLM,不需要 API key)
python demo_intelligent.py

# 使用真实 LLM 的演示
# 需要先配置 API key
python demo_intelligent.py
```

---

## 📚 使用方法

### Python API 使用

#### 基础使用

```python
from intelligent_migrator import IntelligentMigrator, MigrationMode
from llm_providers import create_llm_provider

# 1. 创建 LLM 提供者
provider = create_llm_provider("openai")  # 或 "anthropic", "ollama"

# 2. 创建智能迁移器
migrator = IntelligentMigrator(
    llm_provider=provider,
    mode=MigrationMode.HYBRID  # 自动选择最佳模式
)

# 3. 执行迁移
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

results = migrator.migrate(
    java_code,
    validate=True,      # 验证生成的代码
    refactor=True       # 重构为 Pythonic 风格
)

# 4. 查看结果
if results['success']:
    print(results['python_code'])
    print(f"模式: {results['mode_used']}")
    print(f"业务分析: {results['business_analysis']}")
else:
    print(f"错误: {results['errors']}")
```

#### 三种模式详解

```python
# 模式 1: 规则映射 (快速、免费)
migrator = IntelligentMigrator(mode=MigrationMode.RULE_BASED)
# 适用: 简单 POJO、DTO、实体类

# 模式 2: 语义理解 (高质量、需要 LLM)
migrator = IntelligentMigrator(
    llm_provider=provider,
    mode=MigrationMode.SEMANTIC
)
# 适用: 复杂业务逻辑、服务类、算法

# 模式 3: 混合模式 (推荐)
migrator = IntelligentMigrator(
    llm_provider=provider,
    mode=MigrationMode.HYBRID  # 自动选择
)
# 自动决策: 简单类用规则,复杂类用 LLM
```

---

## 🔧 LLM 提供者配置

### OpenAI (最推荐)

**优点**: 质量最高、速度快、稳定
**缺点**: 需要付费

```python
from llm_providers import OpenAIProvider

provider = OpenAIProvider(
    api_key="sk-...",                    # 可选,默认从环境变量读取
    model="gpt-4-turbo-preview",         # 或 "gpt-3.5-turbo" 更便宜
    base_url="https://api.openai.com/v1" # 可选,用于代理
)
```

**成本估算**:
- GPT-4: ~$0.01-0.03/次
- GPT-3.5: ~$0.001-0.002/次

### Anthropic Claude

**优点**: 质量高、上下文长
**缺点**: 需要付费

```python
from llm_providers import AnthropicProvider

provider = AnthropicProvider(
    api_key="sk-ant-...",                      # 可选
    model="claude-3-5-sonnet-20241022"         # 或 "claude-3-opus"
)
```

**成本估算**:
- Claude 3.5 Sonnet: ~$0.01-0.02/次

### Ollama (免费推荐)

**优点**: 完全免费、数据隐私
**缺点**: 需要本地 GPU、质量略低

```python
from llm_providers import OllamaProvider

provider = OllamaProvider(
    model="codellama",                    # 或 "llama2", "mistral"
    base_url="http://localhost:11434"    # Ollama 服务地址
)
```

**模型推荐**:
- `codellama`: 代码专用,最推荐
- `llama2`: 通用模型
- `mistral`: 轻量高效

---

## 💡 最佳实践

### 1. 根据项目规模选择模式

```python
# 小项目 (<100个类) - 全部使用规则映射
migrator = IntelligentMigrator(mode=MigrationMode.RULE_BASED)

# 中型项目 (100-1000个类) - 混合模式
migrator = IntelligentMigrator(
    llm_provider=provider,
    mode=MigrationMode.HYBRID
)

# 大型项目 (>1000个类) - 分批处理
# 简单类用规则,核心类用语义
```

### 2. 成本优化

```python
# 策略 1: 先用免费模式预览
mock_migrator = IntelligentMigrator(
    llm_provider=create_llm_provider("mock"),
    mode=MigrationMode.HYBRID
)
results = mock_migrator.migrate(java_code)

# 策略 2: 只对复杂类使用 LLM
if results['mode_used'] == MigrationMode.SEMANTIC:
    # 使用真实 LLM 重新生成
    real_migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("openai"),
        mode=MigrationMode.SEMANTIC
    )
    results = real_migrator.migrate(java_code)
```

### 3. 批量迁移脚本

```python
import os
from pathlib import Path

def migrate_project(java_dir: str, output_dir: str):
    """批量迁移整个项目"""

    migrator = IntelligentMigrator(
        llm_provider=create_llm_provider("openai"),
        mode=MigrationMode.HYBRID
    )

    for java_file in Path(java_dir).rglob("*.java"):
        with open(java_file, 'r', encoding='utf-8') as f:
            java_code = f.read()

        results = migrator.migrate(java_code)

        if results['success']:
            # 保存 Python 文件
            rel_path = java_file.relative_to(java_dir)
            py_file = Path(output_dir) / rel_path.with_suffix('.py')
            py_file.parent.mkdir(parents=True, exist_ok=True)

            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(results['python_code'])

            print(f"✓ {java_file} -> {py_file}")
        else:
            print(f"✗ {java_file} 失败: {results['errors']}")

# 使用
migrate_project("./java_project/src", "./python_project/src")
```

---

## 📊 效果对比

### 示例: UserService 迁移

#### 输入 (Java)
```java
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
```

#### 输出对比

**规则映射模式** (快速但不完整):
```python
class UserService:
    """Java 类 UserService 的 Python 实现"""

    def create_user(self, email: str, name: str) -> User:
        """TODO: 实现方法体"""
        pass  # ❌ 需要手动实现

    def _is_valid_email(self, email: str) -> bool:
        """TODO: 实现方法体"""
        pass  # ❌ 需要手动实现
```

**语义理解模式** (完整实现):
```python
from datetime import datetime
from typing import Optional

class UserService:
    """
    用户服务类 - 处理用户创建和验证

    职责:
    - 创建新用户并持久化
    - 验证用户邮箱格式
    """

    def __init__(self, repository: 'UserRepository'):
        self._repository = repository

    def create_user(self, email: str, name: str) -> 'User':
        """
        创建新用户

        Args:
            email: 用户邮箱
            name: 用户名称

        Returns:
            创建的用户对象

        Raises:
            ValueError: 邮箱格式无效
        """
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")

        user = User(email=email, name=name)
        user.created_at = datetime.now()

        return self._repository.save(user)

    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        return email is not None and '@' in email
```

---

## 🐛 故障排除

### 问题 1: LLM API 调用失败

```python
# 错误: "OpenAI API 调用失败"
# 解决:
# 1. 检查 API key
import os
print(os.getenv('OPENAI_API_KEY'))

# 2. 检查网络
# 3. 尝试使用代理
provider = OpenAIProvider(
    api_key="sk-...",
    base_url="https://your-proxy.com/v1"
)
```

### 问题 2: Ollama 连接失败

```bash
# 错误: "Ollama API 调用失败"
# 解决:
# 1. 确保 Ollama 正在运行
ollama serve

# 2. 检查模型是否已下载
ollama list

# 3. 如果没有,下载模型
ollama pull codellama
```

### 问题 3: 生成质量不佳

```python
# 策略 1: 提高温度参数
results = migrator.migrate(java_code)  # 使用默认 temperature=0.2

# 策略 2: 使用更好的模型
provider = OpenAIProvider(model="gpt-4-turbo-preview")  # 而不是 gpt-3.5

# 策略 3: 启用重构
results = migrator.migrate(java_code, refactor=True)
```

---

## 📈 性能优化

### 1. 缓存 LLM 响应

```python
import hashlib
import json

class CachedLLMProvider:
    def __init__(self, base_provider, cache_file="llm_cache.json"):
        self.provider = base_provider
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def complete(self, prompt, system=None, **kwargs):
        # 生成缓存键
        cache_key = hashlib.md5(
            (prompt + (system or "")).encode()
        ).hexdigest()

        # 检查缓存
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 调用 LLM
        response = self.provider.complete(prompt, system, **kwargs)

        # 保存缓存
        self.cache[cache_key] = response
        self._save_cache()

        return response

    def _load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
```

### 2. 并行处理

```python
from concurrent.futures import ThreadPoolExecutor

def migrate_files_parallel(java_files, max_workers=5):
    """并行迁移多个文件"""
    migrator = IntelligentMigrator(...)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for java_file in java_files:
            future = executor.submit(migrate_single_file, java_file, migrator)
            futures.append(future)

        for future in futures:
            result = future.result()
            print(f"完成: {result}")
```

---

## 📝 下一步

现在你已经有了完整的智能迁移系统!

**推荐操作:**
1. ✅ 运行 `python demo_intelligent.py` 查看效果
2. ✅ 配置真实的 LLM (OpenAI/Anthropic/Ollama)
3. ✅ 在实际项目中测试
4. ✅ 根据需要调整复杂度阈值

**可选扩展:**
- 添加更多设计模式识别
- 集成代码质量检查
- 添加 Web UI
- 支持增量迁移

---

## 💬 反馈和支持

遇到问题? 有建议?
- 查看 [AGENT_COMPARISON.md](AGENT_COMPARISON.md) 了解详细对比
- 查看源代码注释了解实现细节
- 提交 issue 或 PR

**享受智能代码迁移! 🎉**
