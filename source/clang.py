from typing import List

import requests

from utils.ip import get_opposite_cidr, get_opposite_ipv6_cidr
from loguru import logger

CLANG_CN_IPV4_URL = 'http://ispip.clang.cn/all_cn_cidr.txt'
CLANG_CN_IPV6_URL = 'https://ispip.clang.cn/all_cn_ipv6.txt'
DEFAULT_TIMEOUT = 30


def _fetch_cidr_from_url(url: str) -> List[str]:
    """
    从 URL 获取 CIDR 列表
    
    Args:
        url: 数据源 URL
        
    Returns:
        CIDR 列表
        
    Raises:
        ValueError: 请求失败时抛出
    """
    res = requests.get(url, timeout=DEFAULT_TIMEOUT)
    if res.status_code != 200:
        raise ValueError(f'Failed to fetch CIDR from {url}, status: {res.status_code}')
    
    ip_cidr = []
    for line in res.text.split():
        line = line.strip()
        if line and not line.startswith('#'):
            ip_cidr.append(line)
    return ip_cidr


def get_cn_cidr() -> List[str]:
    """
    获取中国 IPv4 CIDR 列表
    
    Returns:
        IPv4 CIDR 列表
    """
    ip_cidr = _fetch_cidr_from_url(CLANG_CN_IPV4_URL)
    logger.info(f'Got {len(ip_cidr)} CN IPv4 CIDR records')
    return ip_cidr


def get_non_cn_cidr() -> List[str]:
    """
    获取非中国 IPv4 CIDR 列表
    
    Returns:
        IPv4 CIDR 列表
    """
    cn_cidr = get_cn_cidr()
    return get_opposite_cidr(cn_cidr)


def get_cn_ipv6_cidr() -> List[str]:
    """
    获取中国 IPv6 CIDR 列表
    
    Returns:
        IPv6 CIDR 列表
    """
    ip_cidr = _fetch_cidr_from_url(CLANG_CN_IPV6_URL)
    logger.info(f'Got {len(ip_cidr)} CN IPv6 CIDR records')
    return ip_cidr


def get_non_cn_ipv6_cidr() -> List[str]:
    """
    获取非中国 IPv6 CIDR 列表
    
    Returns:
        IPv6 CIDR 列表
    """
    cn_cidr = get_cn_ipv6_cidr()
    return get_opposite_ipv6_cidr(cn_cidr)
