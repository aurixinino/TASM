# TriCore TC1.6 Instruction Set Architecture

*Generated on November 01, 2025 from tricore_instruction_set.csv*

## Overview

This document provides a comprehensive reference for the TriCore TC1.6 instruction set architecture. The TriCore architecture features a unified 32-bit RISC/MCU/DSP processor core designed for real-time embedded applications.

### Key Features

- **Total Instructions**: 526 instruction variants
- **Unique Mnemonics**: 209 base instructions
- **Instruction Sizes**: 16-bit and 32-bit encodings
  - **16-bit Instructions**: 75 variants (compact encoding)
  - **32-bit Instructions**: 451 variants (full encoding)

### Instruction Format

TriCore instructions use two primary encoding formats:

- **16-bit Format**: Compact instructions for frequent operations
- **32-bit Format**: Full instructions with extended addressing and immediate values

### Quick Reference - Common Instructions

| Category | Instruction | Example | Description |
|----------|-------------|---------|-------------|
| **Arithmetic** | `ADD` | `ADD D[c],D[a],D[b]` | Add two registers |
| | `SUB` | `SUB D[c],D[a],const9` | Subtract immediate |
| **Load/Store** | `LD.W` | `LD.W D[a],[A[b]]` | Load word from memory |
| | `ST.W` | `ST.W [A[a]],D[b]` | Store word to memory |
| **Logical** | `AND` | `AND D[c],D[a],D[b]` | Bitwise AND |
| | `OR` | `OR D[c],D[a],const9` | Bitwise OR with immediate |
| **Branch** | `JEQ` | `JEQ D[a],const4,disp15` | Jump if equal |
| | `CALL` | `CALL disp24` | Call subroutine |
| **System** | `NOP` | `NOP` | No operation |
| | `RET` | `RET` | Return from subroutine |

---

## Instruction Categories


### Instruction Distribution by Category

| Category | Count | Percentage |
|----------|-------|------------|
| Arithmetic | 66 | 12.5% |
| Logical | 24 | 4.6% |
| Bit Operations | 22 | 4.2% |
| Load/Store | 91 | 17.3% |
| Branch/Jump | 62 | 11.8% |
| System | 5 | 1.0% |
| Floating Point | 0 | 0.0% |
| Packed Operations | 154 | 29.3% |
| Address Operations | 0 | 0.0% |
| Other | 102 | 19.4% |

---

## Arithmetic Instructions

*66 instructions*

### ABS

**Absolute Value**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01C0000B` | 32-bit | `ABS D[c],D[b]` | See pag.49 |

### ABS.B

**Absolute Value Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x05C0000B` | 32-bit | `ABS.B D[c],D[b]` | See pag.50 |

### ABS.H

**Absolute Value Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07C0000B` | 32-bit | `ABS.H D[c],D[b]` | See pag.50 |

### ABSDIF

**Absolute Value of Difference**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E0008B` | 32-bit | `ABSDIF D[c],D[a],const9` | See pag.52 |
| `0x00E0008B` | 32-bit | `ABSDIF D[c],D[a],D[b]` | See pag.52 |

### ABSDIF.B

**Absolute Value of Difference Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04E0000B` | 32-bit | `ABSDIF.B D[c],D[a],D[b]` | See pag.53 |

### ABSDIF.H

**Absolute Value of Difference Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x06E0000B` | 32-bit | `ABSDIF.H D[c],D[a],D[b]` | See pag.53 |

### ABSDIFS

**Absolute Value of Difference with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00F0008B` | 32-bit | `ABSDIFS D[c],D[a],const9` | See pag.55 |
| `0x00F0000B` | 32-bit | `ABSDIFS D[c],D[a],D[b]` | See pag.55 |

### ABSDIFS.H

**Absolute Value of Difference Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x06F0000B` | 32-bit | `ABSDIFS.H D[c],D[a],D[b]` | See pag.56 |

### ABSS

**Absolute Value with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01D0000B` | 32-bit | `ABSS D[c],D[b]` | See pag.57 |

### ABSS.H

**Absolute Value Packed Half-word with Saturatio**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07D0000B` | 32-bit | `ABSS.H D[c],D[b]` | See pag.58 |

### ADD

**Add**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000008B` | 32-bit | `ADD D[c],D[a],const9` | See pag.59 |
| `0x0000000B` | 32-bit | `ADD D[c],D[a],D[b]` | See pag.59 |
| `0xC2` | 16-bit | `ADD D[a],const4` | See pag.59 |
| `0x92` | 16-bit | `ADD D[a],D[15],const4` | See pag.59 |
| `0x9A` | 16-bit | `ADD D[15],D[a],const4` | See pag.59 |
| `0x42` | 16-bit | `ADD D[a],D[b]` | See pag.60 |
| `0x12` | 16-bit | `ADD D[a],D[15],D[b]` | See pag.60 |
| `0x1A` | 16-bit | `ADD D[15],D[a],D[b]` | See pag.60 |

### ADD.A

**Add Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00100001` | 32-bit | `ADD.A A[c],A[a],A[b]` | See pag.62 |
| `0xB0` | 16-bit | `ADD.A A[a],const4` | See pag.62 |
| `0x30` | 16-bit | `ADD.A A[a],A[b]` | See pag.62 |

### ADD.B

**Add Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0400000B` | 32-bit | `ADD.B D[c],D[a],D[b]` | See pag.63 |

### ADD.H

**Add Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0600000B` | 32-bit | `ADD.H D[c],D[a],D[b]` | See pag.63 |

### ADDC

**Add with Carry**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0050008B` | 32-bit | `ADDC D[c],D[a],const9` | See pag.65 |
| `0x0050000B` | 32-bit | `ADDC D[c],D[a],D[b]` | See pag.65 |

### ADDI

**Add Immediate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x1B` | 32-bit | `ADDI D[c],D[a],const16 (RLC)` | See pag.66 |

### ADDIH

**Add Immediate High**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x9B` | 32-bit | `ADDIH D[c],D[a],const16 (RLC)` | See pag.67 |

### ADDIH.A

**Add Immediate High to Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x11` | 32-bit | `ADDIH.A A[c],A[a],const16 (RLC)` | See pag.68 |

### ADDS

**Add Signed with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0020008B` | 32-bit | `ADDS D[c],D[a],const9` | See pag.69 |
| `0x0020000B` | 32-bit | `ADDS D[c],D[a],D[b]` | See pag.69 |
| `0x22` | 16-bit | `ADDS D[a],D[b],` | See pag.69 |

### ADDS.H

**Add Signed Packed Half-word with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0620000B` | 32-bit | `ADDS.H D[c],D[a],D[b]` | See pag.71 |

### ADDS.HU

**Add Unsigned Packed Half-word with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0630000B` | 32-bit | `ADDS.HU D[c],D[a],D[b]` | See pag.71 |

### ADDS.U

**Add Unsigned with Saturation**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0030008B` | 32-bit | `ADDS.U D[c],D[a],const9` | See pag.73 |
| `0x0030000B` | 32-bit | `ADDS.U D[c],D[a],D[b]` | See pag.73 |

### ADDSC.A

**Add Scaled Index to Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x06000001` | 32-bit | `ADDSC.A A[c],A[b],D[a],n` | See pag.74 |
| `0x10` | 16-bit | `ADDSC.A A[a],A[b],D[15],n (SRRS)` | See pag.74 |

### ADDSC.AT

**Add Bit-Scaled Index to Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x06200001` | 32-bit | `ADDSC.AT A[c],A[b],D[a]` | See pag.74 |

### ADDX

**Add Extended**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0040008B` | 32-bit | `ADDX D[c],D[a],const9` | See pag.76 |
| `0x0040000B` | 32-bit | `ADDX D[c],D[a],D[b]` | See pag.76 |

### CLO

**Count Leading Ones**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01C0000F` | 32-bit | `CLO D[c],D[a]` | See pag.115 |

### CLO.H

**Count Leading Ones in Packed Half-words**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07D0000F` | 32-bit | `CLO.H D[c],D[a]` | See pag.116 |

### CLS

**Count Leading Signs**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01D0000F` | 32-bit | `CLS D[c],D[a]` | See pag.117 |

### CLS.H

**Count Leading Signs in Packed Half-words**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07E0000F` | 32-bit | `CLS.H D[c],D[a]` | See pag.118 |

### CLZ

**Count Leading Zeros**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01B0000F` | 32-bit | `CLZ D[c],D[a]` | See pag.119 |

### CLZ.H

**Count Leading Zeros in Packed Half-words**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07C0000F` | 32-bit | `CLZ.H D[c],D[a]` | See pag.120 |

### DIV

**Divide**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0200004B` | 32-bit | `DIV E[c],D[a],D[b]` | See pag.134 |

