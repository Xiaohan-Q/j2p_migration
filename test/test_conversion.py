"""
Java to Python 迁移工具测试用例
"""
import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ast_parser import JavaASTParser
from semantic_mapper import SemanticMapper
from migration_planner import MigrationPlanner
from code_generater import PythonCodeGenerator
from validator import MigrationValidator


class TestJavaParser:
    """测试 Java 解析器"""

    def test_parse_simple_class(self):
        """测试解析简单的 Java 类"""
        java_code = """
        public class HelloWorld {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        assert structure is not None
        assert len(structure['classes']) == 1
        assert structure['classes'][0]['name'] == 'HelloWorld'

    def test_parse_class_with_fields(self):
        """测试解析带字段的类"""
        java_code = """
        public class Person {
            private String name;
            private int age;

            public Person(String name, int age) {
                this.name = name;
                this.age = age;
            }

            public String getName() {
                return name;
            }
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        assert len(structure['classes']) == 1
        person_class = structure['classes'][0]

        assert len(person_class['fields']) == 2
        assert len(person_class['constructors']) == 1
        assert len(person_class['methods']) == 1


class TestSemanticMapper:
    """测试语义映射器"""

    def test_map_basic_types(self):
        """测试基本类型映射"""
        mapper = SemanticMapper()

        assert mapper.map_type('int') == 'int'
        assert mapper.map_type('String') == 'str'
        assert mapper.map_type('boolean') == 'bool'
        assert mapper.map_type('void') == 'None'

    def test_map_generic_types(self):
        """测试泛型类型映射"""
        mapper = SemanticMapper()

        assert mapper.map_type('List<String>') == 'List[str]'
        assert mapper.map_type('ArrayList<Integer>') == 'list'

    def test_map_array_types(self):
        """测试数组类型映射"""
        mapper = SemanticMapper()

        assert mapper.map_type('int[]') == 'List[int]'
        assert mapper.map_type('String[]') == 'List[str]'

    def test_map_field(self):
        """测试字段映射"""
        mapper = SemanticMapper()

        field_info = {
            'name': 'count',
            'type': 'int',
            'modifiers': ['private', 'static', 'final']
        }

        mapped_field = mapper.map_field(field_info)

        assert mapped_field['python_name'] == 'COUNT'  # 常量大写
        assert mapped_field['is_constant'] is True


class TestMigrationPlanner:
    """测试迁移规划器"""

    def test_analyze_complexity(self):
        """测试复杂度分析"""
        planner = MigrationPlanner()

        java_structure = {
            'imports': ['java.util.List'],
            'classes': [
                {
                    'name': 'Example',
                    'fields': [{'name': 'field1'}],
                    'methods': [{'name': 'method1'}],
                    'extends': None,
                    'implements': []
                }
            ]
        }

        complexity = planner.analyze_complexity(java_structure)

        assert complexity['total_classes'] == 1
        assert complexity['total_methods'] == 1
        assert complexity['total_fields'] == 1

    def test_plan_migration(self):
        """测试生成迁移计划"""
        planner = MigrationPlanner()

        java_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'Simple',
                    'fields': [],
                    'methods': [{'name': 'test', 'modifiers': []}],
                    'constructors': [],
                    'extends': None,
                    'implements': []
                }
            ]
        }

        plan = planner.plan_migration(java_structure)

        assert 'steps' in plan
        assert 'estimated_difficulty' in plan
        assert len(plan['steps']) > 0


class TestCodeGenerator:
    """测试代码生成器"""

    def test_generate_simple_class(self):
        """测试生成简单类"""
        generator = PythonCodeGenerator()

        python_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'HelloWorld',
                    'base_classes': [],
                    'fields': [],
                    'methods': [
                        {
                            'name': 'main',
                            'python_name': 'main',
                            'parameters': [],
                            'return_type': 'None',
                            'decorators': ['@staticmethod'],
                            'is_static': True,
                            'is_private': False,
                            'body': None
                        }
                    ],
                    'constructors': []
                }
            ]
        }

        code = generator.generate_code(python_structure)

        assert 'class HelloWorld:' in code
        assert 'def main()' in code
        assert '@staticmethod' in code

    def test_generate_with_fields(self):
        """测试生成带字段的类"""
        generator = PythonCodeGenerator()

        python_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'Person',
                    'base_classes': [],
                    'fields': [
                        {
                            'name': 'name',
                            'python_name': 'name',
                            'type': 'str',
                            'is_class_variable': False,
                            'is_constant': False
                        }
                    ],
                    'methods': [],
                    'constructors': [
                        {
                            'name': '__init__',
                            'parameters': [
                                {'name': 'name', 'annotation': 'name: str'}
                            ],
                            'body': None
                        }
                    ]
                }
            ]
        }

        code = generator.generate_code(python_structure)

        assert 'class Person:' in code
        assert 'def __init__' in code
        assert 'self.name' in code


class TestValidator:
    """测试验证器"""

    def test_validate_syntax_valid(self):
        """测试验证有效的语法"""
        validator = MigrationValidator()

        valid_code = """
class Test:
    def method(self):
        pass
"""

        is_valid, errors = validator.validate_syntax(valid_code)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_syntax_invalid(self):
        """测试验证无效的语法"""
        validator = MigrationValidator()

        invalid_code = """
class Test
    def method(self)
        pass
"""

        is_valid, errors = validator.validate_syntax(invalid_code)

        assert is_valid is False
        assert len(errors) > 0

    def test_validate_naming_conventions(self):
        """测试命名规范验证"""
        validator = MigrationValidator()

        code = """
class MyClass:
    def myMethod(self):  # 应该是 snake_case
        pass
"""

        is_valid, warnings = validator.validate_naming_conventions(code)

        # 应该有警告因为 myMethod 不是 snake_case
        assert len(warnings) > 0


class TestFullMigration:
    """测试完整迁移流程"""

    def test_complete_migration(self):
        """测试完整的迁移流程"""
        java_code = """
        public class Calculator {
            public int add(int a, int b) {
                return a + b;
            }
        }
        """

        # 步骤 1: 解析
        parser = JavaASTParser()
        java_structure = parser.get_full_structure(java_code)
        assert java_structure is not None

        # 步骤 2: 映射
        mapper = SemanticMapper()
        python_structure = mapper.map_structure(java_structure)
        assert len(python_structure['classes']) == 1

        # 步骤 3: 生成代码
        generator = PythonCodeGenerator()
        python_code = generator.generate_code(python_structure)
        assert 'class Calculator:' in python_code

        # 步骤 4: 验证
        validator = MigrationValidator()
        is_valid, errors = validator.validate_syntax(python_code)
        assert is_valid is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

