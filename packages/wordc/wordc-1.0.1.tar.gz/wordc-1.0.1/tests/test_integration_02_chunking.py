import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).parents[0]

expected01 = """chunking...with chunk size 1024 bytes
4284 the
2192 and
2185 of
1861 a
1685 to
1366 in
1056 i
1024 that
889 his
821 it
783 he
616 but
603 was
595 with
577 s
564 is
551 for
542 all
541 as
458 at
"""


expected02 = """chunking...with chunk size 1 bytes
4284 the
2192 and
2185 of
1861 a
1685 to
1366 in
1056 i
1024 that
889 his
821 it
783 he
616 but
603 was
595 with
577 s
564 is
551 for
542 all
541 as
458 at
"""

expected03 = """chunking...with chunk size 1 bytes
4285 the
2192 and
2185 of
1861 a
1685 to
"""


def test_chunking_usage01():
    test_file = BASE_DIR / "resources" / "mobydick.txt"
    result = subprocess.run(["wordc", test_file, "-c"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == expected01


def test_chunking_usage02():
    test_file = BASE_DIR / "resources" / "mobydick.txt"
    result = subprocess.run(["wordc", test_file, "-c", "-s", "1"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == expected02


def test_chunking_usage03():
    test_file = BASE_DIR / "resources" / "mobydick_final_word.txt"
    result = subprocess.run(["wordc", test_file, "-c", "-s", "1", "-t", "5"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == expected03
