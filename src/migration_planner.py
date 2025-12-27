"""
迁移策略规划模块
分析 Java 代码结构并生成迁移计划
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MigrationStep:
    """迁移步骤"""
    step_id: int
    description: str
    component: str  # 组件类型: class, method, field, etc.
    complexity: str  # 复杂度: low, medium, high
    dependencies: List[int]  # 依赖的步骤ID
    warnings: List[str]  # 警告信息


class MigrationPlanner:
    """迁移策略规划器"""

    def __init__(self):
        self.migration_plan = []
        self.step_counter = 0

    def analyze_complexity(self, java_structure: Dict[str, Any]) -> Dict[str, int]:
        """
        分析代码复杂度

        Args:
            java_structure: Java 代码结构

        Returns:
            复杂度统计信息
        """
        complexity = {
            'total_classes': 0,
            'total_methods': 0,
            'total_fields': 0,
            'total_imports': len(java_structure.get('imports', [])),
            'has_inheritance': False,
            'has_interfaces': False,
            'has_generics': False,
        }

        for cls in java_structure.get('classes', []):
            complexity['total_classes'] += 1
            complexity['total_methods'] += len(cls.get('methods', []))
            complexity['total_fields'] += len(cls.get('fields', []))

            if cls.get('extends'):
                complexity['has_inheritance'] = True
            if cls.get('implements'):
                complexity['has_interfaces'] = True

            # 检查泛型
            for method in cls.get('methods', []):
                for param in method.get('parameters', []):
                    if '<' in param.get('type', ''):
                        complexity['has_generics'] = True

        return complexity

    def create_step(self, description: str, component: str,
                    complexity: str = 'medium', dependencies: List[int] = None,
                    warnings: List[str] = None) -> MigrationStep:
        """创建迁移步骤"""
        self.step_counter += 1
        return MigrationStep(
            step_id=self.step_counter,
            description=description,
            component=component,
            complexity=complexity,
            dependencies=dependencies or [],
            warnings=warnings or []
        )

    def plan_imports_migration(self, java_structure: Dict[str, Any]) -> List[MigrationStep]:
        """规划导入语句迁移"""
        steps = []
        imports = java_structure.get('imports', [])

        if imports:
            warnings = []
            if any('java.io' in imp for imp in imports):
                warnings.append('Java IO 操作需要手动检查和调整')
            if any('javax' in imp for imp in imports):
                warnings.append('javax 包可能需要寻找 Python 等价库')

            step = self.create_step(
                description=f"迁移 {len(imports)} 个导入语句",
                component="imports",
                complexity="low",
                warnings=warnings
            )
            steps.append(step)

        return steps

    def plan_class_migration(self, class_info: Dict[str, Any],
                            import_step_id: Optional[int]) -> List[MigrationStep]:
        """规划单个类的迁移"""
        steps = []
        class_name = class_info['name']
        dependencies = [import_step_id] if import_step_id else []

        # 分析类复杂度
        warnings = []
        complexity = "low"

        if class_info.get('extends'):
            warnings.append(f"类继承自 {class_info['extends']},需要确保父类已迁移")
            complexity = "medium"

        if class_info.get('implements'):
            interfaces = ', '.join(class_info['implements'])
            warnings.append(f"实现了接口: {interfaces},Python 中使用抽象基类")
            complexity = "medium"

        if len(class_info.get('methods', [])) > 10:
            warnings.append("类包含大量方法,建议分阶段迁移")
            complexity = "high"

        # 创建类定义迁移步骤
        class_step = self.create_step(
            description=f"迁移类 {class_name} 的定义和结构",
            component="class",
            complexity=complexity,
            dependencies=dependencies,
            warnings=warnings
        )
        steps.append(class_step)

        # 规划字段迁移
        if class_info.get('fields'):
            field_warnings = []
            for field in class_info['fields']:
                if 'static' in field.get('modifiers', []) and 'final' in field.get('modifiers', []):
                    field_warnings.append(f"常量字段 {field['name']} 将转换为大写命名")

            field_step = self.create_step(
                description=f"迁移类 {class_name} 的 {len(class_info['fields'])} 个字段",
                component="fields",
                complexity="low",
                dependencies=[class_step.step_id],
                warnings=field_warnings
            )
            steps.append(field_step)

        # 规划构造函数迁移
        if class_info.get('constructors'):
            constructor_step = self.create_step(
                description=f"迁移类 {class_name} 的构造函数为 __init__",
                component="constructor",
                complexity="medium",
                dependencies=[class_step.step_id],
                warnings=["Java 构造函数重载将合并为一个 __init__ 方法"]
            )
            steps.append(constructor_step)

        # 规划方法迁移
        if class_info.get('methods'):
            method_warnings = []
            for method in class_info['methods']:
                if 'static' in method.get('modifiers', []):
                    method_warnings.append(f"静态方法 {method['name']} 将添加 @staticmethod 装饰器")

            method_step = self.create_step(
                description=f"迁移类 {class_name} 的 {len(class_info['methods'])} 个方法",
                component="methods",
                complexity="medium",
                dependencies=[class_step.step_id],
                warnings=method_warnings
            )
            steps.append(method_step)

        return steps

    def plan_migration(self, java_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成完整的迁移计划

        Args:
            java_structure: Java 代码结构

        Returns:
            完整的迁移计划
        """
        self.migration_plan = []
        self.step_counter = 0

        # 分析复杂度
        complexity = self.analyze_complexity(java_structure)

        # 1. 规划导入迁移
        import_steps = self.plan_imports_migration(java_structure)
        self.migration_plan.extend(import_steps)
        import_step_id = import_steps[0].step_id if import_steps else None

        # 2. 规划每个类的迁移
        for class_info in java_structure.get('classes', []):
            class_steps = self.plan_class_migration(class_info, import_step_id)
            self.migration_plan.extend(class_steps)

        # 生成迁移计划报告
        plan_report = {
            'complexity_analysis': complexity,
            'total_steps': len(self.migration_plan),
            'steps': self.migration_plan,
            'estimated_difficulty': self._estimate_difficulty(complexity),
            'recommendations': self._generate_recommendations(complexity)
        }

        return plan_report

    def _estimate_difficulty(self, complexity: Dict[str, int]) -> str:
        """评估整体迁移难度"""
        score = 0

        if complexity['total_classes'] > 5:
            score += 2
        if complexity['total_methods'] > 20:
            score += 2
        if complexity['has_inheritance']:
            score += 1
        if complexity['has_interfaces']:
            score += 1
        if complexity['has_generics']:
            score += 1

        if score <= 2:
            return "简单"
        elif score <= 5:
            return "中等"
        else:
            return "复杂"

    def _generate_recommendations(self, complexity: Dict[str, int]) -> List[str]:
        """生成迁移建议"""
        recommendations = []

        if complexity['total_classes'] > 3:
            recommendations.append("建议按类分批迁移,逐步测试验证")

        if complexity['has_inheritance']:
            recommendations.append("先迁移父类,再迁移子类以保证继承关系正确")

        if complexity['has_interfaces']:
            recommendations.append("使用 Python 的 abc 模块实现抽象基类")

        if complexity['has_generics']:
            recommendations.append("使用 typing 模块提供类型注解")

        if complexity['total_imports'] > 10:
            recommendations.append("仔细检查第三方库依赖,寻找 Python 等价库")

        return recommendations

    def print_plan(self, plan: Dict[str, Any]) -> None:
        """打印迁移计划"""
        print("\n" + "="*60)
        print("Java to Python 迁移计划")
        print("="*60)

        print("\n【复杂度分析】")
        for key, value in plan['complexity_analysis'].items():
            print(f"  {key}: {value}")

        print(f"\n【整体难度】{plan['estimated_difficulty']}")
        print(f"【总步骤数】{plan['total_steps']}")

        print("\n【迁移步骤】")
        for step in plan['steps']:
            print(f"\n步骤 {step.step_id}: {step.description}")
            print(f"  组件: {step.component}")
            print(f"  复杂度: {step.complexity}")
            if step.dependencies:
                print(f"  依赖步骤: {step.dependencies}")
            if step.warnings:
                print(f"  ⚠️  警告:")
                for warning in step.warnings:
                    print(f"    - {warning}")

        print("\n【建议】")
        for i, rec in enumerate(plan['recommendations'], 1):
            print(f"  {i}. {rec}")

        print("\n" + "="*60)


# 向后兼容的函数接口
def plan_migration(java_code: str) -> str:
    """
    基于 Java 代码生成迁移步骤 (兼容旧接口)

    Args:
        java_code: Java 源代码

    Returns:
        迁移步骤描述
    """
    steps = []
    if "public class" in java_code:
        steps.append("迁移类结构")
    if "System.out.println" in java_code:
        steps.append("迁移输出语句")
    if "public static void main" in java_code:
        steps.append("迁移主函数")

    return "迁移步骤: " + ", ".join(steps) if steps else "无需迁移"