### DIV.U

**Divide Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0210004B` | 32-bit | `DIV.U E[c],D[a],D[b]` | See pag.134 |

### MAX

**Maximum Value**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0340008B` | 32-bit | `MAX D[c],D[a],const9` | See pag.265 |
| `0x0340000B` | 32-bit | `MAX D[c],D[a],D[b]` | See pag.265 |

### MAX.B

**Maximum Value Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x05A0000B` | 32-bit | `MAX.B D[c],D[a],D[b]` | See pag.267 |

### MAX.BU

**Maximum Value Packed Byte Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x05B0000B` | 32-bit | `MAX.BU D[c],D[a],D[b]` | See pag.267 |

### MAX.H

**Maximum Value Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07A0000B` | 32-bit | `MAX.H D[c],D[a],D[b]` | See pag.268 |

### MAX.HU

**Maximum Value Packed Half-word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x07B0000B` | 32-bit | `MAX.HU D[c],D[a],D[b]` | See pag.268 |

### MAX.U

**Maximum Value Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0360008B` | 32-bit | `MAX.U D[c],D[a],const9` | See pag.265 |
| `0x0360000B` | 32-bit | `MAX.U D[c],D[a],D[b]` | See pag.265 |

### MIN

**Minimum Value**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0300008B` | 32-bit | `MIN D[c],D[a],const9` | See pag.270 |
| `0x0300000B` | 32-bit | `MIN D[c],D[a],D[b]` | See pag.270 |

### MIN.B

**Minimum Value Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0580000B` | 32-bit | `MIN.B D[c],D[a],D[b]` | See pag.272 |

### MIN.BU

**Minimum Value Packed Byte Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0590000B` | 32-bit | `MIN.BU D[c],D[a],D[b]` | See pag.272 |

### MIN.H

**Minimum Value Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0780000B` | 32-bit | `MIN.H D[c],D[a],D[b]` | See pag.273 |

### MIN.HU

**Minimum Value Packed Half-word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0790000B` | 32-bit | `MIN.HU D[c],D[a],D[b]` | See pag.273 |

### MIN.U

**Minimum Value Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0320008B` | 32-bit | `MIN.U D[c],D[a],const9` | See pag.270 |
| `0x0320000B` | 32-bit | `MIN.U D[c],D[a],D[b]` | See pag.270 |

---

## Logical Instructions

*24 instructions*

### AND

**Bitwise AND**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0080008F` | 32-bit | `AND D[c],D[a],const9` | See pag.77 |
| `0x0080000F` | 32-bit | `AND D[c],D[a],D[b]` | See pag.77 |
| `0x16` | 16-bit | `AND D[15],const8 (SC)` | See pag.77 |
| `0x26` | 16-bit | `AND D[a],D[b]` | See pag.77 |

### AND.AND.T

**Accumulating Bit Logical AND-AND**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000047` | 32-bit | `AND.AND.T D[c],D[a],pos1,D[b],pos2` | See pag.79 |

### AND.ANDN.T

**Accumulating Bit Logical AND-AND-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00300047` | 32-bit | `AND.ANDN.T D[c],D[a,] pos1,D[b],pos2` | See pag.79 |

### AND.EQ

**Equal Accumulating**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0200008B` | 32-bit | `AND.EQ D[c],D[a],const9` | See pag.81 |
| `0x0200000B` | 32-bit | `AND.EQ D[c],D[a],D[b]` | See pag.81 |

### AND.GE

**Greater Than or Equal Accumulating**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0240008B` | 32-bit | `AND.GE D[c],D[a],const9` | See pag.82 |
| `0x0240000B` | 32-bit | `AND.GE D[c],D[a],D[b]` | See pag.82 |

### AND.GE.U

**Greater Than or Equal Accumulating Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0250008B` | 32-bit | `AND.GE.U D[c],D[a],const9` | See pag.82 |
| `0x0250000B` | 32-bit | `AND.GE.U D[c],D[a],D[b]` | See pag.82 |

### AND.LT

**Less Than Accumulating**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0220008B` | 32-bit | `AND.LT D[c],D[a],const9` | See pag.84 |
| `0x0220000B` | 32-bit | `AND.LT D[c],D[a],D[b]` | See pag.84 |

### AND.LT.U

**Less Than Accumulating Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0230008B` | 32-bit | `AND.LT.U D[c],D[a],const9` | See pag.84 |
| `0x0230000B` | 32-bit | `AND.LT.U D[c],D[a],D[b]` | See pag.84 |

### AND.NE

**Not Equal Accumulating**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0210008B` | 32-bit | `AND.NE D[c],D[a],const9` | See pag.86 |
| `0x0210000B` | 32-bit | `AND.NE D[c],D[a],D[b]` | See pag.86 |

### AND.NOR.T

**Accumulating Bit Logical AND-NOR**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00200047` | 32-bit | `AND.NOR.T D[c],D[a],pos1,D[b],pos2` | See pag.79 |

### AND.OR.T

**Accumulating Bit Logical AND-OR**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00100047` | 32-bit | `AND.OR.T D[c],D[a],pos1,D[b],pos2` | See pag.79 |

### AND.T

**Bit Logical AND**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000087` | 32-bit | `AND.T D[c],D[a],pos1,D[b],pos2` | See pag.87 |

### ANDN

**Bitwise AND-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E0008F` | 32-bit | `ANDN D[c],D[a],const9` | See pag.88 |
| `0x00E0000F` | 32-bit | `ANDN D[c],D[a],D[b]` | See pag.88 |

### ANDN.T

**Bit Logical AND-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00300087` | 32-bit | `ANDN.T D[c],D[a],pos1,D[b],pos2` | See pag.89 |

---

## Bit Operations Instructions

*22 instructions*

### BMERGE

**Bit Merge**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0010004B` | 32-bit | `BMERGE D[c],D[a],D[b]` | See pag.92 |

### BSPLIT

**Bit Split**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0090004B` | 32-bit | `BSPLIT E[c],D[a]` | See pag.93 |

### DEXTR

**Extract from Double Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000077` | 32-bit | `DEXTR D[c],D[a],D[b],pos` | See pag.129 |
| `0x00400017` | 32-bit | `DEXTR D[c],D[a],D[b],D[d]` | See pag.129 |

### EXTR

**Extract Bit Field**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00200037` | 32-bit | `EXTR D[c],D[a],pos,width` | See pag.150 |
| `0x00200017` | 32-bit | `EXTR D[c],D[a],E[d]` | See pag.150 |
| `0x00200057` | 32-bit | `EXTR D[c],D[a],D[d],width` | See pag.150 |

### EXTR.U

**Extract Bit Field Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00300037` | 32-bit | `EXTR.U D[c],D[a],pos,width` | See pag.150 |
| `0x00300017` | 32-bit | `EXTR.U D[c],D[a],E[d]` | See pag.150 |
| `0x00300057` | 32-bit | `EXTR.U D[c],D[a],D[d],width` | See pag.151 |

### IMASK

**Insert Mask**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x001000B7` | 32-bit | `IMASK E[c],const4,pos,width` | See pag.159 |
| `0x001000D7` | 32-bit | `IMASK E[c],const4,D[d],width` | See pag.159 |
| `0x00100037` | 32-bit | `IMASK E[c],D[b],pos,width` | See pag.159 |
| `0x00100057` | 32-bit | `IMASK E[c],D[b],D[d],width` | See pag.159 |

### INS.T

**Insert Bit**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000067` | 32-bit | `INS.T D[c],D[a],pos1,D[b],pos2` | See pag.161 |

### INSERT

**Insert Bit Field**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000B7` | 32-bit | `INSERT D[c],D[a],const4,pos,width` | See pag.162 |
| `0x00000097` | 32-bit | `INSERT D[c],D[a],const4,E[d]` | See pag.162 |
| `0x000000D7` | 32-bit | `INSERT D[c],D[a],const4,D[d],width` | See pag.162 |
| `0x00000037` | 32-bit | `INSERT D[c],D[a],D[b],pos,width` | See pag.162 |
| `0x00000017` | 32-bit | `INSERT D[c],D[a],D[b],E[d]` | See pag.163 |
| `0x00000057` | 32-bit | `INSERT D[c],D[a],D[b],D[d],width` | See pag.163 |

### INSN.T

**Insert Bit-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00100067` | 32-bit | `INSN.T D[c],D[a],pos1,D[b],pos2` | See pag.161 |

---

## Load/Store Instructions

*91 instructions*

### LD.A

