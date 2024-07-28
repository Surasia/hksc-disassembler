from click.testing import CliRunner
from hksc_disassembler.cli.disassembler import disassemble

def test_cli_hsc() -> None:
    runner = CliRunner()
    result = runner.invoke(disassemble, ['./tests/files/hsc_example.luac'])
    assert result.exit_code == 0

def test_cli_luas() -> None:
    runner = CliRunner()
    result = runner.invoke(disassemble, ['./tests/files/luas_example.luac'])
    assert result.exit_code == 0