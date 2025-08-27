## 使用指导（IB Analysis 工具集）

本指南涵盖安装、常用命令、各操作的示例与注意事项。命令行入口为 `iba`。

### 1. 安装与环境

```bash
# 建议使用虚拟环境
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

验证：
```bash
iba --help
iba operations
```

可选：使用非可编辑安装或构建 wheel 参见 README 的“快速安装”。

### 2. 全量命令速查（Excel）

- 打开项目根目录的 `commands_reference.csv`（可直接用 Excel 查看、筛选、排序）。
- 含所有 `iba analyze <operation>` 的参数与简述。

### 3. 通用参数（适用于大多数 analyze 命令）

- `--format|-f`: stdout|csv|html|json
- `--output|-o`: 输出文件路径（当选择 csv/html/json 时）
- `--lines|-n`: 输出行数（-1 为全部）
- `--sort|-s`: 按列序号排序（1 起；负数为降序；0 关闭）
- `--extend|-e`: 追加列（逗号分隔）。部分操作支持特殊拓展，如 `port --extend pairs`
- `--overview`: 概览
- `--check`: 异常检测
- `--plot`: 关系图/散点图（部分操作）
- `--similar COLUMN`: 查找与某列统计相近的列（部分操作）
- 过滤：`--filter-mode column|guid|smart` 与 `--filter`（见下文示例）

### 4. 各操作说明与示例

#### 4.1 xmit（传输/等待）

```bash
iba analyze xmit <ibdir> --overview
iba analyze xmit <ibdir> --check
iba analyze xmit <ibdir> --format csv --output xmit.csv
```

常用拓展列（示例）：
```bash
iba analyze xmit <ibdir> --extend "Xmit Data Gbps,Xmit Wait Gbps" --sort 3 --lines 100
```

#### 4.2 cable（线缆/光模块）

```bash
iba analyze cable <ibdir>
iba analyze cable <ibdir> --check
iba analyze cable <ibdir> --check --format csv --output cables.csv
```

- 异常包含“Optical Module Temperature High”：温度 ≥ 70°C（等于 70 也判为异常）。
- `Vendor/PN/Temperature (c)` 来自 `START_CABLE_INFO (CABLE_INFO)`。

#### 4.3 port（端口/配对视图）

```bash
# 基础
iba analyze port <ibdir>

# 配对视图（手动）
iba analyze port <ibdir> --extend pairs

# 检查模式（默认即输出“配对视图”）
iba analyze port <ibdir> --check

# 导出 CSV
iba analyze port <ibdir> --check --format csv --output ports_pairs.csv
```

行为说明：
- `Link Downed Counter 1/2` 均直接来自 `START_PM_INFO (PM_INFO)`，对两端口分别取值。
- `--check` 时默认过滤“双方计数均 > 0”的行，便于快速聚焦异常。
- `Vendor1/2` 优先来自 `CABLE_INFO`：右侧 `Vendor2` 先按右侧 `(NodeGUID_r, PortNumber_r)` 匹配，若无再回退 `(Target GUID, Target Port)`，最后才使用拓扑节点 Vendor 兜底。

#### 4.4 topo（拓扑/可视化）

```bash
iba analyze topo <ibdir>
iba analyze topo <ibdir> --format html --output network.html
```

- 无 `PM_INFO` 时自动降级为节点概览；有 `PM_INFO` 时补充邻接类型统计。
- HTML 使用 PyVis 生成，可在浏览器交互查看。

#### 4.5 hca / ber / pminfo / histogram

```bash
iba analyze hca <ibdir> --overview
iba analyze ber <ibdir> --check --format csv --output ber.csv
iba analyze pminfo <ibdir> --overview --format csv --output pminfo.csv
iba analyze histogram <ibdir> --overview --format csv --output histogram.csv
```

#### 4.6 cc（拥塞控制）

```bash
iba analyze cc <ibdir> --overview
iba analyze cc <ibdir> --format csv --output cc.csv
```

- 需要目录内存在 `.ppcc` 文件；否则无法提供 CC 计数（会提示缺失）。

#### 4.7 brief / nlastic（汇总/弹性）

```bash
iba analyze brief <ibdir>                 # 默认打印表格（前 50 行）
iba analyze brief <ibdir> --overview      # 各模块概览汇总
iba analyze brief <ibdir> --check         # 异常汇总视图
iba analyze brief <ibdir> --format csv --output brief.csv

# nlastic 当前等价于 brief（别名）
iba analyze nlastic <ibdir>
```

说明：
- `brief` 的表格默认包含 Xmit、Port/PM_INFO 关键计数、Cable（温度/厂商/PN）、CC（RTT）等跨模块字段（不存在的列会自动剔除）。
- `--overview` 会尽量拼接各模块的 `print_overview` 输出，展示多区段回显。

#### 4.8 tableau（导出到可视化）

```bash
iba analyze tableau <ibdir>
```

- 目前为占位实现（加载数据成功但不输出文件）。如需导出多个标准化 CSV（nodes/edges/ports/pminfo/cable）或 zip 包，请提出需求，我可按指定结构实现。

### 5. 过滤示例

按列过滤：
```bash
iba analyze xmit <ibdir> --filter-mode column --filter "Xmit Data Gbps" ">" 50
```

按 GUID：
```bash
iba analyze xmit <ibdir> --filter-mode guid --filter 0x1234 0x5678 0x9abc
```

智能匹配（名称/列/GUID）：
```bash
iba analyze xmit <ibdir> --filter-mode smart --filter "hostname-1" "Xmit Wait Gbps" ">" 5
```

### 6. 平台兼容与显示

- Windows：已处理 tqdm 与 Rich 的进度条兼容；如需更安静可加 `--quiet`。
- 终端颜色：已使用 Rich 渲染 ANSI；若仍出现“\x1b[xxm”裸码，请反馈终端类型与截图。

### 7. 常见问题（FAQ）

- `pip install -e .` 报未找到 `pyproject.toml`：项目已提供；若仍报错，请先 `pip install -U pip setuptools`。
- `ModuleNotFoundError: No module named 'src'`：项目已统一包路径到 `ib_analysis.*`；若旧环境缓存了老版本，请 `pip uninstall -y ib-analysis` 后重装。
- Pandas “Columns must be same length as key / Length mismatch”：项目内部已修复多处宽列赋值与形状对齐；如仍出现，请提供 traceback 与触发命令。
- `cc` 无数据：确认目录内是否存在 `.ppcc` 文件。

### 8. 建议工作流

1) `xmit --overview / --check`：扫描带宽与等待
2) `port --check`：配对视图，快速锁定 `Link Downed Counter` 异常
3) `cable --check`：检查光模块温度与厂商/PN
4) `ber --check`：检查误码
5) 汇总：`brief --overview / --check`；导出 CSV 汇总
6) 可视化：`topo --format html` 生成交互拓扑图


