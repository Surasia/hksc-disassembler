from io import BytesIO
import struct

__all__ = ["read_integer", "read_string", "read_float", "read_bool", "read_double"]


def read_integer(f: BytesIO, signed: bool, size: int, byteorder: str = "big") -> int:
    """Read integer from bytes."""
    return int.from_bytes(f.read(size), byteorder, signed=signed)  # type: ignore


def read_bool(f: BytesIO, signed: bool, size: int, byteorder: str = "big") -> bool:
    """Read bool from bytes."""
    return bool.from_bytes(f.read(size), byteorder, signed=signed)  # type: ignore


def read_string(f: BytesIO, size: int) -> str:
    """Reads string of specified size."""
    return struct.unpack(f"{size}s", f.read(size))[0].decode("utf-8")


def read_float(f: BytesIO, byteorder: str = "big") -> float:
    """Read float from bytes."""
    if byteorder == "big":
        return struct.unpack(">f", f.read(4))[0]
    else:
        return struct.unpack("f", f.read(4))[0]


def read_double(f: BytesIO, byteorder: str = "big") -> float:
    """Read double from bytes."""
    if byteorder == "big":
        return struct.unpack(">d", f.read(4))[0]
    else:
        return struct.unpack("d", f.read(4))[0]
