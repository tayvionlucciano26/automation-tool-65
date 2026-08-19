import time
from typing import List, Dict

class DataProcessor:
    def __init__(self, data: List[Dict]):
        self.data = data

    def optimize_data_processing(self) -> List[Dict]:
        start_time = time.perf_counter()
        processed = [self.process_item(item) for item in self.data]  # Use list comprehension for performance
        end_time = time.perf_counter()
        print(f"Processing took {end_time - start_time:.4f} seconds")
        return processed

    def process_item(self, item: Dict) -> Dict:
        # Simulate data processing with a simple transformation
        return {k: v * 2 for k, v in item.items()}

if __name__ == '__main__':
    sample_data = [{'value': 1}, {'value': 2}, {'value': 3}]
    processor = DataProcessor(sample_data)
    results = processor.optimize_data_processing()
    print(results)