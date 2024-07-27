import click

from ..loader.hs import HavokScriptFile
from ..loader.hs_constant import HSConstant
from ..loader.hs_debug import HSFunctionDebugInfo
from ..loader.hs_function import HSFunction
from ..loader.hs_instruction import HSInstruction
from ..loader.hs_structure import HSStructBlock


@click.group()
def cli() -> None:
    pass


def print_instruction(instruction: HSInstruction) -> None:
    click.secho(f"     - {instruction.opCode.name}", fg="yellow", nl=False)
    for arg in instruction.args:
        click.secho(f" {arg.mode.name}", fg="bright_cyan", nl=False)
        click.secho(f"({arg.value})", fg="bright_blue", nl=False)
    click.echo()


def print_constant(constant: HSConstant) -> None:
    click.secho(f"     - {constant.type.name}", fg="yellow", nl=False)
    click.secho(f" {constant.value}", fg="bright_cyan")


def print_header(hk_file: HavokScriptFile) -> None:
    click.secho("Endianness: ", fg="yellow", nl=False)
    click.secho(hk_file.header.endianness.name, fg="bright_cyan")

    click.secho("Int Size: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.intSize}", fg="bright_cyan")

    click.secho("Type Size: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.tSize}", fg="bright_cyan")

    click.secho("Instruction Size: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.instructionSize}", fg="bright_cyan")

    click.secho("Number Size: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.numberSize}", fg="bright_cyan")

    click.secho("Number Type: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.numberType.name}", fg="bright_cyan")

    click.secho("Extensions: ", fg="yellow", nl=False)
    click.secho(f"{hk_file.header.compatBits.name}", fg="bright_cyan")

    click.echo()


def print_debug(debug_info: HSFunctionDebugInfo) -> None:
    click.secho("     - Function Name: ", fg="yellow", nl=False)
    click.secho(f"{debug_info.functionName}", fg="bright_cyan")

    click.secho("     - Path: ", fg="yellow", nl=False)
    click.secho(f"{debug_info.path}", fg="bright_cyan")

    click.secho("       Locals: ", fg="bright_blue")

    for local in debug_info.locals:
        click.secho("          - ", fg="yellow", nl=False)
        click.secho(local.localName, fg="bright_cyan")

    click.secho("       UpValues: ", fg="bright_blue")

    for upvalue in debug_info.upValues:
        click.secho("          - ", fg="yellow", nl=False)
        click.secho(upvalue, fg="bright_cyan")

    click.echo()


def print_enums(hk_file: HavokScriptFile) -> None:
    for enum in hk_file.enums.entries:
        click.secho("Name: ", fg="yellow", nl=False)
        click.secho(enum.name, fg="bright_cyan")

        click.secho("Value: ", fg="yellow", nl=False)
        click.secho(enum.value, fg="bright_cyan")
    click.echo()


def print_structures(structure: HSStructBlock) -> None:
    click.secho("- Structure: ", fg="bright_blue", nl=False)
    click.secho(structure.header.name, fg="bright_cyan")
    for member in structure.members:
        click.secho(f"   - {member.header.type.name} ", fg="yellow", nl=False)
        click.secho(member.header.name, fg="bright_cyan")
    click.echo()


def print_functions(function: HSFunction) -> None:
    if function.hasDebugInfo and function.debugInfo.functionName != "":
        click.secho(f"- Function: {function.debugInfo.functionName}", fg="bright_blue")
    else:
        click.secho(f"- Function: {hex(function.functionOffset)}", fg="bright_blue")

    click.secho("    - UpValue Count: ", fg="yellow", nl=False)
    click.secho(function.upValueCount, fg="bright_cyan")

    click.secho("    - Parameter Count: ", fg="yellow", nl=False)
    click.secho(function.paramCount, fg="bright_cyan")

    click.secho("    - Variable Arguments: ", fg="yellow", nl=False)
    click.secho(function.isVarArg, fg="bright_cyan")

    click.secho("    - Slot Count: ", fg="yellow", nl=False)
    click.secho(function.slotCount, fg="bright_cyan")

    click.secho("    - Max Stack Count: ", fg="yellow", nl=False)
    click.secho(function.maxStackCount, fg="bright_cyan")

    click.secho("   Instructions:", fg="bright_blue")

    for instruction in function.instructions:
        print_instruction(instruction)

    click.secho("   Constants:", fg="bright_blue")

    for constant in function.constants:
        print_constant(constant)

    if function.hasDebugInfo:
        click.secho("   Debug Info:", fg="bright_blue")
        print_debug(function.debugInfo)

    for func in function.childFunctions:
        print_functions(func)
        click.echo()


@cli.command()
@click.argument("path", type=click.File("rb"))
def disassemble(path: click.File) -> None:
    hk_file = HavokScriptFile()
    hk_file.read(path)  # type: ignore

    click.secho("[Header Info]", fg="bright_green")
    print_header(hk_file)

    click.secho("[Enum Types]", fg="bright_green")
    print_enums(hk_file)

    click.secho("[Functions]", fg="bright_green")
    print_functions(hk_file.mainFunction)

    click.secho("[Structures]", fg="bright_green")
    for structure in hk_file.structures:
        print_structures(structure)


if __name__ == "__main__":
    cli()
