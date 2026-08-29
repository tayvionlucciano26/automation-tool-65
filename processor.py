import json
from typing import List, Dict, Any

def validate_record(record: Dict[str, Any]) -> bool:
    """Check if the input record meets all validation criteria."""
    if not isinstance(record, dict):
        return False
    required = ['id', 'name', 'value']
    for field in required:
        if field not in record:
            return False
    if not isinstance(record['id'], int) or record['id'] <= 0:
        return False
    if not isinstance(record['name'], str) or len(record['name'].strip()) == 0:
        return False
    if not isinstance(record['value'], (int, float)) or record['value'] < 0:
        return False
    return True

def process_inputs(inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Main processing loop that includes input validation."""
    processed_records = []
    for index, record in enumerate(inputs):
        if not validate_record(record):
            print(f"Invalid input at position {index}: {record}")
            continue
        cleaned_name = record['name'].strip().capitalize()
        adjusted_value = round(record['value'] * 1.05, 2)
        processed = {
            'id': record['id'],
            'name': cleaned_name,
            'value': adjusted_value,
            'status': 'processed'
        }
        processed_records.append(processed)
    return processed_records

if __name__ == "__main__":
    test_data = [
        {"id": 101, "name": "item one", "value": 50.5},
        {"id": 0, "name": "bad id", "value": 10},
        {"id": 102, "name": "", "value": 20},
        {"id": 103, "name": "item two", "value": -5},
        {"id": 104, "name": "  item three  ", "value": 75}
    ]
    results = process_inputs(test_data)
    print("Successfully processed records:")
    for rec in results:
        print(json.dumps(rec, indent=2))
