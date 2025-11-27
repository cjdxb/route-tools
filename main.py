#!/usr/bin/env python3
"""
BGP/IP 路由工具集主程序

使用命令行参数选择不同的功能：
- google: 生成 Google 服务 IP 的 RouterOS 脚本
- global: 生成非中国 IP 的 RouterOS 脚本
- direct: 生成包含直连规则的 RouterOS 脚本
"""

import argparse
import sys
from typing import List

from loguru import logger

from generator.ros import generate_ros_script
from source.clang import get_cn_cidr, get_non_cn_cidr
from source.google import get_google_service_cidr
from source.xshell import read_xshell_dir_ips
from utils.ip import get_opposite_cidr


# ==================== 配置 ====================

# 自定义排除的 IP 地址（直连）
CUSTOMER_EXCLUDE_IP: List[str] = [
    '216.218.221.6',
    '216.218.221.42',
    '74.82.46.6',
    '103.177.162.23'
]

# Google DNS（可选排除）
GOOGLE_DNS_IP: List[str] = ['8.8.8.8', '8.8.4.4']

# Xshell 配置目录（用于 direct 模式）
XSHELL_CONFIG_DIR = r'D:\Files Sync\SynologyDrive\配置文件\服务器安全\Xshell配置'


# ==================== 功能函数 ====================

def cmd_google(output: str, addr_list: str) -> int:
    """
    生成 Google 服务 IP 的 RouterOS 脚本
    
    Args:
        output: 输出文件路径
        addr_list: 地址列表名称
    """
    logger.info('Generating Google service IP RouterOS script...')
    
    proxy_ip = list(get_google_service_cidr('ipv4'))
    logger.info(f'Got {len(proxy_ip)} Google service IPv4 CIDR entries')
    
    generate_ros_script(proxy_ip, addr_list, output)
    logger.success(f'Script generated: {output}')
    return 0


def cmd_global(output: str, addr_list: str) -> int:
    """
    生成非中国 IP 的 RouterOS 脚本
    
    Args:
        output: 输出文件路径
        addr_list: 地址列表名称
    """
    logger.info('Generating non-China IP RouterOS script...')
    
    proxy_ip = get_non_cn_cidr()
    logger.info(f'Got {len(proxy_ip)} non-CN IPv4 CIDR entries')
    
    generate_ros_script(proxy_ip, addr_list, output)
    logger.success(f'Script generated: {output}')
    return 0


def cmd_direct(output: str, addr_list: str, xshell_dir: str = None) -> int:
    """
    生成包含直连规则的 RouterOS 脚本
    
    Args:
        output: 输出文件路径
        addr_list: 地址列表名称
        xshell_dir: Xshell 配置目录路径
    """
    logger.info('Generating direct connection rules RouterOS script...')
    
    # 获取中国 IP
    cn_cidr = get_cn_cidr()
    logger.info(f'Got {len(cn_cidr)} CN IPv4 CIDR entries')
    
    # 获取服务器 IP（如果指定了 Xshell 配置目录）
    server_ip = []
    if xshell_dir:
        try:
            server_ip = read_xshell_dir_ips(dir_path=xshell_dir)
            logger.info(f'Got {len(server_ip)} server IPs from Xshell config')
        except Exception as e:
            logger.warning(f'Failed to read Xshell config: {e}')
    
    # 获取 Google 服务 IP（过滤空值）
    google_ip = [ip for ip in get_google_service_cidr('ipv4') if ip]
    logger.info(f'Got {len(google_ip)} Google service IPv4 entries')
    
    # 合并所有直连 IP
    direct_ip = cn_cidr + server_ip + CUSTOMER_EXCLUDE_IP + google_ip
    logger.info(f'Total direct IPs: {len(direct_ip)} entries')
    
    # 生成代理 IP（补集）
    proxy_ip = get_opposite_cidr(direct_ip)
    logger.info(f'Generated {len(proxy_ip)} proxy CIDR entries')
    
    # 生成 RouterOS 脚本
    generate_ros_script(proxy_ip, addr_list, output)
    logger.success(f'Script generated: {output}')
    return 0


# ==================== 主程序 ====================

def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog='bgp-tools',
        description='BGP/IP 路由工具集 - 生成各种路由器配置脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s google                      # 生成 Google 服务 IP 脚本
  %(prog)s global                      # 生成非中国 IP 脚本
  %(prog)s direct                      # 生成直连规则脚本
  %(prog)s google -o my-google.rsc     # 指定输出文件
  %(prog)s global -l MY-LIST           # 指定地址列表名称
        '''
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # google 子命令
    google_parser = subparsers.add_parser(
        'google',
        help='生成 Google 服务 IP 的 RouterOS 脚本'
    )
    google_parser.add_argument(
        '-o', '--output',
        default='lst0-google',
        help='输出文件路径 (默认: lst0-google)'
    )
    google_parser.add_argument(
        '-l', '--list',
        dest='addr_list',
        default='GOOGLE',
        help='地址列表名称 (默认: GOOGLE)'
    )
    
    # global 子命令
    global_parser = subparsers.add_parser(
        'global',
        help='生成非中国 IP 的 RouterOS 脚本'
    )
    global_parser.add_argument(
        '-o', '--output',
        default='lst0-global',
        help='输出文件路径 (默认: lst0-global)'
    )
    global_parser.add_argument(
        '-l', '--list',
        dest='addr_list',
        default='GLOBAL-R1',
        help='地址列表名称 (默认: GLOBAL-R1)'
    )
    
    # direct 子命令
    direct_parser = subparsers.add_parser(
        'direct',
        help='生成包含直连规则的 RouterOS 脚本'
    )
    direct_parser.add_argument(
        '-o', '--output',
        default='lst0-global',
        help='输出文件路径 (默认: lst0-global)'
    )
    direct_parser.add_argument(
        '-l', '--list',
        dest='addr_list',
        default='GLOBAL-R1',
        help='地址列表名称 (默认: GLOBAL-R1)'
    )
    direct_parser.add_argument(
        '-x', '--xshell-dir',
        dest='xshell_dir',
        default=None,
        help='Xshell 配置目录路径 (可选)'
    )
    
    # 全局选项
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='静默模式，只显示错误'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser


def main() -> int:
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 配置日志级别
    logger.remove()
    if args.quiet:
        logger.add(sys.stderr, level="ERROR")
    elif args.verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")
    
    # 执行对应命令
    if args.command == 'google':
        return cmd_google(args.output, args.addr_list)
    elif args.command == 'global':
        return cmd_global(args.output, args.addr_list)
    elif args.command == 'direct':
        return cmd_direct(args.output, args.addr_list, args.xshell_dir)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
