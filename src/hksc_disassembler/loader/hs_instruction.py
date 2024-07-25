from typing import List
from io import BytesIO

from ..common.reader import read_integer
from .hs_opcodes import HSOpArgMode, HSOpArgModeBC, HSOpCode, HSOpModeList, HSOpModes, HSOpArgModeA, HSOpMode


class HSInstructionException(Exception):
    pass


class HSOpArg:
    def __init__(self, mode: HSOpArgMode, value: int) -> None:
        self.mode: HSOpArgMode = mode
        self.value: int = value


class HSInstruction:
    def __init__(self) -> None:
        self.opCode: HSOpCode = HSOpCode(0)
        self.args: List[HSOpArg] = []

    def read(self, f: BytesIO, endianness: str) -> None:
        raw: int = read_integer(f, False, 4, endianness)
        self.opCode = HSOpCode(raw >> 25)
        opModes: HSOpModes = HSOpModeList[self.opCode]
        self.read_op_a(raw, opModes)
        self.read_op_bc(raw, opModes)

    def read_op_a(self, raw: int, opModes: HSOpModes) -> None:
        mode: HSOpArgMode = HSOpArgMode.NUMBER if opModes.opArgModeA == HSOpArgModeA.UNUSED else HSOpArgMode.REG
        value: int = raw & 0xFF
        self.args.append(HSOpArg(mode, value))

    def read_op_abc_b(self, raw: int, opModes: HSOpModes) -> None:
        mode: HSOpArgMode
        value: int

        match opModes.opArgModeB:
            case HSOpArgModeBC.NUMBER:
                mode = HSOpArgMode.NUMBER
                value = (raw >> 17) & 0xFF
            case HSOpArgModeBC.OFFSET:
                mode = HSOpArgMode.NUMBER
                value = (raw >> 17) & 0x1FF
            case HSOpArgModeBC.REG:
                mode = HSOpArgMode.REG
                value = (raw >> 17) & 0xFF
            case HSOpArgModeBC.REG_OR_CONST:
                value = (raw >> 17) & 0x1FF
                if value < 0x100:
                    mode = HSOpArgMode.REG
                else:
                    mode = HSOpArgMode.CONST
                    value &= 0xFF
            case HSOpArgModeBC.CONST:
                mode = HSOpArgMode.CONST
                value = (raw >> 17) & 0xFF
            case _:
                raise HSInstructionException("ABC_B argument type does not match!")

        self.args.append(HSOpArg(mode, value))

    def read_op_abc_c(self, raw: int, opModes: HSOpModes) -> None:
        mode: HSOpArgMode
        value: int

        match opModes.opArgModeC:
            case HSOpArgModeBC.NUMBER:
                mode = HSOpArgMode.NUMBER
                value = (raw >> 8) & 0xFF
            case HSOpArgModeBC.OFFSET:
                mode = HSOpArgMode.NUMBER
                value = (raw >> 8) & 0x1FF
            case HSOpArgModeBC.REG:
                mode = HSOpArgMode.REG
                value = (raw >> 8) & 0xFF
            case HSOpArgModeBC.REG_OR_CONST:
                value = (raw >> 8) & 0x1FF
                if value < 0x100:
                    mode = HSOpArgMode.REG
                else:
                    mode = HSOpArgMode.CONST
                    value &= 0xFF
            case HSOpArgModeBC.CONST:
                mode = HSOpArgMode.CONST
                value = (raw >> 8) & 0xFF
            case _:
                raise HSInstructionException("ABC_C argument type does not match!")

        self.args.append(HSOpArg(mode, value))

    def read_op_non_abc_b(self, raw: int, opModes: HSOpModes) -> None:
        value = (raw >> 8) & 0x1FFFF
        mode = HSOpArgMode(0)
        if opModes.opMode == HSOpMode.ASBX:
            value -= 0xFFFF
        if HSOpArgModeBC.NUMBER or HSOpArgModeBC.OFFSET:
            mode = HSOpArgMode.NUMBER
        elif HSOpArgModeBC.CONST:
            mode = HSOpArgMode.CONST

        self.args.append(HSOpArg(mode, value))

    def read_op_bc(self, raw: int, opModes: HSOpModes) -> None:
        if opModes.opArgModeB != HSOpArgModeBC.UNUSED:
            if opModes.opMode == HSOpMode.ABC:
                self.read_op_abc_b(raw, opModes)
            else:
                self.read_op_non_abc_b(raw, opModes)

        if opModes.opMode == HSOpMode.ABC and opModes.opArgModeC != HSOpArgModeBC.UNUSED:
            self.read_op_abc_c(raw, opModes)
