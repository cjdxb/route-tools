from typing import Iterable
from loguru import logger


def generate_bird_route(
    cidr: Iterable[str],
    next_hop: str,
    conf_path: str
) -> None:
    """
    生成 BIRD 路由配置文件
    
    Args:
        cidr: IP CIDR 列表
        next_hop: 下一跳地址
        conf_path: 配置文件输出路径
    """
    routes = []
    for c in cidr:
        logger.debug(f'Adding bird route: route {c} via {next_hop};')
        routes.append(f'route {c} via {next_hop};')
    
    content = '\n'.join(routes)
    with open(conf_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f'Generated BIRD route config with {len(routes)} routes: {conf_path}')
