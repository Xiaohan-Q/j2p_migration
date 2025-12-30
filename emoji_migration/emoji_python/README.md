# emoji-python

Python 版本的 emoji-java 库，由 Java 自动迁移而来。

## 功能

- Emoji 数据模型和管理
- Emoji 解析和转换
- Fitzpatrick 肤色修饰符支持
- 字典树（Trie）高效匹配

## 使用示例

```python
from emoji_python import Fitzpatrick, Emoji, EmojiManager

# 使用 Fitzpatrick 枚举
skin_tone = Fitzpatrick.TYPE_3

# TODO: 添加更多示例（需要实现 EmojiManager 等类）
```

## 模块说明

- `Emoji.py` - Emoji 数据模型
- `EmojiLoader.py` - Emoji 数据加载器
- `EmojiManager.py` - Emoji 管理器
- `EmojiParser.py` - Emoji 解析器
- `EmojiTrie.py` - 字典树数据结构
- `Fitzpatrick.py` - Fitzpatrick 肤色修饰符枚举

## 注意事项

这是从 Java 代码自动迁移的 Python 实现，可能需要进一步的人工调整和优化。

## 原始项目

基于 [emoji-java](https://github.com/vdurmont/emoji-java)
