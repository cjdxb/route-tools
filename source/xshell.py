from typing import List

from utils.data import check_charset, file_walker
from utils.ip import cidr_format, is_public_ipv4, is_ipv4
from loguru import logger


def read_xshell_config_ip(path: str) -> List[str]:
    """
    从 Xshell 配置文件中读取 IP 地址
    
    Args:
        path: Xshell 配置文件路径
        
    Returns:
        CIDR 格式的 IP 列表
    """
    cidr_list = []
    encoding = check_charset(path)
    
    with open(path, 'r', encoding=encoding) as f:
        for line in f:
            if not line.startswith('Host='):
                continue
            
            ip = line.replace('Host=', '').strip()
            if is_ipv4(ip) and is_public_ipv4(ip):
                cidr = cidr_format(ip)
                if cidr:
                    cidr_list.append(cidr)
    
    logger.debug(f'Got {len(cidr_list)} IPs from {path}')
    return cidr_list


def read_xshell_dir_ips(dir_path: str) -> List[str]:
    """
    从目录中读取所有 Xshell 配置文件的 IP 地址
    
    Args:
        dir_path: Xshell 配置文件目录
        
    Returns:
        去重后的 CIDR 列表
    """
    file_list = file_walker(dir_path)
    cidr_set = set()
    
    for file in file_list:
        try:
            cidr_set.update(read_xshell_config_ip(file))
        except Exception as e:
            logger.warning(f'Failed to read {file}: {e}')
    
    result = list(cidr_set)
    logger.info(f'Got {len(result)} unique IPs from {dir_path}')
    return result
