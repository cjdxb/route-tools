import sys
from typing import List

from generator.ros import generate_ros_script
from source.google import get_google_service_cidr
from loguru import logger


CUSTOMER_EXCLUDE_IP: List[str] = ['8.8.8.8', '8.8.4.4']


def main() -> int:
    """生成 Google 服务 IP 的 RouterOS 脚本"""
    proxy_ip = list(get_google_service_cidr('ipv4'))
    logger.info(f'Got {len(proxy_ip)} Google service IPv4 CIDR entries')
    
    generate_ros_script(proxy_ip, 'lst0-google', 'GOOGLE')
    return 0


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    sys.exit(main())


def subs():
    pass 
