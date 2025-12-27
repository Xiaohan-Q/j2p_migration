"""
扩展的测试用例
全面测试 Java to Python 迁移工具的各个功能
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
from config import MigrationConfig
from logger import get_logger


class TestLogger:
    """测试日志系统"""

    def test_logger_creation(self):
        """测试日志器创建"""
        logger = get_logger(verbose=True)
        assert logger is not None
        assert logger.verbose is True

    def test_logger_methods(self):
        """测试日志方法"""
        logger = get_logger()
        # 这些方法应该不抛出异常
        logger.info("Test info")
        logger.debug("Test debug")
        logger.warning("Test warning")
        logger.error("Test error")
        logger.success("Test success")


class TestConfig:
    """测试配置管理"""

    def test_default_config(self):
        """测试默认配置"""
        config = MigrationConfig()
        assert config.verbose is False
        assert config.indent_size == 4
        assert config.add_type_hints is True

    def test_config_to_dict(self):
        """测试配置转字典"""
        config = MigrationConfig(verbose=True, indent_size=2)
        config_dict = config.to_dict()

        assert config_dict['verbose'] is True
        assert config_dict['indent_size'] == 2

    def test_config_from_dict(self):
        """测试从字典创建配置"""
        config_dict = {
            'verbose': True,
            'indent_size': 2,
            'add_type_hints': False
        }
        config = MigrationConfig.from_dict(config_dict)

        assert config.verbose is True
        assert config.indent_size == 2
        assert config.add_type_hints is False


class TestAdvancedParsing:
    """测试高级解析功能"""

    def test_parse_inheritance(self):
        """测试解析继承关系"""
        java_code = """
        public class Dog extends Animal {
            public void bark() {
                System.out.println("Woof!");
            }
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        assert len(structure['classes']) == 1
        assert structure['classes'][0]['extends'] == 'Animal'

    def test_parse_interfaces(self):
        """测试解析接口实现"""
        java_code = """
        public class MyClass implements Runnable, Serializable {
            public void run() {}
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        assert len(structure['classes']) == 1
        assert 'Runnable' in structure['classes'][0]['implements']
        assert 'Serializable' in structure['classes'][0]['implements']

    def test_parse_static_fields(self):
        """测试解析静态字段"""
        java_code = """
        public class Config {
            private static final String VERSION = "1.0";
            private static int counter = 0;
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        fields = structure['classes'][0]['fields']
        assert len(fields) == 2

        # 检查静态和 final 修饰符
        version_field = next(f for f in fields if f['name'] == 'VERSION')
        assert 'static' in version_field['modifiers']
        assert 'final' in version_field['modifiers']

    def test_parse_generic_types(self):
        """测试解析泛型类型"""
        java_code = """
        public class Container {
            private List<String> items;
            private Map<String, Integer> counts;
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        fields = structure['classes'][0]['fields']
        assert len(fields) == 2

    def test_parse_multiple_classes(self):
        """测试解析多个类"""
        java_code = """
        public class First {
            public void method1() {}
        }

        class Second {
            public void method2() {}
        }
        """

        parser = JavaASTParser()
        structure = parser.get_full_structure(java_code)

        assert len(structure['classes']) == 2


class TestAdvancedMapping:
    """测试高级映射功能"""

    def test_map_snake_case(self):
        """测试驼峰命名转 snake_case"""
        mapper = SemanticMapper()

        assert mapper._to_snake_case('getUserName') == 'get_user_name'
        assert mapper._to_snake_case('XMLParser') == 'xml_parser'
        assert mapper._to_snake_case('simpleMethod') == 'simple_method'

    def test_map_constant_naming(self):
        """测试常量命名映射"""
        mapper = SemanticMapper()

        field_info = {
            'name': 'maxSize',
            'type': 'int',
            'modifiers': ['public', 'static', 'final'],
            'initializer': '100'
        }

        mapped_field = mapper.map_field(field_info)
        assert mapped_field['python_name'] == 'MAX_SIZE'
        assert mapped_field['is_constant'] is True

    def test_map_private_method(self):
        """测试私有方法映射"""
        mapper = SemanticMapper()

        method_info = {
            'name': 'calculateTotal',
            'modifiers': ['private'],
            'return_type': 'int',
            'parameters': []
        }

        mapped_method = mapper.map_method(method_info)
        assert mapped_method['python_name'].startswith('_')
        assert mapped_method['is_private'] is True

    def test_map_static_method(self):
        """测试静态方法映射"""
        mapper = SemanticMapper()

        method_info = {
            'name': 'getInstance',
            'modifiers': ['public', 'static'],
            'return_type': 'MyClass',
            'parameters': []
        }

        mapped_method = mapper.map_method(method_info)
        assert '@staticmethod' in mapped_method['decorators']
        assert mapped_method['is_static'] is True


class TestMigrationPlanner:
    """测试迁移规划器"""

    def test_complexity_analysis(self):
        """测试复杂度分析"""
        planner = MigrationPlanner()

        java_structure = {
            'imports': ['java.util.List', 'java.util.Map'],
            'classes': [
                {
                    'name': 'Complex',
                    'fields': [
                        {'name': 'field1', 'type': 'String'},
                        {'name': 'field2', 'type': 'int'}
                    ],
                    'methods': [
                        {'name': 'method1', 'parameters': [], 'modifiers': []},
                        {'name': 'method2', 'parameters': [], 'modifiers': []}
                    ],
                    'constructors': [{'parameters': []}],
                    'extends': 'BaseClass',
                    'implements': ['Interface1']
                }
            ]
        }

        complexity = planner.analyze_complexity(java_structure)

        assert complexity['total_classes'] == 1
        assert complexity['total_methods'] == 2
        assert complexity['total_fields'] == 2
        assert complexity['total_imports'] == 2
        assert complexity['has_inheritance'] is True
        assert complexity['has_interfaces'] is True

    def test_migration_plan_generation(self):
        """测试迁移计划生成"""
        planner = MigrationPlanner()

        java_structure = {
            'imports': ['java.util.List'],
            'classes': [
                {
                    'name': 'Example',
                    'fields': [{'name': 'data', 'type': 'String'}],
                    'methods': [{'name': 'getData', 'modifiers': [], 'parameters': []}],
                    'constructors': [{'parameters': []}],
                    'extends': None,
                    'implements': []
                }
            ]
        }

        plan = planner.plan_migration(java_structure)

        assert 'steps' in plan
        assert 'complexity_analysis' in plan
        assert 'estimated_difficulty' in plan
        assert 'recommendations' in plan
        assert len(plan['steps']) > 0


class TestCodeGenerator:
    """测试代码生成器"""

    def test_generate_class_with_inheritance(self):
        """测试生成带继承的类"""
        generator = PythonCodeGenerator()

        python_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'Dog',
                    'base_classes': ['Animal'],
                    'fields': [],
                    'methods': [
                        {
                            'name': 'bark',
                            'python_name': 'bark',
                            'parameters': [],
                            'return_type': 'None',
                            'decorators': [],
                            'is_static': False,
                            'is_private': False
                        }
                    ],
                    'constructors': []
                }
            ]
        }

        code = generator.generate_code(python_structure)

        assert 'class Dog(Animal):' in code
        assert 'def bark(self)' in code

    def test_generate_static_method(self):
        """测试生成静态方法"""
        generator = PythonCodeGenerator()

        python_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'Utils',
                    'base_classes': [],
                    'fields': [],
                    'methods': [
                        {
                            'name': 'helper',
                            'python_name': 'helper',
                            'parameters': [{'name': 'value', 'annotation': 'value: int'}],
                            'return_type': 'str',
                            'decorators': ['@staticmethod'],
                            'is_static': True,
                            'is_private': False
                        }
                    ],
                    'constructors': []
                }
            ]
        }

        code = generator.generate_code(python_structure)

        assert '@staticmethod' in code
        assert 'def helper(value: int) -> str:' in code

    def test_generate_class_variables(self):
        """测试生成类变量"""
        generator = PythonCodeGenerator()

        python_structure = {
            'imports': [],
            'classes': [
                {
                    'name': 'Config',
                    'base_classes': [],
                    'fields': [
                        {
                            'name': 'VERSION',
                            'python_name': 'VERSION',
                            'type': 'str',
                            'is_class_variable': True,
                            'is_constant': True,
                            'initializer': '"1.0"'
                        }
                    ],
                    'methods': [],
                    'constructors': []
                }
            ]
        }

        code = generator.generate_code(python_structure)

        assert 'VERSION: str = "1.0"' in code


class TestValidator:
    """测试验证器"""

    def test_validate_valid_syntax(self):
        """测试验证有效语法"""
        validator = MigrationValidator()

        valid_code = """
class Example:
    def __init__(self):
        self.value = 0

    def get_value(self) -> int:
        return self.value
"""

        is_valid, errors = validator.validate_syntax(valid_code)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_invalid_syntax(self):
        """测试验证无效语法"""
        validator = MigrationValidator()

        invalid_code = """
class Example
    def method(self)
        pass
"""

        is_valid, errors = validator.validate_syntax(invalid_code)

        assert is_valid is False
        assert len(errors) > 0

    def test_validate_type_annotations(self):
        """测试类型注解验证"""
        validator = MigrationValidator()

        code_with_annotations = """
class Example:
    def method(self, value: int) -> str:
        return str(value)
"""

        is_valid, warnings = validator.check_type_annotations(code_with_annotations)

        # 应该通过验证
        assert len(warnings) == 0


class TestIntegration:
    """集成测试"""

    def test_full_pipeline_simple_class(self):
        """测试完整流程 - 简单类"""
        java_code = """
        public class SimpleClass {
            private int value;

            public SimpleClass(int value) {
                this.value = value;
            }

            public int getValue() {
                return value;
            }
        }
        """

        # 步骤 1: 解析
        parser = JavaASTParser()
        java_structure = parser.get_full_structure(java_code)
        assert java_structure is not None
        assert len(java_structure['classes']) == 1

        # 步骤 2: 规划
        planner = MigrationPlanner()
        plan = planner.plan_migration(java_structure)
        assert plan is not None
        assert 'steps' in plan

        # 步骤 3: 映射
        mapper = SemanticMapper()
        python_structure = mapper.map_structure(java_structure)
        assert len(python_structure['classes']) == 1

        # 步骤 4: 生成
        generator = PythonCodeGenerator()
        python_code = generator.generate_code(python_structure)
        assert 'class SimpleClass:' in python_code

        # 步骤 5: 验证
        validator = MigrationValidator()
        is_valid, errors = validator.validate_syntax(python_code)
        assert is_valid is True

    def test_full_pipeline_complex_class(self):
        """测试完整流程 - 复杂类"""
        java_code = """
        public class ComplexClass extends BaseClass implements Interface1 {
            private static final String CONSTANT = "value";
            private List<String> items;

            public ComplexClass() {
                this.items = new ArrayList<>();
            }

            public static String getConstant() {
                return CONSTANT;
            }

            public void addItem(String item) {
                items.add(item);
            }
        }
        """

        # 完整流程
        parser = JavaASTParser()
        java_structure = parser.get_full_structure(java_code)

        mapper = SemanticMapper()
        python_structure = mapper.map_structure(java_structure)

        generator = PythonCodeGenerator()
        python_code = generator.generate_code(python_structure)

        validator = MigrationValidator()
        is_valid, errors = validator.validate_syntax(python_code)

        assert is_valid is True
        assert 'class ComplexClass(BaseClass, Interface1):' in python_code


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
