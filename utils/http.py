from typing import Optional
import requests
from loguru import logger


DEFAULT_TIMEOUT = 30
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def get_url_content(
    url: str,
    timeout: int = DEFAULT_TIMEOUT,
    headers: Optional[dict] = None
) -> str:
    """
    获取 URL 内容
    
    Args:
        url: 请求的 URL
        timeout: 超时时间(秒)
        headers: 自定义请求头
        
    Returns:
        响应内容文本
        
    Raises:
        requests.RequestException: 请求失败时抛出
    """
    request_headers = headers or DEFAULT_HEADERS
    try:
        response = requests.get(url, timeout=timeout, headers=request_headers)
        response.raise_for_status()
        logger.debug(f'Successfully fetched {url}')
        return response.text
    except requests.RequestException as e:
        logger.error(f'HTTP request failed for {url}: {e}')
        raise
