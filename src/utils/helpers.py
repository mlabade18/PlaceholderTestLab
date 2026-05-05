import re
from typing import Any, List, Dict, Set
from config.config import Config

def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_response_time(response_time: float) -> bool:
    """Check if response time is within threshold."""
    return response_time <= Config.RESPONSE_TIME_THRESHOLD

def extract_ids(data: List[Dict], key: str = "id") -> Set[Any]:
    """Extract unique IDs from a list of dictionaries."""
    return {item.get(key) for item in data if key in item}

def find_orphan_records(child_data: List[Dict], parent_ids: Set, foreign_key: str) -> List[Dict]:
    """Find records that reference non-existent parent records."""
    return [item for item in child_data if item.get(foreign_key) not in parent_ids]
