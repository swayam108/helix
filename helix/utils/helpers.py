"""Helper utilities and common functions"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime


def serialize_to_json(obj: Any) -> str:
    """Serialize Python objects to JSON"""
    return json.dumps(obj, default=str, indent=2)


def deserialize_from_json(json_str: str) -> Any:
    """Deserialize JSON to Python objects"""
    return json.loads(json_str)


def parse_yaml_config(filepath: str) -> Dict[str, Any]:
    """Parse YAML configuration file"""
    try:
        import yaml
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except ImportError:
        raise ImportError("PyYAML is required for config parsing")
    except Exception as e:
        raise Exception(f"Error parsing config file: {e}")


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def format_file_size(bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024
    return f"{bytes:.2f}TB"


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL"""
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def retry_async(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retrying async functions"""
    import asyncio
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator
