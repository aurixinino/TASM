## Instruction Type Analysis\n\n### Overall Statistics\n\n- **Total Instructions**: 316\n- **Operand Count Distribution**:\n  - 0 operands: 17 instructions (5.4%)\n  - 1 operands: 22 instructions (7.0%)\n  - 2 operands: 62 instructions (19.6%)\n  - 3 operands: 150 instructions (47.5%)\n  - 4 operands: 32 instructions (10.1%)\n  - 5 operands: 33 instructions (10.4%)\n- **Instruction Size Distribution**:\n  - 16-bit: 10 instructions (3.2%)\n  - 32-bit: 306 instructions (96.8%)\n\n### Instruction Categories\n\n| Category | Count | Percentage | Key Instructions |\n|----------|-------|------------|------------------|\n| Arithmetic | 115 | 36.4% | ABS, ABS.B, ABS.H, ABSDIF, ABSDIF.B (+110 more) |\n| Miscellaneous | 51 | 16.1% | BISR, BMERGE, CLO, CLS, CLZ (+46 more) |\n| Branch/Jump | 39 | 12.3% | CALL, CALLA, CALLI, DVADJ, FCALL (+34 more) |\n| Load/Store | 33 | 10.4% | CMOV, CMOVN, DVSTEP, DVSTEP.U, LD.A (+28 more) |\n| Logical | 32 | 10.1% | AND, AND.AND.T, AND.ANDN.T, AND.EQ, AND.GE (+27 more) |\n| Packed/DSP | 23 | 7.3% | CLO.H, CLS.H, CLZ.H, CRC32.B, DVINIT.B (+18 more) |\n| System | 15 | 4.7% | CACHEA.I, CACHEA.W, CACHEA.WI, CACHEI.I, CACHEI.W (+10 more) |\n| Bit Operations | 8 | 2.5% | BSPLIT, DEXTR, EXTR, EXTR.U, IMASK (+3 more) |\n\n### Common Syntax Patterns\n\n| Pattern | Frequency | Example |\n|---------|-----------|---------|\n| `D[x],D[x],D[x]` | 64 | ABSDIF.B D[c],D[a],D[b] |\n| `D[x],D[x],const` | 44 | ABSDIF D[c],D[a],const9 |\n| `D[x],D[x],D[x],const` | 21 | CADD D[c],D[d],D[a],const9 |\n| `D[x],D[x]` | 16 | ABS D[c],D[b] |\n| `E[x],E[x],D[x],D[x] LL,n` | 14 | MADD.H E[c],E[d],D[a],D[b] LL,n |\n| `E[x],D[x],D[x]` | 10 | DIV E[c],D[a],D[b] |\n| `disp24` | 8 | CALL disp24 |\n| `D[x],const,disp15` | 8 | JEQ D[a],const4,disp15 |\n| `D[x],D[x],pos,D[x],pos` | 7 | AND.AND.T D[c],D[a],pos1,D[b],pos2 |\n| `E[x],E[x],D[x]` | 7 | DVADJ E[c],E[d],D[b] |\n\n# TriCore TC1.8 Instruction Set Architecture

*Generated on November 01, 2025 from comprehensive manual analysis*

## Overview

This document provides a comprehensive reference for the TriCore TC1.8 instruction set architecture with real examples extracted from the official Infineon manual. The TriCore architecture features a unified 32-bit RISC/MCU/DSP processor core designed for automotive and industrial real-time embedded applications.

### Key Features

- **Total Instructions**: 309 instruction variants
- **Unique Mnemonics**: 309 base instructions
- **Instruction Sizes**: 16-bit and 32-bit encodings
  - **16-bit Instructions**: 10 variants (compact encoding)
  - **32-bit Instructions**: 299 variants (full encoding)
- **Enhanced Bit Fields**: Complete bit field analysis with 83+ instructions
- **Manual Examples**: Real usage examples extracted from TC1.8 Architecture Manual

### Instruction Format

TriCore TC1.8 instructions use two primary encoding formats:

- **16-bit Format**: Compact instructions for frequent operations
- **32-bit Format**: Full instructions with extended addressing and immediate values

### Quick Reference - Common Instructions

| Category | Instruction | Manual Example | Description |
|----------|-------------|----------------|-------------|
| **Arithmetic** | `ABS` | `ABS D[3], D[1]` | Absolute value (page 66) |
| **Arithmetic** | `ABSDIF` | `ABSDIF D[3], D[1], #126` | Absolute difference (page 69) |
| **Arithmetic** | `MAX` | `MAX D[3], D[1], #126` | Maximum value (page 336) |
| **Packed** | `MADDMS.H` | `MADDMS.H E[0], E[2], D[4], D[5], #0` | Multiply-add packed (page 310) |
| **System** | `ADD` | `ADD D[3], D[2], #5` | Add with immediate |
| **Load/Store** | `LD.W` | `LD.W D[a], [A[b]]` | Load word from memory |

---

## Instruction Categories

### Instruction Distribution by Category

| Category | Count | Percentage |
|----------|-------|------------|
| Arithmetic | 112 | 36.2% |
| Logical | 30 | 9.7% |
| Bit Operations | 7 | 2.3% |
| Load/Store | 20 | 6.5% |
| Branch/Jump | 39 | 12.6% |
| System | 7 | 2.3% |
| Floating Point | 0 | 0.0% |
| Packed Operations | 18 | 5.8% |
| Address Operations | 15 | 4.9% |
| Other | 61 | 19.7% |

---

## Arithmetic Instructions

*112 instructions*

### ABS

**Absolute Value**

**Manual Examples:**
```assembly
ABS D[3], D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01C0000B` | 32-bit | `ABS D[c],D[b]` | Page 66 |

### ABS.B

**Absolute Value Packed Byte**

**Manual Examples:**
```assembly
ABS.B D[3], D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x05C0000B` | 32-bit | `ABS.B D[c],D[b]` | Page 67 |

### ABS.H

**Absolute Value Packed Half-word**

**Manual Examples:**
```assembly
ABS.H D[3], D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07C0000B` | 32-bit | `ABS.H D[c],D[b]` | Page 68 |

### ABSDIF

**Absolute Value of Difference**

**Manual Examples:**
```assembly
ABSDIF D[3], D[1], #126
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E0008B` | 32-bit | `ABSDIF D[c],D[a],const9` | Page 69 |

### ABSDIF.B

**Absolute Value of Difference Packed Byte**

**Manual Examples:**
```assembly
ABSDIF.B D[3], D[1], D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04E0000B` | 32-bit | `ABSDIF.B D[c],D[a],D[b]` | Page 70 |

### ABSDIF.H

**Absolute Value of Difference Packed Half-word**

**Manual Examples:**
```assembly
ABSDIF.H D[3], D[1], D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x06E0000B` | 32-bit | `ABSDIF.H D[c],D[a],D[b]` | Page 71 |

### ABSDIFS

**Absolute Value of Difference with Saturation**

**Manual Examples:**
```assembly
ABSDIFS D[3], D[1], #126
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00F0008B` | 32-bit | `ABSDIFS D[c],D[a],const9` | Page 72 |

### ABSDIFS.H

**Absolute Value of Difference Packed Half-word**

**Manual Examples:**
```assembly
ABSDIFS.H D[3], D[1], D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x06F0000B` | 32-bit | `ABSDIFS.H D[c],D[a],D[b]` | Page 73 |

### ABSS

**Absolute Value with Saturation**

**Manual Examples:**
```assembly
ABSS D[3], D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01D0000B` | 32-bit | `ABSS D[c],D[b]` | Page 74 |

### ABSS.H

**Absolute Value Packed Half-word with Saturatio**

**Manual Examples:**
```assembly
ABSS.H D[3], D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07D0000B` | 32-bit | `ABSS.H D[c],D[b]` | Page 75 |

### ADD

**Add**

**Manual Examples:**
```assembly
ADD D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000008B` | 32-bit | `ADD D[c],D[a],const9` | Page 76 |

### ADD.A

**Add Address**

**Manual Examples:**
```assembly
ADD.A A[3],A[2],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00100001` | 32-bit | `ADD.A A[c],A[a],A[b]` | Page 77 |

### ADD.B

**Add Packed Byte**

**Manual Examples:**
```assembly
ADD.B D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0400000B` | 32-bit | `ADD.B D[c],D[a],D[b]` | Page 78 |

### ADD.H

**Add Packed Half-word**

**Manual Examples:**
```assembly
ADD.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0600000B` | 32-bit | `ADD.H D[c],D[a],D[b]` | Page 79 |

### ADDC

**Add with Carry**

**Manual Examples:**
```assembly
ADDC D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0050008B` | 32-bit | `ADDC D[c],D[a],const9` | Page 80 |

### ADDI

**Add Immediate**

**Manual Examples:**
```assembly
ADDI D[3],D[2],#100 (RLC)
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x1B` | 32-bit | `ADDI D[c],D[a],const16 (RLC)` | Page 81 |

### ADDIH

**Add Immediate High**

**Manual Examples:**
```assembly
ADDIH D[3],D[2],#100 (RLC)
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x9B` | 32-bit | `ADDIH D[c],D[a],const16 (RLC)` | Page 82 |

### ADDIH.A

**Add Immediate High to Address**

**Manual Examples:**
```assembly
ADDIH.A A[3],A[2],#100 (RLC)
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x11` | 32-bit | `ADDIH.A A[c],A[a],const16 (RLC)` | Page 83 |

### ADDS

**Add Signed with Saturation**

**Manual Examples:**
```assembly
ADDS D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0020008B` | 32-bit | `ADDS D[c],D[a],const9` | Page 84 |

### ADDS.H

**Add Signed Packed Half-word with Saturation**

**Manual Examples:**
```assembly
ADDS.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0620000B` | 32-bit | `ADDS.H D[c],D[a],D[b]` | Page 85 |

### ADDS.HU

**Add Unsigned Packed Half-word with Saturation**

**Manual Examples:**
```assembly
ADDS.HU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0630000B` | 32-bit | `ADDS.HU D[c],D[a],D[b]` | Page 86 |

### ADDS.U

**Add Unsigned with Saturation**

**Manual Examples:**
```assembly
ADDS.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0030008B` | 32-bit | `ADDS.U D[c],D[a],const9` | Page 87 |

### ADDSC.A

**Add Scaled Index to Address**

**Manual Examples:**
```assembly
ADDSC.A A[3],A[1],D[2],n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x06000001` | 32-bit | `ADDSC.A A[c],A[b],D[a],n` | Page 88 |

### ADDSC.AT

**Add Bit-Scaled Index to Address**

**Manual Examples:**
```assembly
ADDSC.AT A[3],A[1],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x06200001` | 32-bit | `ADDSC.AT A[c],A[b],D[a]` | Page 89 |

### ADDX

**Add Extended**

**Manual Examples:**
```assembly
ADDX D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0040008B` | 32-bit | `ADDX D[c],D[a],const9` | Page 90 |

### CADD

**Conditional Add**

**Manual Examples:**
```assembly
CADD D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000AB` | 32-bit | `CADD D[c],D[d],D[a],const9` | Page 196 |

### CADDN

**Conditional Add-Not**

**Manual Examples:**
```assembly
CADDN D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x001000AB` | 32-bit | `CADDN D[c],D[d],D[a],const9` | Page 204 |

### CSUB

**Conditional Subtract**

**Manual Examples:**
```assembly
CSUB D[3],D[d],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0020002B` | 32-bit | `CSUB D[c],D[d],D[a],D[b]` | Page 204 |

### CSUBN

**Conditional Subtract-Not**

**Manual Examples:**
```assembly
CSUBN D[3],D[d],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0030002B` | 32-bit | `CSUBN D[c],D[d],D[a],D[b]` | Page 184 |

### DIV

**Divide**

**Manual Examples:**
```assembly
DIV E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0200004B` | 32-bit | `DIV E[c],D[a],D[b]` | Page 221 |

### DIV.U

**Divide Unsigned**

**Manual Examples:**
```assembly
DIV.U E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0210004B` | 32-bit | `DIV.U E[c],D[a],D[b]` | Page 239 |

### DIV64

**DIV64 Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `DIV64` | Page 166 |

### DIV64.U

**DIV64.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `DIV64.U` | Page 168 |

### IXMAX

**Find Maximum Index**

**Manual Examples:**
```assembly
IXMAX E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00A0006B` | 32-bit | `IXMAX E[c],E[d],D[b]` | Page 274 |

### IXMAX.U

**Find Maximum Index (unsigned)**

