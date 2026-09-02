import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

def load_json_config(filepath: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_config(data: Dict[str, Any], filepath: str) -> None:
    """Save data to a JSON configuration file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def run_command(cmd: List[str], timeout: int = 60) -> str:
    """Run a shell command and return its output."""
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with code {result.returncode}: {result.stderr}")
    return result.stdout.strip()

def backup_file(source: str, backup_dir: str = "backups") -> str:
    """Backup a file to the specified directory."""
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    source_path = Path(source)
    backup_name = f"{source_path.stem}_backup_{source_path.suffix[1:] if source_path.suffix else 'bak'}"
    backup_path = Path(backup_dir) / f"{backup_name}{source_path.suffix}"
    shutil.copy2(source, backup_path)
    return str(backup_path)

def ensure_directory(path: str) -> None:
    """Create directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """List all files in a directory, filter by extension if provided."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    files = []
    for item in dir_path.iterdir():
        if item.is_file():
            if extension is None or item.suffix == extension:
                files.append(str(item))
    return sorted(files)

def clean_directory(directory: str, pattern: str = "*") -> int:
    """Delete files matching the pattern and return the count."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return 0
    count = 0
    for file_path in dir_path.glob(pattern):
        if file_path.is_file():
            file_path.unlink()
            count += 1
    return count