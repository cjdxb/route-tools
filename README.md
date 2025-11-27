# BGP/IP 路由工具集 | Route Tools

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

A Python toolkit for generating router configuration scripts, supporting IP CIDR data from multiple sources and generating configuration scripts for RouterOS (MikroTik), BIRD, iKuai, and other routers.

### ✨ Features

- 🌐 **Multiple Data Sources**
  - Google Services and Google Cloud IP ranges
  - AWS IP ranges
  - APNIC delegated data (by country/region)
  - Clang China IP data source
  
- 🔧 **Multiple Router Output Formats**
  - RouterOS (MikroTik) address list scripts
  - BIRD routing configuration
  - iKuai router IP lists

- 📡 **IPv4 and IPv6 Dual-Stack Support**

- 🧮 **IP Address Calculation**
  - CIDR complement calculation
  - Public/private address detection
  - Address formatting and validation

### 📦 Installation

#### Requirements

- Python >= 3.8

#### Install dependencies with pip

```bash
pip install -r requirements.txt
```

#### Dependencies

- `chardet` - Character encoding detection
- `IPy` - IP address handling
- `loguru` - Logging
- `requests` - HTTP requests
- `netaddr` - Network address manipulation

### 🚀 Quick Start

#### Command Line Tools

The project provides a unified command-line tool `main.py` with subcommands:

```bash
# Show help
python main.py --help

# Or use entry point after installation
bgp-tools --help
```

##### 1. Generate Google Service IP Script

```bash
python main.py google
python main.py google -o output.rsc -l MY-LIST
```

Generates a RouterOS script for Google service IPv4 addresses.

##### 2. Generate Global Route Script (Non-China IP)

```bash
python main.py global
python main.py global -o output.rsc -l MY-LIST
```

Generates a RouterOS script for non-China IPv4 CIDR.

##### 3. Generate Direct Connection Rules Script

```bash
python main.py direct
python main.py direct -o output.rsc -l MY-LIST -x /path/to/xshell/config
```

Generates a RouterOS script containing direct connection rules for China IP, server IP, Google services, etc.

##### Common Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file path |
| `-l, --list` | Address list name |
| `-v, --verbose` | Show detailed logs |
| `-q, --quiet` | Quiet mode, show errors only |

### 📁 Project Structure

```
route-tools/
├── main.py                # Main entry point (unified CLI)
├── config.py              # Global configuration
├── generator/             # Configuration generator module
│   ├── ros.py            # RouterOS script generation
│   ├── bird.py           # BIRD configuration generation
│   └── ikuai.py          # iKuai configuration generation
├── source/                # Data source module
│   ├── apnic.py          # APNIC data source
│   ├── aws.py            # AWS IP ranges
│   ├── clang.py          # Clang China IP data source
│   ├── google.py         # Google IP ranges
│   └── xshell.py         # Xshell configuration reader
├── utils/                 # Utility module
│   ├── data.py           # Data processing utilities
│   ├── http.py           # HTTP request utilities
│   ├── ip.py             # IP address processing utilities
│   └── number.py         # Number utility functions
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependency list
└── LICENSE               # MIT License
```

### 📖 Module Documentation

#### Data Sources (source/)

| Module | Function | Data Source |
|--------|----------|-------------|
| `apnic.py` | Fetch APNIC allocated IP data | ftp.apnic.net |
| `aws.py` | Fetch AWS IP ranges | ip-ranges.amazonaws.com |
| `clang.py` | Fetch China IP CIDR | ispip.clang.cn |
| `google.py` | Fetch Google service/cloud IP | gstatic.com |
| `xshell.py` | Read server IP from Xshell config | Local files |

#### Configuration Generators (generator/)

| Module | Function | Output Format |
|--------|----------|---------------|
| `ros.py` | RouterOS address list script | `.rsc` script |
| `bird.py` | BIRD routing configuration | Config file |
| `ikuai.py` | iKuai IP list | Text list |

#### Utility Modules (utils/)

| Module | Function |
|--------|----------|
| `ip.py` | IP/CIDR validation, formatting, complement calculation |
| `http.py` | HTTP request wrapper |
| `number.py` | Number utility functions |
| `data.py` | Data processing utilities |

### 💡 Usage Examples

#### Get China IP CIDR

```python
from source.clang import get_cn_cidr, get_non_cn_cidr

# Get China IPv4 CIDR
cn_cidrs = get_cn_cidr()

# Get non-China IPv4 CIDR (complement)
non_cn_cidrs = get_non_cn_cidr()
```

#### Get Google Service IP

```python
from source.google import get_google_service_cidr, get_google_cloud_cidr

# Get Google service IPv4
google_ipv4 = list(get_google_service_cidr('ipv4'))

# Get Google Cloud specific region IPv4
asia_ipv4 = list(get_google_cloud_cidr('ipv4', scope='asia-east1'))
```

