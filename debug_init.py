"""
调试 initializer 类型
"""
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ast_parser import JavaASTParser

# Java 示例代码
java_code = """
public class Person {
    private String name;
    private int age;
    private static int count = 0;
}
"""

parser = JavaASTParser()
java_structure = parser.get_full_structure(java_code)

print("Java structure:")
for cls in java_structure.get('classes', []):
    print(f"\nClass: {cls['name']}")
    for field in cls.get('fields', []):
        print(f"  Field: {field['name']}")
        print(f"    Type: {field['type']}")
        print(f"    Initializer: {field.get('initializer')}")
        print(f"    Initializer type: {type(field.get('initializer'))}")

        init = field.get('initializer')
        if init:
            print(f"    Initializer repr: {repr(init)}")
            print(f"    Initializer dir: {[x for x in dir(init) if not x.startswith('_')]}")
            if hasattr(init, '__dict__'):
                print(f"    Initializer dict: {init.__dict__}")
