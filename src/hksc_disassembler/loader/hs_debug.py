from io import BytesIO
from typing import List

from ..common.reader import read_integer
from .hs_type_reader import read_t_string
from .hs_header import HSHeader


class HSFunctionDebugInfoLocals:
    def __init__(self) -> None:
        self.localName: str = ""
        self.start: int = -1
        self.end: int = -1

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.localName = read_t_string(f, header)
        self.start = read_integer(f, False, 4, header.byteorder)
        self.end = read_integer(f, False, 4, header.byteorder)


class HSFunctionDebugInfo:
    def __init__(self) -> None:
        self.lineCount: int = -1
        self.localsCount: int = -1
        self.upValueCount: int = -1
        self.lineBegin: int = -1
        self.lineEnd: int = -1
        self.path: str = ""
        self.functionName: str = ""
        self.lines: List[int] = []
        self.locals: List[HSFunctionDebugInfoLocals] = []
        self.upValues: List[str] = []

    def read(self, f: BytesIO, header: HSHeader):
        self.lineCount = read_integer(f, False, 4, header.byteorder)
        self.localsCount = read_integer(f, False, 4, header.byteorder)
        self.upValueCount = read_integer(f, False, 4, header.byteorder)
        self.lineBegin = read_integer(f, False, 4, header.byteorder)
        self.lineEnd = read_integer(f, False, 4, header.byteorder)
        self.path = read_t_string(f, header)
        self.functionName = read_t_string(f, header)

        for _ in range(self.lineCount):
            line: int = read_integer(f, False, 4, header.byteorder)
            self.lines.append(line)

        for _ in range(self.localsCount):
            local: HSFunctionDebugInfoLocals = HSFunctionDebugInfoLocals()
            local.read(f, header)
            self.locals.append(local)

        for _ in range(self.upValueCount):
            upValue: str = read_t_string(f, header)
            self.upValues.append(upValue)