#### Get AWS IP Ranges

```python
from source.aws import get_aws_cidr

# Get all AWS IPv4
aws_ipv4 = list(get_aws_cidr('ipv4'))

# Get specific region
us_east_ipv4 = list(get_aws_cidr('ipv4', region='us-east-1'))
```

#### Generate RouterOS Script

```python
from generator.ros import generate_ros_script, generate_ros_ipv6_script

# Generate IPv4 address list script
generate_ros_script(cidrs, 'my-address-list', 'output.rsc')

# Generate IPv6 address list script
generate_ros_ipv6_script(cidrs_v6, 'my-v6-list', 'output-v6.rsc')
```

#### Generate BIRD Route Configuration

```python
from generator.bird import generate_bird_route

generate_bird_route(cidrs, '192.168.1.1', 'routes.conf')
```

#### IP Address Tools

```python
from utils.ip import is_ipv4, is_ipv4_cidr, is_public_ipv4, get_opposite_cidr

# Validate IP address
is_ipv4('192.168.1.1')  # True

# Validate CIDR
is_ipv4_cidr('192.168.0.0/24')  # True

# Check if public IP
is_public_ipv4('8.8.8.8')  # True

# Calculate CIDR complement
opposite = get_opposite_cidr(['192.168.0.0/16', '10.0.0.0/8'])
```

### ⚙️ Configuration

Edit `config.py` to customize:

- HTTP request timeout
- Data source URLs
- Custom excluded IP addresses
- Log level and format

```python
# HTTP configuration
HTTP_TIMEOUT = 30

# Custom excluded IP addresses
CUSTOMER_EXCLUDE_IPS = [
    '216.218.221.6',
    '216.218.221.42',
]
```

### 🛠️ Development

#### Install development dependencies

```bash
pip install -e ".[dev]"
```

#### Run tests

```bash
pytest
```

#### Code formatting

```bash
black .
isort .
```

### 📄 License

This project is open-sourced under the [MIT License](LICENSE).

### 🤝 Contributing

Issues and Pull Requests are welcome!

---

<a name="中文"></a>
## 中文

一个用于生成各种路由器配置脚本的 Python 工具集，支持从多种数据源获取 IP CIDR 信息，并生成 RouterOS (MikroTik)、BIRD、iKuai 等路由器的配置脚本。

### ✨ 功能特性

- 🌐 **多数据源支持**
  - Google 服务和 Google Cloud IP 范围
  - AWS IP 范围
  - APNIC 分配数据（按国家/地区）
  - Clang 中国 IP 数据源
  
- 🔧 **多路由器格式输出**
  - RouterOS (MikroTik) 地址列表脚本
  - BIRD 路由配置
  - iKuai 路由器 IP 列表

- 📡 **IPv4 和 IPv6 双栈支持**

- 🧮 **IP 地址计算**
  - CIDR 补集计算
  - 公网/私网地址判断
  - 地址格式化和验证

### 📦 安装

#### 环境要求

- Python >= 3.8

#### 使用 pip 安装依赖

```bash
pip install -r requirements.txt
```

#### 依赖包

- `chardet` - 字符编码检测
- `IPy` - IP 地址处理
- `loguru` - 日志记录
- `requests` - HTTP 请求
- `netaddr` - 网络地址处理

### 🚀 快速开始

#### 命令行工具

项目提供统一的命令行工具 `main.py`，通过子命令区分不同功能：

```bash
# 显示帮助
python main.py --help

# 安装后可使用入口点
bgp-tools --help
```

##### 1. 生成 Google 服务 IP 脚本

```bash
python main.py google
python main.py google -o output.rsc -l MY-LIST
```

生成 Google 服务 IPv4 地址的 RouterOS 脚本。

##### 2. 生成全球路由脚本（非中国 IP）

```bash
python main.py global
python main.py global -o output.rsc -l MY-LIST
```

生成非中国 IPv4 CIDR 的 RouterOS 脚本。

##### 3. 生成直连规则脚本

```bash
python main.py direct
python main.py direct -o output.rsc -l MY-LIST -x /path/to/xshell/config
```

生成包含中国 IP、服务器 IP、Google 服务等直连规则的 RouterOS 脚本。

##### 通用选项

| 选项 | 说明 |
|------|------|
| `-o, --output` | 输出文件路径 |
| `-l, --list` | 地址列表名称 |
| `-v, --verbose` | 显示详细日志 |
| `-q, --quiet` | 静默模式，只显示错误 |

### 📁 项目结构

