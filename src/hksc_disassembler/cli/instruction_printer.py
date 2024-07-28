import click
from typing import List

from ..loader.hs_opcodes import HSOpArgMode, HSOpCode
from ..loader.hs_instruction import HSInstruction, HSOpArg
from ..loader.hs_constant import HSConstant


def print_instruction(i: HSInstruction, c: List[HSConstant]) -> None:
    click.secho(f"     - {i.opCode.name}: ", fg="yellow", nl=False)

    match i.opCode:
        case HSOpCode.GETFIELD | HSOpCode.GETFIELD_R1:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho("-> ", nl=False)
            print_arg(i.args[2])
            print_constant(i.args[2], c)

        case HSOpCode.LOADK:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            print_constant(i.args[1], c)

        case HSOpCode.LOADBOOL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            click.secho(f"[{bool(i.args[1].value)}] ", fg="bright_blue", nl=False)
            print_arg(i.args[2])

        case HSOpCode.GETGLOBAL_MEM | HSOpCode.GETGLOBAL:
            print_arg(i.args[0])
            click.secho(":= ", nl=False)
            print_arg(i.args[1])
            print_constant(i.args[1], c)

        case HSOpCode.SETGLOBAL:
            print_arg(i.args[1])
            print_constant(i.args[1], c)
            click.secho(":= ", nl=False)
            print_arg(i.args[0])

        case _:
            for arg in i.args:
                if arg.mode == HSOpArgMode.CONST:
                    print_arg(arg)
                    print_constant(arg, c)
                else:
                    print_arg(arg)
    click.echo()


def print_arg(arg: HSOpArg) -> None:
    click.secho(f"{arg.mode.name}(", fg="bright_cyan", nl=False)
    click.secho(f"{arg.value}) ", fg="bright_blue", nl=False)


def print_constant(arg: HSOpArg, constants: List[HSConstant]) -> None:
    click.secho(f"[{constants[arg.value].value}] ", nl=False, fg="bright_blue")
