# 安装和环境配置指南

## 系统要求
### 最低配置
- **CPU**: x86_64 架构，4 核以上
- **GPU**: NVIDIA Maxwell 架构以上，显存 4GB+
- **驱动**: 版本 545+ (支持 CUDA 12)
- **内存**: 16GB+
- **存储**: 50GB 可用空间
- **操作系统**: Linux (Ubuntu 20.04+/Fedora 36+) / Windows 10+ / macOS (CPU 仅支持)

### 推荐配置 (当前测试平台)
- **CPU**: Intel Core i7-14700K (20 核)
- **GPU**: NVIDIA RTX 4070 SUPER 12GB
- **驱动**: 550.54.15 (CUDA 12.6)
- **内存**: 32GB DDR4 3600MHz
- **存储**: 2TB NVMe SSD
- **操作系统**: Ubuntu 22.04 LTS

## 安装步骤

### 1. 安装 NVIDIA 驱动和 CUDA
#### Ubuntu 系统
```bash
# 添加 NVIDIA 驱动 PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# 安装推荐驱动
sudo ubuntu-drivers autoinstall

# 重启系统
sudo reboot

# 验证驱动安装
nvidia-smi
```

预期输出应显示 NVIDIA 驱动版本 >= 545，CUDA 版本 >= 12.0。

#### CUDA 工具包 (可选)
Newton 自带 Warp 运行时，不需要单独安装 CUDA 工具包，但如果需要开发自定义内核，可以安装：
```bash
# 安装 CUDA 12.6
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-12-6

# 添加到环境变量
echo 'export PATH=/usr/local/cuda-12.6/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 验证 CUDA 安装
nvcc --version
```

### 2. 安装 Python 环境
推荐使用 Python 3.10 - 3.13 版本：
```bash
# Ubuntu 安装 Python
sudo apt install python3.10 python3.10-venv python3.10-dev

# 验证 Python 版本
python3.10 --version
```

### 3. 安装 uv 包管理器
uv 是高性能的 Python 包管理器，比 pip 快 10-100 倍：
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uv --version
```

### 4. 克隆 Newton 仓库
```bash
git clone https://github.com/newton-physics/newton.git
cd newton
```

### 5. 创建虚拟环境并安装依赖
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装核心依赖和示例依赖
uv sync --extra examples --extra dev

# 验证安装
uv run -m newton.examples basic_pendulum --test
```

如果看到测试通过的输出，说明安装成功。

### 可选：安装 PyTorch 支持
对于需要 PyTorch 的示例（如强化学习策略），安装 PyTorch：
```bash
# CUDA 12
uv sync --extra torch-cu12

# CUDA 13
uv sync --extra torch-cu13
```

## 常见问题

### Q: 运行示例时出现 "CUDA out of memory" 错误
**A:**
1. 关闭其他占用 GPU 显存的程序
2. 减小示例中的分辨率、粒子数量或网格精度
3. 尝试使用 CPU 运行：`--device cpu` 参数

### Q: 运行 viewer 时出现 OpenGL 错误
**A:**
1. 确保安装了最新的显卡驱动
2. Ubuntu 系统安装 mesa 依赖：
   ```bash
   sudo apt install libgl1-mesa-glx libgl1-mesa-dri
   ```
3. 尝试使用其他 viewer：`--viewer rerun` 或 `--viewer null`

### Q: 导入错误 "No module named 'xxx'"
**A:**
1. 确保已经激活虚拟环境：`source .venv/bin/activate`
2. 重新安装依赖：`uv sync --extra examples --extra dev`
3. 检查 Python 版本是否符合要求：`python --version`

### Q: USD 导入导出功能不可用
**A:**
1. USD 仅支持 Python < 3.14 版本
2. 确保安装了 usd-core 包：`uv add usd-core>=25.5`
3. ARM 架构系统使用 usd-exchange 包替代

### Q: 示例运行卡顿或帧率低
**A:**
参考 [硬件优化指南](hardware_optimization.md) 进行性能调优。

## 验证安装成功
运行以下命令验证所有组件正常工作：
```bash
# 列出示例
uv run -m newton.examples

# 运行基础摆示例
uv run -m newton.examples basic_pendulum --num-frames 100 --viewer null

# 运行测试
uv run -m newton.tests -k test_basic_pendulum
```

如果所有命令都成功执行，说明环境配置完成。
