import subprocess

from pathlib import Path

BASE_DIR = Path(__file__).parents[0]

expected01 = """4284 the
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

expected02 = """4284 the
2192 and
2185 of
1861 a
1685 to
"""


def test_nominal():
    test_file = BASE_DIR / "resources" / "mobydick.txt"
    result = subprocess.run(["wordc", test_file], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == expected01


def test_argument_t():
    test_file = BASE_DIR / "resources" / "mobydick.txt"
    result = subprocess.run(["wordc", test_file, "-t", "5"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == expected02

