# hksc-disassembler Changelog

## 0.2.3 (2024-08-01)
### Fixes:
- Formatting issues with debug info has been fixed.

## 0.2.2 (2024-08-01)
### Improvements:
- Constants, Instructions and Debug Info path will now only print if they exist.
- Made changes to formatting to be more similar to a YAML-like syntax.
# New Features:
- Added support for BK math operations.

## 0.2.1 (2024-07-29)
### Fixes:
- Incorrect reading on the SETTABLE instruction has been fixed.

## 0.2.0 (2024-07-29)
### New Features:
- Documentation has been added for basic info regarding HavokScript
- Many OpCodes will now print according to their lopcodes.h definitions.
- Tests have been added as part of the CI.
- HSVarArg is now a flag.

## 0.1.5 (2024-07-28)
### Fixes:
- Structures will now only print if there's more than one.
### New Features:
- Moved instructions to its own printer, which will now properly print out values for GETFIELD, GETFIELD_R1, LOADK, LOADBOOL, GETGLOBAL_MEM and GETGLOBAL.

## 0.1.4 (2024-07-27)
### Fixes:
- Incorrect header data reading now fixed.
### New Features:
- Instructions with CONST() and the LOADK OpCode will now display the constant commented.

## 0.1.3 (2024-07-27)
### Fixes:
- Floats and doubles are now read with their proper byte order.
- Naming changes for disassembler CLI

## 0.1.2 (2024-07-27)
### Fixes:
- Floats and integers are now read properly, according to their type.

## 0.1.1 (2024-07-25)
### Fixes:
- Changed Magenta to bright blue for better readability.

## 0.1.0 (2024-07-25)
Initial Release.