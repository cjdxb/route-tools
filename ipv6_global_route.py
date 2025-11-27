import sys

from generator.ros import generate_ros_script
from source.clang import get_non_cn_cidr
from loguru import logger


def main() -> int:
    """生成非中国 IP 的 RouterOS 脚本"""
    proxy_ip = get_non_cn_cidr()
    logger.info(f'Got {len(proxy_ip)} non-CN IPv4 CIDR entries')
    
    generate_ros_script(proxy_ip, 'lst0-global', 'GLOBAL-R1')
    return 0


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    sys.exit(main())

