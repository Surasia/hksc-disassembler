from io import BytesIO
from typing import Any

from ..common.reader import read_bool, read_integer
from .hs_type_reader import read_t_string, read_t_number
from .hs_header import HSHeader
from .hs_opcodes import HSType


class HSConstant:
    def __init__(self) -> None:
        self.type: HSType = HSType(0)
        self.value: Any = None

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.type = HSType(read_integer(f, False, 1, header.byteorder))

        match self.type:
            case HSType.TNIL:
                self.value = None
            case HSType.TBOOLEAN:
                self.value = read_bool(f, False, 1, header.byteorder)
            case HSType.TLIGHTUSERDATA:
                self.value = read_integer(f, True, 8, header.byteorder)
            case HSType.TNUMBER:
                self.value = read_t_number(f, header)
            case HSType.TSTRING:
                self.value = read_t_string(f, header)
            case HSType.TUI64:
                self.value = read_integer(f, False, 8, header.byteorder)
            case _:
                assert False, f"Type not implemented: {self.type.name}"
