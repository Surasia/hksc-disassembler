from io import BytesIO
from typing import List

from ..common.reader import read_integer, read_string


class HSEnum:
    def __init__(self) -> None:
        self.value: int = -1
        self.length: int = -1
        self.name: str = ""

    def read(self, f: BytesIO, endianness: str) -> None:
        self.value = read_integer(f, False, 4, endianness)
        self.length = read_integer(f, False, 4, endianness)

        if self.length != 0:
            self.name = read_string(f, self.length - 1)
            f.seek(1, 1)  # Skip terminator


class HSEnums:
    def __init__(self) -> None:
        self.count: int = -1
        self.entries: List[HSEnum] = []

    def read(self, f: BytesIO, endianness: str) -> None:
        self.count = read_integer(f, False, 4, endianness)
        for _ in range(self.count):
            entry = HSEnum()
            entry.read(f, endianness)
            self.entries.append(entry)