```
route-tools/
├── main.py                # 主入口文件（统一 CLI）
├── config.py              # 全局配置文件
├── generator/             # 配置生成器模块
│   ├── ros.py            # RouterOS 脚本生成
│   ├── bird.py           # BIRD 配置生成
│   └── ikuai.py          # iKuai 配置生成
├── source/                # 数据源模块
│   ├── apnic.py          # APNIC 数据源
│   ├── aws.py            # AWS IP 范围
│   ├── clang.py          # Clang 中国 IP 数据源
│   ├── google.py         # Google IP 范围
│   └── xshell.py         # Xshell 配置读取
├── utils/                 # 工具模块
│   ├── data.py           # 数据处理工具
│   ├── http.py           # HTTP 请求工具
│   ├── ip.py             # IP 地址处理工具
│   └── number.py         # 数值处理工具
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
└── LICENSE               # MIT 许可证
```

### 📖 模块说明

#### 数据源 (source/)

| 模块 | 功能 | 数据源 |
|------|------|--------|
| `apnic.py` | 获取 APNIC 分配的 IP 数据 | ftp.apnic.net |
| `aws.py` | 获取 AWS IP 范围 | ip-ranges.amazonaws.com |
| `clang.py` | 获取中国 IP CIDR | ispip.clang.cn |
| `google.py` | 获取 Google 服务/云 IP | gstatic.com |
| `xshell.py` | 从 Xshell 配置读取服务器 IP | 本地文件 |

#### 配置生成器 (generator/)

| 模块 | 功能 | 输出格式 |
|------|------|----------|
| `ros.py` | RouterOS 地址列表脚本 | `.rsc` 脚本 |
| `bird.py` | BIRD 路由配置 | 配置文件 |
| `ikuai.py` | iKuai IP 列表 | 文本列表 |

#### 工具模块 (utils/)

| 模块 | 功能 |
|------|------|
| `ip.py` | IP/CIDR 验证、格式化、补集计算 |
| `http.py` | HTTP 请求封装 |
| `number.py` | 数值工具函数 |
| `data.py` | 数据处理工具 |

### 💡 使用示例

#### 获取中国 IP CIDR

```python
from source.clang import get_cn_cidr, get_non_cn_cidr

# 获取中国 IPv4 CIDR
cn_cidrs = get_cn_cidr()

# 获取非中国 IPv4 CIDR（补集）
non_cn_cidrs = get_non_cn_cidr()
```

#### 获取 Google 服务 IP

```python
from source.google import get_google_service_cidr, get_google_cloud_cidr

# 获取 Google 服务 IPv4
google_ipv4 = list(get_google_service_cidr('ipv4'))

# 获取 Google Cloud 特定区域 IPv4
asia_ipv4 = list(get_google_cloud_cidr('ipv4', scope='asia-east1'))
```

#### 获取 AWS IP 范围

```python
from source.aws import get_aws_cidr

# 获取 AWS 所有 IPv4
aws_ipv4 = list(get_aws_cidr('ipv4'))

# 获取特定区域
us_east_ipv4 = list(get_aws_cidr('ipv4', region='us-east-1'))
```

#### 生成 RouterOS 脚本

```python
from generator.ros import generate_ros_script, generate_ros_ipv6_script

# 生成 IPv4 地址列表脚本
generate_ros_script(cidrs, 'my-address-list', 'output.rsc')

# 生成 IPv6 地址列表脚本
generate_ros_ipv6_script(cidrs_v6, 'my-v6-list', 'output-v6.rsc')
```

#### 生成 BIRD 路由配置

```python
from generator.bird import generate_bird_route

generate_bird_route(cidrs, '192.168.1.1', 'routes.conf')
```

#### IP 地址工具

```python
from utils.ip import is_ipv4, is_ipv4_cidr, is_public_ipv4, get_opposite_cidr

# 验证 IP 地址
is_ipv4('192.168.1.1')  # True

# 验证 CIDR
is_ipv4_cidr('192.168.0.0/24')  # True

# 检查是否为公网 IP
is_public_ipv4('8.8.8.8')  # True

# 计算 CIDR 补集
opposite = get_opposite_cidr(['192.168.0.0/16', '10.0.0.0/8'])
```

### ⚙️ 配置

编辑 `config.py` 文件可以自定义：

- HTTP 请求超时时间
- 数据源 URL
- 自定义排除的 IP 地址
- 日志级别和格式

```python
# HTTP 配置
HTTP_TIMEOUT = 30

# 自定义排除的 IP 地址
CUSTOMER_EXCLUDE_IPS = [
    '216.218.221.6',
    '216.218.221.42',
]
```

### 🛠️ 开发

#### 安装开发依赖

```bash
pip install -e ".[dev]"
```

#### 运行测试

```bash
pytest
```

#### 代码格式化

```bash
black .
isort .
```

### 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

