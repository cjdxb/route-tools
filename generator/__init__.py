"""
配置生成器模块

为不同路由器/设备生成配置文件
"""
from .bird import generate_bird_route
from .ikuai import generate_list
from .ros import generate_ros_script, generate_ros_ipv6_script

__all__ = [
    'generate_bird_route',
    'generate_list',
    'generate_ros_script',
    'generate_ros_ipv6_script',
]
