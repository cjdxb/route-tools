from typing import Iterable, Literal
from loguru import logger

IpVersionType = Literal['ipv4', 'ipv6']


def _generate_ros_address_list_script(
    ip_cidr: Iterable[str],
    addr_list: str,
    ip_version: IpVersionType = 'ipv4'
) -> str:
    """
    生成 RouterOS 地址列表脚本内容
    
    Args:
        ip_cidr: IP CIDR 列表
        addr_list: 地址列表名称
        ip_version: IP 版本
        
    Returns:
        脚本内容字符串
    """
    ip_cmd = 'ip' if ip_version == 'ipv4' else 'ipv6'
    
    script = f'/log info "Loading {addr_list} {ip_version} address list"\n'
    script += f'/{ip_cmd} firewall address-list remove [/{ip_cmd} firewall address-list find list={addr_list}]\n'
    script += f'/{ip_cmd} firewall address-list'
    
    for cidr in ip_cidr:
        script += f'\n:do {{ add address={cidr} list={addr_list} }} on-error={{}}'
    
    return script


def generate_ros_script(
    ip_cidr: Iterable[str],
    addr_list: str,
    output_path: str
) -> None:
    """
    生成 RouterOS IPv4 地址列表脚本并保存到文件
    
    Args:
        ip_cidr: IP CIDR 列表
        addr_list: 地址列表名称
        output_path: 输出文件路径
    """
    script = _generate_ros_address_list_script(ip_cidr, addr_list, 'ipv4')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script)
    logger.info(f'Generated RouterOS IPv4 script: {output_path}')


def generate_ros_ipv6_script(
    ip_cidr: Iterable[str],
    addr_list: str,
    output_path: str
) -> None:
    """
    生成 RouterOS IPv6 地址列表脚本并保存到文件
    
    Args:
        ip_cidr: IP CIDR 列表
        addr_list: 地址列表名称
        output_path: 输出文件路径
    """
    script = _generate_ros_address_list_script(ip_cidr, addr_list, 'ipv6')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script)
    logger.info(f'Generated RouterOS IPv6 script: {output_path}')
