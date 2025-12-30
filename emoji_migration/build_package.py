"""
创建 emoji-python 包并进行集成测试
整合所有生成的 Python 模块
"""
import sys
from pathlib import Path
import shutil

# 设置编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from logger import get_logger


class EmojiPackageBuilder:
    """构建 emoji-python 包"""

    def __init__(self):
        self.logger = get_logger(verbose=True, use_color=True)
        self.output_dir = Path(__file__).parent / 'output'
        self.package_dir = Path(__file__).parent / 'emoji_python'

    def build_package(self):
        """构建 Python 包"""
        self.logger.info("="*80)
        self.logger.info("构建 emoji-python 包")
        self.logger.info("="*80)

        # 创建包目录
        if self.package_dir.exists():
            self.logger.warning(f"包目录已存在，将被覆盖: {self.package_dir}")
            shutil.rmtree(self.package_dir)

        self.package_dir.mkdir(parents=True)
        self.logger.success(f"创建包目录: {self.package_dir}")

        # 复制所有 Python 文件
        modules = ['Emoji', 'EmojiLoader', 'EmojiManager', 'EmojiParser', 'EmojiTrie', 'Fitzpatrick']
        copied_files = []

        for module in modules:
            src_file = self.output_dir / module / f"{module}.py"
            dst_file = self.package_dir / f"{module}.py"

            if src_file.exists():
                shutil.copy2(src_file, dst_file)
                self.logger.success(f"  ✓ 复制: {module}.py")
                copied_files.append(module)
            else:
                self.logger.error(f"  ✗ 未找到: {module}.py")

        # 创建 __init__.py
        self.create_init_file(copied_files)

        # 创建 README
        self.create_readme()

        # 创建 setup.py
        self.create_setup()

        # 创建示例代码
        self.create_examples()

        self.logger.info("\n" + "="*80)
        self.logger.success("包构建完成!")
        self.logger.info("="*80)
        self.logger.info(f"\n包位置: {self.package_dir}")
        self.logger.info(f"包含模块: {len(copied_files)} 个")
        self.logger.info("\n下一步:")
        self.logger.info("  1. cd emoji_python")
        self.logger.info("  2. python -m pytest tests/  # 运行测试")
        self.logger.info("  3. python examples/demo.py  # 运行示例")

    def create_init_file(self, modules):
        """创建 __init__.py"""
        init_content = '''"""
emoji-python: Python port of emoji-java library
A lightweight Python library for working with emojis.
"""

__version__ = '0.1.0'
__author__ = 'Auto-generated from emoji-java'

# Import main classes
'''

        for module in modules:
            init_content += f"from .{module} import *\n"

        init_content += '''
__all__ = [
'''
        for module in modules:
            init_content += f"    '{module}',\n"
        init_content += ''']
'''

        init_file = self.package_dir / '__init__.py'
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(init_content)

        self.logger.success(f"  ✓ 创建: __init__.py")

    def create_readme(self):
        """创建 README"""
        readme_content = '''# emoji-python

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
'''

        readme_file = self.package_dir / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        self.logger.success(f"  ✓ 创建: README.md")

    def create_setup(self):
        """创建 setup.py"""
        setup_content = '''from setuptools import setup, find_packages

setup(
    name='emoji-python',
    version='0.1.0',
    description='Python port of emoji-java library',
    author='Auto-generated',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        # Add dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
'''

        setup_file = self.package_dir / 'setup.py'
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(setup_content)

        self.logger.success(f"  ✓ 创建: setup.py")

    def create_examples(self):
        """创建示例代码"""
        examples_dir = self.package_dir / 'examples'
        examples_dir.mkdir(exist_ok=True)

        demo_content = '''"""
emoji-python 使用示例
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from Fitzpatrick import Fitzpatrick


def demo_fitzpatrick():
    """演示 Fitzpatrick 枚举"""
    print("=" * 60)
    print("Fitzpatrick 肤色修饰符演示")
    print("=" * 60)

    # 遍历所有肤色类型
    print("\\n所有 Fitzpatrick 类型:")
    for fitz in Fitzpatrick:
        print(f"  {fitz.name}: {fitz.value}")

    # 根据 unicode 查找
    print("\\n根据 Unicode 查找:")
    unicode_str = "🏻"
    found = Fitzpatrick.fitzpatrick_from_unicode(unicode_str)
    if found:
        print(f"  找到: {found.name}")
    else:
        print(f"  未找到匹配的类型")

    print("\\n✓ 演示完成")


if __name__ == '__main__':
    try:
        demo_fitzpatrick()
    except Exception as e:
        print(f"\\n错误: {e}")
        import traceback
        traceback.print_exc()
'''

        demo_file = examples_dir / 'demo.py'
        with open(demo_file, 'w', encoding='utf-8') as f:
            f.write(demo_content)

        self.logger.success(f"  ✓ 创建: examples/demo.py")

    def create_tests_directory(self):
        """创建测试目录并复制测试文件"""
        tests_dir = self.package_dir / 'tests'
        tests_dir.mkdir(exist_ok=True)

        # 创建 __init__.py
        (tests_dir / '__init__.py').touch()

        # 复制测试文件
        modules = ['Emoji', 'EmojiLoader', 'EmojiManager', 'EmojiParser', 'EmojiTrie', 'Fitzpatrick']

        for module in modules:
            test_src = self.output_dir / module / f"test_{module}.py"
            test_dst = tests_dir / f"test_{module}.py"

            if test_src.exists():
                shutil.copy2(test_src, test_dst)
                self.logger.success(f"  ✓ 复制测试: test_{module}.py")

        self.logger.success(f"  ✓ 创建: tests/")


def main():
    """主函数"""
    builder = EmojiPackageBuilder()
    builder.build_package()
    builder.create_tests_directory()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n用户中断")
    except Exception as e:
        print(f"\\n\\n错误: {e}")
        import traceback
        traceback.print_exc()
