import os
import shutil
from typing import List, Dict, Any

class Processor:
    """Handles task processing and resource cleanup for automation."""

    def __init__(self, temp_dir: str = "/tmp/automation"):
        self.temp_dir = temp_dir
        self.tasks: List[Dict[str, Any]] = []
        self.processed: List[Dict[str, Any]] = []
        os.makedirs(self.temp_dir, exist_ok=True)

    def add_task(self, task: Dict[str, Any]) -> None:
        """Add a new task to the queue."""
        if 'id' not in task:
            task['id'] = len(self.tasks) + 1
        self.tasks.append(task)

    def process_all(self) -> List[Dict[str, Any]]:
        """Process all pending tasks."""
        for task in self.tasks[:]:
            result = self._process_task(task)
            self.processed.append(result)
            self.tasks.remove(task)
        return self.processed

    def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to handle individual task processing."""
        task_type = task.get('type', 'unknown')
        if task_type == 'file':
            return self._handle_file_task(task)
        elif task_type == 'data':
            return self._handle_data_task(task)
        else:
            return {'id': task.get('id', 0), 'status': 'skipped', 'reason': 'unknown type'}

    def _handle_file_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a file-based task."""
        src = task.get('source')
        if src and os.path.exists(src):
            dest = os.path.join(self.temp_dir, os.path.basename(src))
            shutil.copy(src, dest)
            return {'id': task['id'], 'status': 'processed', 'output': dest}
        return {'id': task.get('id', 0), 'status': 'failed', 'reason': 'source not found'}

    def _handle_data_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a data manipulation task."""
        data = task.get('data', {})
        cleaned = {k: v for k, v in sorted(data.items()) if v is not None}
        return {'id': task.get('id', 0), 'status': 'processed', 'result': cleaned}

    def cleanup(self) -> None:
        """Clean up temporary files and reset state."""
        if os.path.exists(self.temp_dir):
            for item in os.listdir(self.temp_dir):
                path = os.path.join(self.temp_dir, item)
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception:
                    pass
        self.tasks.clear()
        self.processed.clear()

    def get_summary(self) -> Dict[str, Any]:
        """Return summary of processed tasks."""
        return {
            'total_processed': len(self.processed),
            'pending': len(self.tasks),
            'temp_dir': self.temp_dir
        }