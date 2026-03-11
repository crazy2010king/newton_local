# 基础示例 (Basic)

基础示例包含 Newton 物理引擎的核心入门示例，帮助用户快速了解基本功能和使用方法。

## 示例列表

### 1. basic_pendulum (基础摆)
**功能：** 最简单的单摆示例，演示刚体、关节和基本仿真流程
**运行命令：**
```bash
uv run -m newton.examples basic_pendulum
```
**要点：**
- 创建单个刚体和旋转关节
- 演示基本的仿真循环
- 理解关节参数和约束设置
**预期效果：** 单摆在重力作用下往复摆动，无阻力时持续摆动。

### 2. basic_urdf (URDF 导入)
**功能：** 演示如何导入 URDF 机器人模型
**运行命令：**
```bash
uv run -m newton.examples basic_urdf
```
**要点：**
- URDF 文件加载和解析
- 铰接体 (Articulation) 创建
- 关节控制和驱动
**预期效果：** 加载并显示简单的 URDF 机器人模型，关节按预设轨迹运动。

### 3. basic_viewer (查看器基础)
**功能：** 演示查看器的基本使用和自定义渲染
**运行命令：**
```bash
uv run -m newton.examples basic_viewer
```
**要点：**
- 查看器 UI 交互
- 自定义几何渲染
- 调试可视化功能
**预期效果：** 显示基本的 3D 场景，支持鼠标交互、视角控制。

### 4. basic_shapes (基本形状)
**功能：** 演示所有支持的基本几何形状
**运行命令：**
```bash
uv run -m newton.examples basic_shapes
```
**要点：**
- 球体、盒子、胶囊、平面、圆柱体等基本形状
- 碰撞形状设置
- 材质参数调整
**预期效果：** 显示各种基本几何形状，演示不同形状的碰撞和物理特性。

### 5. basic_joints (关节类型)
**功能：** 演示所有支持的关节类型
**运行命令：**
```bash
uv run -m newton.examples basic_joints
```
**要点：**
- 旋转关节、滑动关节、球关节、固定关节等
- 关节限位和阻尼设置
- 关节驱动参数
**预期效果：** 展示各种关节类型的运动特性，每个关节按各自自由度运动。

### 6. basic_conveyor (传送带)
**功能：** 演示传送带效果的实现
**运行命令：**
```bash
uv run -m newton.examples basic_conveyor
```
**要点：**
- 自定义接触表面速度
- 物体输送效果
- 碰撞过滤设置
**预期效果：** 传送带上的物体被自动向前输送，演示特殊碰撞表面特性。

### 7. basic_heightfield (高度场)
**功能：** 演示高度场地形的使用
**运行命令：**
```bash
uv run -m newton.examples basic_heightfield
```
**要点：**
- 高度场数据创建
- 地形碰撞检测
- 高度场渲染
**预期效果：** 随机生成的地形上，小球在起伏的地形上滚动。

### 8. recording (录制功能)
**功能：** 演示仿真过程的录制和回放
**运行命令：**
```bash
uv run -m newton.examples recording
```
**要点：**
- 仿真状态录制
- 二进制录制格式
- 高效数据存储
**预期效果：** 录制摆的运动过程，生成录制文件。

### 9. replay_viewer (回放查看器)
**功能：** 演示录制文件的回放
**运行命令：**
```bash
uv run -m newton.examples replay_viewer
```
**要点：**
- 录制文件加载
- 回放控制（播放、暂停、快进）
- 时间轴导航
**预期效果：** 回放之前录制的仿真过程，支持交互控制。

## 性能数据 (RTX 4070 SUPER)
| 示例 | 帧率 (FPS) | 显存占用 | CPU 使用率 |
|------|-----------|---------|-----------|
| basic_pendulum | 1200+ | <100MB | <5% |
| basic_shapes | 800+ | <200MB | <10% |
| basic_joints | 600+ | <200MB | <10% |
| basic_heightfield | 500+ | <300MB | <15% |

## 学习路径
1. 从 `basic_pendulum` 开始，理解 Newton 基本架构
2. 学习 `basic_shapes` 和 `basic_joints` 掌握基本组件
3. 尝试 `basic_viewer` 了解可视化和交互
4. 逐步学习更复杂的示例
