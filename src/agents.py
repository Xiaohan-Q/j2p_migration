"""
Agent 架构设计
定义各个迁移 Agent 的接口和协调机制
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class AgentResult:
    """Agent 执行结果"""
    status: AgentStatus
    output: Any
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]


class BaseAgent(ABC):
    """迁移 Agent 基类"""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.errors = []
        self.warnings = []
        self.logger = None

    @abstractmethod
    def execute(self, input_data: Any) -> AgentResult:
        """
        执行 Agent 任务

        Args:
            input_data: 输入数据

        Returns:
            Agent 执行结果
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """
        验证输入数据

        Args:
            input_data: 输入数据

        Returns:
            是否有效
        """
        pass

    def set_logger(self, logger):
        """设置日志器"""
        self.logger = logger

    def log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(f"[{self.name}] {message}")

    def log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(f"[{self.name}] {message}")
        self.errors.append(message)

    def log_warning(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warning(f"[{self.name}] {message}")
        self.warnings.append(message)


class ParserAgent(BaseAgent):
    """Java 代码解析 Agent"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("ParserAgent", config)
        from ast_parser import JavaASTParser
        self.parser = JavaASTParser()

    def validate_input(self, input_data: Any) -> bool:
        """验证输入是否为有效的 Java 代码字符串"""
        return isinstance(input_data, str) and len(input_data.strip()) > 0

    def execute(self, input_data: str) -> AgentResult:
        """
        解析 Java 代码

        Args:
            input_data: Java 源代码字符串

        Returns:
            包含解析结构的 AgentResult
        """
        self.status = AgentStatus.RUNNING
        self.log_info("开始解析 Java 代码")

        if not self.validate_input(input_data):
            self.log_error("无效的输入数据")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )

        try:
            java_structure = self.parser.get_full_structure(input_data)

            if not java_structure:
                self.log_error("Java 代码解析失败")
                self.status = AgentStatus.FAILED
                return AgentResult(
                    status=AgentStatus.FAILED,
                    output=None,
                    errors=self.errors,
                    warnings=self.warnings,
                    metadata={}
                )

            self.log_info(f"解析成功: 找到 {len(java_structure.get('classes', []))} 个类")
            self.status = AgentStatus.SUCCESS

            return AgentResult(
                status=AgentStatus.SUCCESS,
                output=java_structure,
                errors=self.errors,
                warnings=self.warnings,
                metadata={
                    'num_classes': len(java_structure.get('classes', [])),
                    'num_imports': len(java_structure.get('imports', []))
                }
            )

        except Exception as e:
            self.log_error(f"解析过程中发生异常: {str(e)}")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )


class MapperAgent(BaseAgent):
    """语义映射 Agent"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("MapperAgent", config)
        from semantic_mapper import SemanticMapper
        self.mapper = SemanticMapper()

    def validate_input(self, input_data: Any) -> bool:
        """验证输入是否为有效的 Java 结构"""
        return isinstance(input_data, dict) and 'classes' in input_data

    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        执行语义映射

        Args:
            input_data: Java 代码结构

        Returns:
            包含 Python 结构的 AgentResult
        """
        self.status = AgentStatus.RUNNING
        self.log_info("开始语义映射")

        if not self.validate_input(input_data):
            self.log_error("无效的 Java 结构")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )

        try:
            python_structure = self.mapper.map_structure(input_data)

            self.log_info(f"映射完成: {len(python_structure.get('classes', []))} 个类")
            self.status = AgentStatus.SUCCESS

            return AgentResult(
                status=AgentStatus.SUCCESS,
                output=python_structure,
                errors=self.errors,
                warnings=self.warnings,
                metadata={
                    'num_classes': len(python_structure.get('classes', []))
                }
            )

        except Exception as e:
            self.log_error(f"映射过程中发生异常: {str(e)}")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )


class GeneratorAgent(BaseAgent):
    """代码生成 Agent"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("GeneratorAgent", config)
        from code_generater import PythonCodeGenerator
        self.generator = PythonCodeGenerator()

    def validate_input(self, input_data: Any) -> bool:
        """验证输入是否为有效的 Python 结构"""
        return isinstance(input_data, dict) and 'classes' in input_data

    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        生成 Python 代码

        Args:
            input_data: Python 代码结构

        Returns:
            包含生成代码的 AgentResult
        """
        self.status = AgentStatus.RUNNING
        self.log_info("开始生成 Python 代码")

        if not self.validate_input(input_data):
            self.log_error("无效的 Python 结构")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )

        try:
            python_code = self.generator.generate_code(input_data)
            python_code = self.generator.format_code(python_code)

            self.log_info("代码生成完成")
            self.status = AgentStatus.SUCCESS

            return AgentResult(
                status=AgentStatus.SUCCESS,
                output=python_code,
                errors=self.errors,
                warnings=self.warnings,
                metadata={
                    'code_length': len(python_code),
                    'num_lines': python_code.count('\n')
                }
            )

        except Exception as e:
            self.log_error(f"代码生成过程中发生异常: {str(e)}")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )


class ValidatorAgent(BaseAgent):
    """验证 Agent"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("ValidatorAgent", config)
        from validator import MigrationValidator
        self.validator = MigrationValidator()

    def validate_input(self, input_data: Any) -> bool:
        """验证输入"""
        if not isinstance(input_data, dict):
            return False
        return 'java_code' in input_data and 'python_code' in input_data

    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        验证生成的代码

        Args:
            input_data: 包含 java_code, python_code, python_structure 的字典

        Returns:
            包含验证报告的 AgentResult
        """
        self.status = AgentStatus.RUNNING
        self.log_info("开始验证代码")

        if not self.validate_input(input_data):
            self.log_error("无效的输入数据")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )

        try:
            report = self.validator.validate_migration(
                input_data['java_code'],
                input_data['python_code'],
                input_data.get('python_structure')
            )

            if report['overall_status'] == 'failed':
                self.log_warning("验证发现问题")
                self.status = AgentStatus.SUCCESS  # 验证本身成功,但发现了问题
            else:
                self.log_info(f"验证完成: {report['overall_status']}")
                self.status = AgentStatus.SUCCESS

            return AgentResult(
                status=AgentStatus.SUCCESS,
                output=report,
                errors=self.errors,
                warnings=self.warnings,
                metadata={
                    'validation_status': report['overall_status']
                }
            )

        except Exception as e:
            self.log_error(f"验证过程中发生异常: {str(e)}")
            self.status = AgentStatus.FAILED
            return AgentResult(
                status=AgentStatus.FAILED,
                output=None,
                errors=self.errors,
                warnings=self.warnings,
                metadata={}
            )


class MigrationOrchestrator:
    """迁移编排器 - 协调所有 Agent"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = None

        # 创建各个 Agent
        self.parser_agent = ParserAgent(config)
        self.mapper_agent = MapperAgent(config)
        self.generator_agent = GeneratorAgent(config)
        self.validator_agent = ValidatorAgent(config)

        self.results = {}

    def set_logger(self, logger):
        """设置所有 Agent 的日志器"""
        self.logger = logger
        self.parser_agent.set_logger(logger)
        self.mapper_agent.set_logger(logger)
        self.generator_agent.set_logger(logger)
        self.validator_agent.set_logger(logger)

    def orchestrate_migration(self, java_code: str,
                             validate: bool = True) -> Dict[str, Any]:
        """
        编排完整的迁移流程

        Args:
            java_code: Java 源代码
            validate: 是否执行验证

        Returns:
            包含所有结果的字典
        """
        if self.logger:
            self.logger.section("开始迁移编排")

        # 步骤 1: 解析
        parser_result = self.parser_agent.execute(java_code)
        self.results['parser'] = parser_result

        if parser_result.status != AgentStatus.SUCCESS:
            return self._build_failure_response("解析失败")

        # 步骤 2: 映射
        mapper_result = self.mapper_agent.execute(parser_result.output)
        self.results['mapper'] = mapper_result

        if mapper_result.status != AgentStatus.SUCCESS:
            return self._build_failure_response("映射失败")

        # 步骤 3: 生成
        generator_result = self.generator_agent.execute(mapper_result.output)
        self.results['generator'] = generator_result

        if generator_result.status != AgentStatus.SUCCESS:
            return self._build_failure_response("代码生成失败")

        # 步骤 4: 验证 (可选)
        if validate:
            validation_input = {
                'java_code': java_code,
                'python_code': generator_result.output,
                'python_structure': mapper_result.output
            }
            validator_result = self.validator_agent.execute(validation_input)
            self.results['validator'] = validator_result

        return self._build_success_response()

    def _build_success_response(self) -> Dict[str, Any]:
        """构建成功响应"""
        return {
            'success': True,
            'java_structure': self.results['parser'].output,
            'python_structure': self.results['mapper'].output,
            'python_code': self.results['generator'].output,
            'validation_report': self.results.get('validator', {}).output if 'validator' in self.results else None,
            'errors': [],
            'warnings': []
        }

    def _build_failure_response(self, reason: str) -> Dict[str, Any]:
        """构建失败响应"""
        all_errors = [reason]
        all_warnings = []

        for agent_result in self.results.values():
            all_errors.extend(agent_result.errors)
            all_warnings.extend(agent_result.warnings)

        return {
            'success': False,
            'java_structure': None,
            'python_structure': None,
            'python_code': None,
            'validation_report': None,
            'errors': all_errors,
            'warnings': all_warnings
        }

    def get_agent_statuses(self) -> Dict[str, str]:
        """获取所有 Agent 的状态"""
        return {
            'parser': self.parser_agent.status.value,
            'mapper': self.mapper_agent.status.value,
            'generator': self.generator_agent.status.value,
            'validator': self.validator_agent.status.value
        }
