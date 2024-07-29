from enum import IntFlag
from io import BytesIO
from typing import List

from ..common.reader import align_to_bytes, read_integer
from .hs_debug import HSFunctionDebugInfo
from .hs_header import HSHeader
from .hs_instruction import HSInstruction
from .hs_constant import HSConstant


class HSVarArg(IntFlag):
    VARARG_HASARG = 1
    VARARG_ISVARARG = 2
    VARARG_NEEDSARG = 4


class HSFunction:
    def __init__(self) -> None:
        self.upValueCount: int = -1
        self.paramCount: int = -1
        self.isVarArg: HSVarArg = HSVarArg(1)
        self.slotCount: int = -1
        self.unk: int = -1
        self.instructionCount: int = -1
        self.instructions: List[HSInstruction] = []
        self.constantCount: int = -1
        self.constants: List[HSConstant] = []
        self.hasDebugInfo: int = -1
        self.debugInfo: HSFunctionDebugInfo = HSFunctionDebugInfo()
        self.childFunctionCount: int = -1
        self.childFunctions: List[HSFunction] = []
        self.functionOffset: int = -1

    def read(self, f: BytesIO, header: HSHeader) -> None:
        self.upValueCount = read_integer(f, False, 4, header.byteorder)
        self.paramCount = read_integer(f, False, 4, header.byteorder)
        self.isVarArg = HSVarArg(read_integer(f, False, 1, header.byteorder))
        self.slotCount = read_integer(f, False, 4, header.byteorder)
        self.unk = read_integer(f, False, 4, header.byteorder)
        self.instructionCount = read_integer(f, False, 4, header.byteorder)

        align_to_bytes(f, 4)

        for _ in range(self.instructionCount):
            instruction: HSInstruction = HSInstruction()
            instruction.read(f, header.byteorder)
            self.instructions.append(instruction)

        self.constantCount = read_integer(f, False, 4, header.byteorder)
        for _ in range(self.constantCount):
            constant: HSConstant = HSConstant()
            constant.read(f, header)
            self.constants.append(constant)

        self.hasDebugInfo = read_integer(f, False, 4, header.byteorder)
        if self.hasDebugInfo:
            self.debugInfo.read(f, header)

        function_count = read_integer(f, False, 4, header.byteorder)
        for _ in range(function_count):
            child_function = HSFunction()
            child_function.read(f, header)
            self.childFunctions.append(child_function)

        self.functionOffset = f.tell()
