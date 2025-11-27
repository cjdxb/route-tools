"""
BGP Tools 配置文件

集中管理项目的所有配置项
"""
from typing import List

# ==================== 网络请求配置 ====================
HTTP_TIMEOUT: int = 30  # HTTP 请求超时时间（秒）
HTTP_USER_AGENT: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# ==================== 数据源 URL ====================
# Google
GOOGLE_SERVICE_URL: str = 'https://www.gstatic.com/ipranges/goog.json'
GOOGLE_CLOUD_URL: str = 'https://www.gstatic.com/ipranges/cloud.json'

# AWS
AWS_IP_RANGES_URL: str = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

# APNIC
APNIC_DELEGATED_URL: str = 'http://ftp.apnic.net/stats/apnic/delegated-apnic-latest'

# Clang (中国 IP 数据源)
CLANG_CN_IPV4_URL: str = 'http://ispip.clang.cn/all_cn_cidr.txt'
CLANG_CN_IPV6_URL: str = 'https://ispip.clang.cn/all_cn_ipv6.txt'

# ==================== 输出配置 ====================
DEFAULT_OUTPUT_ENCODING: str = 'utf-8'

# ==================== 自定义 IP 列表 ====================
# 需要排除（直连）的 IP 地址
CUSTOMER_EXCLUDE_IPS: List[str] = [
    '216.218.221.6',
    '216.218.221.42',
    '74.82.46.6',
    '103.177.162.23',
]

# Google DNS（可选排除）
GOOGLE_DNS_IPS: List[str] = [
    '8.8.8.8',
    '8.8.4.4',
]

# ==================== 日志配置 ====================
LOG_LEVEL: str = 'INFO'
LOG_FORMAT: str = '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
