import re
from typing import Any, Dict

def validate_input_data(data: Dict[str, Any]) -> bool:
    """Validates input structure and value constraints."""
    required_keys = {'task_id', 'payload', 'priority'}
    
    # Check for required dictionary keys
    if not all(key in data for key in required_keys):
        return False
    
    # Validate task_id format
    if not isinstance(data['task_id'], str) or not re.match(r'^task-\d+$', data['task_id']):
        return False
    
    # Validate priority bounds
    if not isinstance(data['priority'], int) or not (0 <= data['priority'] <= 10):
        return False
    
    # Validate payload is not empty
    if not data['payload']:
        return False
        
    return True

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Removes potential malicious or malformed characters."""
    if isinstance(data.get('payload'), str):
        data['payload'] = data['payload'].strip()[:1024]
    return data