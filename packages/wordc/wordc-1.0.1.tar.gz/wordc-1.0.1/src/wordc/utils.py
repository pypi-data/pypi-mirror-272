# Core Library modules
import functools
import time
from pathlib import Path
from typing import Any, Callable

# Third party modules
import chardet

# Local modules
from .config import config


def determine_chunking(file_path: Path, memory: int) -> bool:
    """Examine file size and file size to available memory ratio to determine if
    chunking is necessary
    """
    filesize = Path(file_path).stat().st_size
    filesize_mb = filesize / (1024 * 1024)
    ratio = (filesize / memory) * 100
    if ratio > config.memory_threshold or filesize_mb > config.filesize_threshold:
        return True
    return False


def detect_encoding(file_path: Path) -> str:
    """Utility to detect the file encoding"""
    with open(file_path, "rb") as file:
        raw_data = file.read(config.sample_size)
        result = chardet.detect(raw_data)["encoding"]
        if config.encoding != "utf-8":
            return config.encoding
        elif config.encoding == "utf-8" and result == "ascii":
            return config.encoding
    return result


def is_binary(file_path: Path) -> bool:
    """Check if a file is binary by examining the first few bytes."""
    with open(file_path, "rb") as f:
        # Read the first few bytes
        data = f.read(config.sample_size)
        # Check for null bytes or non-printable ASCII characters
        for byte in data:
            if byte == 0:  # Null byte
                return True
            elif byte < 32 and byte not in (
                9,
                10,
                13,
            ):  # Non-printable ASCII characters
                return True
    return False


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t1 = time.perf_counter()
        value = func(*args, **kwargs)
        t2 = time.perf_counter()
        elapsed_time = t2 - t1
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper
