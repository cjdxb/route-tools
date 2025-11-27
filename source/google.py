import json
from typing import Generator, Literal, Optional

from utils.http import get_url_content
from loguru import logger

IpVersion = Literal['ipv4', 'ipv6']

GOOGLE_SERVICE_URL = 'https://www.gstatic.com/ipranges/goog.json'
GOOGLE_CLOUD_URL = 'https://www.gstatic.com/ipranges/cloud.json'


def get_google_service_cidr(ip_version: IpVersion = 'ipv4') -> Generator[str, None, None]:
    """
    获取 Google 服务的 IP CIDR 列表
    
    Args:
        ip_version: IP 版本，'ipv4' 或 'ipv6'
        
    Yields:
        IP CIDR 字符串
    """
    res = json.loads(get_url_content(GOOGLE_SERVICE_URL))
    prefix_key = f'{ip_version}Prefix'
    
    for item in res['prefixes']:
        prefix = item.get(prefix_key)
        if prefix:
            yield prefix
    
    logger.info(f'Fetched Google service {ip_version} CIDR list')


def get_google_cloud_cidr(
    ip_version: IpVersion = 'ipv4',
    scope: Optional[str] = None
) -> Generator[str, None, None]:
    """
    获取 Google Cloud 的 IP CIDR 列表
    
    Args:
        ip_version: IP 版本，'ipv4' 或 'ipv6'
        scope: 范围过滤，如 'asia-east1'
        
    Yields:
        IP CIDR 字符串
    """
    res = json.loads(get_url_content(GOOGLE_CLOUD_URL))
    prefix_key = f'{ip_version}Prefix'
    
    for item in res['prefixes']:
        if scope is not None and item.get('scope') != scope:
            continue
        prefix = item.get(prefix_key)
        if prefix:
            yield prefix
    
    logger.info(f'Fetched Google Cloud {ip_version} CIDR list (scope={scope})')
