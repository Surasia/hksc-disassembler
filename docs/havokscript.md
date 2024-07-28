# HavokScript 5.1 Overview

## Introduction
HavokScript 5.1 is an extension/fork of Lua 5.1.x, included in the now-discontinued Havok Game SDK. It is intended to be a "drop-in" replacement of existing Lua VMs that game engines used, adding Havok-specific features and bindings. It also included a Visual Studio plugin for debugging, alongside a profiler allowing for more granular testing over the built-in lua debug functionality.

## Games That Feature HavokScript
- Multiple FromSoftware games (Dark Souls, Bloodborne, Sekiro, Armored Core 6, Elden Ring)
- Halo 5/Halo Infinite
- Multiple Call Of Duty entries (Black Ops II and later)
- Civilisation VI
- many more...

## Extensions
The Havok license allows for studios to modify and extend the source code used in Havok products such as HavokScript. Multiple studios have created their own "Extensions" to the HavokScript VM to integrate with their engines, such as Infinity Ward and Treyarch in their Call Of Duty titles.

## Feature Extensions
The HavokScript compiler features flags that can be toggled to extend the capabilities of the VM. These include:
- Memoization
- Structures
- The "SELF" opCode
- Doubles type
- Native Int capability

These extensions are toggled on an engine-wide scale, with bytecode files containing "compatibility bits" in their function headers to indicate the features used.