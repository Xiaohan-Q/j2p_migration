"""
迁移计划可视化模块
增强的迁移计划展示和进度追踪
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class VisualizationOptions:
    """可视化选项"""
    show_progress_bar: bool = True
    show_step_details: bool = True
    show_dependencies: bool = True
    show_warnings: bool = True
    show_recommendations: bool = True
    use_colors: bool = True
    export_format: str = "console"  # console, json, html, markdown


class MigrationVisualizer:
    """迁移计划可视化器"""

    def __init__(self, options: Optional[VisualizationOptions] = None):
        self.options = options or VisualizationOptions()
        self.start_time = None
        self.current_step = 0
        self.total_steps = 0

    def print_header(self, title: str):
        """打印标题"""
        separator = "=" * 80
        print(f"\n{separator}")
        print(f"  {title}")
        print(f"{separator}\n")

    def print_section(self, title: str):
        """打印章节"""
        separator = "-" * 80
        print(f"\n{separator}")
        print(f"  {title}")
        print(f"{separator}\n")

    def print_plan_summary(self, plan: Dict[str, Any]):
        """打印迁移计划摘要"""
        self.print_header("Java to Python 迁移计划")

        # 复杂度分析
        print("【复杂度分析】")
        complexity = plan.get('complexity_analysis', {})
        print(f"  • 总类数:       {complexity.get('total_classes', 0)}")
        print(f"  • 总方法数:     {complexity.get('total_methods', 0)}")
        print(f"  • 总字段数:     {complexity.get('total_fields', 0)}")
        print(f"  • 导入数:       {complexity.get('total_imports', 0)}")
        print(f"  • 包含继承:     {'是' if complexity.get('has_inheritance') else '否'}")
        print(f"  • 包含接口:     {'是' if complexity.get('has_interfaces') else '否'}")
        print(f"  • 包含泛型:     {'是' if complexity.get('has_generics') else '否'}")

        # 整体评估
        print(f"\n【整体评估】")
        print(f"  • 迁移难度:     {plan.get('estimated_difficulty', '未知')}")
        print(f"  • 总步骤数:     {plan.get('total_steps', 0)}")

        # 迁移步骤概览
        if self.options.show_step_details:
            self.print_section("迁移步骤详情")
            self._print_steps(plan.get('steps', []))

        # 建议
        if self.options.show_recommendations:
            recommendations = plan.get('recommendations', [])
            if recommendations:
                self.print_section("迁移建议")
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec}")

    def _print_steps(self, steps: List):
        """打印步骤列表"""
        for step in steps:
            complexity_emoji = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴'
            }

            emoji = complexity_emoji.get(step.complexity, '⚪')
            print(f"\n步骤 {step.step_id}: {step.description}")
            print(f"  组件:       {step.component}")
            print(f"  复杂度:     {emoji} {step.complexity}")

            if self.options.show_dependencies and step.dependencies:
                deps = ", ".join(str(d) for d in step.dependencies)
                print(f"  依赖步骤:   {deps}")

            if self.options.show_warnings and step.warnings:
                print(f"  ⚠️  警告:")
                for warning in step.warnings:
                    print(f"      • {warning}")

    def print_progress(self, current: int, total: int, description: str = ""):
        """打印进度"""
        self.current_step = current
        self.total_steps = total

        if self.options.show_progress_bar:
            percentage = (current / total * 100) if total > 0 else 0
            bar_length = 50
            filled = int(bar_length * current / total) if total > 0 else 0
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\n进度: [{bar}] {current}/{total} ({percentage:.1f}%)")
            if description:
                print(f"当前: {description}")

    def start_migration(self):
        """开始迁移"""
        self.start_time = datetime.now()
        self.print_header("开始 Java to Python 代码迁移")

    def end_migration(self, success: bool):
        """结束迁移"""
        if self.start_time:
            duration = datetime.now() - self.start_time
            duration_str = str(duration).split('.')[0]  # 去除微秒

            status = "✅ 成功" if success else "❌ 失败"
            self.print_section(f"迁移完成 - {status}")
            print(f"  总耗时: {duration_str}")

    def print_validation_summary(self, report: Dict[str, Any]):
        """打印验证摘要"""
        self.print_section("验证结果摘要")

        status_emoji = {
            'success': '✅',
            'warning': '⚠️',
            'failed': '❌'
        }

        overall_status = report.get('overall_status', 'unknown')
        emoji = status_emoji.get(overall_status, '❓')

        print(f"总体状态: {emoji} {overall_status.upper()}")

        # 检查项统计
        checks = report.get('checks', {})
        passed = sum(1 for c in checks.values() if c.get('passed', False))
        total = len(checks)

        print(f"\n检查项通过: {passed}/{total}")

        # 错误和警告统计
        errors = report.get('errors', [])
        warnings = report.get('warnings', [])

        if errors:
            print(f"❌ 错误数: {len(errors)}")
        if warnings:
            print(f"⚠️  警告数: {len(warnings)}")

    def export_plan_to_json(self, plan: Dict[str, Any], output_file: str):
        """导出计划为 JSON"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'plan': {
                'complexity_analysis': plan.get('complexity_analysis', {}),
                'estimated_difficulty': plan.get('estimated_difficulty', ''),
                'total_steps': plan.get('total_steps', 0),
                'steps': [
                    {
                        'step_id': s.step_id,
                        'description': s.description,
                        'component': s.component,
                        'complexity': s.complexity,
                        'dependencies': s.dependencies,
                        'warnings': s.warnings
                    }
                    for s in plan.get('steps', [])
                ],
                'recommendations': plan.get('recommendations', [])
            }
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"\n迁移计划已导出到: {output_file}")

    def export_plan_to_markdown(self, plan: Dict[str, Any], output_file: str):
        """导出计划为 Markdown"""
        lines = []
        lines.append("# Java to Python 迁移计划\n")

        # 复杂度分析
        lines.append("## 复杂度分析\n")
        complexity = plan.get('complexity_analysis', {})
        lines.append(f"- 总类数: {complexity.get('total_classes', 0)}")
        lines.append(f"- 总方法数: {complexity.get('total_methods', 0)}")
        lines.append(f"- 总字段数: {complexity.get('total_fields', 0)}")
        lines.append(f"- 导入数: {complexity.get('total_imports', 0)}")
        lines.append(f"- 包含继承: {'是' if complexity.get('has_inheritance') else '否'}")
        lines.append(f"- 包含接口: {'是' if complexity.get('has_interfaces') else '否'}")
        lines.append(f"- 包含泛型: {'是' if complexity.get('has_generics') else '否'}\n")

        # 整体评估
        lines.append("## 整体评估\n")
        lines.append(f"- 迁移难度: **{plan.get('estimated_difficulty', '未知')}**")
        lines.append(f"- 总步骤数: {plan.get('total_steps', 0)}\n")

        # 迁移步骤
        lines.append("## 迁移步骤\n")
        for step in plan.get('steps', []):
            lines.append(f"### 步骤 {step.step_id}: {step.description}\n")
            lines.append(f"- 组件: `{step.component}`")
            lines.append(f"- 复杂度: {step.complexity}")

            if step.dependencies:
                deps = ", ".join(str(d) for d in step.dependencies)
                lines.append(f"- 依赖步骤: {deps}")

            if step.warnings:
                lines.append("\n⚠️ **警告:**")
                for warning in step.warnings:
                    lines.append(f"  - {warning}")

            lines.append("")

        # 建议
        recommendations = plan.get('recommendations', [])
        if recommendations:
            lines.append("## 迁移建议\n")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"\n迁移计划已导出到: {output_file}")
