"""
Java to Python Migration Tool
一个功能完整的 Java → Python 代码迁移工具
"""

__version__ = "1.0.0"
__author__ = "Migration Tool Team"

from .ast_parser import JavaASTParser, parse_java_code
from .semantic_mapper import SemanticMapper, map_java_to_python
from .migration_planner import MigrationPlanner, plan_migration
from .code_generater import PythonCodeGenerator, generate_python_code
from .validator import MigrationValidator, validate_migration

__all__ = [
    'JavaASTParser',
    'SemanticMapper',
    'MigrationPlanner',
    'PythonCodeGenerator',
    'MigrationValidator',
    'parse_java_code',
    'map_java_to_python',
    'plan_migration',
    'generate_python_code',
    'validate_migration',
]