**Manual Examples:**
```assembly
IXMAX.U E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00B0006B` | 32-bit | `IXMAX.U E[c],E[d],D[b]` | Page 308 |

### IXMIN

**Find Minimum Index**

**Manual Examples:**
```assembly
IXMIN E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0080006B` | 32-bit | `IXMIN E[c],E[d],D[b]` | Page 279 |

### IXMIN.U

**Find Minimum Index (unsigned)**

**Manual Examples:**
```assembly
IXMIN.U E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0090006B` | 32-bit | `IXMIN.U E[c],E[d],D[b]` | Page 289 |

### MADD

**Multiply-Add**

**Manual Examples:**
```assembly
MADD D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00200013` | 32-bit | `MADD D[c],D[d],D[a],const9` | Page 282 |

### MADD.H

**Packed Multiply-Add Q Format**

**Manual Examples:**
```assembly
MADD.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00680083` | 32-bit | `MADD.H E[c],E[d],D[a],D[b] LL,n` | Page 347 |

### MADD.Q

**Multiply-Add Q Format**

**Manual Examples:**
```assembly
MADD.Q D[3],D[d],D[2],D[1],n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00080043` | 32-bit | `MADD.Q D[c],D[d],D[a],D[b],n` | Page 322 |

### MADD.U

**Multiply-Add Unsigned**

**Manual Examples:**
```assembly
MADD.U E[c],E[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00200013` | 32-bit | `MADD.U E[c],E[d],D[a],const9` | Page 288 |

### MADDM.H

**Packed Multiply-Add Q Format Multi-precision**

**Manual Examples:**
```assembly
MADDM.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00780083` | 32-bit | `MADDM.H E[c],E[d],D[a],D[b] LL,n` | Page 348 |

### MADDMS.H

**Packed Multiply-Add Q Format Multi-precision,**

**Manual Examples:**
```assembly
MADDMS.H E[0], E[2], D[4], D[5]UL, #0
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00F80083` | 32-bit | `MADDMS.H E[c],E[d],D[a],D[b] LL,n` | Page 310 |

### MADDR.H

**Packed Multiply-Add Q Format with Rounding**

**Manual Examples:**
```assembly
MADDR.H D[3],D[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00380083` | 32-bit | `MADDR.H D[c],D[d],D[a],D[b] LL,n` | Page 287 |

### MADDR.Q

**Multiply-Add Q Format with Rounding**

**Manual Examples:**
```assembly
MADDR.Q D[3],D[d],D[2] L,D[1] L,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x001C0043` | 32-bit | `MADDR.Q D[c],D[d],D[a] L,D[b] L,n` | Page 263 |

### MADDRS.H

**Packed Multiply-Add Q Format with Rounding,Sa**

**Manual Examples:**
```assembly
MADDRS.H D[3],D[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00B80083` | 32-bit | `MADDRS.H D[c],D[d],D[a],D[b] LL,n` | Page 299 |

### MADDRS.Q

**Multiply-Add Q Format with Rounding,Saturated**

**Manual Examples:**
```assembly
MADDRS.Q D[3],D[d],D[2] L,D[1] L,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x009C0043` | 32-bit | `MADDRS.Q D[c],D[d],D[a] L,D[b] L,n` | Page 275 |

### MADDS

**Multiply-Add,Saturated**

**Manual Examples:**
```assembly
MADDS D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00A00013` | 32-bit | `MADDS D[c],D[d],D[a],const9` | Page 314 |

### MADDS.H

**Packed Multiply-Add Q Format,Saturated**

**Manual Examples:**
```assembly
MADDS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E80083` | 32-bit | `MADDS.H E[c],E[d],D[a],D[b] LL,n` | Page 317 |

### MADDS.Q

**Multiply-Add Q Format,Saturated**

**Manual Examples:**
```assembly
MADDS.Q D[3],D[d],D[2],D[1],n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00880043` | 32-bit | `MADDS.Q D[c],D[d],D[a],D[b],n` | Page 265 |

### MADDS.U

**Multiply-Add Unsigned,Saturated**

**Manual Examples:**
```assembly
MADDS.U D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00800013` | 32-bit | `MADDS.U D[c],D[d],D[a],const9` | Page 336 |

### MADDSU.H

**Packed Multiply-Add/Subtract Q Format**

**Manual Examples:**
```assembly
MADDSU.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x006800C3` | 32-bit | `MADDSU.H E[c],E[d],D[a],D[b] LL,n` | Page 300 |

### MADDSUM.H

**Packed Multiply-Add/Subtract Q Format Multi-pr**

**Manual Examples:**
```assembly
MADDSUM.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x007800C3` | 32-bit | `MADDSUM.H E[c],E[d],D[a],D[b] LL,n` | Page 290 |

### MADDSUMS.H

**Packed Multiply-Add/Subtract Q Format Multi-pr**

**Manual Examples:**
```assembly
MADDSUMS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00F800C3` | 32-bit | `MADDSUMS.H E[c],E[d],D[a],D[b] LL,n` | Page 354 |

### MADDSUR.H

**Packed Multiply-Add/Subtract Q Format with Rou**

**Manual Examples:**
```assembly
MADDSUR.H D[3],D[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x003800C3` | 32-bit | `MADDSUR.H D[c],D[d],D[a],D[b] LL,n` | Page 269 |

### MADDSURS.H

**Packed Multiply-Add/Subtract Q Format with Rou**

**Manual Examples:**
```assembly
MADDSURS.H D[3],D[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00B800C3` | 32-bit | `MADDSURS.H D[c],D[d],D[a],D[b] LL,n` | Page 260 |

### MADDSUS.H

**Packed Multiply-Add/Subtract Q Format Saturate**

**Manual Examples:**
```assembly
MADDSUS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E800C3` | 32-bit | `MADDSUS.H E[c],E[d],D[a],D[b] LL,n` | Page 286 |

### MAX

**Maximum Value**

**Manual Examples:**
```assembly
MAX D[3], D[1], #126
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0340008B` | 32-bit | `MAX D[c],D[a],const9` | Page 336 |

### MAX.B

**Maximum Value Packed Byte**

**Manual Examples:**
```assembly
MAX.B D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x05A0000B` | 32-bit | `MAX.B D[c],D[a],D[b]` | Page 350 |

### MAX.BU

**Maximum Value Packed Byte Unsigned**

**Manual Examples:**
```assembly
MAX.BU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x05B0000B` | 32-bit | `MAX.BU D[c],D[a],D[b]` | Page 320 |

### MAX.H

**Maximum Value Packed Half-word**

**Manual Examples:**
```assembly
MAX.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07A0000B` | 32-bit | `MAX.H D[c],D[a],D[b]` | Page 359 |

### MAX.HU

**Maximum Value Packed Half-word Unsigned**

**Manual Examples:**
```assembly
MAX.HU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07B0000B` | 32-bit | `MAX.HU D[c],D[a],D[b]` | Page 267 |

### MAX.U

**Maximum Value Unsigned**

**Manual Examples:**
```assembly
MAX.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0360008B` | 32-bit | `MAX.U D[c],D[a],const9` | Page 321 |

### MIN

**Minimum Value**

**Manual Examples:**
```assembly
MIN D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0300008B` | 32-bit | `MIN D[c],D[a],const9` | Page 336 |

### MIN.B

**Minimum Value Packed Byte**

**Manual Examples:**
```assembly
MIN.B D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0580000B` | 32-bit | `MIN.B D[c],D[a],D[b]` | Page 263 |

### MIN.BU

**Minimum Value Packed Byte Unsigned**

**Manual Examples:**
```assembly
MIN.BU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0590000B` | 32-bit | `MIN.BU D[c],D[a],D[b]` | Page 286 |

### MIN.H

**Minimum Value Packed Half-word**

**Manual Examples:**
```assembly
MIN.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0780000B` | 32-bit | `MIN.H D[c],D[a],D[b]` | Page 328 |

### MIN.HU

**Minimum Value Packed Half-word Unsigned**

**Manual Examples:**
```assembly
MIN.HU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0790000B` | 32-bit | `MIN.HU D[c],D[a],D[b]` | Page 307 |

### MIN.U

**Minimum Value Unsigned**

**Manual Examples:**
```assembly
MIN.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0320008B` | 32-bit | `MIN.U D[c],D[a],const9` | Page 312 |

### MSUB

**Multiply-Subtract**

**Manual Examples:**
```assembly
MSUB D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00200033` | 32-bit | `MSUB D[c],D[d],D[a],const9` | Page 326 |

### MSUB.H

**Packed Multiply-Subtract Q Format**

**Manual Examples:**
```assembly
MSUB.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x006800A3` | 32-bit | `MSUB.H E[c],E[d],D[a],D[b] LL,n` | Page 300 |

### MSUB.Q

**Multiply-Subtract Q Format**

**Manual Examples:**
```assembly
MSUB.Q D[3],D[d],D[2],D[1],n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00040063` | 32-bit | `MSUB.Q D[c],D[d],D[a],D[b],n` | Page 277 |

### MSUB.U

**Multiply-Subtract Unsigned**

**Manual Examples:**
```assembly
MSUB.U E[c],E[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00400033` | 32-bit | `MSUB.U E[c],E[d],D[a],const9` | Page 333 |

### MSUBAD.H

**Packed Multiply-Subtract/Add Q Format**

**Manual Examples:**
```assembly
MSUBAD.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x006800E3` | 32-bit | `MSUBAD.H E[c],E[d],D[a],D[b] LL,n` | Page 278 |

### MSUBADM.H

**Packed Multiply-Subtract/Add Q Format-Multi-pr**

**Manual Examples:**
```assembly
MSUBADM.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x007800E3` | 32-bit | `MSUBADM.H E[c],E[d],D[a],D[b] LL,n` | Page 313 |

### MSUBADMS.H

**Packed Multiply-Subtract/Add Q Format-Multi-pr**

**Manual Examples:**
```assembly
MSUBADMS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00F800E3` | 32-bit | `MSUBADMS.H E[c],E[d],D[a],D[b] LL,n` | Page 319 |

### MSUBADR.H

**MSUBADR.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBADR.H` | Page 388 |

### MSUBADRS.H

**MSUBADRS.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBADRS.H` | Page 391 |

### MSUBADS.H

**Packed Multiply-Subtract/Add Q Format,Saturat**

**Manual Examples:**
```assembly
MSUBADS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E800E3` | 32-bit | `MSUBADS.H E[c],E[d],D[a],D[b] LL,n` | Page 294 |

### MSUBM.H

**MSUBM.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBM.H` | Page 394 |

### MSUBMS.H

**MSUBMS.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBMS.H` | Page 396 |

### MSUBR.H

**MSUBR.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBR.H` | Page 398 |

### MSUBR.Q

**MSUBR.Q Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBR.Q` | Page 404 |

### MSUBRS.H

**MSUBRS.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBRS.H` | Page 401 |

### MSUBRS.Q

**MSUBRS.Q Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MSUBRS.Q` | Page 406 |

### MSUBS

**Multiply-Subtract,Saturated**

**Manual Examples:**
```assembly
MSUBS D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00A00033` | 32-bit | `MSUBS D[c],D[d],D[a],const9` | Page 291 |

### MSUBS.H

**Packed Multiply-Subtract Q Format,Saturated**

**Manual Examples:**
```assembly
MSUBS.H E[c],E[d],D[2],D[1] LL,n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E800A3` | 32-bit | `MSUBS.H E[c],E[d],D[a],D[b] LL,n` | Page 272 |

### MSUBS.Q

**Multiply-Subtract Q Format,Saturated**

**Manual Examples:**
```assembly
MSUBS.Q D[3],D[d],D[2],D[1],n
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00880063` | 32-bit | `MSUBS.Q D[c],D[d],D[a],D[b],n` | Page 329 |

### MSUBS.U

**Multiply-Subtract Unsigned,Saturated**

**Manual Examples:**
```assembly
MSUBS.U D[3],D[d],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00800033` | 32-bit | `MSUBS.U D[c],D[d],D[a],const9` | Page 336 |

### MUL

**MUL Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MUL` | Page 410 |

### MUL.H

**MUL.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MUL.H` | Page 413 |

### MUL.Q

**MUL.Q Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MUL.Q` | Page 415 |

### MUL.U

**MUL.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MUL.U` | Page 418 |

### MULM.H

**MULM.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULM.H` | Page 420 |

### MULP

**MULP Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULP` | Page 422 |

### MULR.H

