from io import BytesIO
from hksc_disassembler.loader.hs import HavokScriptFile


def test_hsc() -> None:
    with open("./tests/files/hsc_example.luac", "rb") as f:
        hk_file: HavokScriptFile = HavokScriptFile()
        hk_file.read(BytesIO(f.read()))


def test_luas() -> None:
    with open("./tests/files/luas_example.luac", "rb") as f:
        hk_file: HavokScriptFile = HavokScriptFile()
        hk_file.read(BytesIO(f.read()))
