"""
IP 数据源模块

提供从各种数据源获取 IP CIDR 的功能
"""
from .apnic import get_ip_range_by_country, get_non_ip_range_by_country
from .aws import get_aws_cidr
from .clang import get_cn_cidr, get_non_cn_cidr, get_cn_ipv6_cidr, get_non_cn_ipv6_cidr
from .google import get_google_service_cidr, get_google_cloud_cidr
from .xshell import read_xshell_config_ip, read_xshell_dir_ips

__all__ = [
    # APNIC
    'get_ip_range_by_country',
    'get_non_ip_range_by_country',
    # AWS
    'get_aws_cidr',
    # Clang
    'get_cn_cidr',
    'get_non_cn_cidr',
    'get_cn_ipv6_cidr',
    'get_non_cn_ipv6_cidr',
    # Google
    'get_google_service_cidr',
    'get_google_cloud_cidr',
    # Xshell
    'read_xshell_config_ip',
    'read_xshell_dir_ips',
]
