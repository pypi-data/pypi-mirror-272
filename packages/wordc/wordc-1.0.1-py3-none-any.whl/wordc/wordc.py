#!/usr/bin/env python3
# Core Library modules
import sys
from collections import Counter
from collections.abc import Generator
from pathlib import Path

# Third party modules
import psutil

# Local modules
from . import utils
from .cli import parse_args
from .config import config
from .exceptions import file_exception


@file_exception
def read_file_contents(doc: Path, encoding: str) -> str:
    """Read a file normally - used for relatively small files"""
    with open(doc, encoding=encoding) as file:
        return file.read()


@file_exception
def read_file_chunks(doc: Path, encoding: str, chunk_size: int) -> Generator:
    """Read a file chunked into a specific size - used for large files"""
    with open(doc, encoding=encoding) as file:
        remainder: str = ""
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            total_chunk = remainder + chunk
            try:
                space_index = total_chunk.rindex(" ")
            except ValueError:
                remainder += chunk
                continue
            yield total_chunk[: space_index + 1]
            remainder = total_chunk[space_index + 1 :]
        if remainder:
            yield remainder


def fail_early_tests(file_path: Path) -> None:
    if not file_path.exists() or not file_path.is_file():
        print(f"The file '{file_path.name}' does not appear to be a file")
        sys.exit(1)
    if utils.is_binary(file_path):
        print(f"The file '{file_path.name}' appears to be a binary file")
        sys.exit(1)


def process_contents(content: str) -> Counter:
    """Process the text to remove punctuation etc"""
    words = "".join(c if c.isalnum() else " " for c in content).split()
    words = [word.lower() for word in words]
    word_counts = Counter(words)
    return word_counts


def main() -> None:
    args, parser = parse_args(sys.argv[1:])
    config.chunk = args.chunk
    config.chunk_size = args.size
    config.encoding = args.encoding
    config.top_words = args.top_words
    file_path = Path(args.filename)

    fail_early_tests(file_path)
    available_memory = psutil.virtual_memory().available
    auto_chunking = utils.determine_chunking(file_path, available_memory)
    config.encoding = utils.detect_encoding(file_path)

    if config.chunk or auto_chunking:
        print(f"chunking...with chunk size {config.chunk_size} bytes")
        word_counter: Counter = Counter()
        for content in read_file_chunks(file_path, config.encoding, config.chunk_size):
            processed = process_contents(content)
            word_counter.update(processed)

    else:
        content = read_file_contents(file_path, config.encoding)
        word_counter = process_contents(content)

    if word_counter:
        for word, count in word_counter.most_common(config.top_words):
            print(count, word)


if __name__ == "__main__":
    SystemExit(main())  # type: ignore
