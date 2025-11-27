import json
from typing import Generator, Literal, Optional

from utils.http import get_url_content
from loguru import logger

IpVersion = Literal['ipv4', 'ipv6']

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_aws_cidr(
    ip_version: IpVersion = 'ipv4',
    region: Optional[str] = None
) -> Generator[str, None, None]:
    """
    获取 AWS 的 IP CIDR 列表
    
    Args:
        ip_version: IP 版本，'ipv4' 或 'ipv6'
        region: AWS 区域过滤，如 'us-east-1'
        
    Yields:
        IP CIDR 字符串
    """
    res = json.loads(get_url_content(AWS_IP_RANGES_URL))
    
    # IPv4 和 IPv6 使用不同的键
    if ip_version == 'ipv4':
        prefixes = res.get('prefixes', [])
        prefix_key = 'ip_prefix'
    else:
        prefixes = res.get('ipv6_prefixes', [])
        prefix_key = 'ipv6_prefix'
    
    for item in prefixes:
        if region is not None and item.get('region') != region:
            continue
        prefix = item.get(prefix_key)
        if prefix:
            yield prefix
    
    logger.info(f'Fetched AWS {ip_version} CIDR list (region={region})')
