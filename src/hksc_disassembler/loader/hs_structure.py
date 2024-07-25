from io import BytesIO
from typing import List

from ..common.reader import read_integer
from .hs_type_reader import read_t_string
from .hs_header import HSCompatibility, HSHeader
from .hs_opcodes import HSType


class HSStructHeader:
    def __init__(self) -> None:
        self.name: str = ""
        self.unk0: int = -1
        self.structId: int = -1
        self.type: HSType = HSType(0)
        self.unk1: int = -1
        self.unk2: int = -1

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.name = read_t_string(f, header)
        self.unk0 = read_integer(f, True, 4, header.byteorder)
        self.structId = read_integer(f, False, 4, header.byteorder)
        self.type = HSType(read_integer(f, True, 4, header.byteorder))
        self.unk1 = read_integer(f, False, 4, header.byteorder)
        self.unk2 = read_integer(f, False, 4, header.byteorder)


class HSStructMember:
    def __init__(self) -> None:
        self.header: HSStructHeader = HSStructHeader()
        self.index: int = -1

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.header.read(f, header)
        self.index = read_integer(f, True, 4, header.byteorder)


class HSStructBlock:
    def __init__(self) -> None:
        self.header: HSStructHeader = HSStructHeader()
        self.memberCount: int = 0
        self.extendCount: int = 0
        self.extendedStructs: List[str] = []
        self.members: List[HSStructMember] = []

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.header.read(f, header)
        self.memberCount = read_integer(f, True, 4, header.byteorder)

        if HSCompatibility.STRUCTURES in header.compatBits:
            self.extendCount = read_integer(f, True, 4, header.byteorder)
            for _ in range(self.extendCount):
                extended_struct: str = read_t_string(f, header)
                self.extendedStructs.append(extended_struct)

        for _ in range(self.memberCount):
            member = HSStructMember()
            member.read(f, header)
            self.members.append(member)
