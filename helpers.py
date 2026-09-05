import os
import shutil
import logging
from pathlib import Path
from typing import List, Union

logger = logging.getLogger(__name__)

def clear_temp_directory(path: Union[str, Path], extension: str = ".tmp") -> int:
    """Removes files with specific extension from target directory."""
    target = Path(path)
    count = 0
    if not target.exists():
        return 0

    for item in target.glob(f"*{extension}"):
        try:
            if item.is_file():
                item.unlink()
                count += 1
        except OSError as e:
            logger.error(f"failed to remove {item}: {e}")
    return count

def organize_files_by_extension(source: str, target_base: str) -> dict:
    """Groups files into subdirectories based on their suffix."""
    summary = {}
    source_dir = Path(source)
    base_dir = Path(target_base)

    for file in [f for f in source_dir.iterdir() if f.is_file()]:
        ext = file.suffix.lower() or ".no_ext"
        dest_dir = base_dir / ext.lstrip(".")
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(file), str(dest_dir / file.name))
        summary[ext] = summary.get(ext, 0) + 1
        
    return summary

def validate_path_exists(path: str) -> bool:
    """Checks if provided string is a valid directory path."""
    return Path(path).is_dir()