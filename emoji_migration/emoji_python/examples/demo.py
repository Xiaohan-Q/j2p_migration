"""
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
    print("\n所有 Fitzpatrick 类型:")
    for fitz in Fitzpatrick:
        print(f"  {fitz.name}: {fitz.value}")

    # 根据 unicode 查找
    print("\n根据 Unicode 查找:")
    unicode_str = "🏻"
    found = Fitzpatrick.fitzpatrick_from_unicode(unicode_str)
    if found:
        print(f"  找到: {found.name}")
    else:
        print(f"  未找到匹配的类型")

    print("\n✓ 演示完成")


if __name__ == '__main__':
    try:
        demo_fitzpatrick()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
