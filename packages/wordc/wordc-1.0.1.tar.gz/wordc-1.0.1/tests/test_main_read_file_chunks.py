import pytest
from wordc import wordc
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]


def test_nominal():
    test_file = BASE_DIR / "resources" / "small.txt"
    gen = wordc.read_file_chunks(test_file, "utf-8", 1024)
    expected_words = ["hello ", "world\n"]

    for expected_word in expected_words:
        generated_word = next(gen)
        assert generated_word == expected_word

    with pytest.raises(StopIteration):
        next(gen)


def test_minimal_chunks():
    test_file = BASE_DIR / "resources" / "100_bytes.txt"
    gen = wordc.read_file_chunks(test_file, "utf-8", 10)
    expected_words = ["Now, in ", "his heart, ", "Ahab had ", "some\nglimpse of ",
                      "this\n"]

    for expected_word in expected_words:
        generated_word = next(gen)
        assert generated_word == expected_word

    with pytest.raises(StopIteration):
        next(gen)