**Load Word to Address Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x08000085` | 32-bit | `LD.A A[a],off18` | See pag.197 |
| `0x09800009` | 32-bit | `LD.A A[a],A[b],off10` | See pag.197 |
| `0x01800029` | 32-bit | `LD.A A[a],P[b]` | See pag.197 |
| `0x05800029` | 32-bit | `LD.A A[a],P[b],off10` | See pag.197 |
| `0x01800009` | 32-bit | `LD.A A[a],A[b],off10` | See pag.198 |
| `0x05800009` | 32-bit | `LD.A A[a],A[b],off10` | See pag.198 |
| `0x00000099` | 32-bit | `LD.A A[a],A[b],off16` | See pag.198 |
| `0xD8` | 16-bit | `LD.A A[15],A[10],const8` | See pag.198 |
| `0xD4` | 16-bit | `LD.A A[c],A[b]` | See pag.198 |
| `0xC4` | 16-bit | `LD.A A[c],A[b]` | See pag.198 |
| `0xC8` | 16-bit | `LD.A A[c],A[15],off4` | See pag.199 |
| `0xCC` | 16-bit | `LD.A A[15],A[b],off4` | See pag.199 |

### LD.B

**Load Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000005` | 32-bit | `LD.B D[a],off18` | See pag.200 |
| `0x08000009` | 32-bit | `LD.B D[a],A[b],off10` | See pag.200 |
| `0x00000029` | 32-bit | `LD.B D[a],P[b]` | See pag.200 |
| `0x04000029` | 32-bit | `LD.B D[a],P[b],off10` | See pag.200 |
| `0x00000009` | 32-bit | `LD.B D[a],A[b],off10` | See pag.201 |
| `0x04000009` | 32-bit | `LD.B D[a],A[b],off10` | See pag.201 |
| `0x00000079` | 32-bit | `LD.B D[a],A[b],off16` | See pag.201 |

### LD.BU

**Load Byte Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04000005` | 32-bit | `LD.BU D[a],off18` | See pag.201 |
| `0x08400009` | 32-bit | `LD.BU D[a],A[b],off10` | See pag.201 |
| `0x00400029` | 32-bit | `LD.BU D[a],P[b]` | See pag.201 |
| `0x04400029` | 32-bit | `LD.BU D[a],P[b],off10` | See pag.202 |
| `0x00400009` | 32-bit | `LD.BU D[a],A[b],off10` | See pag.202 |
| `0x04400009` | 32-bit | `LD.BU D[a],A[b],off10` | See pag.202 |
| `0x00000039` | 32-bit | `LD.BU D[a],A[b],off16` | See pag.202 |
| `0x14` | 16-bit | `LD.BU D[c],A[b]` | See pag.203 |
| `0x04` | 16-bit | `LD.BU D[c],A[b]` | See pag.203 |
| `0x08` | 16-bit | `LD.BU D[c],A[15],off4` | See pag.203 |
| `0x0C` | 16-bit | `LD.BU D[15],A[b],off4` | See pag.203 |

### LD.D

**Load Double-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04000085` | 32-bit | `LD.D E[a],off18` | See pag.204 |
| `0x09400009` | 32-bit | `LD.D E[a],A[b],off10` | See pag.204 |
| `0x01400029` | 32-bit | `LD.D E[a],P[b]` | See pag.204 |
| `0x05400029` | 32-bit | `LD.D E[a],P[b],off10` | See pag.204 |
| `0x01400009` | 32-bit | `LD.D E[a],A[b],off10` | See pag.205 |
| `0x05400009` | 32-bit | `LD.D E[a],A[b],off10` | See pag.205 |

### LD.DA

**Load Double-word to Address Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0C000085` | 32-bit | `LD.DA P[a],off18` | See pag.206 |
| `0x09C00009` | 32-bit | `LD.DA P[a],A[b],off10` | See pag.206 |
| `0x01C00029` | 32-bit | `LD.DA P[a],P[b]` | See pag.206 |
| `0x05C00029` | 32-bit | `LD.DA P[a],P[b],off10` | See pag.206 |
| `0x01C00009` | 32-bit | `LD.DA P[a],A[b],off10` | See pag.207 |
| `0x05C00009` | 32-bit | `LD.DA P[a],A[b],off10` | See pag.207 |

### LD.H

**Load Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x08000005` | 32-bit | `LD.H D[a],off18` | See pag.208 |
| `0x08800009` | 32-bit | `LD.H D[a],A[b],off10` | See pag.208 |
| `0x00800029` | 32-bit | `LD.H D[a],P[b]` | See pag.208 |
| `0x04800029` | 32-bit | `LD.H D[a],P[b],off10` | See pag.208 |
| `0x00800009` | 32-bit | `LD.H D[a],A[b],off10` | See pag.209 |
| `0x04800009` | 32-bit | `LD.H D[a],A[b],off10` | See pag.209 |
| `0x000000C9` | 32-bit | `LD.H D[a],A[b],off16` | See pag.209 |
| `0x94` | 16-bit | `LD.H D[c],A[b]` | See pag.209 |
| `0x84` | 16-bit | `LD.H D[c],A[b]` | See pag.209 |
| `0x88` | 16-bit | `LD.H D[c],A[15],off4` | See pag.209 |
| `0x8C` | 16-bit | `LD.H D[15],A[b],off4` | See pag.210 |

### LD.HU

**Load Half-word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0C000005` | 32-bit | `LD.HU D[a],off18` | See pag.210 |
| `0x08C00009` | 32-bit | `LD.HU D[a],A[b],off10` | See pag.210 |
| `0x00C00029` | 32-bit | `LD.HU D[a],P[b]` | See pag.210 |
| `0x04C00029` | 32-bit | `LD.HU D[a],P[b],off10` | See pag.210 |
| `0x00C00009` | 32-bit | `LD.HU D[a],A[b],off10` | See pag.211 |
| `0x04C00009` | 32-bit | `LD.HU D[a],A[b],off10` | See pag.211 |
| `0x000000B9` | 32-bit | `LD.HU D[a],A[b],off16` | See pag.211 |

### LD.Q

**Load Half-word Signed Fraction**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000045` | 32-bit | `LD.Q D[a],off18` | See pag.212 |
| `0x0A000009` | 32-bit | `LD.Q D[a],A[b],off10` | See pag.212 |
| `0x02000029` | 32-bit | `LD.Q D[a],P[b]` | See pag.212 |
| `0x06000029` | 32-bit | `LD.Q D[a],P[b],off10` | See pag.212 |
| `0x02000009` | 32-bit | `LD.Q D[a],A[b],off10` | See pag.213 |
| `0x06000009` | 32-bit | `LD.Q D[a],A[b],off10` | See pag.213 |

### LD.W

**Load Word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000085` | 32-bit | `LD.W D[a],off18` | See pag.214 |
| `0x09000009` | 32-bit | `LD.W D[a],A[b],off10` | See pag.214 |
| `0x01000029` | 32-bit | `LD.W D[a],P[b]` | See pag.214 |
| `0x05000029` | 32-bit | `LD.W D[a],P[b],off10` | See pag.214 |
| `0x01000009` | 32-bit | `LD.W D[a],A[b],off10` | See pag.215 |
| `0x05000009` | 32-bit | `LD.W D[a],A[b],off10` | See pag.215 |
| `0x00000019` | 32-bit | `LD.W D[a],A[b],off16` | See pag.215 |
| `0x58` | 16-bit | `LD.W D[15],A[10],const8` | See pag.215 |
| `0x54` | 16-bit | `LD.W D[c],A[b]` | See pag.215 |
| `0x44` | 16-bit | `LD.W D[c],A[b]` | See pag.215 |
| `0x48` | 16-bit | `LD.W D[c],A[15],off4` | See pag.216 |
| `0x4C` | 16-bit | `LD.W D[15],A[b],off4` | See pag.216 |

### LDLCX

**Load Lower Context**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x08000015` | 32-bit | `LDLCXoff18` | See pag.217 |
| `0x09000049` | 32-bit | `LDLCX A[b],off10` | See pag.217 |

### LDMST

**Load-Modify-Store**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x040000E5` | 32-bit | `LDMST off18,E[a]` | See pag.218 |
| `0x08400049` | 32-bit | `LDMST A[b],off10,E[a]` | See pag.218 |
| `0x00400069` | 32-bit | `LDMST P[b],E[a]` | See pag.218 |
| `0x04400069` | 32-bit | `LDMST P[b],off10,E[a]` | See pag.218 |
| `0x00400049` | 32-bit | `LDMST A[b],off10,E[a]` | See pag.219 |
| `0x04400049` | 32-bit | `LDMST A[b],off10,E[a]` | See pag.219 |

### LDUCX

**Load Upper Context**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0C000015` | 32-bit | `LDUCX off18` | See pag.220 |
| `0x09400049` | 32-bit | `LDUCX A[b],off10` | See pag.220 |

