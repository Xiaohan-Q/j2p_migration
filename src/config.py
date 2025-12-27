"""
配置文件管理模块
管理迁移工具的配置选项
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
from pathlib import Path


@dataclass
class MigrationConfig:
    """迁移配置"""

    # 日志配置
    verbose: bool = False
    use_color: bool = True
    log_file: Optional[str] = None

    # 解析配置
    skip_errors: bool = False
    strict_mode: bool = True

    # 代码生成配置
    indent_size: int = 4
    max_line_length: int = 100
    add_type_hints: bool = True
    add_docstrings: bool = True

    # 验证配置
    run_validation: bool = True
    run_static_analysis: bool = False
    run_execution_test: bool = False

    # 迁移计划配置
    show_plan: bool = False
    show_warnings: bool = True
    show_recommendations: bool = True

    # 输出配置
    output_format: str = "python"  # python, json, yaml
    overwrite_existing: bool = False
    create_backup: bool = True

    # 类型映射自定义
    custom_type_mapping: Dict[str, str] = field(default_factory=dict)

    # 导入映射自定义
    custom_import_mapping: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'MigrationConfig':
        """从字典创建配置"""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})

    @classmethod
    def from_file(cls, config_file: str) -> 'MigrationConfig':
        """从 JSON 配置文件加载"""
        path = Path(config_file)
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")

        with open(path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)

        return cls.from_dict(config_dict)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'verbose': self.verbose,
            'use_color': self.use_color,
            'log_file': self.log_file,
            'skip_errors': self.skip_errors,
            'strict_mode': self.strict_mode,
            'indent_size': self.indent_size,
            'max_line_length': self.max_line_length,
            'add_type_hints': self.add_type_hints,
            'add_docstrings': self.add_docstrings,
            'run_validation': self.run_validation,
            'run_static_analysis': self.run_static_analysis,
            'run_execution_test': self.run_execution_test,
            'show_plan': self.show_plan,
            'show_warnings': self.show_warnings,
            'show_recommendations': self.show_recommendations,
            'output_format': self.output_format,
            'overwrite_existing': self.overwrite_existing,
            'create_backup': self.create_backup,
            'custom_type_mapping': self.custom_type_mapping,
            'custom_import_mapping': self.custom_import_mapping,
        }

    def save_to_file(self, config_file: str):
        """保存配置到 JSON 文件"""
        path = Path(config_file)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def merge(self, other: 'MigrationConfig') -> 'MigrationConfig':
        """合并两个配置 (other 优先)"""
        merged_dict = self.to_dict()
        other_dict = other.to_dict()

        for key, value in other_dict.items():
            if value is not None:
                merged_dict[key] = value

        return MigrationConfig.from_dict(merged_dict)


# 默认配置
DEFAULT_CONFIG = MigrationConfig()


def get_default_config() -> MigrationConfig:
    """获取默认配置"""
    return MigrationConfig()
