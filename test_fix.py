"""
测试修复后的代码生成
"""
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ast_parser import JavaASTParser
from semantic_mapper import SemanticMapper
from code_generater import PythonCodeGenerator

# Java 示例代码
java_code = """
public class Person {
    private String name;
    private int age;
    private static int count = 0;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
        count++;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public static int getCount() {
        return count;
    }

    public void introduce() {
        System.out.println("Hello, I am " + name);
    }
}
"""

# 解析和生成
parser = JavaASTParser()
mapper = SemanticMapper()
generator = PythonCodeGenerator()

java_structure = parser.get_full_structure(java_code)
python_structure = mapper.map_structure(java_structure)
python_code = generator.generate_code(python_structure)
python_code = generator.format_code(python_code)

# 保存生成的代码
output_file = Path(__file__).parent / 'example' / 'Person.py'
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(python_code)

print("Code generated successfully!")
print(f"Output saved to: {output_file}")
print("\n" + "="*70)
print("Generated Python code:")
print("="*70)
print(python_code)