### LEA

**Load Effective Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000C5` | 32-bit | `LEA A[a],off18` | See pag.221 |
| `0x0A000049` | 32-bit | `LEA A[a],A[b],off10` | See pag.221 |
| `0x000000D9` | 32-bit | `LEA A[a],A[b],off16` | See pag.221 |

---

## Branch/Jump Instructions

*62 instructions*

### CALL

**Call**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000006D` | 32-bit | `CALL disp24` | See pag.110 |
| `0x5C` | 16-bit | `CALL disp8` | See pag.110 |

### CALLA

**Call Absolute**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000ED` | 32-bit | `CALLA disp24` | See pag.112 |

### CALLI

**Call Indirect**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000002D` | 32-bit | `CALLI A[a]` | See pag.113 |

### FCALL

**Fast Call**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000061` | 32-bit | `FCALL disp24` | See pag.152 |

### FCALLA

**Fast Call Absolute**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000E1` | 32-bit | `FCALLA disp24` | See pag.153 |

### FCALLI

**Fast Call Indirect**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0010002D` | 32-bit | `FCALLI A[a]` | See pag.154 |

### FRET

**Return from Fast Call**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x7000` | 16-bit | `FRET` | See pag.155 |
| `0x00C0000D` | 32-bit | `FRET` | See pag.155 |

### J

**Jump Unconditional**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000001D` | 32-bit | `J disp24` | See pag.169 |
| `0x3C` | 16-bit | `J disp8` | See pag.169 |

### JA

**Jump Unconditional Absolute**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000009D` | 32-bit | `JA disp24` | See pag.170 |

### JEQ

**Jump if Equal**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000DF` | 32-bit | `JEQ D[a],const4,disp15` | See pag.171 |
| `0x0000005F` | 32-bit | `JEQ D[a],D[b],disp15` | See pag.171 |
| `0x1E` | 16-bit | `JEQ D[15],const4,disp4` | See pag.171 |
| `0x9E` | 16-bit | `JEQ D[15],const4,disp4` | See pag.171 |
| `0x3E` | 16-bit | `JEQ D[15],D[b],disp4` | See pag.171 |
| `0xBE` | 16-bit | `JEQ D[15],D[b],disp4` | See pag.172 |

### JEQ.A

**Jump if Equal Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000007D` | 32-bit | `JEQ.A A[a],A[b],disp15` | See pag.173 |

### JGE

**Jump if Greater Than or Equal**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000FF` | 32-bit | `JGE D[a],const4,disp15` | See pag.174 |
| `0x0000007F` | 32-bit | `JGE D[a],D[b],disp15` | See pag.174 |

### JGE.U

**Jump if Greater Than or Equal Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x800000FF` | 32-bit | `JGE.U D[a],const4,disp15` | See pag.174 |
| `0x8000007F` | 32-bit | `JGE.U D[a],D[b],disp15` | See pag.174 |

### JGEZ

**Jump if Greater Than or Equal to Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0xCE` | 16-bit | `JGEZ D[b],disp4` | See pag.176 |

### JGTZ

**Jump if Greater Than Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x4E` | 16-bit | `JGTZ D[b],disp4` | See pag.177 |

### JI

**Jump Indirect**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0030002D` | 32-bit | `JI A[a]` | See pag.178 |
| `0xDC` | 16-bit | `JI A[a]` | See pag.178 |

### JL

**Jump and Link**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000005D` | 32-bit | `JL disp24` | See pag.179 |

### JLA

**Jump and Link Absolute**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000DD` | 32-bit | `JLA disp24` | See pag.180 |

### JLEZ

**Jump if Less Than or Equal to Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x8E` | 16-bit | `JLEZ D[b],disp4` | See pag.181 |

### JLI

**Jump and Link Indirect**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0020002D` | 32-bit | `JLI A[a]` | See pag.182 |

### JLT

**Jump if Less Than**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000BF` | 32-bit | `JLT D[a],const4,disp15` | See pag.183 |
| `0x0000003F` | 32-bit | `JLT D[a],D[b],disp15` | See pag.183 |

### JLT.U

**Jump if Less Than Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x800000BF` | 32-bit | `JLT.U D[a],const4,disp15` | See pag.183 |
| `0x8000003F` | 32-bit | `JLT.U D[a],D[b],disp15` | See pag.183 |

### JLTZ

**Jump if Less Than Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0E` | 16-bit | `JLTZ D[b],disp4` | See pag.185 |

### JNE

**Jump if Not Equal**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x800000DF` | 32-bit | `JNE D[a],const4,disp15` | See pag.186 |
| `0x8000005F` | 32-bit | `JNE D[a],D[b],disp15` | See pag.186 |
| `0x5E` | 16-bit | `JNE D[15],const4,disp4` | See pag.186 |
| `0xDE` | 16-bit | `JNE D[15],const4,disp4` | See pag.186 |
| `0x7E` | 16-bit | `JNE D[15],D[b],disp4` | See pag.186 |
| `0xFE` | 16-bit | `JNE D[15],D[b],disp4` | See pag.187 |

### JNE.A

**Jump if Not Equal Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x8000007D` | 32-bit | `JNE.A A[a],A[b],disp15` | See pag.188 |

### JNED

**Jump if Not Equal and Decrement**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x8000009F` | 32-bit | `JNED D[a],const4,disp15` | See pag.189 |
| `0x8000001F` | 32-bit | `JNED D[a],D[b],disp15` | See pag.189 |

### JNEI

**Jump if Not Equal and Increment**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000009F` | 32-bit | `JNEI D[a],const4,disp15` | See pag.190 |
| `0x0000001F` | 32-bit | `JNEI D[a],D[b],disp15` | See pag.190 |

### JNZ

**Jump if Not Equal to Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0xEE` | 16-bit | `JNZ D[15],disp8` | See pag.191 |
| `0xF6` | 16-bit | `JNZ D[b],disp4` | See pag.191 |

### JNZ.A

**Jump if Not Equal to Zero Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x800000BD` | 32-bit | `JNZ.A A[a],disp15` | See pag.192 |
| `0x7C` | 16-bit | `JNZ.A A[b],disp4` | See pag.192 |

### JNZ.T

**Jump if Not Equal to Zero Bit**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x8000006F` | 32-bit | `JNZ.T D[a],n,disp15` | See pag.193 |
| `0xAE` | 16-bit | `JNZ.T D[15],n,disp4` | See pag.193 |

### JZ

**Jump if Zero (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x6E` | 16-bit | `JZ D[15],disp8` | See pag.194 |
| `0x76` | 16-bit | `JZ D[b],disp4` | See pag.194 |

### JZ.A

**Jump if Zero Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000BD` | 32-bit | `JZ.A A[a],disp15` | See pag.195 |
| `0xBC` | 16-bit | `JZ.A A[b],disp4` | See pag.195 |

### JZ.T

**Jump if Zero Bit**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000006F` | 32-bit | `JZ.T D[a],n,disp15` | See pag.196 |
| `0x2E` | 16-bit | `JZ.T D[15],n,disp4` | See pag.196 |

### LOOP

**Loop**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000FD` | 32-bit | `LOOP A[b],disp15` | See pag.222 |
| `0xFC` | 16-bit | `LOOP A[b],disp4` | See pag.222 |

### LOOPU

**Loop Unconditional**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x800000FD` | 32-bit | `LOOPU disp15` | See pag.223 |

---

## System Instructions

*5 instructions*

### DEBUG

**Debug**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00` | 16-bit | `DEBUG` | See pag.128 |
| `0x0100000D` | 32-bit | `DEBUG` | See pag.128 |

### DSYNC

**Synchronize Data**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0480000D` | 32-bit | `DSYNC` | See pag.131 |

### ISYNC

**Synchronize Instructions**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04C0000D` | 32-bit | `ISYNC` | See pag.164 |

### MFCR

**Move From Core Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000004D` | 32-bit | `MFCR D[c],const16` | See pag.269 |

---

## Packed Operations Instructions

*154 instructions*

### CADD

**Conditional Add**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000AB` | 32-bit | `CADD D[c],D[d],D[a],const9` | See pag.106 |
| `0x0000002B` | 32-bit | `CADD D[c],D[d],D[a],D[b]` | See pag.106 |
| `0x8A` | 16-bit | `CADD D[a],D[15],const4` | See pag.106 |

### CADDN

**Conditional Add-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x001000AB` | 32-bit | `CADDN D[c],D[d],D[a],const9` | See pag.108 |
| `0x0010002B` | 32-bit | `CADDN D[c],D[d],D[a],D[b]` | See pag.108 |
| `0xCA` | 16-bit | `CADDN D[a],D[15],const4` | See pag.108 |

