from io import BytesIO
from typing import List

from ..common.reader import read_integer
from .hs_function import HSFunction
from .hs_enum import HSEnums
from .hs_header import HSHeader
from .hs_structure import HSStructBlock


class HavokScriptFile:
    def __init__(self) -> None:
        self.header: HSHeader = HSHeader()
        self.enums: HSEnums = HSEnums()
        self.mainFunction: HSFunction = HSFunction()
        self.structures: List[HSStructBlock] = []

    def read(self, f: BytesIO) -> None:
        self.header.read(f)
        self.enums.read(f, self.header.byteorder)
        self.mainFunction.read(f, self.header)
        f.seek(4, 1)

        while read_integer(f, False, 8, self.header.byteorder) != 0:
            f.seek(-8, 1)
            structure: HSStructBlock = HSStructBlock()
            structure.read(f, self.header)
            self.structures.append(structure)
