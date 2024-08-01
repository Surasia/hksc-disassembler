import click

from ..loader.hs_function import HSFunction
from ..loader.hs_opcodes import HSOpArgMode, HSOpCode, HSType
from ..loader.hs_instruction import HSInstruction, HSOpArg


class InstructionPrinter:
    def __init__(self, function: HSFunction):
        self.function: HSFunction = function

    def print_instructions(self) -> None:
        for instruction in self.function.instructions:
            self.print_instruction(instruction)

    def print_instruction(self, i: HSInstruction) -> None:
        if i.opCode != HSOpCode.DATA:
            click.secho(f"   - {i.opCode.name}: ", fg="yellow", nl=False)

        match i.opCode:
            case HSOpCode.GETFIELD | HSOpCode.GETFIELD_R1 | HSOpCode.GETFIELD_MM:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                self.print_arg(i.args[2])

            case HSOpCode.LOADK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1], True)

            case HSOpCode.LOADBOOL:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho(f"[{bool(i.args[1].value)}]", fg="bright_blue", nl=False)
                click.secho("; ", nl=False)
                self.print_arg(i.args[2])
                if bool(i.args[2].value):
                    click.secho("pc++", nl=False)

            case HSOpCode.GETGLOBAL_MEM | HSOpCode.GETGLOBAL:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1], True)

            case HSOpCode.SETGLOBAL:
                self.print_arg(i.args[1], True)
                click.secho(":= ", nl=False)
                self.print_arg(i.args[0])

            case HSOpCode.SETFIELD | HSOpCode.SETFIELD_R1:
                self.print_arg(i.args[0])
                self.print_arg(i.args[1])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.MOVE:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])

            case HSOpCode.LOADNIL:
                self.print_arg(i.args[0])
                click.secho(":= ... := ", nl=False)
                self.print_arg(i.args[1])
                click.secho(":= nil", nl=False)

            case HSOpCode.GETUPVAL:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("UpValue", nl=False, fg="bright_cyan")
                click.secho(f"[{i.args[1].value}]", fg="bright_blue", nl=False)

            case HSOpCode.GETTABLE | HSOpCode.GETTABLE_S:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("Index: ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.SETUPVAL | HSOpCode.SETUPVAL_R1:
                self.print_arg(i.args[1])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[0])
                click.secho("UpValue", nl=False, fg="bright_cyan")
                click.secho(f"[{i.args[0].value}]", fg="bright_blue", nl=False)

            case HSOpCode.SETTABLE | HSOpCode.SETTABLE_S | HSOpCode.SETTABLE_BK | HSOpCode.SETTABLE_S_BK:
                self.print_arg(i.args[0])
                click.secho("Index: ", nl=False)
                self.print_arg(i.args[1])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.NEWTABLE:
                self.print_arg(i.args[0])
                click.secho(":= {} size = ", nl=False)
                self.print_arg(i.args[1])
                self.print_arg(i.args[2])

            case HSOpCode.SELF:
                self.print_arg(i.args[0])
                click.secho(f"[{i.args[0].value + 1}] ", nl=False, fg="bright_blue")
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("; ", nl=False)
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("Index: ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.ADD | HSOpCode.ADD_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("+ ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.SUB | HSOpCode.SUB_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("- ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.MUL | HSOpCode.MUL_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("* ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.DIV | HSOpCode.DIV_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("/ ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.MOD | HSOpCode.MOD_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("% ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.POW | HSOpCode.POW_BK:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("^ ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.UNM:
                self.print_arg(i.args[0])
                click.secho(":= -", nl=False)
                self.print_arg(i.args[1])

            case HSOpCode.NOT | HSOpCode.NOT_R1:
                self.print_arg(i.args[0])
                click.secho(":= not ", nl=False)
                self.print_arg(i.args[1])

            case HSOpCode.LEN:
                self.print_arg(i.args[0])
                click.secho(":= length of ", nl=False)
                self.print_arg(i.args[1])

            case HSOpCode.CONCAT:
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho(".. ... .. ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.JMP:
                click.secho("pc += ", nl=False)
                self.print_arg(i.args[1])

            case HSOpCode.EQ | HSOpCode.EQ_BK:
                click.secho("if ", nl=False)
                self.print_arg(i.args[1])
                click.secho("== ", nl=False)
                self.print_arg(i.args[2])
                click.secho("~= ", nl=False)
                self.print_arg(i.args[0])
                click.secho("then pc++", nl=False)

            case HSOpCode.LT | HSOpCode.LT_BK:
                click.secho("if ", nl=False)
                self.print_arg(i.args[1])
                click.secho("< ", nl=False)
                self.print_arg(i.args[2])
                click.secho("~= ", nl=False)
                self.print_arg(i.args[0])
                click.secho("then pc++", nl=False)

            case HSOpCode.LE | HSOpCode.LE_BK:
                click.secho("if ", nl=False)
                self.print_arg(i.args[1])
                click.secho("<= ", nl=False)
                self.print_arg(i.args[2])
                click.secho("~= ", nl=False)
                self.print_arg(i.args[0])
                click.secho("then pc++", nl=False)

            case HSOpCode.TEST:
                click.secho("if not ", nl=False)
                self.print_arg(i.args[0])
                click.secho("<=> ", nl=False)
                self.print_arg(i.args[1])
                click.secho("then pc++", nl=False)

            case HSOpCode.TESTSET:
                click.secho("if ", nl=False)
                self.print_arg(i.args[1])
                click.secho("<=> ", nl=False)
                self.print_arg(i.args[2])
                click.secho("then ", nl=False)
                self.print_arg(i.args[0])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[1])
                click.secho("else pc++", nl=False)

            case HSOpCode.CHECKTYPE:
                self.print_arg(i.args[0])
                click.secho("? ", nl=False)
                self.print_arg(i.args[1])
                click.secho(f"[{HSType(i.args[1].value).name}]", nl=False, fg="bright_blue")

            case HSOpCode.NEWSTRUCT:
                self.print_arg(i.args[0])
                click.secho(":= {} size = ", nl=False)
                self.print_arg(i.args[1])
                self.print_arg(i.args[2])

            case HSOpCode.SETSLOTN:
                self.print_arg(i.args[0])
                click.secho("Slot: ", nl=False)
                self.print_arg(i.args[1])
                click.secho(":= nil", nl=False)

            case HSOpCode.SETSLOTI | HSOpCode.SETSLOTS | HSOpCode.SETSLOTMT | HSOpCode.SETSLOT:
                self.print_arg(i.args[0])
                click.secho("Slot: ", nl=False)
                self.print_arg(i.args[1])
                click.secho(":= ", nl=False)
                self.print_arg(i.args[2])

            case HSOpCode.DATA:
                ...

            case _:
                for arg in i.args:
                    self.print_arg(arg)

        if i.opCode != HSOpCode.DATA:
            click.echo()

    def print_arg(self, arg: HSOpArg, is_const: bool = False) -> None:
        click.secho(f"{arg.mode.name}(", fg="bright_cyan", nl=False)
        click.secho(f"{arg.value}) ", fg="bright_blue", nl=False)

        if arg.mode == HSOpArgMode.CONST or is_const:
            if self.function.constants:
                self.print_constant(arg)

    def print_constant(self, arg: HSOpArg) -> None:
        click.secho(f"[{self.function.constants[arg.value].value}] ", nl=False, fg="bright_blue")