### CSUB

**Conditional Subtract**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0020002B` | 32-bit | `CSUB D[c],D[d],D[a],D[b]` | See pag.126 |

### CSUBN

**Conditional Subtract-Not**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0030002B` | 32-bit | `CSUBN D[c],D[d],D[a],D[b]` | See pag.127 |

### MADD

**Multiply-Add**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00200013` | 32-bit | `MADD D[c],D[d],D[a],const9` | See pag.230 |
| `0x00600013` | 32-bit | `MADD E[c],E[d],D[a],const9` | See pag.230 |
| `0x000A0003` | 32-bit | `MADD D[c],D[d],D[a],D[b]` | See pag.230 |
| `0x006A0003` | 32-bit | `MADD E[c],E[d],D[a],D[b]` | See pag.230 |

### MADD.H

**Packed Multiply-Add Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00680083` | 32-bit | `MADD.H E[c],E[d],D[a],D[b] LL,n` | See pag.233 |
| `0x00640083` | 32-bit | `MADD.H E[c],E[d],D[a],D[b] LU,n` | See pag.233 |
| `0x00600083` | 32-bit | `MADD.H E[c],E[d],D[a],D[b] UL,n` | See pag.233 |
| `0x006C0083` | 32-bit | `MADD.H E[c],E[d],D[a],D[b] UU,n` | See pag.234 |

### MADD.Q

**Multiply-Add Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00080043` | 32-bit | `MADD.Q D[c],D[d],D[a],D[b],n` | See pag.237 |
| `0x006C0043` | 32-bit | `MADD.Q E[c],E[d],D[a],D[b],n` | See pag.237 |
| `0x00040043` | 32-bit | `MADD.Q D[c],D[d],D[a],D[b] L,n` | See pag.237 |
| `0x00640043` | 32-bit | `MADD.Q E[c],E[d],D[a],D[b] L,n` | See pag.237 |
| `0x00000043` | 32-bit | `MADD.Q D[c],D[d],D[a],D[b] U,n` | See pag.238 |
| `0x00600043` | 32-bit | `MADD.Q E[c],E[d],D[a],D[b] U,n` | See pag.238 |
| `0x00140043` | 32-bit | `MADD.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.238 |
| `0x00740043` | 32-bit | `MADD.Q E[c],E[d],D[a] L,D[b] L,n` | See pag.238 |
| `0x00100043` | 32-bit | `MADD.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.238 |
| `0x00700043` | 32-bit | `MADD.Q E[c],E[d],D[a] U,D[b] U,n` | See pag.239 |

### MADD.U

**Multiply-Add Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00200013` | 32-bit | `MADD.U E[c],E[d],D[a],const9` | See pag.243 |
| `0x00680003` | 32-bit | `MADD.U E[c],E[d],D[a],D[b]` | See pag.243 |

### MADDM.H

**Packed Multiply-Add Q Format Multi-precision**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00780083` | 32-bit | `MADDM.H E[c],E[d],D[a],D[b] LL,n` | See pag.245 |
| `0x00740083` | 32-bit | `MADDM.H E[c],E[d],D[a],D[b] LU,n` | See pag.245 |
| `0x00700083` | 32-bit | `MADDM.H E[c],E[d],D[a],D[b] UL,n` | See pag.245 |
| `0x007C0083` | 32-bit | `MADDM.H E[c],E[d],D[a],D[b] UU,n` | See pag.246 |

### MADDMS.H

**Packed Multiply-Add Q Format Multi-precision,**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00F80083` | 32-bit | `MADDMS.H E[c],E[d],D[a],D[b] LL,n` | See pag.246 |
| `0x00F40083` | 32-bit | `MADDMS.H E[c],E[d],D[a],D[b] LU,n` | See pag.246 |
| `0x00F00083` | 32-bit | `MADDMS.H E[c],E[d],D[a],D[b] UL,n` | See pag.247 |
| `0x00FC0083` | 32-bit | `MADDMS.H E[c],E[d],D[a],D[b] UU,n` | See pag.247 |

### MADDR.H

**Packed Multiply-Add Q Format with Rounding**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00380083` | 32-bit | `MADDR.H D[c],D[d],D[a],D[b] LL,n` | See pag.248 |
| `0x00340083` | 32-bit | `MADDR.H D[c],D[d],D[a],D[b] LU,n` | See pag.248 |
| `0x00300083` | 32-bit | `MADDR.H D[c],D[d],D[a],D[b] UL,n` | See pag.249 |
| `0x00780043` | 32-bit | `MADDR.H D[c],E[d],D[a],D[b] UL,n` | See pag.249 |
| `0x003C0083` | 32-bit | `MADDR.H D[c],D[d],D[a],D[b] UU,n` | See pag.249 |

### MADDR.Q

**Multiply-Add Q Format with Rounding**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x001C0043` | 32-bit | `MADDR.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.252 |
| `0x00180043` | 32-bit | `MADDR.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.252 |

### MADDRS.H

**Packed Multiply-Add Q Format with Rounding,Sa**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00B80083` | 32-bit | `MADDRS.H D[c],D[d],D[a],D[b] LL,n` | See pag.249 |
| `0x00B40083` | 32-bit | `MADDRS.H D[c],D[d],D[a],D[b] LU,n` | See pag.250 |
| `0x00B00083` | 32-bit | `MADDRS.H D[c],D[d],D[a],D[b] UL,n` | See pag.250 |
| `0x00F80043` | 32-bit | `MADDRS.H D[c],E[d],D[a],D[b] UL,n` | See pag.250 |
| `0x00BC0083` | 32-bit | `MADDRS.H D[c],D[d],D[a],D[b] UU,n` | See pag.251 |

### MADDRS.Q

**Multiply-Add Q Format with Rounding,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x009C0043` | 32-bit | `MADDRS.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.252 |
| `0x00980043` | 32-bit | `MADDRS.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.253 |

### MADDS

**Multiply-Add,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00A00013` | 32-bit | `MADDS D[c],D[d],D[a],const9` | See pag.231 |
| `0x00E00013` | 32-bit | `MADDS E[c],E[d],D[a],const9` | See pag.231 |
| `0x008A0003` | 32-bit | `MADDS D[c],D[d],D[a],D[b]` | See pag.231 |
| `0x00EA0003` | 32-bit | `MADDS E[c],E[d],D[a],D[b]` | See pag.231 |

### MADDS.H

**Packed Multiply-Add Q Format,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E80083` | 32-bit | `MADDS.H E[c],E[d],D[a],D[b] LL,n` | See pag.234 |
| `0x00E40083` | 32-bit | `MADDS.H E[c],E[d],D[a],D[b] LU,n` | See pag.234 |
| `0x00E00083` | 32-bit | `MADDS.H E[c],E[d],D[a],D[b] UL,n` | See pag.235 |
| `0x00EC0083` | 32-bit | `MADDS.H E[c],E[d],D[a],D[b] UU,n` | See pag.235 |

### MADDS.Q

**Multiply-Add Q Format,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00880043` | 32-bit | `MADDS.Q D[c],D[d],D[a],D[b],n` | See pag.239 |
| `0x00EC0043` | 32-bit | `MADDS.Q E[c],E[d],D[a],D[b],n` | See pag.239 |
| `0x00840043` | 32-bit | `MADDS.Q D[c],D[d],D[a],D[b] L,n` | See pag.239 |
| `0x00E40043` | 32-bit | `MADDS.Q E[c],E[d],D[a],D[b] L,n` | See pag.239 |
| `0x00800043` | 32-bit | `MADDS.Q D[c],D[d],D[a],D[b] U,n` | See pag.240 |
| `0x00E00043` | 32-bit | `MADDS.Q E[c],E[d],D[a],D[b] U,n` | See pag.240 |
| `0x00940043` | 32-bit | `MADDS.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.240 |
| `0x00F40043` | 32-bit | `MADDS.Q E[c],E[d],D[a] L,D[b] L,n` | See pag.240 |
| `0x00900043` | 32-bit | `MADDS.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.240 |
| `0x00F00043` | 32-bit | `MADDS.Q E[c],E[d],D[a] U,D[b] U,n` | See pag.241 |

### MADDS.U

**Multiply-Add Unsigned,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00800013` | 32-bit | `MADDS.U D[c],D[d],D[a],const9` | See pag.243 |
| `0x00C00013` | 32-bit | `MADDS.U E[c],E[d],D[a],const9` | See pag.243 |
| `0x00880003` | 32-bit | `MADDS.U D[c],D[d],D[a],D[b]` | See pag.244 |
| `0x00E80003` | 32-bit | `MADDS.U D[c],D[d],D[a],const9` | See pag.244 |