**MULR.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULR.H` | Page 423 |

### MULR.Q

**MULR.Q Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULR.Q` | Page 425 |

### MULS

**MULS Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULS` | Page 412 |

### MULS.U

**MULS.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MULS.U` | Page 419 |

### RSUB

**RSUB Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RSUB` | Page 464 |

### RSUBS

**RSUBS Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RSUBS` | Page 465 |

### RSUBS.U

**RSUBS.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RSUBS.U` | Page 466 |

### SUB

**SUB Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUB` | Page 523 |

### SUB.A

**SUB.A Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUB.A` | Page 525 |

### SUB.B

**SUB.B Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUB.B` | Page 526 |

### SUB.H

**SUB.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUB.H` | Page 527 |

### SUBC

**SUBC Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBC` | Page 528 |

### SUBS

**SUBS Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBS` | Page 529 |

### SUBS.H

**SUBS.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBS.H` | Page 531 |

### SUBS.HU

**SUBS.HU Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBS.HU` | Page 532 |

### SUBS.U

**SUBS.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBS.U` | Page 530 |

### SUBX

**SUBX Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SUBX` | Page 533 |

## Logical Instructions

*30 instructions*

### AND

**Bitwise AND**

**Manual Examples:**
```assembly
AND D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0080008F` | 32-bit | `AND D[c],D[a],const9` | Page 91 |

### AND.AND.T

**Accumulating Bit Logical AND-AND**

**Manual Examples:**
```assembly
AND.AND.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000047` | 32-bit | `AND.AND.T D[c],D[a],pos1,D[b],pos2` | Page 93 |

### AND.ANDN.T

**Accumulating Bit Logical AND-AND-Not**

**Manual Examples:**
```assembly
AND.ANDN.T D[3],D[a,] pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00300047` | 32-bit | `AND.ANDN.T D[c],D[a,] pos1,D[b],pos2` | Page 93 |

### AND.EQ

**Equal Accumulating**

**Manual Examples:**
```assembly
AND.EQ D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0200008B` | 32-bit | `AND.EQ D[c],D[a],const9` | Page 93 |

### AND.GE

**Greater Than or Equal Accumulating**

**Manual Examples:**
```assembly
AND.GE D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0240008B` | 32-bit | `AND.GE D[c],D[a],const9` | Page 94 |

### AND.GE.U

**Greater Than or Equal Accumulating Unsigned**

**Manual Examples:**
```assembly
AND.GE.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0250008B` | 32-bit | `AND.GE.U D[c],D[a],const9` | Page 95 |

### AND.LT

**Less Than Accumulating**

**Manual Examples:**
```assembly
AND.LT D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0220008B` | 32-bit | `AND.LT D[c],D[a],const9` | Page 92 |

### AND.LT.U

**Less Than Accumulating Unsigned**

**Manual Examples:**
```assembly
AND.LT.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0230008B` | 32-bit | `AND.LT.U D[c],D[a],const9` | Page 93 |

### AND.NE

**Not Equal Accumulating**

**Manual Examples:**
```assembly
AND.NE D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0210008B` | 32-bit | `AND.NE D[c],D[a],const9` | Page 92 |

### AND.NOR.T

**Accumulating Bit Logical AND-NOR**

**Manual Examples:**
```assembly
AND.NOR.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00200047` | 32-bit | `AND.NOR.T D[c],D[a],pos1,D[b],pos2` | Page 93 |

### AND.OR.T

**Accumulating Bit Logical AND-OR**

**Manual Examples:**
```assembly
AND.OR.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00100047` | 32-bit | `AND.OR.T D[c],D[a],pos1,D[b],pos2` | Page 93 |

### AND.T

**Bit Logical AND**

**Manual Examples:**
```assembly
AND.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000087` | 32-bit | `AND.T D[c],D[a],pos1,D[b],pos2` | Page 92 |

### ANDN

**Bitwise AND-Not**

**Manual Examples:**
```assembly
ANDN D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E0008F` | 32-bit | `ANDN D[c],D[a],const9` | Page 118 |

### ANDN.T

**Bit Logical AND-Not**

**Manual Examples:**
```assembly
ANDN.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00300087` | 32-bit | `ANDN.T D[c],D[a],pos1,D[b],pos2` | Page 106 |

### NAND

**NAND Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NAND` | Page 426 |

### NOR

**NOR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NOR` | Page 432 |

### NOT

**NOT Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NOT` | Page 434 |

### OR

**OR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `OR` | Page 435 |

### OR.EQ

**OR.EQ Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `OR.EQ` | Page 441 |

### OR.GE

**OR.GE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `OR.GE` | Page 442 |

### OR.GE.U

**OR.GE.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `OR.GE.U` | Page 443 |

### OR.NE

**OR.NE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `OR.NE` | Page 446 |

### ORN

**ORN Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `ORN` | Page 448 |

### RESTORE

**RESTORE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RESTORE` | Page 456 |

### XNOR

**XNOR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XNOR` | Page 548 |

### XOR

**XOR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XOR` | Page 550 |

### XOR.EQ

**XOR.EQ Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XOR.EQ` | Page 551 |

### XOR.GE

**XOR.GE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XOR.GE` | Page 552 |

### XOR.GE.U

**XOR.GE.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XOR.GE.U` | Page 553 |

### XOR.NE

**XOR.NE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `XOR.NE` | Page 556 |

## Bit Operations Instructions

*7 instructions*

### DEXTR

**Extract from Double Register**

**Manual Examples:**
```assembly
DEXTR D[3],D[2],D[1],pos
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000077` | 32-bit | `DEXTR D[c],D[a],D[b],pos` | Page 211 |

### EXTR

**Extract Bit Field**

**Manual Examples:**
```assembly
EXTR D[3],D[2],pos,width
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00200037` | 32-bit | `EXTR D[c],D[a],pos,width` | Page 240 |

### EXTR.U

**Extract Bit Field Unsigned**

**Manual Examples:**
```assembly
EXTR.U D[3],D[2],pos,width
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00300037` | 32-bit | `EXTR.U D[c],D[a],pos,width` | Page 243 |

### IMASK

**Insert Mask**

**Manual Examples:**
```assembly
IMASK E[c],#3,pos,width
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x001000B7` | 32-bit | `IMASK E[c],const4,pos,width` | Page 280 |

### INS.T

**Insert Bit**

**Manual Examples:**
```assembly
INS.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000067` | 32-bit | `INS.T D[c],D[a],pos1,D[b],pos2` | Page 325 |

### INSERT

**Insert Bit Field**

**Manual Examples:**
```assembly
INSERT D[3],D[2],#3,pos,width
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000B7` | 32-bit | `INSERT D[c],D[a],const4,pos,width` | Page 357 |

### INSN.T

**Insert Bit-Not**

**Manual Examples:**
```assembly
INSN.T D[3],D[2],pos1,D[1],pos2
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00100067` | 32-bit | `INSN.T D[c],D[a],pos1,D[b],pos2` | Page 317 |

## Load/Store Instructions

*20 instructions*

### DVSTEP

**Divide-Step**

**Manual Examples:**
```assembly
DVSTEP E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00F0006B` | 32-bit | `DVSTEP E[c],E[d],D[b]` | Page 239 |

### DVSTEP.U

**Divide-Step Unsigned**

**Manual Examples:**
```assembly
DVSTEP.U E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00E0006B` | 32-bit | `DVSTEP.U E[c],E[d],D[b]` | Page 220 |

### LD.A

**Load Word to Address Register**

**Manual Examples:**
```assembly
LD.A A[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x08000085` | 32-bit | `LD.A A[a],off18` | Page 320 |

### LD.B

**Load Byte**

**Manual Examples:**
```assembly
LD.B D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000005` | 32-bit | `LD.B D[a],off18` | Page 276 |

### LD.BU

**Load Byte Unsigned**

**Manual Examples:**
```assembly
LD.BU D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04000005` | 32-bit | `LD.BU D[a],off18` | Page 290 |

### LD.D

**Load Double-word**

**Manual Examples:**
```assembly
LD.D E[a],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04000085` | 32-bit | `LD.D E[a],off18` | Page 267 |

### LD.DA

**Load Double-word to Address Register**

**Manual Examples:**
```assembly
LD.DA P[a],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0C000085` | 32-bit | `LD.DA P[a],off18` | Page 347 |

### LD.DD

**LD.DD Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `LD.DD` | Page 258 |

### LD.H

**Load Half-word**

**Manual Examples:**
```assembly
LD.H D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x08000005` | 32-bit | `LD.H D[a],off18` | Page 308 |

### LD.HU

**Load Half-word Unsigned**

**Manual Examples:**
```assembly
LD.HU D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0C000005` | 32-bit | `LD.HU D[a],off18` | Page 295 |

### LD.Q

**Load Half-word Signed Fraction**

**Manual Examples:**
```assembly
LD.Q D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000045` | 32-bit | `LD.Q D[a],off18` | Page 307 |

### LD.W

**Load Word**

**Manual Examples:**
```assembly
LD.W D[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000085` | 32-bit | `LD.W D[a],off18` | Page 284 |

### LDLCX

**Load Lower Context**

**Manual Examples:**
```assembly
LDLCX #50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x08000015` | 32-bit | `LDLCXoff18` | Page 352 |

### LDMST

**Load-Modify-Store**

**Manual Examples:**
```assembly
LDMST #50,E[a]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x040000E5` | 32-bit | `LDMST off18,E[a]` | Page 346 |

### LDUCX

**Load Upper Context**

**Manual Examples:**
```assembly
LDUCX #50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0C000015` | 32-bit | `LDUCX off18` | Page 293 |

### LEA

**Load Effective Address**

**Manual Examples:**
```assembly
LEA A[2],#50
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000C5` | 32-bit | `LEA A[a],off18` | Page 269 |

### RSTV

