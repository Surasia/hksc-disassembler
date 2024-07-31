from io import BytesIO

from .hs_header import HSHeader, HSNumberType
from ..common.reader import read_integer, read_string, read_double, read_float


def read_t_string(f: BytesIO, header: HSHeader) -> str:
    size: int = read_integer(f, False, header.tSize, header.byteorder)
    string: str = ""
    if size != 0:
        string = read_string(f, size - 1)
        f.seek(1, 1)

    return string


def read_t_number(f: BytesIO, header: HSHeader) -> int | float:
    value: int | float
    if header.numberType == HSNumberType.INTEGER:
        value = read_integer(f, True, header.intSize, header.byteorder)
    else:
        if header.intSize == 8:
            value = read_double(f, header.byteorder)
        else:
            value = read_float(f, header.byteorder)

    return value