### MADDSU.H

**Packed Multiply-Add/Subtract Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x006800C3` | 32-bit | `MADDSU.H E[c],E[d],D[a],D[b] LL,n` | See pag.254 |
| `0x006400C3` | 32-bit | `MADDSU.H E[c],E[d],D[a],D[b] LU,n` | See pag.254 |
| `0x006000C3` | 32-bit | `MADDSU.H E[c],E[d],D[a],D[b] UL,n` | See pag.255 |
| `0x006C00C3` | 32-bit | `MADDSU.H E[c],E[d],D[a],D[b] UU,n` | See pag.255 |

### MADDSUM.H

**Packed Multiply-Add/Subtract Q Format Multi-pr**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x007800C3` | 32-bit | `MADDSUM.H E[c],E[d],D[a],D[b] LL,n` | See pag.258 |
| `0x007400C3` | 32-bit | `MADDSUM.H E[c],E[d],D[a],D[b] LU,n` | See pag.258 |
| `0x007000C3` | 32-bit | `MADDSUM.H E[c],E[d],D[a],D[b] UL,n` | See pag.259 |
| `0x007C00C3` | 32-bit | `MADDSUM.H E[c],E[d],D[a],D[b] UU,n` | See pag.259 |

### MADDSUMS.H

**Packed Multiply-Add/Subtract Q Format Multi-pr**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00F800C3` | 32-bit | `MADDSUMS.H E[c],E[d],D[a],D[b] LL,n` | See pag.259 |
| `0x00F400C3` | 32-bit | `MADDSUMS.H E[c],E[d],D[a],D[b] LU,n` | See pag.259 |
| `0x00F000C3` | 32-bit | `MADDSUMS.H E[c],E[d],D[a],D[b] UL,n` | See pag.260 |
| `0x00FC00C3` | 32-bit | `MADDSUMS.H E[c],E[d],D[a],D[b] UU,n` | See pag.260 |

### MADDSUR.H

**Packed Multiply-Add/Subtract Q Format with Rou**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x003800C3` | 32-bit | `MADDSUR.H D[c],D[d],D[a],D[b] LL,n` | See pag.261 |
| `0x003400C3` | 32-bit | `MADDSUR.H D[c],D[d],D[a],D[b] LU,n` | See pag.261 |
| `0x003000C3` | 32-bit | `MADDSUR.H D[c],D[d],D[a],D[b] UL,n` | See pag.262 |
| `0x003C00C3` | 32-bit | `MADDSUR.H D[c],D[d],D[a],D[b] UU,n` | See pag.262 |

### MADDSURS.H

**Packed Multiply-Add/Subtract Q Format with Rou**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00B800C3` | 32-bit | `MADDSURS.H D[c],D[d],D[a],D[b] LL,n` | See pag.262 |
| `0x00B400C3` | 32-bit | `MADDSURS.H D[c],D[d],D[a],D[b] LU,n` | See pag.262 |
| `0x00B000C3` | 32-bit | `MADDSURS.H D[c],D[d],D[a],D[b] UL,n` | See pag.263 |
| `0x00BC00C3` | 32-bit | `MADDSURS.H D[c],D[d],D[a],D[b] UU,n` | See pag.263 |

### MADDSUS.H

**Packed Multiply-Add/Subtract Q Format Saturate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E800C3` | 32-bit | `MADDSUS.H E[c],E[d],D[a],D[b] LL,n` | See pag.255 |
| `0x00E400C3` | 32-bit | `MADDSUS.H E[c],E[d],D[a],D[b] LU,n` | See pag.255 |
| `0x00E000C3` | 32-bit | `MADDSUS.H E[c],E[d],D[a],D[b] UL,n` | See pag.256 |
| `0x00EC00C3` | 32-bit | `MADDSUS.H E[c],E[d],D[a],D[b] UU,n` | See pag.256 |

### MSUB

**Multiply-Subtract**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00200033` | 32-bit | `MSUB D[c],D[d],D[a],const9` | See pag.283 |
| `0x00600033` | 32-bit | `MSUB E[c],E[d],D[a],const9` | See pag.283 |
| `0x000A0023` | 32-bit | `MSUB D[c],D[d],D[a],D[b]` | See pag.283 |
| `0x006A0023` | 32-bit | `MSUB E[c],E[d],D[a],D[b]` | See pag.283 |

### MSUB.H

**Packed Multiply-Subtract Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x006800A3` | 32-bit | `MSUB.H E[c],E[d],D[a],D[b] LL,n` | See pag.286 |
| `0x006400A3` | 32-bit | `MSUB.H E[c],E[d],D[a],D[b] LU,n` | See pag.286 |
| `0x006000A3` | 32-bit | `MSUB.H E[c],E[d],D[a],D[b] UL,n` | See pag.286 |
| `0x006C00A3` | 32-bit | `MSUB.H E[c],E[d],D[a],D[b] UU,n` | See pag.287 |

### MSUB.Q

**Multiply-Subtract Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00040063` | 32-bit | `MSUB.Q D[c],D[d],D[a],D[b],n` | See pag.290 |
| `0x006C0063` | 32-bit | `MSUB.Q E[c],E[d],D[a],D[b],n` | See pag.290 |
| `0x00040063` | 32-bit | `MSUB.Q D[c],D[d],D[a],D[b] L,n` | See pag.290 |
| `0x00640063` | 32-bit | `MSUB.Q E[c],E[d],D[a],D[b] L,n` | See pag.290 |
| `0x00000063` | 32-bit | `MSUB.Q D[c],D[d],D[a],D[b] U,n` | See pag.291 |
| `0x00600063` | 32-bit | `MSUB.Q E[c],E[d],D[a],D[b] U,n` | See pag.291 |
| `0x00140063` | 32-bit | `MSUB.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.291 |
| `0x00740063` | 32-bit | `MSUB.Q E[c],E[d],D[a] L,D[b] L,n` | See pag.291 |
| `0x00100063` | 32-bit | `MSUB.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.291 |
| `0x00700063` | 32-bit | `MSUB.Q E[c],E[d],D[a] U,D[b] U,n` | See pag.292 |

### MSUB.U

**Multiply-Subtract Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00400033` | 32-bit | `MSUB.U E[c],E[d],D[a],const9` | See pag.296 |
| `0x00680023` | 32-bit | `MSUB.U E[c],E[d],D[a],D[b]` | See pag.296 |

### MSUBAD.H

**Packed Multiply-Subtract/Add Q Format**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x006800E3` | 32-bit | `MSUBAD.H E[c],E[d],D[a],D[b] LL,n` | See pag.298 |
| `0x006400E3` | 32-bit | `MSUBAD.H E[c],E[d],D[a],D[b] LU,n` | See pag.298 |
| `0x006000E3` | 32-bit | `MSUBAD.H E[c],E[d],D[a],D[b] UL,n` | See pag.299 |
| `0x006C00E3` | 32-bit | `MSUBAD.H E[c],E[d],D[a],D[b] UU,n` | See pag.299 |

### MSUBADM.H

**Packed Multiply-Subtract/Add Q Format-Multi-pr**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x007800E3` | 32-bit | `MSUBADM.H E[c],E[d],D[a],D[b] LL,n` | See pag.302 |
| `0x007400E3` | 32-bit | `MSUBADM.H E[c],E[d],D[a],D[b] LU,n` | See pag.302 |
| `0x007000E3` | 32-bit | `MSUBADM.H E[c],E[d],D[a],D[b] UL,n` | See pag.303 |
| `0x007C00E3` | 32-bit | `MSUBADM.H E[c],E[d],D[a],D[b] UU,n` | See pag.303 |

### MSUBADMS.H

**Packed Multiply-Subtract/Add Q Format-Multi-pr**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00F800E3` | 32-bit | `MSUBADMS.H E[c],E[d],D[a],D[b] LL,n` | See pag.303 |
| `0x00F400E3` | 32-bit | `MSUBADMS.H E[c],E[d],D[a],D[b] LU,n` | See pag.303 |
| `0x00F000E3` | 32-bit | `MSUBADMS.H E[c],E[d],D[a],D[b] UL,n` | See pag.304 |
| `0x00FC00E3` | 32-bit | `MSUBADMS.H E[c],E[d],D[a],D[b] UU,n` | See pag.304 |

### MSUBADS.H

**Packed Multiply-Subtract/Add Q Format,Saturat**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E800E3` | 32-bit | `MSUBADS.H E[c],E[d],D[a],D[b] LL,n` | See pag.299 |
| `0x00E400E3` | 32-bit | `MSUBADS.H E[c],E[d],D[a],D[b] LU,n` | See pag.299 |
| `0x00E000E3` | 32-bit | `MSUBADS.H E[c],E[d],D[a],D[b] UL,n` | See pag.300 |
| `0x00EC00E3` | 32-bit | `MSUBADS.H E[c],E[d],D[a],D[b] UU,n` | See pag.300 |

