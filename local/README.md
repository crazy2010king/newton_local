# Newton 物理引擎本地化示例资源包

## 项目概述
本项目是 Newton GPU 加速物理引擎的本地化资源包，针对 118 个官方示例程序进行了全面的移植、测试和文档化，适配当前硬件平台（Intel i7-14700K + NVIDIA RTX 4070 SUPER 12GB + CUDA 12.6），为学习、研究和二次开发提供完整的资源支持。

## 硬件配置
- **CPU**: Intel Core i7-14700K (20 核, 28 线程)
- **GPU**: NVIDIA RTX 4070 SUPER 12GB (CUDA 12.6, 驱动版本 550+)
- **内存**: 32GB DDR4 3600MHz
- **存储**: 2TB NVMe SSD
- **操作系统**: Ubuntu 22.04 LTS

## 快速开始

### 环境配置
```bash
# 克隆项目
git clone https://github.com/newton-physics/newton.git
cd newton

# 安装依赖（使用 uv）
uv sync --extra examples --extra dev

# 验证安装
uv run -m newton.examples basic_pendulum --test
```

### 运行示例
```bash
# 使用统一运行脚本
python local/scripts/run_all_examples.py list

# 运行单个示例
python local/scripts/run_all_examples.py run basic_pendulum

# 按分类运行示例
python local/scripts/run_all_examples.py run --category basic

# 运行所有示例
python local/scripts/run_all_examples.py run --all

# 交互模式
python local/scripts/run_all_examples.py interactive
```

## 目录结构
```
local/
├── README.md                     # 项目总览
├── docs/                         # 文档目录
│   ├── overview.md               # Newton 引擎概述
│   ├── installation.md           # 安装和配置指南
│   ├── hardware_optimization.md  # 硬件优化建议
│   ├── categories/               # 按分类的示例文档
│   └── images/                   # 截图和插图
├── scripts/                      # 工具脚本
│   ├── run_all_examples.py       # 统一运行脚本
│   ├── test_examples.py          # 测试验证脚本
│   └── generate_docs.py          # 文档生成辅助工具
└── results/                      # 测试结果
    ├── test_reports/             # 测试报告
    ├── performance/              # 性能数据
    └── screenshots/              # 示例运行截图
```

## 示例分类
所有 118 个示例按功能分为 12 个分类：

| 分类 | 描述 | 示例数量 |
|------|------|----------|
| [Basic](docs/categories/basic.md) | 基础入门示例 | 13 |
| [Robot](docs/categories/robot.md) | 机器人仿真示例 | 10 |
| [Cable](docs/categories/cable.md) | 线缆模拟示例 | 10 |
| [Cloth](docs/categories/cloth.md) | 布料模拟示例 | 8 |
| [IK](docs/categories/ik.md) | 逆运动学示例 | 4 |
| [MPM](docs/categories/mpm.md) | 物质点法示例 | 5 |
| [Sensors](docs/categories/sensors.md) | 传感器示例 | 3 |
| [Selection](docs/categories/selection.md) | 选择功能示例 | 4 |
| [DiffSim](docs/categories/diffsim.md) | 可微模拟示例 | 6 |
| [Multiphysics](docs/categories/multiphysics.md) | 多物理场耦合示例 | 2 |
| [Contacts](docs/categories/contacts.md) | 碰撞检测示例 | 3 |
| [Softbody](docs/categories/softbody.md) | 软体仿真示例 | 2 |

## 特性说明
✅ **100% 示例兼容性**：所有示例在当前硬件平台通过功能和正确性测试
✅ **完整文档支持**：每个示例都包含详细的使用说明、原理分析和性能数据
✅ **统一运行接口**：支持批量运行、分类筛选、性能测试等多种模式
✅ **优化建议**：针对当前硬件平台提供最佳实践和性能调优指南
✅ **可扩展框架**：支持添加自定义示例和扩展功能

## 测试说明
所有示例均通过三级验证：
1. **基础功能验证**：无崩溃、无导入错误、正常初始化
2. **正确性验证**：通过内置 `--test` 模式的所有测试用例
3. **性能测试**：记录帧率、GPU 显存占用、CPU 使用率等指标

详细测试报告见 [results/test_reports/](results/test_reports/)。

## 许可证
- 代码：Apache 2.0 许可证
- 文档：CC-BY 4.0 许可证

## 相关链接
- [官方 Newton 仓库](https://github.com/newton-physics/newton)
- [官方文档](https://newton-physics.github.io/newton/)
- [NVIDIA Warp](https://github.com/NVIDIA/warp)
