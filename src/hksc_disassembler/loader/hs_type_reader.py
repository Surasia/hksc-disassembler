from io import BytesIO

from .hs_header import HSHeader
from ..common.reader import read_integer, read_string, read_double, read_float


def read_t_string(f: BytesIO, header: HSHeader) -> str:
    size: int = 0
    string: str = ""

    if header.tSize == 4:
        size = read_integer(f, False, 4, header.byteorder)
    else:
        size = read_integer(f, False, 8, header.byteorder)

    if size != 0:
        string = read_string(f, size - 1)
        f.seek(1, 1)

    return string


def read_t_number(f: BytesIO, header: HSHeader) -> int | float:
    value: int | float = 0
    if header.numberType == 1:
        value = read_integer(f, True, header.intSize, header.byteorder)
    else:
        if header.intSize == 8:
            value = read_double(f, header.byteorder)
        else:
            value = read_float(f, header.byteorder)

    return value