### MSUBS

**Multiply-Subtract,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00A00033` | 32-bit | `MSUBS D[c],D[d],D[a],const9` | See pag.284 |
| `0x00E00033` | 32-bit | `MSUBS E[c],E[d],D[a],const9` | See pag.284 |
| `0x008A0023` | 32-bit | `MSUBS D[c],D[d],D[a],D[b]` | See pag.284 |
| `0x00EA0023` | 32-bit | `MSUBS E[c],E[d],D[a],D[b]` | See pag.284 |

### MSUBS.H

**Packed Multiply-Subtract Q Format,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E800A3` | 32-bit | `MSUBS.H E[c],E[d],D[a],D[b] LL,n` | See pag.287 |
| `0x00E400A3` | 32-bit | `MSUBS.H E[c],E[d],D[a],D[b] LU,n` | See pag.287 |
| `0x00E000A3` | 32-bit | `MSUBS.H E[c],E[d],D[a],D[b] UL,n` | See pag.288 |
| `0x00EC00A3` | 32-bit | `MSUBS.H E[c],E[d],D[a],D[b] UU,n` | See pag.288 |

### MSUBS.Q

**Multiply-Subtract Q Format,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00880063` | 32-bit | `MSUBS.Q D[c],D[d],D[a],D[b],n` | See pag.292 |
| `0x00EC0063` | 32-bit | `MSUBS.Q E[c],E[d],D[a],D[b],n` | See pag.292 |
| `0x00840063` | 32-bit | `MSUBS.Q D[c],D[d],D[a],D[b] L,n` | See pag.292 |
| `0x00E40063` | 32-bit | `MSUBS.Q E[c],E[d],D[a],D[b] L,n` | See pag.292 |
| `0x00800063` | 32-bit | `MSUBS.Q D[c],D[d],D[a],D[b] U,n` | See pag.293 |
| `0x00E00063` | 32-bit | `MSUBS.Q E[c],E[d],D[a],D[b] U,n` | See pag.293 |
| `0x00940063` | 32-bit | `MSUBS.Q D[c],D[d],D[a] L,D[b] L,n` | See pag.293 |
| `0x00F40063` | 32-bit | `MSUBS.Q E[c],E[d],D[a] L,D[b] L,n` | See pag.293 |
| `0x00900063` | 32-bit | `MSUBS.Q D[c],D[d],D[a] U,D[b] U,n` | See pag.293 |
| `0x00F00063` | 32-bit | `MSUBS.Q E[c],E[d],D[a] U,D[b] U,n` | See pag.294 |

### MSUBS.U

**Multiply-Subtract Unsigned,Saturated**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00800033` | 32-bit | `MSUBS.U D[c],D[d],D[a],const9` | See pag.296 |
| `0x00C00033` | 32-bit | `MSUBS.U E[c],E[d],D[a],const9` | See pag.296 |
| `0x00880023` | 32-bit | `MSUBS.U D[c],D[d],D[a],D[b]` | See pag.297 |
| `0x00E80023` | 32-bit | `MSUBS.U E[c],E[d],D[a],D[b]` | See pag.297 |

---

## Other Instructions

*102 instructions*

### BISR

**Begin Interrupt Service Routine**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0xAD` | 32-bit | `BISR const9` | See pag.90 |
| `0xE0` | 16-bit | `BISR const8` | See pag.90 |

### CACHEA.I

**Cache Address,Invalidate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0B800089` | 32-bit | `CACHEA.I A[b],off10` | See pag.94 |
| `0x038000A9` | 32-bit | `CACHEA.I P[b]` | See pag.94 |
| `0x078000A9` | 32-bit | `CACHEA.I P[b],off10` | See pag.94 |
| `0x03800089` | 32-bit | `CACHEA.I A[b],off10` | See pag.95 |
| `0x07800089` | 32-bit | `CACHEA.I A[b],off10` | See pag.95 |

### CACHEA.W

**Cache Address,Writeback**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0B000089` | 32-bit | `CACHEA.W A[b],off10` | See pag.96 |
| `0x030000A9` | 32-bit | `CACHEA.W P[b]` | See pag.96 |
| `0x070000A9` | 32-bit | `CACHEA.W P[b],off10` | See pag.96 |
| `0x89` | 32-bit | `CACHEA.W A[b],off10` | See pag.97 |
| `0x03000089` | 32-bit | `CACHEA.W A[b],off10` | See pag.97 |

### CACHEA.WI

**Cache Address,Writeback and Invalidate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0B400089` | 32-bit | `CACHEA.WI A[b],off10` | See pag.98 |
| `0x034000A9` | 32-bit | `CACHEA.WI P[b]` | See pag.98 |
| `0x074000A9` | 32-bit | `CACHEA.WI P[b],off10` | See pag.98 |
| `0x03400089` | 32-bit | `CACHEA.WI A[b],off10` | See pag.99 |
| `0x07400089` | 32-bit | `CACHEA.WI A[b],off10` | See pag.99 |

### CACHEI.I

**Cache Index,Invalidate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0A800089` | 32-bit | `CACHEI.I A[b],off10` | See pag.102 |
| `0x02800089` | 32-bit | `CACHEI.I A[b],off10` | See pag.102 |
| `0x06800089` | 32-bit | `CACHEI.I A[b],off10` | See pag.102 |

### CACHEI.W

**Cache Index,Writeback**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0AC00089` | 32-bit | `CACHEI.W A[b],off10` | See pag.100 |
| `0x02C00089` | 32-bit | `CACHEI.W A[b],off10` | See pag.100 |
| `0x06C00089` | 32-bit | `CACHEI.W A[b],off10` | See pag.100 |

### CACHEI.WI

**Cache Index,Writeback,Invalidate**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0BC00089` | 32-bit | `CACHEI.WI A[b],off10` | See pag.104 |
| `0x03C00089` | 32-bit | `CACHEI.WI A[b],off10` | See pag.104 |
| `0x07C00089` | 32-bit | `CACHEI.WI A[b],off10` | See pag.104 |

### CMOV

**Conditional Move (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0xAA` | 16-bit | `CMOV D[a],D[15],const4` | See pag.121 |
| `0x2A` | 16-bit | `CMOV D[a],D[15],D[b]` | See pag.121 |

### CMOVN

**Conditional Move-Not (16-bit)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0xEA` | 16-bit | `CMOVN D[a],D[15],const4` | See pag.122 |
| `0x6A` | 16-bit | `CMOVN D[a],D[15],D[b]` | See pag.122 |

### CMPSWAP.W

**Compare and Swap**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x08C00049` | 32-bit | `CMPSWAP.W A[b],off10,E[a]` | See pag.123 |
| `0x00C00069` | 32-bit | `CMPSWAP.W P[b],E[a]` | See pag.123 |
| `0x04C00069` | 32-bit | `CMPSWAP.W P[b],off10,E[a]` | See pag.123 |
| `0x00C00049` | 32-bit | `CMPSWAP.W A[b],off10,E[a]` | See pag.124 |
| `0x04C00049` | 32-bit | `CMPSWAP.W A[b],off10,E[a]` | See pag.124 |

### CRC32

**CRC32**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0030004B` | 32-bit | `CRC32 D[c],D[b],D[a]` | See pag.125 |

### DISABLE

**Disable Interrupts**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0340000D` | 32-bit | `DISABLE` | See pag.130 |
| `0x03C0000D` | 32-bit | `DISABLE D[a]` | See pag.130 |

### DVADJ

**Divide-Adjust**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00D0006B` | 32-bit | `DVADJ E[c],E[d],D[b]` | See pag.132 |

### DVINIT

**Divide-Initialization Word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x05A0004B` | 32-bit | `DVINIT.B E[c],D[a],D[b]` | See pag.136 |

### DVINIT.B

**Divide-Initialization Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x03A0004B` | 32-bit | `DVINIT.H E[c],D[a],D[b]` | See pag.137 |

### DVINIT.BU

**Divide-Initialization Byte Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x02A0004B` | 32-bit | `DVINIT.HU E[c],D[a],D[b]` | See pag.137 |

### DVINIT.H

