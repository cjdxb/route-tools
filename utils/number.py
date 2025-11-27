from typing import Any


def is_int(x: Any) -> bool:
    """
    检查值是否可以转换为整数
    
    Args:
        x: 任意值
        
    Returns:
        如果可以转换为整数则返回 True
    """
    try:
        int(x)
        return True
    except (ValueError, TypeError):
        return False
