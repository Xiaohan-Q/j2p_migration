# 快速开始指南

## 🎯 演示视频录制流程

### 步骤 1: 运行第一部分演示（传统模式介绍）
```bash
python demo_video/demo_script.py --part 3
```
这会显示：
- 📄 示例 Java 代码
- ⚙️ 迁移命令提示

### 步骤 2: 在另一个终端运行实际迁移
```bash
python src/main.py -i demo_video/Calculator.java -o demo_video/Calculator.py -f
```
这会显示：
- ℹ️ 步骤进度（1/5 到 5/5）
- ✅ 成功消息
- 📊 验证报告

### 步骤 3: 运行第二部分演示（Agent 模式）
```bash
python demo_video/demo_script.py --part 4
```
这会展示：
- 🤖 6 阶段工作流
- ✅ 各阶段完成状态

## 📝 完整命令参考

### 演示脚本
```bash
# 完整演示（所有 7 部分）
python demo_video/demo_script.py

# 单独部分
python demo_video/demo_script.py --part 1  # 开场介绍
python demo_video/demo_script.py --part 2  # 核心功能
python demo_video/demo_script.py --part 3  # 传统模式
python demo_video/demo_script.py --part 4  # Agent 模式
python demo_video/demo_script.py --part 5  # emoji-java 案例
python demo_video/demo_script.py --part 6  # 验证展示
python demo_video/demo_script.py --part 7  # 总结
```

### 迁移工具
```bash
# 基本用法
python src/main.py -i <输入文件> -o <输出文件>

# 强制覆盖
python src/main.py -i <输入文件> -o <输出文件> -f

# 详细输出
python src/main.py -i <输入文件> -o <输出文件> -v

# 跳过验证
python src/main.py -i <输入文件> -o <输出文件> --no-validate

# 显示迁移计划
python src/main.py -i <输入文件> --show-plan

# 组合参数
python src/main.py -i <输入文件> -o <输出文件> -f -v
```

## 🎬 录制建议

### 屏幕布局
- **左侧**: 运行 Part 3 和 Part 4 演示脚本
- **右侧**: 运行实际迁移命令

### 录制顺序
1. 录制 Part 1 和 Part 2（介绍部分）
2. 录制 Part 3（传统模式介绍）
3. 切换到另一个终端，录制实际迁移过程
4. 录制 Part 4（Agent 模式演示）
5. 录制 Part 5-7（案例和总结）

### 时间控制
- Part 1: ~30 秒
- Part 2: ~45 秒
- Part 3: ~20 秒
- 实际迁移: ~5 秒
- Part 4: ~20 秒
- Part 5: ~45 秒
- Part 6: ~30 秒
- Part 7: ~30 秒

**总时长**: 约 3.5-4 分钟

## ⚡ 常见问题

### Q: 为什么 Part 3 不直接运行迁移？
A: 为了避免 subprocess 超时问题，将演示和实际执行分离，你可以在另一个终端手动控制。

### Q: 如何加快演示速度？
A: 使用 `--no-validate` 跳过验证步骤，可将迁移时间从 5 秒减少到 1 秒。

### Q: 可以修改暂停时间吗？
A: 可以，编辑 `demo_script.py` 中的 `pause()` 调用参数。

### Q: 如何清理生成的文件？
A: 运行 `del demo_video\Calculator.py` (Windows) 或 `rm demo_video/Calculator.py` (Unix)

## 🔧 故障排除

### 编码错误
如果看到乱码或编码错误：
```bash
# Windows
chcp 65001

# 或者使用 Python 直接设置
set PYTHONIOENCODING=utf-8
```

### 文件已存在
始终使用 `-f` 参数避免交互提示：
```bash
python src/main.py -i demo_video/Calculator.java -o demo_video/Calculator.py -f
```

### 超时问题
如果迁移超时，使用 `--no-validate`:
```bash
python src/main.py -i demo_video/Calculator.java -o demo_video/Calculator.py -f --no-validate
```