**Divide-Initialization Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x01A0004B` | 32-bit | `DVINIT E[c],D[a],D[b]` | See pag.137 |

### DVINIT.HU

**Divide-Initialization Half-word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00A0004B` | 32-bit | `DVINIT.U E[c],D[a],D[b]` | See pag.137 |

### DVINIT.U

**Divide-Initialization Word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04A0004B` | 32-bit | `DVINIT.BU E[c],D[a],D[b]` | See pag.137 |

### DVSTEP

**Divide-Step**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00F0006B` | 32-bit | `DVSTEP E[c],E[d],D[b]` | See pag.139 |

### DVSTEP.U

**Divide-Step Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00E0006B` | 32-bit | `DVSTEP.U E[c],E[d],D[b]` | See pag.140 |

### ENABLE

**Enable Interrupts**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0300000D` | 32-bit | `ENABLE` | See pag.141 |

### EQ

**Equal**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0100008B` | 32-bit | `EQ D[c],D[a],const9` | See pag.142 |
| `0x0100000B` | 32-bit | `EQ D[c],D[a],D[b]` | See pag.142 |
| `0xBA` | 16-bit | `EQ D[15],D[a],const4` | See pag.142 |
| `0x3A` | 16-bit | `EQ D[15],D[a],D[b]` | See pag.142 |

### EQ.A

**Equal to Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04000001` | 32-bit | `EQ.A D[c],A[a],A[b]` | See pag.144 |

### EQ.B

**Equal Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0500000B` | 32-bit | `EQ.B D[c],D[a],D[b]` | See pag.145 |

### EQ.H

**Equal Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0700000B` | 32-bit | `EQ.H D[c],D[a],D[b]` | See pag.145 |

### EQ.W

**Equal Packed Word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0900000B` | 32-bit | `EQ.W D[c],D[a],D[b]` | See pag.145 |

### EQANY.B

**Equal Any Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0560008B` | 32-bit | `EQANY.B D[c],D[a],const9` | See pag.147 |
| `0x0560000B` | 32-bit | `EQANY.B D[c],D[a],D[b]` | See pag.147 |

### EQANY.H

**Equal Any Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0760008B` | 32-bit | `EQANY.H D[c],D[a],const9` | See pag.147 |
| `0x0760000B` | 32-bit | `EQANY.H D[c],D[a],D[b]` | See pag.148 |

### EQZ.A

**Equal Zero Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04800001` | 32-bit | `EQZ.A D[c],A[a]` | See pag.149 |

### GE

**Greater Than or Equal**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0140008B` | 32-bit | `GE D[c],D[a],const9` | See pag.156 |
| `0x0140000B` | 32-bit | `GE D[c],D[a],D[b]` | See pag.156 |

### GE.A

**Greater Than or Equal Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04300001` | 32-bit | `GE.A D[c],A[a],A[b]` | See pag.158 |

### GE.U

**Greater Than or Equal Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0150008B` | 32-bit | `GE.U D[c],D[a],const9` | See pag.156 |
| `0x0150000B` | 32-bit | `GE.U D[c],D[a],D[b]` | See pag.156 |

### IXMAX

**Find Maximum Index**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00A0006B` | 32-bit | `IXMAX E[c],E[d],D[b]` | See pag.165 |

### IXMAX.U

**Find Maximum Index (unsigned)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00B0006B` | 32-bit | `IXMAX.U E[c],E[d],D[b]` | See pag.165 |

### IXMIN

**Find Minimum Index**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0080006B` | 32-bit | `IXMIN E[c],E[d],D[b]` | See pag.167 |

### IXMIN.U

**Find Minimum Index (unsigned)**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0090006B` | 32-bit | `IXMIN.U E[c],E[d],D[b]` | See pag.167 |

### LT

**Less Than**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0120008B` | 32-bit | `LT D[c],D[a],const9` | See pag.224 |
| `0x0120000B` | 32-bit | `LT D[c],D[a],D[b]` | See pag.224 |
| `0xFA` | 16-bit | `LT D[15],D[a],const4` | See pag.224 |
| `0x7A` | 16-bit | `LT D[15],D[a],D[b]` | See pag.224 |

### LT.A

**Less Than Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04200001` | 32-bit | `LT.A D[c],A[a],A[b]` | See pag.226 |

### LT.B

**Less Than Packed Byte**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0520000B` | 32-bit | `LT.B D[c],D[a],D[b]` | See pag.227 |

### LT.BU

**Less Than Packed Byte Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0530000B` | 32-bit | `LT.BU D[c],D[a],D[b]` | See pag.227 |

### LT.H

**Less Than Packed Half-word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0720000B` | 32-bit | `LT.H D[c],D[a],D[b]` | See pag.228 |

### LT.HU

**Less Than Packed Half-word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0730000B` | 32-bit | `LT.HU D[c],D[a],D[b]` | See pag.228 |

### LT.U

**Less Than Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0130008B` | 32-bit | `LT.U D[c],D[a],const9` | See pag.225 |
| `0x0130000B` | 32-bit | `LT.U D[c],D[a],D[b]` | See pag.225 |

### LT.W

**Less Than Packed Word**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0920000B` | 32-bit | `LT.W D[c],D[a],D[b]` | See pag.229 |

### LT.WU

**Less Than Packed Word Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0930000B` | 32-bit | `LT.WU D[c],D[a],D[b]` | See pag.229 |

### MOV

**Move**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000003B` | 32-bit | `MOV D[c],const16` | See pag.274 |
| `0x000000FB` | 32-bit | `MOV E[c],const16` | See pag.274 |
| `0x01F0000B` | 32-bit | `MOV D[c],D[b]` | See pag.274 |
| `0x0800000B` | 32-bit | `MOV E[c],D[b]` | See pag.274 |
| `0x0810000B` | 32-bit | `MOV E[c],D[a],D[b]` | See pag.274 |
| `0xDA` | 16-bit | `MOV D[15],const8` | See pag.275 |
| `0x82` | 16-bit | `MOV D[a],const4` | See pag.275 |
| `0xD2` | 16-bit | `MOV E[a],const4` | See pag.275 |
| `0x02` | 16-bit | `MOV D[a],D[b]` | See pag.275 |

### MOV.A

**Move Value to Address Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x06300001` | 32-bit | `MOV.A A[c],D[b]` | See pag.277 |
| `0xA0` | 16-bit | `MOV.A A[a],const4` | See pag.277 |
| `0x60` | 16-bit | `MOV.A A[a],D[b]` | See pag.277 |

### MOV.AA

**Move Address from Address Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000001` | 32-bit | `MOV.AA A[c],A[b]` | See pag.278 |
| `0x40` | 16-bit | `MOV.AA A[a],A[b]` | See pag.278 |

### MOV.D

**Move Address to Data Register**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x04C00001` | 32-bit | `MOV.D D[c],A[b]` | See pag.279 |
| `0x80` | 16-bit | `MOV.D D[a],A[b]` | See pag.279 |

### MOV.U

**Move Unsigned**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x000000BB` | 32-bit | `MOV.U D[c],const16` | See pag.280 |

### MOVH

**Move High**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x0000007B` | 32-bit | `MOVH D[c],const16` | See pag.281 |

### MOVH.A

**Move High to Address**

| OpCode | Size | Syntax | Description |
|--------|------|--------|-------------|
| `0x00000091` | 32-bit | `MOVH.A A[c],const16` | See pag.282 |

---

## Appendices

### A. OpCode Size Distribution

The TriCore architecture uses variable-length instruction encoding:

- **16-bit instructions** are used for the most common operations to achieve code density
- **32-bit instructions** provide extended addressing modes and immediate values

### B. Addressing Modes

TriCore supports various addressing modes encoded in the instruction syntax:

- **Register Direct**: `D[a]`, `A[a]` - Direct register access
- **Register Indirect**: `[A[a]]` - Memory access via address register
- **Pre/Post Increment**: `[A[a]+]`, `[+A[a]]` - Auto-increment addressing
- **Offset Addressing**: `[A[a] + off]` - Base plus offset
- **Bit Field**: `D[a][pos:width]` - Bit field operations
- **Immediate**: `const4`, `const9`, `const16` - Immediate values

### C. Register Types

- **D[0]-D[15]**: 32-bit data registers
- **A[0]-A[15]**: 32-bit address registers  
- **E[0], E[2], ..., E[14]**: 64-bit extended data registers
- **Special registers**: PSW, PC, etc.

### D. Reference Documentation

This instruction set documentation is based on the TriCore TC1.6 architecture specification. For complete details including:

- Detailed instruction behavior
- Exception handling
- Pipeline interactions  
- Performance characteristics

Refer to the official Infineon TriCore Architecture Manual.

---

*This documentation was automatically generated from the TASM TriCore instruction set database.*
