from typing import List, Optional

import netaddr
from IPy import IP

from .number import is_int
from loguru import logger

# 保留/私有 IPv4 地址段
RESERVED_IPV4_CIDRS = [
    '0.0.0.0/8',        # 本网络
    '10.0.0.0/8',       # 私有网络
    '100.64.0.0/10',    # 运营商级 NAT
    '127.0.0.0/8',      # 本地回环
    '169.254.0.0/16',   # 链路本地
    '172.16.0.0/12',    # 私有网络
    '172.97.0.0/16',    # 自定义保留
    '192.0.0.0/29',     # IETF 协议分配
    '192.0.0.170/31',   # NAT64/DNS64 发现
    '192.0.2.0/24',     # 文档示例 (TEST-NET-1)
    '192.168.0.0/16',   # 私有网络
    '198.18.0.0/15',    # 基准测试
    '198.51.100.0/24',  # 文档示例 (TEST-NET-2)
    '203.0.113.0/24',   # 文档示例 (TEST-NET-3)
    '224.0.0.0/4',      # 组播
    '240.0.0.0/4',      # 保留
    '255.255.255.255/32',  # 广播
]

# 全球单播 IPv6 地址段
GLOBAL_UNICAST_IPV6 = '2000::/3'


def is_ipv4(ip: str) -> bool:
    """检查是否为有效的 IPv4 地址"""
    if not ip or ip.count('.') != 3:
        return False
    
    parts = ip.split('.')
    if is_int(parts[0]) and int(parts[0]) == 0:
        return False
    
    for part in parts:
        if not is_int(part):
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True


def is_ipv4_cidr(cidr: str) -> bool:
    """检查是否为有效的 IPv4 CIDR"""
    if not cidr or '/' not in cidr or cidr.count('/') != 1:
        return False
    
    net, prefix = cidr.split('/')
    if not is_ipv4(net):
        return False
    
    if not is_int(prefix):
        return False
    
    prefix_num = int(prefix)
    return 1 <= prefix_num <= 32


def is_public_ipv4(ip: str) -> bool:
    """检查是否为公网 IPv4 地址"""
    return IP(str(ip)).iptype().upper() == 'PUBLIC'


def cidr_format(x: str) -> Optional[str]:
    """
    格式化为 CIDR 格式
    
    Args:
        x: IP 地址或 CIDR
        
    Returns:
        CIDR 格式字符串，无效输入返回 None
    """
    x = str(x).strip()
    if is_ipv4_cidr(x):
        return x
    elif is_ipv4(x):
        return f'{x}/32'
    return None


def get_opposite_cidr(cidr: List[str]) -> List[str]:
    """
    获取给定 CIDR 列表的补集（排除保留地址段）
    
    Args:
        cidr: IPv4 CIDR 列表
        
    Returns:
        补集 CIDR 列表
    """
    full_set = netaddr.IPSet(['0.0.0.0/0'])
    input_set = netaddr.IPSet(cidr)
    reserved_set = netaddr.IPSet(RESERVED_IPV4_CIDRS)
    
    opposite_set = full_set ^ input_set ^ reserved_set
    opposite_cidr = [str(c.cidr) for c in opposite_set.iter_cidrs()]
    
    logger.info(f'Generated {len(opposite_cidr)} opposite IPv4 CIDR entries')
    return opposite_cidr


def get_opposite_ipv6_cidr(cidr: List[str]) -> List[str]:
    """
    获取给定 IPv6 CIDR 列表的补集（仅限全球单播地址段）
    
    Args:
        cidr: IPv6 CIDR 列表
        
    Returns:
        补集 CIDR 列表
    """
    global_unicast = netaddr.IPSet([GLOBAL_UNICAST_IPV6])
    input_set = netaddr.IPSet(cidr)
    
    opposite_set = global_unicast ^ input_set
    opposite_cidr = [str(c.cidr) for c in opposite_set.iter_cidrs()]
    
    logger.info(f'Generated {len(opposite_cidr)} opposite IPv6 CIDR entries')
    return opposite_cidr