**RSTV Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RSTV` | Page 463 |

### ST

**ST Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `ST` | Page 517 |

### STLCX

**STLCX Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `STLCX` | Page 521 |

### STUCX

**STUCX Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `STUCX` | Page 522 |

## Branch/Jump Instructions

*39 instructions*

### CALL

**Call**

**Manual Examples:**
```assembly
CALL disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000006D` | 32-bit | `CALL disp24` | Page 201 |

### CALLA

**Call Absolute**

**Manual Examples:**
```assembly
CALLA disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000ED` | 32-bit | `CALLA disp24` | Page 184 |

### CALLI

**Call Indirect**

**Manual Examples:**
```assembly
CALLI A[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000002D` | 32-bit | `CALLI A[a]` | Page 196 |

### DVADJ

**Divide-Adjust**

**Manual Examples:**
```assembly
DVADJ E[c],E[d],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00D0006B` | 32-bit | `DVADJ E[c],E[d],D[b]` | Page 221 |

### FCALL

**Fast Call**

**Manual Examples:**
```assembly
FCALL disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000061` | 32-bit | `FCALL disp24` | Page 354 |

### FCALLA

**Fast Call Absolute**

**Manual Examples:**
```assembly
FCALLA disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000E1` | 32-bit | `FCALLA disp24` | Page 359 |

### FCALLI

**Fast Call Indirect**

**Manual Examples:**
```assembly
FCALLI A[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0010002D` | 32-bit | `FCALLI A[a]` | Page 264 |

### FRET

**Return from Fast Call**

**Manual Examples:**
```assembly
FRET
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x7000` | 16-bit | `FRET` | Page 291 |

### J

**Jump Unconditional**

**Manual Examples:**
```assembly
J disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000001D` | 32-bit | `J disp24` | Page 314 |

### JA

**Jump Unconditional Absolute**

**Manual Examples:**
```assembly
JA disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000009D` | 32-bit | `JA disp24` | Page 324 |

### JEQ

**Jump if Equal**

**Manual Examples:**
```assembly
JEQ D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000DF` | 32-bit | `JEQ D[a],const4,disp15` | Page 322 |

### JEQ.A

**Jump if Equal Address**

**Manual Examples:**
```assembly
JEQ.A A[2],A[1],disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000007D` | 32-bit | `JEQ.A A[a],A[b],disp15` | Page 291 |

### JGE

**Jump if Greater Than or Equal**

**Manual Examples:**
```assembly
JGE D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000FF` | 32-bit | `JGE D[a],const4,disp15` | Page 289 |

### JGE.U

**Jump if Greater Than or Equal Unsigned**

**Manual Examples:**
```assembly
JGE.U D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x800000FF` | 32-bit | `JGE.U D[a],const4,disp15` | Page 294 |

### JGEZ

**Jump if Greater Than or Equal to Zero (16-bit)**

**Manual Examples:**
```assembly
JGEZ D[1],disp4
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0xCE` | 16-bit | `JGEZ D[b],disp4` | Page 302 |

### JGTZ

**Jump if Greater Than Zero (16-bit)**

**Manual Examples:**
```assembly
JGTZ D[1],disp4
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x4E` | 16-bit | `JGTZ D[b],disp4` | Page 312 |

### JI

**Jump Indirect**

**Manual Examples:**
```assembly
JI A[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0030002D` | 32-bit | `JI A[a]` | Page 356 |

### JL

**Jump and Link**

**Manual Examples:**
```assembly
JL disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000005D` | 32-bit | `JL disp24` | Page 309 |

### JLA

**Jump and Link Absolute**

**Manual Examples:**
```assembly
JLA disp24
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000DD` | 32-bit | `JLA disp24` | Page 304 |

### JLEZ

**Jump if Less Than or Equal to Zero (16-bit)**

**Manual Examples:**
```assembly
JLEZ D[1],disp4
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x8E` | 16-bit | `JLEZ D[b],disp4` | Page 301 |

### JLI

**Jump and Link Indirect**

**Manual Examples:**
```assembly
JLI A[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0020002D` | 32-bit | `JLI A[a]` | Page 272 |

### JLT

**Jump if Less Than**

**Manual Examples:**
```assembly
JLT D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000BF` | 32-bit | `JLT D[a],const4,disp15` | Page 284 |

### JLT.U

**Jump if Less Than Unsigned**

**Manual Examples:**
```assembly
JLT.U D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x800000BF` | 32-bit | `JLT.U D[a],const4,disp15` | Page 274 |

### JLTZ

**Jump if Less Than Zero (16-bit)**

**Manual Examples:**
```assembly
JLTZ D[1],disp4
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0E` | 16-bit | `JLTZ D[b],disp4` | Page 341 |

### JNE

**Jump if Not Equal**

**Manual Examples:**
```assembly
JNE D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x800000DF` | 32-bit | `JNE D[a],const4,disp15` | Page 304 |

### JNE.A

**Jump if Not Equal Address**

**Manual Examples:**
```assembly
JNE.A A[2],A[1],disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x8000007D` | 32-bit | `JNE.A A[a],A[b],disp15` | Page 296 |

### JNED

**Jump if Not Equal and Decrement**

**Manual Examples:**
```assembly
JNED D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x8000009F` | 32-bit | `JNED D[a],const4,disp15` | Page 357 |

### JNEI

**Jump if Not Equal and Increment**

**Manual Examples:**
```assembly
JNEI D[2],#3,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000009F` | 32-bit | `JNEI D[a],const4,disp15` | Page 310 |

### JNZ

**Jump if Not Equal to Zero (16-bit)**

**Manual Examples:**
```assembly
JNZ D[15],disp8
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0xEE` | 16-bit | `JNZ D[15],disp8` | Page 337 |

### JNZ.A

**Jump if Not Equal to Zero Address**

**Manual Examples:**
```assembly
JNZ.A A[2],disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x800000BD` | 32-bit | `JNZ.A A[a],disp15` | Page 337 |

### JNZ.T

**Jump if Not Equal to Zero Bit**

**Manual Examples:**
```assembly
JNZ.T D[2],n,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x8000006F` | 32-bit | `JNZ.T D[a],n,disp15` | Page 271 |

### JRI

**JRI Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `JRI` | Page 241 |

### JZ

**Jump if Zero (16-bit)**

**Manual Examples:**
```assembly
JZ D[15],disp8
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x6E` | 16-bit | `JZ D[15],disp8` | Page 263 |

### JZ.A

**Jump if Zero Address**

**Manual Examples:**
```assembly
JZ.A A[2],disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000BD` | 32-bit | `JZ.A A[a],disp15` | Page 260 |

### JZ.T

**Jump if Zero Bit**

**Manual Examples:**
```assembly
JZ.T D[2],n,disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000006F` | 32-bit | `JZ.T D[a],n,disp15` | Page 269 |

### LOOP

**Loop**

**Manual Examples:**
```assembly
LOOP A[1],disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000FD` | 32-bit | `LOOP A[b],disp15` | Page 294 |

### LOOPU

**Loop Unconditional**

**Manual Examples:**
```assembly
LOOPU disp15
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x800000FD` | 32-bit | `LOOPU disp15` | Page 356 |

### RET

**RET Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RET` | Page 457 |

### SYSCALL

**SYSCALL Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SYSCALL` | Page 541 |

## System Instructions

*7 instructions*

### DEBUG

**Debug**

**Manual Examples:**
```assembly
DEBUG
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00` | 16-bit | `DEBUG` | Page 235 |

### DISABLE

**Disable Interrupts**

**Manual Examples:**
```assembly
DISABLE
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0340000D` | 32-bit | `DISABLE` | Page 234 |

### DSYNC

**Synchronize Data**

**Manual Examples:**
```assembly
DSYNC
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0480000D` | 32-bit | `DSYNC` | Page 216 |

### ENABLE

**Enable Interrupts**

**Manual Examples:**
```assembly
ENABLE
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0300000D` | 32-bit | `ENABLE` | Page 241 |

### ISYNC

**Synchronize Instructions**

**Manual Examples:**
```assembly
ISYNC
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04C0000D` | 32-bit | `ISYNC` | Page 269 |

### LSYNC

**LSYNC Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `LSYNC` | Page 278 |

### NOP

**NOP Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NOP` | Page 431 |

## Packed Operations Instructions

*18 instructions*

### CLO.H

**Count Leading Ones in Packed Half-words**

**Manual Examples:**
```assembly
CLO.H D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07D0000F` | 32-bit | `CLO.H D[c],D[a]` | Page 206 |

### CLS.H

**Count Leading Signs in Packed Half-words**

**Manual Examples:**
```assembly
CLS.H D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07E0000F` | 32-bit | `CLS.H D[c],D[a]` | Page 204 |

### CLZ.H

**Count Leading Zeros in Packed Half-words**

**Manual Examples:**
```assembly
CLZ.H D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x07C0000F` | 32-bit | `CLZ.H D[c],D[a]` | Page 185 |

### CRC32.B

**CRC32.B Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `CRC32.B` | Page 148 |

### DVINIT.B

**Divide-Initialization Byte**

**Manual Examples:**
```assembly
DVINIT.H E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x03A0004B` | 32-bit | `DVINIT.H E[c],D[a],D[b]` | Page 226 |

### DVINIT.BU

**Divide-Initialization Byte Unsigned**

**Manual Examples:**
```assembly
DVINIT.HU E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x02A0004B` | 32-bit | `DVINIT.HU E[c],D[a],D[b]` | Page 221 |

### DVINIT.H

**Divide-Initialization Half-word**

**Manual Examples:**
```assembly
DVINIT E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01A0004B` | 32-bit | `DVINIT E[c],D[a],D[b]` | Page 239 |

### DVINIT.HU

**Divide-Initialization Half-word Unsigned**

**Manual Examples:**
```assembly
DVINIT.U E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00A0004B` | 32-bit | `DVINIT.U E[c],D[a],D[b]` | Page 211 |

### EQ.B

**Equal Packed Byte**

**Manual Examples:**
```assembly
EQ.B D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0500000B` | 32-bit | `EQ.B D[c],D[a],D[b]` | Page 240 |

### EQ.H

**Equal Packed Half-word**

**Manual Examples:**
```assembly
EQ.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0700000B` | 32-bit | `EQ.H D[c],D[a],D[b]` | Page 250 |

### EQANY.B

**Equal Any Byte**

**Manual Examples:**
```assembly
EQANY.B D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0560008B` | 32-bit | `EQANY.B D[c],D[a],const9` | Page 244 |

### EQANY.H

**Equal Any Half-word**

**Manual Examples:**
```assembly
EQANY.H D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0760008B` | 32-bit | `EQANY.H D[c],D[a],const9` | Page 252 |

### LT.B

**Less Than Packed Byte**

**Manual Examples:**
```assembly
LT.B D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0520000B` | 32-bit | `LT.B D[c],D[a],D[b]` | Page 318 |

### LT.BU

**Less Than Packed Byte Unsigned**

**Manual Examples:**
```assembly
LT.BU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0530000B` | 32-bit | `LT.BU D[c],D[a],D[b]` | Page 310 |

### LT.H

**Less Than Packed Half-word**

**Manual Examples:**
```assembly
LT.H D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0720000B` | 32-bit | `LT.H D[c],D[a],D[b]` | Page 321 |

### LT.HU

**Less Than Packed Half-word Unsigned**

**Manual Examples:**
```assembly
LT.HU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0730000B` | 32-bit | `LT.HU D[c],D[a],D[b]` | Page 273 |

### SH.H

**SH.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH.H` | Page 478 |

### SHA.H

**SHA.H Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SHA.H` | Page 493 |

## Address Operations Instructions

*15 instructions*

### CACHEA.I

**Cache Address,Invalidate**

**Manual Examples:**
```assembly
CACHEA.I A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0B800089` | 32-bit | `CACHEA.I A[b],off10` | Page 181 |

### CACHEA.W

**Cache Address,Writeback**

**Manual Examples:**
```assembly
CACHEA.W A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0B000089` | 32-bit | `CACHEA.W A[b],off10` | Page 187 |

### CACHEA.WI

**Cache Address,Writeback and Invalidate**

**Manual Examples:**
```assembly
CACHEA.WI A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0B400089` | 32-bit | `CACHEA.WI A[b],off10` | Page 184 |

### CACHEI.I

**Cache Index,Invalidate**

**Manual Examples:**
```assembly
CACHEI.I A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0A800089` | 32-bit | `CACHEI.I A[b],off10` | Page 201 |

### CACHEI.W

**Cache Index,Writeback**

**Manual Examples:**
```assembly
CACHEI.W A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0AC00089` | 32-bit | `CACHEI.W A[b],off10` | Page 188 |

### CACHEI.WI

**Cache Index,Writeback,Invalidate**

**Manual Examples:**
```assembly
CACHEI.WI A[1],off10
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0BC00089` | 32-bit | `CACHEI.WI A[b],off10` | Page 187 |

### CMOV

**Conditional Move (16-bit)**

**Manual Examples:**
```assembly
CMOV D[2],D[15],#3
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0xAA` | 16-bit | `CMOV D[a],D[15],const4` | Page 200 |

### CMOVN

**Conditional Move-Not (16-bit)**

**Manual Examples:**
```assembly
CMOVN D[2],D[15],#3
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0xEA` | 16-bit | `CMOVN D[a],D[15],const4` | Page 202 |

### MOV

**Move**

**Manual Examples:**
```assembly
MOV D[3],#100
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000003B` | 32-bit | `MOV D[c],const16` | Page 327 |

### MOV.A

**Move Value to Address Register**

**Manual Examples:**
```assembly
MOV.A A[3],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x06300001` | 32-bit | `MOV.A A[c],D[b]` | Page 300 |

### MOV.AA

**Move Address from Address Register**

**Manual Examples:**
```assembly
MOV.AA A[3],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000001` | 32-bit | `MOV.AA A[c],A[b]` | Page 313 |

### MOV.D

**Move Address to Data Register**

**Manual Examples:**
```assembly
MOV.D D[3],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04C00001` | 32-bit | `MOV.D D[c],A[b]` | Page 320 |

### MOV.U

**Move Unsigned**

**Manual Examples:**
```assembly
MOV.U D[3],#100
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x000000BB` | 32-bit | `MOV.U D[c],const16` | Page 311 |

### MOVH

**Move High**

**Manual Examples:**
```assembly
MOVH D[3],#100
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000007B` | 32-bit | `MOVH D[c],const16` | Page 288 |

### MOVH.A

**Move High to Address**

**Manual Examples:**
```assembly
MOVH.A A[3],#100
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000091` | 32-bit | `MOVH.A A[c],const16` | Page 290 |

## Other Instructions

*61 instructions*

### BISR

**Begin Interrupt Service Routine**

**Manual Examples:**
```assembly
BISR #5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0xAD` | 32-bit | `BISR const9` | Page 174 |

### BMERGE

**Bit Merge**

**Manual Examples:**
```assembly
BMERGE D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0010004B` | 32-bit | `BMERGE D[c],D[a],D[b]` | Page 150 |

### BSPLIT

**Bit Split**

**Manual Examples:**
```assembly
BSPLIT E[c],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0090004B` | 32-bit | `BSPLIT E[c],D[a]` | Page 170 |

### CLO

**Count Leading Ones**

**Manual Examples:**
```assembly
CLO D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01C0000F` | 32-bit | `CLO D[c],D[a]` | Page 194 |

### CLS

**Count Leading Signs**

**Manual Examples:**
```assembly
CLS D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01D0000F` | 32-bit | `CLS D[c],D[a]` | Page 196 |

### CLZ

**Count Leading Zeros**

**Manual Examples:**
```assembly
CLZ D[3],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x01B0000F` | 32-bit | `CLZ D[c],D[a]` | Page 181 |

### CMPSWAP

**CMPSWAP Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `CMPSWAP` | Page 146 |

### CMPSWAP.W

**Compare and Swap**

**Manual Examples:**
```assembly
CMPSWAP.W A[1],off10,E[a]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x08C00049` | 32-bit | `CMPSWAP.W A[b],off10,E[a]` | Page 203 |

### CRC32

**CRC32**

**Manual Examples:**
```assembly
CRC32 D[3],D[1],D[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0030004B` | 32-bit | `CRC32 D[c],D[b],D[a]` | Page 192 |

### CRC32B.W

**CRC32B.W Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `CRC32B.W` | Page 149 |

### CRC32L.W

**CRC32L.W Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `CRC32L.W` | Page 151 |

### CRCN

**CRCN Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `CRCN` | Page 153 |

### DVINIT

**Divide-Initialization Word**

**Manual Examples:**
```assembly
DVINIT.B E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x05A0004B` | 32-bit | `DVINIT.B E[c],D[a],D[b]` | Page 236 |

### DVINIT.U

**Divide-Initialization Word Unsigned**

**Manual Examples:**
```assembly
DVINIT.BU E[c],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04A0004B` | 32-bit | `DVINIT.BU E[c],D[a],D[b]` | Page 224 |

### EQ

**Equal**

**Manual Examples:**
```assembly
EQ D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0100008B` | 32-bit | `EQ D[c],D[a],const9` | Page 240 |

### EQ.A

**Equal to Address**

**Manual Examples:**
```assembly
EQ.A D[3],A[2],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04000001` | 32-bit | `EQ.A D[c],A[a],A[b]` | Page 259 |

### EQ.W

**Equal Packed Word**

**Manual Examples:**
```assembly
EQ.W D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0900000B` | 32-bit | `EQ.W D[c],D[a],D[b]` | Page 259 |

### EQZ.A

**Equal Zero Address**

**Manual Examples:**
```assembly
EQZ.A D[3],A[2]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04800001` | 32-bit | `EQZ.A D[c],A[a]` | Page 245 |

### GE

**Greater Than or Equal**

**Manual Examples:**
```assembly
GE D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0140008B` | 32-bit | `GE D[c],D[a],const9` | Page 315 |

### GE.A

**Greater Than or Equal Address**

**Manual Examples:**
```assembly
GE.A D[3],A[2],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04300001` | 32-bit | `GE.A D[c],A[a],A[b]` | Page 324 |

### GE.U

**Greater Than or Equal Unsigned**

**Manual Examples:**
```assembly
GE.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0150008B` | 32-bit | `GE.U D[c],D[a],const9` | Page 295 |

### LHA

**LHA Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `LHA` | Page 275 |

### LT

**Less Than**

**Manual Examples:**
```assembly
LT D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0120008B` | 32-bit | `LT D[c],D[a],const9` | Page 333 |

### LT.A

**Less Than Address**

**Manual Examples:**
```assembly
LT.A D[3],A[2],A[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x04200001` | 32-bit | `LT.A D[c],A[a],A[b]` | Page 348 |

### LT.U

**Less Than Unsigned**

**Manual Examples:**
```assembly
LT.U D[3],D[2],#5
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0130008B` | 32-bit | `LT.U D[c],D[a],const9` | Page 332 |

### LT.W

**Less Than Packed Word**

**Manual Examples:**
```assembly
LT.W D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0920000B` | 32-bit | `LT.W D[c],D[a],D[b]` | Page 312 |

### LT.WU

**Less Than Packed Word Unsigned**

**Manual Examples:**
```assembly
LT.WU D[3],D[2],D[1]
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0930000B` | 32-bit | `LT.WU D[c],D[a],D[b]` | Page 327 |

### MFCR

**Move From Core Register**

**Manual Examples:**
```assembly
MFCR D[3],#100
```

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x0000004D` | 32-bit | `MFCR D[c],const16` | Page 320 |

### MFDCR

**MFDCR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MFDCR` | Page 343 |

### MTCR

**MTCR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MTCR` | Page 408 |

### MTDCR

**MTDCR Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `MTDCR` | Page 409 |

### NE

**NE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NE` | Page 428 |

### NE.A

**NE.A Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NE.A` | Page 429 |

### NEZ.A

**NEZ.A Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `NEZ.A` | Page 430 |

### PACK

**PACK Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `PACK` | Page 450 |

### PARITY

**PARITY Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `PARITY` | Page 452 |

### POPCNT

**POPCNT Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `POPCNT` | Page 453 |

### REM64

**REM64 Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `REM64` | Page 454 |

### REM64.U

**REM64.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `REM64.U` | Page 455 |

### RFE

**RFE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RFE` | Page 459 |

### RFM

**RFM Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RFM` | Page 461 |

### RSLCX

**RSLCX Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `RSLCX` | Page 462 |

### SAT

**SAT Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SAT` | Page 470 |

### SEL

**SEL Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SEL` | Page 471 |

### SELN

**SELN Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SELN` | Page 472 |

### SH

**SH Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH` | Page 473 |

### SH.EQ

**SH.EQ Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH.EQ` | Page 475 |

### SH.GE

**SH.GE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH.GE` | Page 476 |

### SH.GE.U

**SH.GE.U Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH.GE.U` | Page 477 |

### SH.NE

**SH.NE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SH.NE` | Page 482 |

### SHA

**SHA Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SHA` | Page 491 |

### SHAS

**SHAS Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SHAS` | Page 495 |

### SHUFFLE

**SHUFFLE Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SHUFFLE` | Page 497 |

### SVLCX

**SVLCX Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SVLCX` | Page 534 |

### SWAP

**SWAP Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SWAP` | Page 535 |

### SWAPMSK.W

**SWAPMSK.W Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `SWAPMSK.W` | Page 538 |

### TRAPINV

**TRAPINV Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `TRAPINV` | Page 542 |

### TRAPSV

**TRAPSV Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `TRAPSV` | Page 543 |

### TRAPV

**TRAPV Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `TRAPV` | Page 544 |

### UNPACK

**UNPACK Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `UNPACK` | Page 545 |

### WAIT

**WAIT Operation**

| OpCode | Size | Syntax | Reference |
|--------|------|--------|-----------|
| `0x00000000` | 32-bit | `WAIT` | Page 547 |

---

## Appendix

### Enhanced Bit Field Support

The following instructions have enhanced bit field encoding support:

- **Enhanced Instructions**: 83 instructions with bit field data
- **Bit Field Analysis**: C, B, A, and Const field positions extracted from manual
- **Encoder Support**: Full encoding support in TASM assembler

### Manual Reference

- **Source**: Infineon TriCore TC1.8 Architecture Volume 2 User Manual
- **Examples Extracted**: 12+ real examples from instruction pages
- **Page References**: Complete page mapping for all instructions

### Generation Information

- **Generated**: November 1, 2025
- **Tool**: Comprehensive TriCore Test Generator
- **Source CSV**: tricore_1.8_instruction_set.csv
- **Total Lines**: 746 test instructions

---

*This documentation was automatically generated from manual analysis and instruction enhancement system.*\n\n## Instruction Reference Table\n\nComplete alphabetical reference of all TriCore TC1.8 instructions with manual page numbers.\n\n| Instruction | Long Name | Operands | Size | Manual Page | Syntax Example |\n|-------------|-----------|----------|------|-------------|----------------|\n| `ABS` | Absolute Value | 2 | 32-bit | 66 | `ABS D[c],D[b]` |\n| `ABS.B` | Absolute Value Packed Byte | 2 | 32-bit | 67 | `ABS.B D[c],D[b]` |\n| `ABS.H` | Absolute Value Packed Half-word | 2 | 32-bit | 68 | `ABS.H D[c],D[b]` |\n| `ABSDIF` | Absolute Value of Difference | 3 | 32-bit | 69 | `ABSDIF D[c],D[a],const9` |\n| `ABSDIF.B` | Absolute Value of Difference Packed Byte | 3 | 32-bit | 70 | `ABSDIF.B D[c],D[a],D[b]` |\n| `ABSDIF.H` | Absolute Value of Difference Packed Half... | 3 | 32-bit | 71 | `ABSDIF.H D[c],D[a],D[b]` |\n| `ABSDIFS` | Absolute Value of Difference with Satura... | 3 | 32-bit | 72 | `ABSDIFS D[c],D[a],const9` |\n| `ABSDIFS.H` | Absolute Value of Difference Packed Half... | 3 | 32-bit | 73 | `ABSDIFS.H D[c],D[a],D[b]` |\n| `ABSS` | Absolute Value with Saturation | 2 | 32-bit | 74 | `ABSS D[c],D[b]` |\n| `ABSS.H` | Absolute Value Packed Half-word with Sat... | 2 | 32-bit | 75 | `ABSS.H D[c],D[b]` |\n| `ADD` | Add | 3 | 32-bit | 76 | `ADD D[c],D[a],const9` |\n| `ADD.A` | Add Address | 3 | 32-bit | 77 | `ADD.A A[c],A[a],A[b]` |\n| `ADD.B` | Add Packed Byte | 3 | 32-bit | 78 | `ADD.B D[c],D[a],D[b]` |\n| `ADD.H` | Add Packed Half-word | 3 | 32-bit | 79 | `ADD.H D[c],D[a],D[b]` |\n| `ADDC` | Add with Carry | 3 | 32-bit | 80 | `ADDC D[c],D[a],const9` |\n| `ADDI` | Add Immediate | 3 | 32-bit | 81 | `ADDI D[c],D[a],const16 (RLC)` |\n| `ADDIH` | Add Immediate High | 3 | 32-bit | 82 | `ADDIH D[c],D[a],const16 (RLC)` |\n| `ADDIH.A` | Add Immediate High to Address | 3 | 32-bit | 83 | `ADDIH.A A[c],A[a],const16 (RLC)` |\n| `ADDS` | Add Signed with Saturation | 3 | 32-bit | 84 | `ADDS D[c],D[a],const9` |\n| `ADDS.H` | Add Signed Packed Half-word with Saturat... | 3 | 32-bit | 85 | `ADDS.H D[c],D[a],D[b]` |\n| `ADDS.HU` | Add Unsigned Packed Half-word with Satur... | 3 | 32-bit | 86 | `ADDS.HU D[c],D[a],D[b]` |\n| `ADDS.U` | Add Unsigned with Saturation | 3 | 32-bit | 87 | `ADDS.U D[c],D[a],const9` |\n| `ADDSC.A` | Add Scaled Index to Address | 4 | 32-bit | 88 | `ADDSC.A A[c],A[b],D[a],n` |\n| `ADDSC.AT` | Add Bit-Scaled Index to Address | 3 | 32-bit | 89 | `ADDSC.AT A[c],A[b],D[a]` |\n| `ADDX` | Add Extended | 3 | 32-bit | 90 | `ADDX D[c],D[a],const9` |\n| `AND` | Bitwise AND | 3 | 32-bit | 91 | `AND D[c],D[a],const9` |\n| `AND.AND.T` | Accumulating Bit Logical AND-AND | 5 | 32-bit | 93 | `AND.AND.T D[c],D[a],pos1,D[b],pos2` |\n| `AND.ANDN.T` | Accumulating Bit Logical AND-AND-Not | 5 | 32-bit | 93 | `AND.ANDN.T D[c],D[a,] pos1,D[b],pos...` |\n| `AND.EQ` | Equal Accumulating | 3 | 32-bit | 93 | `AND.EQ D[c],D[a],const9` |\n| `AND.GE` | Greater Than or Equal Accumulating | 3 | 32-bit | 94 | `AND.GE D[c],D[a],const9` |\n| `AND.GE.U` | Greater Than or Equal Accumulating Unsig... | 3 | 32-bit | 95 | `AND.GE.U D[c],D[a],const9` |\n| `AND.LT` | Less Than Accumulating | 3 | 32-bit | 92 | `AND.LT D[c],D[a],const9` |\n| `AND.LT.U` | Less Than Accumulating Unsigned | 3 | 32-bit | 93 | `AND.LT.U D[c],D[a],const9` |\n| `AND.NE` | Not Equal Accumulating | 3 | 32-bit | 92 | `AND.NE D[c],D[a],const9` |\n| `AND.NOR.T` | Accumulating Bit Logical AND-NOR | 5 | 32-bit | 93 | `AND.NOR.T D[c],D[a],pos1,D[b],pos2` |\n| `AND.OR.T` | Accumulating Bit Logical AND-OR | 5 | 32-bit | 93 | `AND.OR.T D[c],D[a],pos1,D[b],pos2` |\n| `AND.T` | Bit Logical AND | 5 | 32-bit | 92 | `AND.T D[c],D[a],pos1,D[b],pos2` |\n| `ANDN` | Bitwise AND-Not | 3 | 32-bit | 118 | `ANDN D[c],D[a],const9` |\n| `ANDN.T` | Bit Logical AND-Not | 5 | 32-bit | 106 | `ANDN.T D[c],D[a],pos1,D[b],pos2` |\n| `BISR` | Begin Interrupt Service Routine | 1 | 32-bit | 174 | `BISR const9` |\n| `BMERGE` | Bit Merge | 3 | 32-bit | 150 | `BMERGE D[c],D[a],D[b]` |\n| `BSPLIT` | Bit Split | 2 | 32-bit | 170 | `BSPLIT E[c],D[a]` |\n| `CACHEA.I` | Cache Address,Invalidate | 2 | 32-bit | 181 | `CACHEA.I A[b],off10` |\n| `CACHEA.W` | Cache Address,Writeback | 2 | 32-bit | 187 | `CACHEA.W A[b],off10` |\n| `CACHEA.WI` | Cache Address,Writeback and Invalidate | 2 | 32-bit | 184 | `CACHEA.WI A[b],off10` |\n| `CACHEI.I` | Cache Index,Invalidate | 2 | 32-bit | 201 | `CACHEI.I A[b],off10` |\n| `CACHEI.W` | Cache Index,Writeback | 2 | 32-bit | 188 | `CACHEI.W A[b],off10` |\n| `CACHEI.WI` | Cache Index,Writeback,Invalidate | 2 | 32-bit | 187 | `CACHEI.WI A[b],off10` |\n| `CADD` | Conditional Add | 4 | 32-bit | 196 | `CADD D[c],D[d],D[a],const9` |\n| `CADDN` | Conditional Add-Not | 4 | 32-bit | 204 | `CADDN D[c],D[d],D[a],const9` |\n| `CALL` | Call | 1 | 32-bit | 201 | `CALL disp24` |\n| `CALLA` | Call Absolute | 1 | 32-bit | 184 | `CALLA disp24` |\n| `CALLI` | Call Indirect | 1 | 32-bit | 196 | `CALLI A[a]` |\n| `CLO` | Count Leading Ones | 2 | 32-bit | 194 | `CLO D[c],D[a]` |\n| `CLO.H` | Count Leading Ones in Packed Half-words | 2 | 32-bit | 206 | `CLO.H D[c],D[a]` |\n| `CLS` | Count Leading Signs | 2 | 32-bit | 196 | `CLS D[c],D[a]` |\n| `CLS.H` | Count Leading Signs in Packed Half-words | 2 | 32-bit | 204 | `CLS.H D[c],D[a]` |\n| `CLZ` | Count Leading Zeros | 2 | 32-bit | 181 | `CLZ D[c],D[a]` |\n| `CLZ.H` | Count Leading Zeros in Packed Half-words | 2 | 32-bit | 185 | `CLZ.H D[c],D[a]` |\n| `CMOV` | Conditional Move (16-bit) | 3 | 16-bit | 200 | `CMOV D[a],D[15],const4` |\n| `CMOVN` | Conditional Move-Not (16-bit) | 3 | 16-bit | 202 | `CMOVN D[a],D[15],const4` |\n| `CMPSWAP` | Compare and Swap | 3 | 32-bit | 146 | `CMPSWAP.W [A[a]],D[b],D[c]` |\n| `CMPSWAP.W` | Compare and Swap | 3 | 32-bit | 203 | `CMPSWAP.W A[b],off10,E[a]` |\n| `CRC32` | CRC32 | 3 | 32-bit | 192 | `CRC32 D[c],D[b],D[a]` |\n| `CRC32.B` | CRC32 Byte | 3 | 32-bit | 148 | `CRC32.B D[c],D[a],D[b]` |\n| `CRC32B.W` | CRC32 Big-Endian Word | 3 | 32-bit | 149 | `CRC32B.W D[c],D[a],D[b]` |\n| `CRC32L.W` | CRC32 Little-Endian Word | 3 | 32-bit | 151 | `CRC32L.W D[c],D[a],D[b]` |\n| `CRCN` | CRC with Polynomial | 3 | 32-bit | 153 | `CRCN D[c],D[a],D[b]` |\n| `CSUB` | Conditional Subtract | 4 | 32-bit | 204 | `CSUB D[c],D[d],D[a],D[b]` |\n| `CSUBN` | Conditional Subtract-Not | 4 | 32-bit | 184 | `CSUBN D[c],D[d],D[a],D[b]` |\n| `DEBUG` | Debug | 0 | 16-bit | 235 | `DEBUG` |\n| `DEXTR` | Extract from Double Register | 4 | 32-bit | 211 | `DEXTR D[c],D[a],D[b],pos` |\n| `DISABLE` | Disable Interrupts | 0 | 32-bit | 234 | `DISABLE` |\n| `DIV` | Divide | 3 | 32-bit | 221 | `DIV E[c],D[a],D[b]` |\n| `DIV.U` | Divide Unsigned | 3 | 32-bit | 239 | `DIV.U E[c],D[a],D[b]` |\n| `DIV64` | Divide 64-bit | 3 | 32-bit | 166 | `DIV64 D[c],D[a],D[b]` |\n| `DIV64.U` | Divide 64-bit Unsigned | 3 | 32-bit | 168 | `DIV64.U D[c],D[a],D[b]` |\n| `DSYNC` | Synchronize Data | 0 | 32-bit | 216 | `DSYNC` |\n| `DVADJ` | Divide-Adjust | 3 | 32-bit | 221 | `DVADJ E[c],E[d],D[b]` |\n| `DVINIT` | Divide-Initialization Word | 3 | 32-bit | 236 | `DVINIT.B E[c],D[a],D[b]` |\n| `DVINIT.B` | Divide-Initialization Byte | 3 | 32-bit | 226 | `DVINIT.H E[c],D[a],D[b]` |\n| `DVINIT.BU` | Divide-Initialization Byte Unsigned | 3 | 32-bit | 221 | `DVINIT.HU E[c],D[a],D[b]` |\n| `DVINIT.H` | Divide-Initialization Half-word | 3 | 32-bit | 239 | `DVINIT E[c],D[a],D[b]` |\n| `DVINIT.HU` | Divide-Initialization Half-word Unsigned | 3 | 32-bit | 211 | `DVINIT.U E[c],D[a],D[b]` |\n| `DVINIT.U` | Divide-Initialization Word Unsigned | 3 | 32-bit | 224 | `DVINIT.BU E[c],D[a],D[b]` |\n| `DVSTEP` | Divide-Step | 3 | 32-bit | 239 | `DVSTEP E[c],E[d],D[b]` |\n| `DVSTEP.U` | Divide-Step Unsigned | 3 | 32-bit | 220 | `DVSTEP.U E[c],E[d],D[b]` |\n| `ENABLE` | Enable Interrupts | 0 | 32-bit | 241 | `ENABLE` |\n| `EQ` | Equal | 3 | 32-bit | 240 | `EQ D[c],D[a],const9` |\n| `EQ.A` | Equal to Address | 3 | 32-bit | 259 | `EQ.A D[c],A[a],A[b]` |\n| `EQ.B` | Equal Packed Byte | 3 | 32-bit | 240 | `EQ.B D[c],D[a],D[b]` |\n| `EQ.H` | Equal Packed Half-word | 3 | 32-bit | 250 | `EQ.H D[c],D[a],D[b]` |\n| `EQ.W` | Equal Packed Word | 3 | 32-bit | 259 | `EQ.W D[c],D[a],D[b]` |\n| `EQANY.B` | Equal Any Byte | 3 | 32-bit | 244 | `EQANY.B D[c],D[a],const9` |\n| `EQANY.H` | Equal Any Half-word | 3 | 32-bit | 252 | `EQANY.H D[c],D[a],const9` |\n| `EQZ.A` | Equal Zero Address | 2 | 32-bit | 245 | `EQZ.A D[c],A[a]` |\n| `EXTR` | Extract Bit Field | 4 | 32-bit | 240 | `EXTR D[c],D[a],pos,width` |\n| `EXTR.U` | Extract Bit Field Unsigned | 4 | 32-bit | 243 | `EXTR.U D[c],D[a],pos,width` |\n| `FCALL` | Fast Call | 1 | 32-bit | 354 | `FCALL disp24` |\n| `FCALLA` | Fast Call Absolute | 1 | 32-bit | 359 | `FCALLA disp24` |\n| `FCALLI` | Fast Call Indirect | 1 | 32-bit | 264 | `FCALLI A[a]` |\n| `FRET` | Return from Fast Call | 0 | 16-bit | 291 | `FRET` |\n| `GE` | Greater Than or Equal | 3 | 32-bit | 315 | `GE D[c],D[a],const9` |\n| `GE.A` | Greater Than or Equal Address | 3 | 32-bit | 324 | `GE.A D[c],A[a],A[b]` |\n| `GE.U` | Greater Than or Equal Unsigned | 3 | 32-bit | 295 | `GE.U D[c],D[a],const9` |\n| `IMASK` | Insert Mask | 4 | 32-bit | 280 | `IMASK E[c],const4,pos,width` |\n| `INS.T` | Insert Bit | 5 | 32-bit | 325 | `INS.T D[c],D[a],pos1,D[b],pos2` |\n| `INSERT` | Insert Bit Field | 5 | 32-bit | 357 | `INSERT D[c],D[a],const4,pos,width` |\n| `INSN.T` | Insert Bit-Not | 5 | 32-bit | 317 | `INSN.T D[c],D[a],pos1,D[b],pos2` |\n| `ISYNC` | Synchronize Instructions | 0 | 32-bit | 269 | `ISYNC` |\n| `IXMAX` | Find Maximum Index | 3 | 32-bit | 274 | `IXMAX E[c],E[d],D[b]` |\n| `IXMAX.U` | Find Maximum Index (unsigned) | 3 | 32-bit | 308 | `IXMAX.U E[c],E[d],D[b]` |\n| `IXMIN` | Find Minimum Index | 3 | 32-bit | 279 | `IXMIN E[c],E[d],D[b]` |\n| `IXMIN.U` | Find Minimum Index (unsigned) | 3 | 32-bit | 289 | `IXMIN.U E[c],E[d],D[b]` |\n| `J` | Jump Unconditional | 1 | 32-bit | 314 | `J disp24` |\n| `JA` | Jump Unconditional Absolute | 1 | 32-bit | 324 | `JA disp24` |\n| `JEQ` | Jump if Equal | 3 | 32-bit | 322 | `JEQ D[a],const4,disp15` |\n| `JEQ.A` | Jump if Equal Address | 3 | 32-bit | 291 | `JEQ.A A[a],A[b],disp15` |\n| `JGE` | Jump if Greater Than or Equal | 3 | 32-bit | 289 | `JGE D[a],const4,disp15` |\n| `JGE.U` | Jump if Greater Than or Equal Unsigned | 3 | 32-bit | 294 | `JGE.U D[a],const4,disp15` |\n| `JGEZ` | Jump if Greater Than or Equal to Zero (1... | 2 | 16-bit | 302 | `JGEZ D[b],disp4` |\n| `JGTZ` | Jump if Greater Than Zero (16-bit) | 2 | 16-bit | 312 | `JGTZ D[b],disp4` |\n| `JI` | Jump Indirect | 1 | 32-bit | 356 | `JI A[a]` |\n| `JL` | Jump and Link | 1 | 32-bit | 309 | `JL disp24` |\n| `JLA` | Jump and Link Absolute | 1 | 32-bit | 304 | `JLA disp24` |\n| `JLEZ` | Jump if Less Than or Equal to Zero (16-b... | 2 | 16-bit | 301 | `JLEZ D[b],disp4` |\n| `JLI` | Jump and Link Indirect | 1 | 32-bit | 272 | `JLI A[a]` |\n| `JLT` | Jump if Less Than | 3 | 32-bit | 284 | `JLT D[a],const4,disp15` |\n| `JLT.U` | Jump if Less Than Unsigned | 3 | 32-bit | 274 | `JLT.U D[a],const4,disp15` |\n| `JLTZ` | Jump if Less Than Zero (16-bit) | 2 | 16-bit | 341 | `JLTZ D[b],disp4` |\n| `JNE` | Jump if Not Equal | 3 | 32-bit | 304 | `JNE D[a],const4,disp15` |\n| `JNE.A` | Jump if Not Equal Address | 3 | 32-bit | 296 | `JNE.A A[a],A[b],disp15` |\n| `JNED` | Jump if Not Equal and Decrement | 3 | 32-bit | 357 | `JNED D[a],const4,disp15` |\n| `JNEI` | Jump if Not Equal and Increment | 3 | 32-bit | 310 | `JNEI D[a],const4,disp15` |\n| `JNZ` | Jump if Not Equal to Zero (16-bit) | 2 | 16-bit | 337 | `JNZ D[15],disp8` |\n| `JNZ.A` | Jump if Not Equal to Zero Address | 2 | 32-bit | 337 | `JNZ.A A[a],disp15` |\n| `JNZ.T` | Jump if Not Equal to Zero Bit | 3 | 32-bit | 271 | `JNZ.T D[a],n,disp15` |\n| `JRI` | Jump Register Indirect | 1 | 32-bit | 241 | `JRI A[a]` |\n| `JZ` | Jump if Zero (16-bit) | 2 | 16-bit | 263 | `JZ D[15],disp8` |\n| `JZ.A` | Jump if Zero Address | 2 | 32-bit | 260 | `JZ.A A[a],disp15` |\n| `JZ.T` | Jump if Zero Bit | 3 | 32-bit | 269 | `JZ.T D[a],n,disp15` |\n| `LD.A` | Load Word to Address Register | 2 | 32-bit | 320 | `LD.A A[a],off18` |\n| `LD.B` | Load Byte | 2 | 32-bit | 276 | `LD.B D[a],off18` |\n| `LD.BU` | Load Byte Unsigned | 2 | 32-bit | 290 | `LD.BU D[a],off18` |\n| `LD.D` | Load Double-word | 2 | 32-bit | 267 | `LD.D E[a],off18` |\n| `LD.DA` | Load Double-word to Address Register | 2 | 32-bit | 347 | `LD.DA P[a],off18` |\n| `LD.DD` | Load Double Data Register | 2 | 32-bit | 258 | `LD.DD E[c],[A[a]]` |\n| `LD.H` | Load Half-word | 2 | 32-bit | 308 | `LD.H D[a],off18` |\n| `LD.HU` | Load Half-word Unsigned | 2 | 32-bit | 295 | `LD.HU D[a],off18` |\n| `LD.Q` | Load Half-word Signed Fraction | 2 | 32-bit | 307 | `LD.Q D[a],off18` |\n| `LD.W` | Load Word | 2 | 32-bit | 284 | `LD.W D[a],off18` |\n| `LDLCX` | Load Lower Context | 1 | 32-bit | 352 | `LDLCX [A[a]]` |\n| `LDMST` | Load-Modify-Store | 2 | 32-bit | 346 | `LDMST off18,E[a]` |\n| `LDUCX` | Load Upper Context | 1 | 32-bit | 293 | `LDUCX off18` |\n| `LEA` | Load Effective Address | 2 | 32-bit | 269 | `LEA A[a],off18` |\n| `LHA` | Load Half-word Arithmetic | 2 | 32-bit | 275 | `LHA D[c],[A[a]]` |\n| `LOOP` | Loop | 2 | 32-bit | 294 | `LOOP A[b],disp15` |\n| `LOOPU` | Loop Unconditional | 1 | 32-bit | 356 | `LOOPU disp15` |\n| `LSYNC` | Load Synchronize | 0 | 32-bit | 278 | `LSYNC` |\n| `LT` | Less Than | 3 | 32-bit | 333 | `LT D[c],D[a],const9` |\n| `LT.A` | Less Than Address | 3 | 32-bit | 348 | `LT.A D[c],A[a],A[b]` |\n| `LT.B` | Less Than Packed Byte | 3 | 32-bit | 318 | `LT.B D[c],D[a],D[b]` |\n| `LT.BU` | Less Than Packed Byte Unsigned | 3 | 32-bit | 310 | `LT.BU D[c],D[a],D[b]` |\n| `LT.H` | Less Than Packed Half-word | 3 | 32-bit | 321 | `LT.H D[c],D[a],D[b]` |\n| `LT.HU` | Less Than Packed Half-word Unsigned | 3 | 32-bit | 273 | `LT.HU D[c],D[a],D[b]` |\n| `LT.U` | Less Than Unsigned | 3 | 32-bit | 332 | `LT.U D[c],D[a],const9` |\n| `LT.W` | Less Than Packed Word | 3 | 32-bit | 312 | `LT.W D[c],D[a],D[b]` |\n| `LT.WU` | Less Than Packed Word Unsigned | 3 | 32-bit | 327 | `LT.WU D[c],D[a],D[b]` |\n| `MADD` | Multiply-Add | 4 | 32-bit | 282 | `MADD D[c],D[d],D[a],const9` |\n| `MADD.H` | Packed Multiply-Add Q Format | 5 | 32-bit | 347 | `MADD.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADD.Q` | Multiply-Add Q Format | 5 | 32-bit | 322 | `MADD.Q D[c],D[d],D[a],D[b],n` |\n| `MADD.U` | Multiply-Add Unsigned | 4 | 32-bit | 288 | `MADD.U E[c],E[d],D[a],const9` |\n| `MADDM.H` | Packed Multiply-Add Q Format Multi-preci... | 5 | 32-bit | 348 | `MADDM.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDMS.H` | Packed Multiply-Add Q Format Multi-preci... | 5 | 32-bit | 310 | `MADDMS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDR.H` | Packed Multiply-Add Q Format with Roundi... | 5 | 32-bit | 287 | `MADDR.H D[c],D[d],D[a],D[b] LL,n` |\n| `MADDR.Q` | Multiply-Add Q Format with Rounding | 5 | 32-bit | 263 | `MADDR.Q D[c],D[d],D[a] L,D[b] L,n` |\n| `MADDRS.H` | Packed Multiply-Add Q Format with Roundi... | 5 | 32-bit | 299 | `MADDRS.H D[c],D[d],D[a],D[b] LL,n` |\n| `MADDRS.Q` | Multiply-Add Q Format with Rounding,Satu... | 5 | 32-bit | 275 | `MADDRS.Q D[c],D[d],D[a] L,D[b] L,n` |\n| `MADDS` | Multiply-Add,Saturated | 4 | 32-bit | 314 | `MADDS D[c],D[d],D[a],const9` |\n| `MADDS.H` | Packed Multiply-Add Q Format,Saturated | 5 | 32-bit | 317 | `MADDS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDS.Q` | Multiply-Add Q Format,Saturated | 5 | 32-bit | 265 | `MADDS.Q D[c],D[d],D[a],D[b],n` |\n| `MADDS.U` | Multiply-Add Unsigned,Saturated | 4 | 32-bit | 336 | `MADDS.U D[c],D[d],D[a],const9` |\n| `MADDSU.H` | Packed Multiply-Add/Subtract Q Format | 5 | 32-bit | 300 | `MADDSU.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDSUM.H` | Packed Multiply-Add/Subtract Q Format Mu... | 5 | 32-bit | 290 | `MADDSUM.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDSUMS.H` | Packed Multiply-Add/Subtract Q Format Mu... | 5 | 32-bit | 354 | `MADDSUMS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MADDSUR.H` | Packed Multiply-Add/Subtract Q Format wi... | 5 | 32-bit | 269 | `MADDSUR.H D[c],D[d],D[a],D[b] LL,n` |\n| `MADDSURS.H` | Packed Multiply-Add/Subtract Q Format wi... | 5 | 32-bit | 260 | `MADDSURS.H D[c],D[d],D[a],D[b] LL,n` |\n| `MADDSUS.H` | Packed Multiply-Add/Subtract Q Format Sa... | 5 | 32-bit | 286 | `MADDSUS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MAX` | Maximum Value | 3 | 32-bit | 336 | `MAX D[c],D[a],const9` |\n| `MAX.B` | Maximum Value Packed Byte | 3 | 32-bit | 350 | `MAX.B D[c],D[a],D[b]` |\n| `MAX.BU` | Maximum Value Packed Byte Unsigned | 3 | 32-bit | 320 | `MAX.BU D[c],D[a],D[b]` |\n| `MAX.H` | Maximum Value Packed Half-word | 3 | 32-bit | 359 | `MAX.H D[c],D[a],D[b]` |\n| `MAX.HU` | Maximum Value Packed Half-word Unsigned | 3 | 32-bit | 267 | `MAX.HU D[c],D[a],D[b]` |\n| `MAX.U` | Maximum Value Unsigned | 3 | 32-bit | 321 | `MAX.U D[c],D[a],const9` |\n| `MFCR` | Move From Core Register | 2 | 32-bit | 320 | `MFCR D[c],const16` |\n| `MFDCR` | Move from Debug Core Register | 2 | 32-bit | N/A | `MFDCR D[c],const16` |\n| `MIN` | Minimum Value | 3 | 32-bit | 336 | `MIN D[c],D[a],const9` |\n| `MIN.B` | Minimum Value Packed Byte | 3 | 32-bit | 263 | `MIN.B D[c],D[a],D[b]` |\n| `MIN.BU` | Minimum Value Packed Byte Unsigned | 3 | 32-bit | 286 | `MIN.BU D[c],D[a],D[b]` |\n| `MIN.H` | Minimum Value Packed Half-word | 3 | 32-bit | 328 | `MIN.H D[c],D[a],D[b]` |\n| `MIN.HU` | Minimum Value Packed Half-word Unsigned | 3 | 32-bit | 307 | `MIN.HU D[c],D[a],D[b]` |\n| `MIN.U` | Minimum Value Unsigned | 3 | 32-bit | 312 | `MIN.U D[c],D[a],const9` |\n| `MOV` | Move | 2 | 32-bit | 327 | `MOV D[c],const16` |\n| `MOV.A` | Move Value to Address Register | 2 | 32-bit | 300 | `MOV.A A[c],D[b]` |\n| `MOV.AA` | Move Address from Address Register | 2 | 32-bit | 313 | `MOV.AA A[c],A[b]` |\n| `MOV.D` | Move Address to Data Register | 2 | 32-bit | 320 | `MOV.D D[c],A[b]` |\n| `MOV.U` | Move Unsigned | 2 | 32-bit | 311 | `MOV.U D[c],const16` |\n| `MOVH` | Move High | 2 | 32-bit | 288 | `MOVH D[c],const16` |\n| `MOVH.A` | Move High to Address | 2 | 32-bit | 290 | `MOVH.A A[c],const16` |\n| `MSUB` | Multiply-Subtract | 4 | 32-bit | 326 | `MSUB D[c],D[d],D[a],const9` |\n| `MSUB.H` | Packed Multiply-Subtract Q Format | 5 | 32-bit | 300 | `MSUB.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUB.Q` | Multiply-Subtract Q Format | 5 | 32-bit | 277 | `MSUB.Q D[c],D[d],D[a],D[b],n` |\n| `MSUB.U` | Multiply-Subtract Unsigned | 4 | 32-bit | 333 | `MSUB.U E[c],E[d],D[a],const9` |\n| `MSUBAD.H` | Packed Multiply-Subtract/Add Q Format | 5 | 32-bit | 278 | `MSUBAD.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUBADM.H` | Packed Multiply-Subtract/Add Q Format-Mu... | 5 | 32-bit | 313 | `MSUBADM.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUBADMS.H` | Packed Multiply-Subtract/Add Q Format-Mu... | 5 | 32-bit | 319 | `MSUBADMS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUBADR.H` | MSUBADR.H Operation | 4 | 32-bit | 388 | `MSUBADR.H D[c],D[a],D[b],const1` |\n| `MSUBADRS.H` | MSUBADRS.H Operation | 4 | 32-bit | 391 | `MSUBADRS.H D[c],D[a],D[b],const1` |\n| `MSUBADS.H` | Packed Multiply-Subtract/Add Q Format,Sa... | 5 | 32-bit | 294 | `MSUBADS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUBM.H` | MSUBM.H Operation | 4 | 32-bit | 394 | `MSUBM.H D[c],D[a],D[b],const1` |\n| `MSUBMS.H` | MSUBMS.H Operation | 4 | 32-bit | 396 | `MSUBMS.H D[c],D[a],D[b],const1` |\n| `MSUBR.H` | MSUBR.H Operation | 4 | 32-bit | 398 | `MSUBR.H D[c],D[a],D[b],const1` |\n| `MSUBR.Q` | MSUBR.Q Operation | 4 | 32-bit | 404 | `MSUBR.Q D[c],D[a],D[b],const1` |\n| `MSUBRS.H` | MSUBRS.H Operation | 4 | 32-bit | 401 | `MSUBRS.H D[c],D[a],D[b],const1` |\n| `MSUBRS.Q` | MSUBRS.Q Operation | 4 | 32-bit | 406 | `MSUBRS.Q D[c],D[a],D[b],const1` |\n| `MSUBS` | Multiply-Subtract,Saturated | 4 | 32-bit | 291 | `MSUBS D[c],D[d],D[a],const9` |\n| `MSUBS.H` | Packed Multiply-Subtract Q Format,Satura... | 5 | 32-bit | 272 | `MSUBS.H E[c],E[d],D[a],D[b] LL,n` |\n| `MSUBS.Q` | Multiply-Subtract Q Format,Saturated | 5 | 32-bit | 329 | `MSUBS.Q D[c],D[d],D[a],D[b],n` |\n| `MSUBS.U` | Multiply-Subtract Unsigned,Saturated | 4 | 32-bit | 336 | `MSUBS.U D[c],D[d],D[a],const9` |\n| `MTCR` | Move to Core Register | 2 | 32-bit | N/A | `MTCR const16,D[a]` |\n| `MTDCR` | Move to Debug Core Register | 2 | 32-bit | N/A | `MTDCR const16,D[a]` |\n| `MUL` | Multiply | 3 | 32-bit | N/A | `MUL D[c],D[a],D[b]` |\n| `MUL.H` | Multiply Packed Half-word | 4 | 32-bit | N/A | `MUL.H D[c],D[a],D[b],const1` |\n| `MUL.Q` | Multiply Q-format | 4 | 32-bit | N/A | `MUL.Q D[c],D[a],D[b],const1` |\n| `MUL.U` | Multiply Unsigned | 3 | 32-bit | N/A | `MUL.U E[c],D[a],D[b]` |\n| `MULM.H` | MULM.H Operation | 4 | 32-bit | 420 | `MULM.H D[c],D[a],D[b],const1` |\n| `MULP` | MULP Operation | 3 | 32-bit | 422 | `MULP E[c],D[a],D[b]` |\n| `MULR.H` | MULR.H Operation | 4 | 32-bit | 423 | `MULR.H D[c],D[a],D[b],const1` |\n| `MULR.Q` | MULR.Q Operation | 4 | 32-bit | 425 | `MULR.Q D[c],D[a],D[b],const1` |\n| `MULS` | MULS Operation | 3 | 32-bit | 412 | `MULS D[c],D[a],D[b]` |\n| `MULS.U` | MULS.U Operation | 3 | 32-bit | 419 | `MULS.U D[c],D[a],D[b]` |\n| `NAND` | Bitwise NAND | 3 | 32-bit | N/A | `NAND D[c],D[a],D[b]` |\n| `NE` | Not Equal | 3 | 32-bit | N/A | `NE D[c],D[a],D[b]` |\n| `NE.A` | Not Equal Address | 3 | 32-bit | N/A | `NE.A D[c],A[a],A[b]` |\n| `NEZ.A` | Not Equal Zero Address | 2 | 32-bit | N/A | `NEZ.A D[c],A[a]` |\n| `NOP` | No Operation | 0 | 32-bit | N/A | `NOP` |\n| `NOR` | Bitwise NOR | 3 | 32-bit | N/A | `NOR D[c],D[a],D[b]` |\n| `NOT` | Bitwise NOT | 2 | 32-bit | N/A | `NOT D[c],D[b]` |\n| `OR` | Bitwise OR Immediate | 3 | 32-bit | N/A | `OR D[c],D[a],const9` |\n| `OR` | Bitwise OR | 3 | 32-bit | N/A | `OR D[c],D[a],D[b]` |\n| `OR.EQ` | OR.EQ Operation | 3 | 32-bit | 441 | `OR.EQ D[c],D[a],D[b]` |\n| `OR.GE` | OR.GE Operation | 3 | 32-bit | 442 | `OR.GE D[c],D[a],D[b]` |\n| `OR.GE.U` | OR.GE.U Operation | 3 | 32-bit | 443 | `OR.GE.U D[c],D[a],D[b]` |\n| `OR.NE` | OR.NE Operation | 3 | 32-bit | 446 | `OR.NE D[c],D[a],D[b]` |\n| `ORN` | OR-Not | 3 | 32-bit | N/A | `ORN D[c],D[a],D[b]` |\n| `PACK` | Pack | 3 | 32-bit | N/A | `PACK D[c],D[a],D[b]` |\n| `PARITY` | Calculate Parity | 2 | 32-bit | N/A | `PARITY D[c],D[a]` |\n| `POPCNT` | Population Count | 2 | 32-bit | N/A | `POPCNT D[c],D[a]` |\n| `REM64` | Remainder 64-bit | 3 | 32-bit | 454 | `REM64 D[c],D[a],D[b]` |\n| `REM64.U` | Remainder 64-bit Unsigned | 3 | 32-bit | 455 | `REM64.U D[c],D[a],D[b]` |\n| `RESTORE` | Restore Context | 1 | 32-bit | N/A | `RESTORE const9` |\n| `RET` | Return | 0 | 32-bit | N/A | `RET` |\n| `RFE` | Return from Exception | 0 | 32-bit | N/A | `RFE` |\n| `RFM` | Return from Monitor | 0 | 32-bit | N/A | `RFM` |\n| `RSLCX` | Restore Lower Context | 0 | 32-bit | N/A | `RSLCX` |\n| `RSTV` | Reset Overflow Flag | 0 | 32-bit | 463 | `RSTV` |\n| `RSUB` | Reverse Subtract | 3 | 32-bit | 464 | `RSUB D[c],D[a],const9` |\n| `RSUBS` | Reverse Subtract with Saturation | 3 | 32-bit | 465 | `RSUBS D[c],D[a],const9` |\n| `RSUBS.U` | Reverse Subtract Unsigned with Saturatio... | 3 | 32-bit | 466 | `RSUBS.U D[c],D[a],const9` |\n| `SAT` | Saturate | 2 | 32-bit | 470 | `SAT.B D[c],D[a]` |\n| `SEL` | Select | 4 | 32-bit | N/A | `SEL D[c],D[a],D[b],pos1` |\n| `SELN` | Select Not | 4 | 32-bit | N/A | `SELN D[c],D[a],D[b],pos1` |\n| `SH` | Shift Left/Right | 3 | 32-bit | N/A | `SH D[c],D[a],const9` |\n| `SH` | Shift by Register | 3 | 32-bit | N/A | `SH D[c],D[a],D[b]` |\n| `SH.EQ` | Shift if Equal | 3 | 32-bit | N/A | `SH.EQ D[c],D[a],const9` |\n| `SH.GE` | Shift if Greater or Equal | 3 | 32-bit | N/A | `SH.GE D[c],D[a],const9` |\n| `SH.GE.U` | Shift if Greater or Equal Unsigned | 3 | 32-bit | N/A | `SH.GE.U D[c],D[a],const9` |\n| `SH.H` | Shift Packed Half-word | 3 | 32-bit | N/A | `SH.H D[c],D[a],const9` |\n| `SH.NE` | Shift if Not Equal | 3 | 32-bit | N/A | `SH.NE D[c],D[a],const9` |\n| `SHA` | Shift Arithmetic | 3 | 32-bit | N/A | `SHA D[c],D[a],const9` |\n| `SHA` | Shift Arithmetic by Register | 3 | 32-bit | N/A | `SHA D[c],D[a],D[b]` |\n| `SHA.H` | Shift Arithmetic Packed Half-word | 3 | 32-bit | N/A | `SHA.H D[c],D[a],const9` |\n| `SHAS` | Shift Arithmetic with Saturation | 3 | 32-bit | N/A | `SHAS D[c],D[a],const9` |\n| `SHUFFLE` | Shuffle | 3 | 32-bit | 497 | `SHUFFLE D[c],D[a],const9` |\n| `ST` | Store Byte | 2 | 32-bit | N/A | `ST.W [A[a]],D[b]` |\n| `ST` | Store Half-word | 2 | 32-bit | N/A | `ST.W [A[a]],D[b]` |\n| `ST` | Store Word | 2 | 32-bit | N/A | `ST.W [A[a]],D[b]` |\n| `STLCX` | Store Lower Context | 1 | 32-bit | N/A | `STLCX [A[a]]` |\n| `STUCX` | Store Upper Context | 1 | 32-bit | 522 | `STUCX [A[a]]` |\n| `SUB` | Subtract Immediate | 3 | 32-bit | N/A | `SUB D[c],D[a],const9` |\n| `SUB` | Subtract | 3 | 32-bit | N/A | `SUB D[c],D[a],D[b]` |\n| `SUB.A` | Subtract Address | 3 | 32-bit | N/A | `SUB.A A[c],A[a],A[b]` |\n| `SUB.B` | Subtract Packed Byte | 3 | 32-bit | N/A | `SUB.B D[c],D[a],D[b]` |\n| `SUB.H` | Subtract Packed Half-word | 3 | 32-bit | N/A | `SUB.H D[c],D[a],D[b]` |\n| `SUBC` | SUBC Operation | 3 | 32-bit | 528 | `SUBC D[c],D[a],D[b]` |\n| `SUBS` | SUBS Operation | 3 | 32-bit | 529 | `SUBS D[c],D[a],D[b]` |\n| `SUBS.H` | SUBS.H Operation | 3 | 32-bit | 531 | `SUBS.H D[c],D[a],D[b]` |\n| `SUBS.HU` | SUBS.HU Operation | 3 | 32-bit | 532 | `SUBS.HU D[c],D[a],D[b]` |\n| `SUBS.U` | SUBS.U Operation | 3 | 32-bit | 530 | `SUBS.U D[c],D[a],D[b]` |\n| `SUBX` | SUBX Operation | 3 | 32-bit | 533 | `SUBX D[c],D[a],D[b]` |\n| `SVLCX` | Save Lower Context | 1 | 32-bit | N/A | `SVLCX [A[a]]` |\n| `SWAP` | Swap Word | 2 | 32-bit | N/A | `SWAP.W [A[a]],D[b]` |\n| `SWAPMSK.W` | Swap Masked Word | 3 | 32-bit | 538 | `SWAPMSK.W [A[a]],D[b],D[c]` |\n| `SYSCALL` | System Call | 1 | 32-bit | N/A | `SYSCALL const9` |\n| `TRAPINV` | Trap on Invalid Operation | 0 | 32-bit | 542 | `TRAPINV` |\n| `TRAPSV` | Trap on Signed Overflow | 0 | 32-bit | 543 | `TRAPSV` |\n| `TRAPV` | Trap on Overflow | 0 | 32-bit | 544 | `TRAPV` |\n| `UNPACK` | Unpack | 2 | 32-bit | N/A | `UNPACK D[c],D[a]` |\n| `WAIT` | Wait for Interrupt | 0 | 32-bit | N/A | `WAIT` |\n| `XNOR` | Exclusive NOR | 3 | 32-bit | N/A | `XNOR D[c],D[a],D[b]` |\n| `XOR` | Bitwise Exclusive OR | 3 | 32-bit | N/A | `XOR D[c],D[a],D[b]` |\n| `XOR` | Bitwise XOR Immediate | 3 | 32-bit | N/A | `XOR D[c],D[a],const9` |\n| `XOR.EQ` | XOR.EQ Operation | 3 | 32-bit | 551 | `XOR.EQ D[c],D[a],D[b]` |\n| `XOR.GE` | XOR.GE Operation | 3 | 32-bit | 552 | `XOR.GE D[c],D[a],D[b]` |\n| `XOR.GE.U` | XOR.GE.U Operation | 3 | 32-bit | 553 | `XOR.GE.U D[c],D[a],D[b]` |\n| `XOR.NE` | XOR.NE Operation | 3 | 32-bit | 556 | `XOR.NE D[c],D[a],D[b]` |\n\n*Total: 316 instructions*\n