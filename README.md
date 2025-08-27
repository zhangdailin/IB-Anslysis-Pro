## IB Analysis — InfiniBand 网络诊断分析工具

现代化的 InfiniBand 网络诊断分析工具集，用于解析与分析 ibdiagnet 导出数据，提供概览、异常检测、过滤、可视化与多种格式导出。命令行入口为 `iba`，支持 Windows、Linux、macOS。

### 快速安装
```bash
# 建议使用虚拟环境（示例）
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

### 快速开始
```bash
iba operations                   # 列出所有操作
iba analyze xmit /path/to/ib --overview
iba analyze cable /path/to/ib --check --format csv --output cables.csv
iba analyze port  /path/to/ib --check --format csv --output ports_pairs.csv
iba analyze topo  /path/to/ib --format html --output network.html
```

### 文档导航
- 安装与环境：见上
- 全量命令与参数速查：见项目根目录 `commands_reference.csv`（可用 Excel 打开）
- 典型用法摘要：
  - `cable --check` 含温度异常（Optical Module Temperature High，≥ 70°C）
  - `port --check` 默认输出“成对视图”，并过滤“两侧 Link Downed Counter 均 > 0”的行；`Vendor1/2` 优先来自 `CABLE_INFO`
  - `topo` 可导出 HTML 拓扑图

### 许可证
MIT，见 `LICENSE`。


