# HavokScript Types

## Info
The Havok Script VM includes predefined types for constants internally, some inherited from Lua itself. These are defined in the header enum declarations, though seem to be universal.

## Definitions
> [!NOTE]
> "Size" is only specified if it is used as a constant type in bytecode. For types used inside the VM, only information is given.

### TNIL
- Info: None (Null/Nil) type.
- Size: 0 bytes.

### TBOOLEAN
- Info: Boolean type.
- Size: 1 byte.
  
## TLIGHTUSERDATA
- Info: C Pointer (void *)
- Size: Specified in header as "tSize"

## TNUMBER
- Info: Integer, float or double.
- Type: Depends on "numberType" in header
- Size: Depends on "numberSize" in header

## TSTRING
- Info: Null Terminated string of variable size.
- Structure:
    - Size: Read as uint32 or uint64 depending on "numberSize" in header.
    - String: Null terminated string of size without encoding.

## TTABLE
- Info: Hash table of values.

## TFUNCTION
- Info: Lua Function pointer.

## TUSERDATA
- Info: C data stored as a lua variable.

## TTHREAD
- Info: Lua Thread stack pointer.

## TIFUNCTION
- Info: Internal Function pointer.

## TCFUNCTION
- Info: C Function pointer.

## TUI64
- Info: 64 bit unsigned integer.
- Size: 8 bytes.

## TSTRUCT
- Info: Havok Structure defined if "STRUCTURES" extension is active.