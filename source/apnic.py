import math
from typing import List, Literal

import requests

from utils.number import is_int
from loguru import logger

IpVersion = Literal['ipv4', 'ipv6']

APNIC_DELEGATED_URL = 'http://ftp.apnic.net/stats/apnic/delegated-apnic-latest'
DEFAULT_TIMEOUT = 60


def _dump_allocated() -> str:
    """
    下载 APNIC 分配数据
    
    Returns:
        原始文本数据
        
    Raises:
        ValueError: 下载失败时抛出
    """
    res = requests.get(APNIC_DELEGATED_URL, timeout=DEFAULT_TIMEOUT)
    if res.status_code != 200:
        raise ValueError(f'Failed to download delegated-apnic-latest, status: {res.status_code}')
    logger.info(f'Downloaded APNIC allocated data from {APNIC_DELEGATED_URL}')
    return res.text


def _parse_apnic_line(line: str) -> tuple:
    """解析 APNIC 数据行"""
    parts = line.split('|')
    if len(parts) < 7:
        return None, None, None, None
    return parts[1], parts[2], parts[3], parts[4]


def get_ip_range_by_country(
    country: str = 'CN',
    ip_version: IpVersion = 'ipv4'
) -> List[str]:
    """
    获取指定国家的 IP CIDR 列表
    
    Args:
        country: 国家代码，如 'CN', 'US'
        ip_version: IP 版本
        
    Returns:
        IP CIDR 列表
    """
    ip_cidr = []
    for line in _dump_allocated().split('\n'):
        if not line.startswith('apnic'):
            continue
        
        allocated_country, version, ip, length = _parse_apnic_line(line)
        if version != ip_version or allocated_country != country:
            continue
        
        if is_int(length):
            prefix_len = int(32 - math.log2(int(length)))
            ip_cidr.append(f"{ip}/{prefix_len}")
    
    logger.info(f'Got {len(ip_cidr)} {country} {ip_version} CIDR records')
    return ip_cidr


def get_non_ip_range_by_country(
    country: str = 'CN',
    ip_version: IpVersion = 'ipv4'
) -> List[str]:
    """
    获取非指定国家的 IP CIDR 列表
    
    Args:
        country: 要排除的国家代码
        ip_version: IP 版本
        
    Returns:
        IP CIDR 列表
    """
    ip_cidr = []
    for line in _dump_allocated().split('\n'):
        if not line.startswith('apnic'):
            continue
        
        allocated_country, version, ip, length = _parse_apnic_line(line)
        if version != ip_version or allocated_country == country:
            continue
        
        if is_int(length):
            prefix_len = int(32 - math.log2(int(length)))
            ip_cidr.append(f"{ip}/{prefix_len}")
    
    logger.info(f'Got {len(ip_cidr)} non-{country} {ip_version} CIDR records')
    return ip_cidr
