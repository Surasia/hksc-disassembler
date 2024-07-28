# hksc_disassembler

[![latest](https://img.shields.io/pypi/v/hksc-disassembler.svg)](https://pypi.python.org/pypi/hksc-disassembler/)

`hksc_disassembler` is a HavokScript 5.1 disassembler written in python. It includes a file parser for lua bytecode, as well as a CLI to interact with library functions.

## Installation

`hksc_disassembler` is available on pypi.

`pip install hksc-disassembler`

## Documentation
Documentation for HavokScript types and internals can be found in the [docs](./docs) folder. As the project gets more complex, additional documentation will be made available to account for it. The goal for the documentation is to both provide context for the logic inside this project, but also document the largely undocumented HavokScript bytecode format.

## CLI Usage

`hksc_disassembler disassamble <path_to_havokscript>`

## Credits
- Soupstream for the amazing [havok-script-tools](https://github.com/soupstream/havok-script-tools), most of which this project is based off of.
- Jake-NotTheMuss for their very insightful [hksc](https://github.com/Jake-NotTheMuss/hksc).
- Katalash for their  [DSLuaDecompiler](https://github.com/katalash/DSLuaDecompiler), a very advanced decompiler for HavokScript.