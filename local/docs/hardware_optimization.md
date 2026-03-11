# RTX 4070 SUPER 硬件优化指南

本文档针对 Intel i7-14700K + NVIDIA RTX 4070 SUPER 12GB 硬件平台提供针对性的性能优化建议，帮助充分发挥硬件性能。

## 平台规格
### CPU: Intel Core i7-14700K
- 架构: Raptor Lake
- 核心: 8 性能核 (P-core) + 12 能效核 (E-core) = 20 核 28 线程
- 基础频率: P-core 3.4GHz / E-core 2.5GHz
- 睿频: 最高 5.4GHz
- 缓存: 33MB L3 + 24MB L2
- 推荐配置: 关闭超线程可获得更稳定的仿真性能

### GPU: NVIDIA RTX 4070 SUPER
- 架构: Ada Lovelace (AD104)
- CUDA 核心: 7168
- Tensor 核心: 224
- RT 核心: 56
- 显存: 12GB GDDR6X, 21Gbps, 336GB/s 带宽
- CUDA 版本: 12.6
- 驱动版本: 推荐 550.54.15 或更高
- 功耗: 220W TDP

## 系统级优化

### 1. NVIDIA 驱动优化
```bash
# 安装性能模式配置
sudo nvidia-smi -pm 1  # 启用持久模式
sudo nvidia-smi -ac 21000,2610  # 设置显存和核心频率（4070 SUPER 最大值）

# 验证设置
nvidia-smi -q | grep -E "Power Management|Applications Clocks"
```

### 2. 禁用图形界面以释放显存
如果不需要桌面环境，可以关闭 GDM 释放约 500MB 显存：
```bash
# 临时关闭
sudo systemctl stop gdm

# 永久禁用（需要时恢复）
sudo systemctl disable gdm
```

### 3. CPU 性能模式
```bash
# 安装 cpufrequtils
sudo apt install cpufrequtils

# 设置性能模式
sudo cpufreq-set -r -g performance

# 验证 CPU 频率
cat /proc/cpuinfo | grep MHz
```

### 4. 内存优化
```bash
# 提高进程优先级
echo -1 | sudo tee /proc/sys/kernel/sched_rt_runtime_us

# 禁用透明大页 (THP) 以减少延迟
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
```

## Warp 运行时优化

### 环境变量配置
在 `~/.bashrc` 中添加以下配置：
```bash
# Warp 优化
export WP_CUDA_LAUNCH_BLOCKING=0  # 禁用启动阻塞
export WP_CUDA_CACHE=1  # 启用内核缓存
export WP_CUDA_OPTIMIZE=3  # 最高优化级别
export WP_JIT_CACHE_DIR=~/.cache/warp  # 缓存编译的内核
export WP_MALLOC_ASYNC=1  # 启用异步内存分配
export WP_THREADS=20  # 设置 CPU 线程数（匹配物理核心数）

# CUDA 优化
export CUDA_MODULE_LOADING=LAZY  # 延迟加载模块
export CUDA_CACHE_MAXSIZE=2147483648  # 增加 CUDA 缓存到 2GB
export CUDA_FORCE_PTX_JIT=0  # 禁用 PTX 即时编译
```

### 内核预热
首次运行示例时 Warp 会编译内核，可能需要较长时间。运行以下命令预编译常用内核：
```bash
# 预热基础内核
uv run -m newton.examples basic_pendulum --num-frames 1 --viewer null
uv run -m newton.examples cloth_hanging --num-frames 1 --viewer null
uv run -m newton.examples mpm_granular --num-frames 1 --viewer null
```

## 示例运行优化建议

### 基础示例
- 预期帧率: 1000+ FPS
- 显存占用: < 500MB
- 优化建议: 无需特别优化，默认配置即可流畅运行

### 布料/软体示例
- 网格精度: 推荐使用 128x128 或更低分辨率
- 预期帧率: 100-500 FPS
- 显存占用: 1-4GB
- 优化建议:
  ```python
  # 减少子步数量
  sim_params.substeps = 2

  # 启用快速碰撞检测
  sim_params.collision.collision_pairs_buffer_size = 1 << 18
  ```

### MPM 示例
- 粒子数量: 推荐 <= 1M 粒子（12GB 显存最大支持约 4M 粒子）
- 预期帧率: 30-200 FPS
- 显存占用: 4-8GB
- 优化建议:
  ```python
  # 调整网格大小
  mpm_params.grid_size = 64

  # 启用 FP16 精度
  mpm_params.particle_dtype = wp.float16
  ```

### 机器人仿真示例
- 预期帧率: 100-1000 FPS
- 显存占用: < 2GB
- 优化建议:
  ```python
  # 减少关节数量或简化碰撞形状
  # 启用关节缓存
  sim_params.articulation.cache_jacobians = True
  ```

### 可微模拟示例
- 批量大小: 推荐 <= 64
- 预期帧率: 10-100 FPS
- 显存占用: 4-10GB
- 优化建议:
  ```python
  # 启用梯度检查点
  import torch
  torch.utils.checkpoint.checkpoint = True

  # 减少历史记录长度
  sim_params.max_history = 10
  ```

## 性能监控
### 实时监控 GPU 状态
```bash
# 基础监控
nvidia-smi dmon -s pucvmet

# 高级监控 (需要 nvidia-utils)
nvtop
```

### 性能基准测试
运行内置的性能测试：
```bash
# 运行所有性能基准
uv run --extra dev -m pytest newton/tests/benchmark/ -v

# 特定基准测试
uv run --extra dev -m pytest newton/tests/benchmark/test_benchmark_mpm.py -v
```

## 常见性能问题排查

### 问题：GPU 利用率低 (< 50%)
**可能原因：**
1. CPU 成为瓶颈（数据准备或后处理太慢）
2. 内核启动开销过大
3. 批量大小太小

**解决方案：**
- 增加每帧处理的工作量
- 启用异步数据传输
- 批量处理多个仿真实例

### 问题：显存不足
**可能原因：**
1. 粒子/网格数量过多
2. 保留了太多历史状态
3. 内存泄漏

**解决方案：**
- 降低仿真分辨率
- 减少历史记录长度 `sim_params.max_history`
- 显式调用 `wp.clear_cache()` 清理缓存
- 使用 `wp.device(0).reset()` 重置设备

### 问题：帧率不稳定
**可能原因：**
1. 动态功耗调整
2. 内核重新编译
3. 系统后台任务干扰

**解决方案：**
- 启用 NVIDIA 持久模式
- 预热所有用到的内核
- 关闭后台程序和系统自动更新

## RTX 4070 SUPER 最佳实践总结
✅ 优先使用 CUDA 设备，避免 CPU 仿真
✅ 预编译 Warp 内核，避免运行时编译开销
✅ 对于 12GB 显存，M PM 粒子数量控制在 1M 以内
✅ 布料网格分辨率不超过 256x256
✅ 可微仿真批量大小不超过 64
✅ 关闭不需要的 viewer 渲染功能以提高性能
✅ 定期清理 Warp 缓存避免显存泄漏

按照以上优化配置，在当前平台上可以获得最佳的仿真性能。
