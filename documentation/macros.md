# TASM Macro System - Complete Guide

## Table of Contents

1. [Overview](#overview)
2. [TASM Pipeline](#tasm-pipeline)
3. [Basic Macro Concepts](#basic-macro-concepts)
4. [Advanced Features](#advanced-features)
5. [C-Like Control Structures](#c-like-control-structures)
6. [Complete Macro Reference](#complete-macro-reference)
7. [Testing](#testing)
8. [Technical Implementation](#technical-implementation)
9. [Limitations and Best Practices](#limitations-and-best-practices)

---

## Overview

The TASM (TriCore Assembler System) includes a powerful **macro expander** that processes macro definitions and expansions before assembly. The system supports:

- **Simple constant macros** for named values
- **Parameterized macros** for code templates
- **Multi-statement macros** using pipe (`|`) separation
- **Token concatenation** with `##` operator
- **Unique label generation** with `__COUNTER__` special token
- **C-like control structures** (FOR, WHILE, DO-WHILE, SWITCH/CASE)

---

## TASM Pipeline

```
Source Code → Macro Expansion → Assembly → Linking → Binary
     ↓              ↓              ↓          ↓         ↓
  .asm with       Expanded       Machine    Resolved   Final
   macros          .asm          opcodes   addresses  executable
```

### Command-Line Usage

```bash
# Using macro files
python src/TASM.py -m data/macros/C_instructions.asm your_file.asm

# Multiple macro files
python src/TASM.py -m macros/system.asm -m macros/math.asm your_file.asm

# Disable macro expansion
python src/TASM.py --no-macros your_file.asm
```

---

## Basic Macro Concepts

### 1. Simple Constant Macros (Object-Like)

Macros without parameters that define named constants.

**Definition:**
```asm
#define BUFFER_SIZE 0x2000
#define LOOP_COUNT 32
#define STATUS_REG d15
```

**Usage & Expansion:**
```asm
; Original code:
mov     a14, #BUFFER_SIZE

; Expands to:
mov     a14, #0x2000
```

### 2. Parameterized Macros (Function-Like)

Macros with parameters that act as code templates.

**Definition:**
```asm
#define SET_VALUE(reg, val) mov reg, #val
#define ZERO_REG(reg) mov reg, #0
#define MOVE_REG(dest, src) mov dest, src
```

**Usage & Expansion:**
```asm
; Original code:
SET_VALUE(d0, 42)
ZERO_REG(d1)
MOVE_REG(d7, d4)

; Expands to:
mov d0, #42
mov d1, #0
mov d7, d4
```

### 3. Zero-Parameter Function-Like Macros

Macros defined with empty parentheses.

**Definition:**
```asm
#define NOP_PAIR() nop | nop
#define ENABLE_INTERRUPTS() enable
```

**Usage:**
```asm
NOP_PAIR()
ENABLE_INTERRUPTS()
```

---

## Advanced Features

### 1. Multi-Statement Macros with Pipe (`|`)

The pipe character separates statements that should expand to multiple lines.

**Definition:**
```asm
#define PUSH_TWO(r1, r2) st.w [a10+], r1 | st.w [a10+], r2
#define INIT_PAIR(r1, r2, v1, v2) mov r1, v1 | mov r2, v2
```

**Expansion:**
```asm
; Original:
PUSH_TWO(d0, d1)

; Expands to:
st.w [a10+], d0
st.w [a10+], d1
```

### 2. Token Concatenation with `##`

The `##` operator concatenates adjacent tokens, enabling dynamic identifier generation.

**Definition:**
```asm
#define MAKE_LABEL(prefix) prefix##_label
#define REG_NAME(num) d##num
```

**Expansion:**
```asm
; Original:
MAKE_LABEL(loop)

; Expands to:
loop_label
```

### 3. Special Token: `__COUNTER__`

A unique incrementing counter for each macro invocation, perfect for generating unique labels.

**Definition:**
```asm
#define UNIQUE_LABEL() label_##__COUNTER__:
#define FOR(counter, count) mov counter, count | for_loop_##__COUNTER__:
#define ENDFOR(counter) loop counter, for_loop_##__COUNTER__
```

**Expansion:**
```asm
; Original:
FOR(d4, #5)
    add d0, d0, d4
ENDFOR(d4)
FOR(d5, #3)
    add d1, d1, d5
ENDFOR(d5)

; Expands to:
mov d4, #5
for_loop_1:
    add d0, d0, d4
loop d4, for_loop_2
mov d5, #3
for_loop_3:
    add d1, d1, d5
loop d5, for_loop_4
```

**Note:** Each macro invocation increments the counter, so paired macros (like FOR/ENDFOR) get different counter values.

---

## C-Like Control Structures

The macro library (`data/macros/C_instructions.asm`) provides familiar C-style control flow.

### FOR Loops

#### Block-Style FOR Loop

**Syntax:**
```asm
FOR(counter, count)
    ; loop body
ENDFOR(counter)
```

**Example:**
```asm
mov     d0, #0              ; sum = 0
FOR(d4, #10)
    add d0, d0, d4          ; sum += i
ENDFOR(d4)
; Result: d0 = 55 (sum of 1..10)
```

**C Equivalent:**
```c
for(int i = count; i > 0; i--) {
    // loop body
}
```

#### Inline FOR Loop

**Syntax:**
```asm
FOR_INLINE(counter, count, init_code, loop_code)
```

**Example:**
```asm
; Using quoted strings for code with commas
FOR_INLINE(d4, #5, 'mov d0, #0', 'add d0, d0, d4')
; Result: d0 = 15 (5+4+3+2+1)
```

**Note:** Use single quotes `'...'` or double quotes `"..."` around code blocks that contain commas. Without quotes, commas are treated as parameter separators.

### WHILE Loops

#### Block-Style WHILE Loop

**Syntax:**
```asm
WHILE(condition_reg, value)
    ; loop body
ENDWHILE(condition_reg, value)
```

**Example:**
```asm
mov     d2, #0              ; condition
mov     d0, #0              ; counter
WHILE(d2, #0)
    add d0, d0, #1
    mov d2, #1              ; exit after one iteration
ENDWHILE(d2, #0)
```

**C Equivalent:**
```c
while(reg == value) {
    // loop body
}
```

#### Inline WHILE Loop

**Syntax:**
```asm
WHILE_INLINE(condition_reg, condition_value, loop_code)
```

**Example:**
```asm
mov     d2, #0
WHILE_INLINE(d2, #0, 'add d0, d0, #1')
```

**Note:** Use quoted strings for code with commas.

### DO-WHILE Loops

#### Block-Style DO-WHILE Loop

**Syntax:**
```asm
DO_WHILE()
    ; loop body
LOOP_WHILE(condition_reg, value)
```

**Example:**
```asm
mov     d2, #5              ; initial non-zero
mov     d0, #0              ; counter
DO_WHILE()
    add d0, d0, #1          ; executes at least once
    mov d2, #0              ; set exit condition
LOOP_WHILE(d2, #0)
; Result: d0 = 1
```

**C Equivalent:**
```c
do {
    // loop body
} while(reg == value);
```

#### Inline DO-WHILE Loop

**Syntax:**
```asm
DO_WHILE_INLINE(loop_code, condition_reg, condition_value)
```

**Example:**
```asm
mov     d2, #0
DO_WHILE_INLINE(add d0, d0, #1, d2, #0)
; Executes once, d0 = 1
```

### SWITCH/CASE Statements

**Syntax:**
```asm
SWITCH(switch_reg)
CASE(switch_reg, value)
    ; case body
CASE(switch_reg, value)
    ; case body
DEFAULT()
    ; default body
ENDSWITCH()
```

**Example:**
```asm
mov     d2, #1              ; switch value
mov     d3, #0              ; result
SWITCH(d2)
CASE(d2, #0)
    mov d3, #10             ; case 0
CASE(d2, #1)
    mov d3, #20             ; case 1
CASE(d2, #2)
    mov d3, #30             ; case 2
DEFAULT()
    mov d3, #99             ; default
ENDSWITCH()
; Result: d3 = 20 (case 1 matched)
```

**C Equivalent:**
```c
switch(reg) {
    case 0: d3 = 10; break;
    case 1: d3 = 20; break;
    case 2: d3 = 30; break;
    default: d3 = 99;
}
```

### Conditional Statements

**Available Conditionals:**
- `IF(reg, value, code)` - If equal
- `IF_ELSE(reg, value, true_code, false_code)` - If-else
- `IF_GT(reg, value, code)` - If greater than
- `IF_LT(reg, value, code)` - If less than
- `IF_GE(reg, value, code)` - If greater or equal
- `IF_LE(reg, value, code)` - If less or equal
- `IF_NEQ(reg, value, code)` - If not equal

**Example:**
```asm
mov     d2, #15
IF_GT(d2, #10, mov d3, #1)
; Result: d3 = 1 (15 > 10)
```

### Ternary Operator

**Syntax:**
```asm
TERNARY(condition_reg, value, dest_reg, true_val, false_val)
```

**Example:**
```asm
mov     d2, #0
TERNARY(d2, #0, d3, #100, #200)
; Result: d3 = 100 (condition true)
```

**C Equivalent:**
```c
dest = (reg == value) ? true_val : false_val;
```

---

## Complete Macro Reference

### Utility Macros

#### MAX(dest, reg1, reg2)
Set destination to maximum of two registers.

```asm
mov     d1, #15
mov     d2, #10
MAX(d0, d1, d2)      ; d0 = 15
```

**Equivalent C:**
```c
dest = (reg1 > reg2) ? reg1 : reg2;
```

#### MIN(dest, reg1, reg2)
Set destination to minimum of two registers.

```asm
mov     d1, #15
mov     d2, #10
MIN(d0, d1, d2)      ; d0 = 10
```

#### ABS_VAL(dest, src)
Absolute value.

```asm
mov     d1, #-5
ABS_VAL(d0, d1)      ; d0 = 5
```

#### INC(reg) / DEC(reg)
Increment/decrement register by 1.

```asm
mov     d0, #5
INC(d0)              ; d0 = 6
DEC(d0)              ; d0 = 5
```

**Equivalent C:**
```c
reg++;  // INC
reg--;  // DEC
```

---

## Testing

### Test Suite

Run the C-macro test suite:

```bash
tests\test_c_macros.bat
```

### Test Files

1. **tests/test_c_macros_simple.asm** - Basic functionality tests
   - Utility macros (MAX, MIN, ABS, INC, DEC)
   - Block-style loops (FOR, WHILE, DO-WHILE)
   - SWITCH/CASE statements
   - Inline loops

2. **tests/test_c_macros.asm** - Comprehensive tests
   - All utility macros
   - Complex loop scenarios
   - Nested loops
   - SWITCH with multiple cases and default
   - Inline loop variants
   - Combined utility operations

### Manual Testing

```bash
# Simple tests
python src\TASM.py -m data\macros\C_instructions.asm tests\test_c_macros_simple.asm

# Comprehensive tests
python src\TASM.py -m data\macros\C_instructions.asm tests\test_c_macros.asm

# Verbose output
python src\TASM.py -m data\macros\C_instructions.asm --info tests\test_c_macros_simple.asm
```

---

## Technical Implementation

### Processing Order

The macro expansion follows this sequence:

1. **Macro Collection** - Parse `#define` directives from source and macro files
2. **Macro Invocation Detection** - Find macro calls in source code
3. **Parameter Substitution** - Replace macro parameters with actual arguments
4. **Special Token Replacement** - Replace `__COUNTER__` and `__UNIQUE__` with counter value
5. **Token Concatenation** - Process `##` operator to merge tokens
6. **Pipe Splitting** - Split multi-statement macros into separate lines
7. **Recursive Expansion** - Expand nested macro calls

### Counter Increment Strategy

- Counter increments **once per function-like macro invocation**
- All `__COUNTER__` tokens in a single macro expansion get the **same value**
- Different invocations get **different counter values**
- Enables paired constructs (FOR/ENDFOR, WHILE/ENDWHILE) to share labels

### Example Counter Sequence

```asm
FOR(d4, #5)         ; Uses counter 1 for mov
                    ; Uses counter 2 for label
ENDFOR(d4)          ; Uses counter 3 for loop

FOR(d5, #3)         ; Uses counter 4 for mov
                    ; Uses counter 5 for label
ENDFOR(d5)          ; Uses counter 6 for loop
```

### Function-Like vs Object-Like Macros

**Object-Like Macros:**
- Defined without parentheses: `#define FOO value`
- Called without parentheses: `FOO`
- No parameter substitution
- Counter NOT incremented (unless body contains `__COUNTER__`)

**Function-Like Macros:**
- Defined with parentheses: `#define FOO(x) body` or `#define FOO() body`
- Called with parentheses: `FOO(arg)` or `FOO()`
- Parameters substituted
- Counter incremented per invocation

---

## Limitations and Best Practices

### TriCore Architecture Constraints

1. **`loop` Instruction Range**
   - The TriCore `loop` instruction has a 4-bit signed displacement field
   - Maximum range: ±15 instructions from loop start
   - For longer loops, use explicit jumps instead of `loop` instruction
   - Consider placing loop bodies closer to loop labels

   **Workaround:**
   ```asm
   ; Instead of FOR/ENDFOR with long body:
   FOR(d4, #5)
   for_body:
       ; long body (>15 instructions)
       sub d4, d4, #1
       jnz d4, for_body
   ; Note: Manual decrement instead of ENDFOR
   ```

2. **Immediate Field Sizes**
   - Various TriCore instructions have limited immediate field sizes
   - Use appropriate instruction variants (16-bit, 32-bit immediates)

### Macro System Limitations

1. **Comma Splitting in Macro Arguments**
   - Commas outside quotes and parentheses are treated as parameter separators
   - **Solution:** Use single quotes `'...'` or double quotes `"..."` around code blocks containing commas
   
   **Example:**
   ```asm
   ; Won't work - comma splits parameters:
   FOR_INLINE(d4, #5, mov d0, #0, add d0, d0, d4)
   
   ; Works - quotes protect the code:
   FOR_INLINE(d4, #5, 'mov d0, #0', 'add d0, d0, d4')
   ```

2. **No Nested Token Concatenation**
   - Token concatenation (`##`) works once per expansion
   - Nested concatenation not supported: `##__COUNTER__##` won't work as expected

3. **No Recursive Macros**
   - Maximum expansion depth: 10 levels
   - Macros cannot call themselves (directly or indirectly)

4. **Static Label Names in SWITCH**
   - Each CASE generates `case_next_##__COUNTER__`
   - Multiple SWITCH statements work fine due to unique counters

### Best Practices

1. **Use Block-Style for Complex Logic**
   ```asm
   ; Good: Readable and maintainable
   FOR(d4, #10)
       add d0, d0, d4
       mov d1, d0
       add d1, d1, #1
   ENDFOR(d4)
   ```

2. **Use Inline for Simple Operations**
   ```asm
   ; Good: Concise for simple cases
   FOR_INLINE(d4, #5, mov d0, #0, add d0, d0, d4)
   ```

3. **Avoid Long Loop Bodies with `loop` Instruction**
   ```asm
   ; If loop body > 15 instructions, use manual decrement
   mov d4, #10
   my_loop:
       ; ... many instructions ...
       sub d4, d4, #1
       jnz d4, my_loop
   ```

4. **Comment Macro Invocations**
   ```asm
   ; Good: Document expected results
   FOR(d4, #10)
       add d0, d0, d4
   ENDFOR(d4)
   ; Result: d0 = sum of 1..10 = 55
   ```

5. **Test Macro Expansions**
   - Review expanded output files in `output/assembly_build/`
   - Use `--info` flag for verbose expansion details
   - Run test suite after macro library changes

---

## Working Examples

### Example 1: Sum Array

```asm
; Sum first 10 elements of an array
mov.a   a4, array_addr      ; array pointer
mov     d0, #0              ; sum
FOR(d4, #10)
    ld.w d1, [a4+]4         ; load and increment pointer
    add d0, d0, d1          ; add to sum
ENDFOR(d4)
; Result: d0 = sum of array[0..9]
```

### Example 2: Find Maximum

```asm
; Find maximum value in array
mov.a   a4, array_addr
mov     d5, #10             ; array size
ld.w    d0, [a4+]4          ; load first element as max
DEC(d5)
FOR(d4, d5)
    ld.w d1, [a4+]4         ; load next element
    MAX(d0, d0, d1)         ; update max if needed
ENDFOR(d4)
; Result: d0 = maximum value
```

### Example 3: State Machine with SWITCH

```asm
; Simple state machine
state_machine:
    ld.w    d2, [a4]        ; load current state
    SWITCH(d2)
    CASE(d2, #0)
        ; State 0: Initialize
        mov d3, #100
        mov d2, #1          ; next state
    CASE(d2, #1)
        ; State 1: Processing
        add d3, d3, #1
        mov d2, #2          ; next state
    CASE(d2, #2)
        ; State 2: Complete
        mov d3, #0
        mov d2, #0          ; reset state
    DEFAULT()
        ; Invalid state
        mov d2, #0          ; reset
    ENDSWITCH()
    st.w    [a4], d2        ; store new state
```

### Example 4: Nested Loops - Matrix Operations

```asm
; Process 3x3 matrix
mov     d0, #0              ; total sum
mov     d6, #3              ; rows
FOR(d4, d6)
    mov d7, #3              ; columns
    FOR(d5, d7)
        add d0, d0, #1      ; increment counter
    ENDFOR(d5)
ENDFOR(d4)
; Result: d0 = 9 (3 * 3)
```

---

## Configuration

### tasm_config.json

```json
{
    "output": {
        "enable_macros": true
    }
}
```

### Command-Line Options

```bash
# Enable macro expansion (default)
python src/TASM.py your_file.asm

# Disable macro expansion
python src/TASM.py --no-macros your_file.asm

# Specify macro file
python src/TASM.py -m data/macros/C_instructions.asm your_file.asm

# Multiple macro files
python src/TASM.py -m macros/system.asm -m macros/math.asm your_file.asm

# Verbose output
python src/TASM.py --info your_file.asm

# Debug output
python src/TASM.py --debug your_file.asm
```

---

## Troubleshooting

### Common Issues

1. **"Maximum macro expansion depth exceeded"**
   - Cause: Recursive macro calls or too many nested macro invocations
   - Solution: Simplify macro definitions, avoid recursive patterns

2. **"Macro expects X arguments, got Y"**
   - Cause: Wrong number of arguments in macro call
   - Solution: Check macro definition, ensure correct argument count

3. **"Invalid label name"**
   - Cause: Macro expansion produced invalid syntax
   - Solution: Review expanded output in `output/assembly_build/`, check macro definition

4. **"Operand value does not fit in field"**
   - Cause: TriCore instruction constraint (not a macro issue)
   - Solution: Use different instruction variant or adjust values

5. **Loop doesn't work with `loop` instruction**
   - Cause: Loop body too large for 4-bit displacement
   - Solution: Use manual decrement and conditional jump instead

### Debug Process

1. Check expanded output:
   ```bash
   # File saved to: output/assembly_build/your_file_expanded.asm
   ```

2. Enable verbose logging:
   ```bash
   python src/TASM.py --debug -m data/macros/C_instructions.asm your_file.asm
   ```

3. Test individual macros:
   ```bash
   # Create minimal test file with single macro call
   python src/TASM.py -m data/macros/C_instructions.asm test_single_macro.asm
   ```

---

## See Also

- [command-line.md](command-line.md) - TASM command-line reference
- [getting-started.md](getting-started.md) - TASM getting started guide
- [tricore_tc1.6.md](tricore_tc1.6.md) - TriCore architecture documentation
- Test files: `tests/test_c_macros*.asm`
- Macro library: `data/macros/C_instructions.asm`
- Implementation: `src/macro.py`

---

## Future Enhancements

Potential future improvements to the macro system:

1. **Variadic Macros** - Support `...` for variable argument count
2. **Stringification** - Support `#` operator to convert tokens to strings
3. **Conditional Expansion** - Support `#if`, `#ifdef`, `#ifndef` directives
4. **Include Guards** - Automatic prevention of multiple inclusion
5. **Macro Libraries** - Standard library of common macros
6. **Better Error Messages** - More context in macro expansion errors
7. **Macro Debugging** - Step-through macro expansion

---

## Appendix: Complete Macro List

### Loop Constructs
- `FOR(counter, count)` / `ENDFOR(counter)`
- `FOR_INLINE(counter, count, init_code, loop_code)`
- `WHILE(reg, val)` / `ENDWHILE(reg, val)`
- `WHILE_INLINE(reg, val, loop_code)`
- `DO_WHILE()` / `LOOP_WHILE(reg, val)`
- `DO_WHILE_INLINE(loop_code, reg, val)`

### Conditional Constructs
- `IF(reg, val, code)`
- `IF_ELSE(reg, val, true_code, false_code)`
- `IF_GT(reg, val, code)`
- `IF_LT(reg, val, code)`
- `IF_GE(reg, val, code)`
- `IF_LE(reg, val, code)`
- `IF_NEQ(reg, val, code)`
- `TERNARY(reg, val, dest, true_val, false_val)`

### Switch/Case
- `SWITCH(reg)`
- `CASE(reg, val)`
- `DEFAULT()`
- `ENDSWITCH()`

### Utility Macros
- `MAX(dest, reg1, reg2)`
- `MIN(dest, reg1, reg2)`
- `ABS_VAL(dest, src)`
- `INC(reg)`
- `DEC(reg)`

---

**Document Version:** 1.0  
**Last Updated:** December 25, 2025  
**Maintained By:** TASM Development Team
