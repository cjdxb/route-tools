import os
from typing import List

import chardet


def file_walker(path: str) -> List[str]:
    """
    递归遍历目录获取所有文件路径
    
    Args:
        path: 起始路径（文件或目录）
        
    Returns:
        文件路径列表
    """
    if not os.path.isdir(path):
        return [path] if os.path.exists(path) else []
    
    all_files = []
    for root, _, files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def check_charset(path: str, sample_size: int = 4096) -> str:
    """
    检测文件编码
    
    Args:
        path: 文件路径
        sample_size: 采样字节数（默认 4096）
        
    Returns:
        检测到的编码名称
    """
    with open(path, 'rb') as f:
        data = f.read(sample_size)
        result = chardet.detect(data)
    return result.get('encoding', 'utf-8')
