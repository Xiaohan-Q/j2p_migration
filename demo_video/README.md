# 演示视频脚本使用说明

## 概述

演示脚本已拆分为两部分：
- **Part 3**: 传统模式演示（仅文字说明，不执行迁移）
- **Part 4**: 智能 Agent 模式演示（模拟工作流）

## 使用方法

### 方式一：分步运行（推荐）

#### 1. 运行 Part 3 - 传统模式介绍
```bash
python demo_video/demo_script.py --part 3
```
这将显示示例 Java 代码和迁移命令，但不实际执行迁移。

#### 2. 手动运行迁移命令
在另一个终端窗口运行：
```bash
python src/main.py -i demo_video/Calculator.java -o demo_video/Calculator.py -f
```
这将实际执行迁移并显示完整的过程。

参数说明：
- `-i`: 输入 Java 文件
- `-o`: 输出 Python 文件
- `-f`: 强制覆盖已存在的文件（避免交互提示）

#### 3. 运行 Part 4 - Agent 模式演示
```bash
python demo_video/demo_script.py --part 4
```
这将展示智能 Agent 的 6 阶段工作流模拟。

### 方式二：完整演示

运行完整演示（包含所有 7 个部分）：
```bash
python demo_video/demo_script.py
```

注意：Part 3 会提示你在另一个终端运行迁移命令。

### 方式三：只运行特定部分

```bash
# Part 1 - 开场介绍
python demo_video/demo_script.py --part 1

# Part 2 - 核心功能
python demo_video/demo_script.py --part 2

# Part 5 - emoji-java 案例
python demo_video/demo_script.py --part 5

# Part 6 - 验证展示
python demo_video/demo_script.py --part 6

# Part 7 - 总结
python demo_video/demo_script.py --part 7
```

## 演示内容

### Part 1: 开场介绍
- 工具介绍
- 背景说明

### Part 2: 核心功能展示
- 双引擎系统介绍
- 传统引擎架构
- 智能 Agent 系统架构

### Part 3: 传统模式演示
- 显示示例 Java 代码
- 显示迁移命令
- 提示手动运行

### Part 4: 智能 Agent 模式
- 6 阶段工作流模拟
  1. 需求分析
  2. 架构设计
  3. 任务规划
  4. 代码生成
  5. 测试生成
  6. 代码审查

### Part 5: emoji-java 真实案例
- 项目信息
- 迁移结果统计
- 代码质量详情

### Part 6: 验证展示
- 验证工具介绍
- 验证结果展示
- 输出结构说明

### Part 7: 总结
- 核心优势
- 获取更多信息

## 注意事项

1. **编码问题已修复**: Windows 平台的 UTF-8 编码问题已解决
2. **手动运行迁移**: Part 3 不会自动运行迁移，需要在另一个终端手动执行
3. **使用 -f 参数**: 建议使用 `-f` 参数强制覆盖，避免交互提示
4. **验证步骤**: 默认会运行验证步骤，如需跳过可添加 `--no-validate` 参数

## 故障排除

如果遇到编码问题，确保：
- 使用 Python 3.6+
- Windows 终端已设置为 UTF-8 编码
- 或运行 `chcp 65001` 切换到 UTF-8 代码页

## 输出文件

运行演示后会生成：
- `demo_video/Calculator.java` - 示例 Java 文件
- `demo_video/Calculator.py` - 迁移生成的 Python 文件（手动运行迁移后）
