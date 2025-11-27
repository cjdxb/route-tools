import sys
from typing import List

from generator.ros import generate_ros_script
from source.clang import get_cn_cidr
from source.google import get_google_service_cidr
from source.xshell import read_xshell_dir_ips
from utils.ip import get_opposite_cidr
from loguru import logger


# 自定义排除的 IP 地址（直连）
CUSTOMER_EXCLUDE_IP: List[str] = [
    '216.218.221.6',
    '216.218.221.42',
    '74.82.46.6',
    '103.177.162.23'
]

# Xshell 配置目录
XSHELL_CONFIG_DIR = r'D:\Files Sync\SynologyDrive\配置文件\服务器安全\Xshell配置'


def main() -> int:
    """生成包含直连规则的 RouterOS 脚本"""
    # 获取中国 IP
    cn_cidr = get_cn_cidr()
    
    # 获取服务器 IP
    server_ip = read_xshell_dir_ips(dir_path=XSHELL_CONFIG_DIR)
    logger.info(f'Server IPs: {server_ip}')
    
    # 获取 Google 服务 IP（过滤空值）
    google_ip = [ip for ip in get_google_service_cidr('ipv4') if ip]
    
    # 合并所有直连 IP
    direct_ip = cn_cidr + server_ip + CUSTOMER_EXCLUDE_IP + google_ip
    logger.info(f'Total direct IPs: {len(direct_ip)} entries')
    
    # 生成代理 IP（补集）
    proxy_ip = get_opposite_cidr(direct_ip)
    
    # 生成 RouterOS 脚本
    generate_ros_script(proxy_ip, 'lst0-global', 'GLOBAL-R1')
    
    return 0


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    sys.exit(main())

