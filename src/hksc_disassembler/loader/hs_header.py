from io import BytesIO
from enum import IntEnum, IntFlag

from ..common.reader import read_integer


class HSHeaderException(Exception):
    pass


class HSNumberType(IntEnum):
    FLOAT = 0
    INTEGER = 1


class HSEndianness(IntEnum):
    BIG = 0
    LITTLE = 1


class HSCompatibility(IntFlag):
    MEMOIZATION = 1 << 0
    STRUCTURES = 1 << 1
    SELF = 1 << 2
    DOUBLES = 1 << 3
    NATIVEINT = 1 << 4


class HSHeader:
    def __init__(self) -> None:
        self.magic: int = -1
        self.version: int = -1
        self.format: int = -1
        self.endianness: HSEndianness = HSEndianness(0)
        self.intSize: int = -1
        self.tSize: int = -1
        self.instructionSize: int = -1
        self.numberSize: int = -1
        self.numberType: HSNumberType = HSNumberType(0)
        self.compatBits: HSCompatibility = HSCompatibility(0)
        self.shared: int = -1
        self.byteorder: str = "little"

    def read(self, f: BytesIO) -> None:
        self.magic = read_integer(f, False, 4)
        if self.magic != 1635077147:  # type: ignore
            raise HSHeaderException("Header magic data does not match!")

        self.version = read_integer(f, False, 1, self.byteorder)
        if self.version != 0x51:
            raise HSHeaderException("Header version data does not match!")

        self.format = read_integer(f, False, 1, self.byteorder)
        if self.format != 14:
            raise HSHeaderException("Header format version data does not match!")

        self.endianness = HSEndianness(read_integer(f, False, 1, self.byteorder))
        if self.endianness == HSEndianness.BIG:
            self.byteorder = "big"

        self.intSize = read_integer(f, False, 1, self.byteorder)
        self.tSize = read_integer(f, False, 1, self.byteorder)
        self.instructionSize = read_integer(f, False, 1, self.byteorder)
        self.numberSize = read_integer(f, False, 1, self.byteorder)
        self.numberType = HSNumberType(read_integer(f, False, 1, self.byteorder))
        self.compatBits = HSCompatibility(read_integer(f, False, 1, self.byteorder))
        self.shared = read_integer(f, False, 1, self.byteorder)
