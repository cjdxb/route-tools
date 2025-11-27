from typing import Iterable
from loguru import logger


def generate_list(ip_cidr: Iterable[str], output_path: str) -> None:
    """
    生成 iKuai 路由器 IP 列表文件
    
    Args:
        ip_cidr: IP CIDR 列表
        output_path: 输出文件路径
    """
    cidr_list = list(ip_cidr)
    content = '\n'.join(cidr_list)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f'Generated iKuai list with {len(cidr_list)} entries: {output_path}')