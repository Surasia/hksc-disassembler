import click
from typing import List

from ..loader.hs_debug import HSFunctionDebugInfo

from ..loader.hs_opcodes import HSOpArgMode, HSOpCode, HSType
from ..loader.hs_instruction import HSInstruction, HSOpArg
from ..loader.hs_constant import HSConstant


def print_instruction(i: HSInstruction, c: List[HSConstant], debug_info: HSFunctionDebugInfo) -> None:
    click.secho(f"     - {i.opCode.name}: ", fg="yellow", nl=False)

    match i.opCode:
        case HSOpCode.GETFIELD | HSOpCode.GETFIELD_R1 | HSOpCode.GETFIELD_MM:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            print_arg(i.args[2], c)

        case HSOpCode.LOADK:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c, True)

        case HSOpCode.LOADBOOL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho(f"[{bool(i.args[1].value)}]", fg="bright_blue", nl=False)
            click.secho("; ", nl=False)
            print_arg(i.args[2])
            if bool(i.args[2].value):
                click.secho("pc++", nl=False)

        case HSOpCode.GETGLOBAL_MEM | HSOpCode.GETGLOBAL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c, True)

        case HSOpCode.SETGLOBAL:
            print_arg(i.args[1], c, True)
            click.secho(":= ", nl=False)
            print_arg(i.args[0])

        case HSOpCode.SETFIELD | HSOpCode.SETFIELD_R1:
            print_arg(i.args[0])
            print_arg(i.args[1], c)
            click.secho(":= ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.MOVE:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])

        case HSOpCode.LOADNIL:
            print_arg(i.args[0])
            click.secho(":= ... := ", nl=False)
            print_arg(i.args[1])
            click.secho(":= nil", nl=False)

        case HSOpCode.GETUPVAL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("UpValue", nl=False, fg="bright_cyan")
            click.secho(f"[{i.args[1].value}]", fg="bright_blue", nl=False)
            if debug_info.upValueCount != 0 and i.args[1].value <= debug_info.upValueCount:
                click.secho(f" [{debug_info.upValues[i.args[1].value]}]", fg="bright_blue", nl=False)

        case HSOpCode.GETTABLE | HSOpCode.GETTABLE_S:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("Index: ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.SETUPVAL | HSOpCode.SETUPVAL_R1:
            print_arg(i.args[1])
            click.secho(":= ", nl=False)
            print_arg(i.args[0])
            click.secho("UpValue", nl=False, fg="bright_cyan")
            click.secho(f"[{i.args[0].value}]", fg="bright_blue", nl=False)
            if debug_info.upValueCount != 0 and i.args[0].value <= debug_info.upValueCount:
                click.secho(f"-- {debug_info.upValues[i.args[0].value]}", fg="bright_blue", nl=False)

        case HSOpCode.SETTABLE | HSOpCode.SETTABLE_S:
            print_arg(i.args[0])
            click.secho("Index: ", nl=False)
            print_arg(i.args[1], c)
            click.secho(":= ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.NEWTABLE:
            print_arg(i.args[0])
            click.secho(":= {} size = ", nl=False)
            print_arg(i.args[1])
            print_arg(i.args[2])

        case HSOpCode.SELF:
            print_arg(i.args[0])
            click.secho(f"[{i.args[0].value + 1}] ", nl=False, fg="bright_blue")
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("; ", nl=False)
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("Index: ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.ADD:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("+ ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.SUB:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("- ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.MUL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("* ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.DIV:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("/ ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.MOD:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("% ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.POW:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho("^ ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.UNM:
            print_arg(i.args[0])
            click.secho(":= -", nl=False)
            print_arg(i.args[1], c)

        case HSOpCode.NOT:
            print_arg(i.args[0])
            click.secho(":= not ", nl=False)
            print_arg(i.args[1], c)

        case HSOpCode.LEN:
            print_arg(i.args[0])
            click.secho(":= length of ", nl=False)
            print_arg(i.args[1], c)

        case HSOpCode.CONCAT:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1], c)
            click.secho(".. ... .. ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.JMP:
            click.secho("pc += ", nl=False)
            print_arg(i.args[1])

        case HSOpCode.EQ:
            click.secho("if ", nl=False)
            print_arg(i.args[1], c)
            click.secho("== ", nl=False)
            print_arg(i.args[2], c)
            click.secho("~= ", nl=False)
            print_arg(i.args[0])
            click.secho("then pc++", nl=False)

        case HSOpCode.LT:
            click.secho("if ", nl=False)
            print_arg(i.args[1], c)
            click.secho("< ", nl=False)
            print_arg(i.args[2], c)
            click.secho("~= ", nl=False)
            print_arg(i.args[0])
            click.secho("then pc++", nl=False)

        case HSOpCode.LE:
            click.secho("if ", nl=False)
            print_arg(i.args[1], c)
            click.secho("<= ", nl=False)
            print_arg(i.args[2], c)
            click.secho("~= ", nl=False)
            print_arg(i.args[0])
            click.secho("then pc++", nl=False)

        case HSOpCode.TEST:
            click.secho("if not ", nl=False)
            print_arg(i.args[0])
            click.secho("<=> ", nl=False)
            print_arg(i.args[1])
            click.secho("then pc++", nl=False)

        case HSOpCode.TESTSET:
            click.secho("if ", nl=False)
            print_arg(i.args[1])
            click.secho("<=> ", nl=False)
            print_arg(i.args[2])
            click.secho("then ", nl=False)
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("else pc++", nl=False)

        case HSOpCode.CHECKTYPE:
            print_arg(i.args[0])
            click.secho("? ", nl=False)
            print_arg(i.args[1])
            click.secho(f"[{HSType(i.args[1].value).name}]", nl=False, fg="bright_blue")

        case HSOpCode.NEWSTRUCT:
            print_arg(i.args[0])
            click.secho(":= {} size = ", nl=False)
            print_arg(i.args[1])
            print_arg(i.args[2])

        case HSOpCode.SETSLOTN:
            print_arg(i.args[0])
            click.secho("Slot: ", nl=False)
            print_arg(i.args[1])
            click.secho(":= nil", nl=False)

        case HSOpCode.SETSLOTI | HSOpCode.SETSLOTS | HSOpCode.SETSLOTMT | HSOpCode.SETSLOT:
            print_arg(i.args[0])
            click.secho("Slot: ", nl=False)
            print_arg(i.args[1])
            click.secho(":= ", nl=False)
            print_arg(i.args[2], c)

        case HSOpCode.DATA:
            print_arg(i.args[0])
            click.secho("-> ", nl=False)
            print_arg(i.args[1])

        case _:
            for arg in i.args:
                print_arg(arg, c)
    click.echo()


def print_arg(arg: HSOpArg, constants: List[HSConstant] = [], is_const: bool = False) -> None:
    click.secho(f"{arg.mode.name}(", fg="bright_cyan", nl=False)
    click.secho(f"{arg.value}) ", fg="bright_blue", nl=False)
    if arg.mode == HSOpArgMode.CONST or is_const:
        print_constant(arg, constants)


def print_constant(arg: HSOpArg, constants: List[HSConstant]) -> None:
    click.secho(f"[{constants[arg.value].value}] ", nl=False, fg="bright_blue")
