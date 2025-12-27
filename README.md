# TASM
TriCore(TM) Assembler

# TASM - Intro
This TriCore(TM) Assembler project wants to build an assembler based on a configurable instruction set, as such an Excel or a json file. The inmtention is to create a flexible infrastructure to being able to expand, adapt, change, modify the instruction set without the need to change the assembler code.

# TASM - Disclamers
This TriCore(TM) Assembler has no productive nor professional purposes and is release as is, with known or un-known bugs and issues.

# TASM - Three-Phase Assembler

**TASM** is a professional three-phase assembler with **NASM-compatible command-line interface**. It provides comprehensive assembly compilation through macro expansion, assembly, and linking phases with full support for the TriCore TC1.6/1.8 architecture.

## Table of Contents

- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Installation](#installation)
- [First Program](#first-program)
- [Syntax Tolerance & Adaptability](#-syntax-tolerance--adaptability)
- [Quick Reference](#-quick-reference)
- [Command-Line Interface](#-command-line-interface)
- [Usage Examples](#-usage-examples)
- [Development Workflow](#development-workflow)
- [Build System Integration](#-build-system-integration)
- [Three-Phase Architecture](#-three-phase-architecture)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#troubleshooting)
- [Requirements](#-requirements)

## 🚀 Key Features

- **TriCore Instruction Set**: Full support for TriCore TC1.6/1.8 architecture (209 unique mnemonics, 526 variants)
- **Intelligent Code Optimization**: Automatic instruction size selection (16-bit vs 32-bit) with `-O32` and `-Ono-implicit` flags
- **NASM-Compatible Interface**: Industry-standard command-line syntax with full option support
- **NASM 3.4.1 Numeric Constants**: All decimal, hex, octal, binary formats with underscores
- **Data Directives**: DB, DW, DD, DQ, RESB, RESW, EQU, TIMES, INCBIN (NASM chapter 3.2)
- **Three-Phase Compilation**: Macro expansion → Assembly → Two-pass linking with optimization
- **Configuration System**: JSON-based config for instruction sets, output paths, endianness
- **Output Formats**: Binary (`.bin`), Intel HEX (`.hex`), Plain text (`.txt`) - ELF64 and OBJ planned
- **Comprehensive Testing**: 6 test suites covering all features (54+ individual tests)
- **Build System Integration**: Works with Make, CMake, CI/CD pipelines
- **Clean Workspace Management**: All build artifacts organized in timestamped directories

## 🚀 Quick Start

```bash
# Show help
python src/TASM.py -h

# Show version
python src/TASM.py -v

# Basic assembly (creates timestamped output directory with all build artifacts)
python src/TASM.py source.asm

# Specify output format and file (intermediates in output/, final binary at specified location)
python src/TASM.py -f bin -o program.bin source.asm

# Preprocess only (clean stdout output)
python src/TASM.py -E source.asm
```

## Installation

### Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **Operating System**: Windows, Linux, or macOS
- **Dependencies**: Standard library only (no external packages required)

### Setup Steps

1. **Clone or Download TASM**:
   ```bash
   git clone <repository-url>
   cd TASM
   ```

2. **Verify Python Installation**:
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

3. **Test TASM Installation**:
   ```bash
   python src/TASM.py --version
   # Should show: TASM version 1.0.0 compiled on 2025-11-01
   ```

4. **Optional: Add to PATH** (for easier access):
   - **Windows**: Add the TASM directory to your PATH environment variable
   - **Linux/macOS**: Create a symbolic link or alias:
     ```bash
     # Create alias in your shell profile (.bashrc, .zshrc, etc.)
     alias TASM="python /path/to/TASM/src/TASM.py"
     ```

## First Program

Let's create and assemble your first TASM program using TriCore assembly:

### 1. Create a Simple TriCore Assembly File

Create `hello_tricore.asm`:
```assembly
; hello_tricore.asm - Simple TriCore test program
; Demonstrates basic TASM assembly with TriCore syntax

.ORG 0x80000000

start:
    ; Initialize data register with a value
    MOV D[0], #0x48         ; Load 'H' (ASCII 72)
    MOV D[1], #0x65         ; Load 'e' (ASCII 101)
    MOV D[2], #0x6C         ; Load 'l' (ASCII 108)
    MOV D[3], #0x6C         ; Load 'l' (ASCII 108)
    MOV D[4], #0x6F         ; Load 'o' (ASCII 111)
    
    ; Store to memory using address registers
    MOVH.A A[2], #HI:0xD0000000     ; Load high part of address
    LEA A[2], [A[2]]LO:0xD0000000   ; Complete address calculation
    
    ST.B [A[2]]0, D[0]      ; Store 'H'
    ST.B [A[2]]1, D[1]      ; Store 'e'
    ST.B [A[2]]2, D[2]      ; Store 'l'
    ST.B [A[2]]3, D[3]      ; Store 'l'
    ST.B [A[2]]4, D[4]      ; Store 'o'
    
    ; Arithmetic operations
    ADD D[5], D[0], D[1]    ; Add two values
    SUB D[6], D[5], #10     ; Subtract immediate
    
    ; Loop example
loop_start:
    MOV D[7], #10           ; Initialize counter
    
loop_body:
    SUB D[7], #1            ; Decrement counter
    JNZ loop_body           ; Jump if not zero
    
    ; End program
    DEBUG                   ; Breakpoint instruction
    J start                 ; Jump back to start (infinite loop)

end_program:
```

### 2. Assemble the Program

```bash
# Basic assembly (creates timestamped output directory)
python src/TASM.py hello_tricore.asm

# Assembly with specific output location
python src/TASM.py -f bin -o hello_tricore.bin hello_tricore.asm

# Assembly with listing file
python src/TASM.py -f bin -o hello_tricore.bin -l hello_tricore.lst hello_tricore.asm
```

### 3. Check the Results

After successful assembly, you'll see organized output:
```
info: TASM 1.0.0 - Three-Phase Assembler
info: Input file: hello_tricore.asm
info: Output format: bin (Binary flat file)
info: Output directory: C:\path\to\output\assembly_build_20251227_120000
info: === COMPILATION COMPLETED SUCCESSFULLY ===
info: Final binary: output\assembly_build_20251227_120000\hello_tricore.bin

# All build artifacts contained in timestamped directory:
output\assembly_build_20251227_120000\
├── hello_tricore_expanded.asm      # Phase 1 output
├── hello_tricore.obj              # Phase 2 output  
├── hello_tricore.bin              # Phase 3 output
├── build.log                      # Detailed logs
└── build_summary.json             # JSON report
```

## 🧩 Syntax Tolerance & Adaptability

TASM is designed to be highly adaptable, supporting a wide range of syntax variations and operand formats found in different vendor assemblers. Its tolerant parser, flexible instruction set loader, and NASM-compatible interface make it easy to migrate, validate, and build code from diverse sources.

### 1. Flexible Register Notation
- Accepts all common register formats:
  - `d4`, `D4`, `d[4]`, `D[4]`, `[d4]`, `[D4]`, `[d[4]]`, `[D[4]]`
  - `a15`, `A15`, `a[15]`, `A[15]`, `[a15]`, `[A15]`, `[a[15]]`, `[A[15]]`
- Case-insensitive matching for register names.

### 2. Compound Operand Parsing
- Supports vendor-specific operand groupings:
  - `[a15]14,d1` → `a15, 14, d1`
  - `d15,[a5]18` → `d15, a5, 18`
  - `[a15]2,d15` → `a15, 2, d15`
  - `d15,[a2]6` → `d15, a2, 6`
- Automatically splits and normalizes compound operands.

### 3. Numeric Constant Formats (NASM 3.4.1 Compatible)
- Decimal: `200`, `0200d`, `0d200`, `-42`, `1_000_000`
- Hexadecimal: `0xc8`, `0Xc8`, `0c8h`, `0hc8`, `$0c8`
- Octal: `310q`, `310o`, `0o310`, `0q310`
- Binary: `11001000b`, `1100_1000b`, `0b1100_1000`, `0y1100_1000`

### 4. Data Directives & Pseudo-Instructions
- Supports NASM-style data directives: `DB`, `DW`, `DD`, `DQ`, `RESB`, `RESW`, `EQU`, `TIMES`, `INCBIN`
- Handles both initialized and uninitialized data regions.

### 5. Macro Expansion & Conditional Assembly
- Full macro system with parameter substitution and recursive expansion.
- Conditional assembly and include file support.

### 6. Label & Symbol Flexibility
- Accepts labels with or without colons.
- Symbol resolution is tolerant to vendor-specific naming conventions.

### 7. Origin & Section Directives
- `.ORG` directive for origin setting.
- Section and segment support for advanced memory layout.

### 8. Instruction Set Adaptability
- Loads instruction definitions from Excel, JSON, XML, or CSV.
- Easily switch processor architectures by changing config file—no code changes required.

### 9. Error Handling & Reporting
- Structured error messages with file, line, and column info.
- Reports unknown instructions, invalid operands, and data directive errors.

### 10. Command-Line Compatibility
- NASM-style CLI options: `-f`, `-o`, `-l`, `-E`, `-D`, `-U`, `-M`, `-MF`, `-MD`, `-g`, `-F`, `-w`, `-W`
- Output format selection: Binary (`.bin`), Intel HEX (`.hex`), Plain Text (`.txt`)
- Planned formats: ELF64, PE/COFF OBJ

### 11. Testing & Validation
- Comprehensive test suite covers all tolerance features.
- Listing file and build log for debugging and validation.

## 📖 Quick Reference

### Numeric Constants (NASM 3.4.1 Compatible)

#### Decimal
```
200         Plain decimal
0200        Leading zeros (still decimal!)
0200d       Explicit decimal suffix
0d200       Explicit decimal prefix
-42         Negative numbers
1_000_000   With underscores
```

#### Hexadecimal
```
0xc8        Standard 0x prefix
0Xc8        Uppercase X
0c8h        Suffix h
0hc8        Prefix 0h
0abh        Must start with 0 if A-F
$0c8        Deprecated $ (needs leading 0)
```

#### Octal
```
310q        Suffix q
310o        Suffix o
0o310       Prefix 0o
0q310       Prefix 0q
```

#### Binary
```
11001000b       Suffix b
1100_1000b      With underscores
1100_1000y      Suffix y
0b1100_1000     Prefix 0b
0y1100_1000     Prefix 0y
```

### Data Directives

#### Initialized Data
```asm
DB 0xFF, 'A', "Hello"          ; 1 byte each
DW 0x1234, 5678                ; 2 bytes each
DD 0x12345678, 1_000_000       ; 4 bytes each
DQ 0x123456789ABCDEF0          ; 8 bytes
DT 1.5                         ; 10 bytes (80-bit float)
DO ...                         ; 16 bytes
DY ...                         ; 32 bytes
DZ ...                         ; 64 bytes
```

#### Uninitialized Data
```asm
RESB 256                       ; Reserve 256 bytes
RESW 100                       ; Reserve 100 words (200 bytes)
RESD 50                        ; Reserve 50 dwords (200 bytes)
RESQ 10                        ; Reserve 10 qwords (80 bytes)
REST 5                         ; Reserve 5 * 10 bytes
RESO 8                         ; Reserve 8 * 16 bytes
RESY 4                         ; Reserve 4 * 32 bytes
RESZ 2                         ; Reserve 2 * 64 bytes
```

#### Pseudo-Instructions
```asm
; Constants
MAX_VALUE   EQU 255
BUFFER_SIZE EQU 1024
FLAGS       EQU 0b0000_1111

; Repeat
TIMES 10 DB 0                  ; 10 zero bytes
TIMES 4 DW 0xFFFF              ; 4 words

; Include Binary
INCBIN "data.bin"              ; Include entire file
INCBIN "data.bin", 0, 512      ; First 512 bytes
INCBIN "data.bin", 1024        ; Skip 1024 bytes
```

### TriCore Assembly Examples

#### Arithmetic Operations
```asm
; Arithmetic operations
ADD D[0], D[1]                 ; 16-bit ADD instruction
ADD D[c], D[a], const9         ; 32-bit ADD with immediate
ABS D[2], D[3]                 ; Absolute value
SUB D[5], D[6], #100           ; Subtract immediate
ABSDIF D[7], D[8], D[9]        ; Absolute difference
```

#### Logical Operations
```asm
; Logical operations  
AND D[c], D[a], D[b]           ; Bitwise AND
OR D[c], D[a], const9          ; Bitwise OR with immediate
XOR D[0], D[1]                 ; Bitwise XOR
NOT D[2]                       ; Bitwise NOT
```

#### Load/Store Operations
```asm
; Load/store operations
LD.W D[a], [A[b]]              ; Load word from memory
LD.B D[c], [A[d]]offset        ; Load byte with offset
ST.W [A[a]], D[b]              ; Store word to memory
ST.H [A[c]]offset, D[d]        ; Store halfword with offset
```

#### Control Flow
```asm
; Control flow
JEQ D[a], const4, loop         ; Jump if equal
JNE D[b], D[c], exit           ; Jump if not equal
CALL func_addr                 ; Function call
RET                            ; Return from function
LOOP D[a], loop_target         ; Loop with counter
```

### Directives

#### Origin and Labels
```asm
.ORG 0x80000000                ; Set origin address

label:                         ; Define label
    DB 0x00

loop_start:
    ; instructions
```

### Common Patterns

#### Data Tables
```asm
lookup_table:
    DB 0x00, 0x01, 0x02, 0x03
    DB 0x10, 0x11, 0x12, 0x13

strings:
    DB "Hello", 0
    DB "World", 0
```

#### Buffers
```asm
input_buffer:
    RESB 256

output_buffer:
    RESB 256

stack:
    RESD 64                    ; 256 bytes
```

#### Mixed Data
```asm
config_block:
    DD 0x12345678              ; Magic number
    DW 0x0100                  ; Version
    DW 256                     ; Buffer size
    DB 0b00001111              ; Flags
    DB 0                       ; Reserved
```

#### Constants
```asm
; Define constants first
STACK_SIZE  EQU 1024
MAX_ITEMS   EQU 100
BASE_ADDR   EQU 0x80000000

; Use in code
buffer:
    RESB STACK_SIZE

items:
    TIMES MAX_ITEMS DW 0
```

## 💻 Command-Line Interface

TASM provides high compatibility with NASM command-line syntax:

```bash
# These commands work identically to NASM
TASM -f bin -o program.bin source.asm
TASM -f hex -o program.hex source.asm  
TASM -E -D DEBUG=1 source.asm
TASM -M source.asm

# Planned formats (not yet implemented):
# TASM -f elf64 -o module.o source.asm
# TASM -f obj -o module.obj source.asm
```

### Basic Command Structure

```bash
python src/TASM.py [options] source_file.asm
```

### Essential Commands

```bash
# Show help
python src/TASM.py -h

# Show version
python src/TASM.py -v

# Basic assembly (creates binary in auto-generated output directory)
python src/TASM.py source.asm

# Assembly with specific output
python src/TASM.py -f bin -o program.bin source.asm
```

### Supported Options

#### Output Control
```
-o FILE, --output FILE        Output file name
-f FORMAT, --format FORMAT    Output format (bin, hex, txt)
                              Planned: elf64, obj
```

#### Preprocessing
```
-E, --preprocess              Preprocess only (output to stdout)
-I DIR, --include DIR         Add include directory
-D SYMBOL[=VALUE]             Define symbol/macro
-U SYMBOL                     Undefine symbol/macro
```

#### Listing & Debug
```
-l [FILE]                     Generate listing file
-g FORMAT                     Generate debug information
-F FORMAT                     Set debug format
```

#### Dependencies
```
-M                            Generate Makefile dependencies
-MF FILE                      Dependency file name
-MD FILE                      Same as -M -MF
```

#### Warnings & Verbosity
```
-w                            Disable warnings
-W[no-]warning                Enable/disable specific warning
--verbose                     Verbose output
```

#### Build Configuration
```
--output-dir DIR              Set output directory
--no-macros                   Skip macro expansion
--info                        Show detailed information
```

### Output Formats

```
-f bin                 Binary flat file (default) ✓ IMPLEMENTED
-f hex                 Intel HEX format ✓ IMPLEMENTED
-f txt                 Plain text with addresses and opcodes ✓ IMPLEMENTED

Planned (not yet implemented):
-f elf64               Linux ELF 64-bit (PLANNED)
-f obj                 Windows PE/COFF Object (PLANNED)
```

## 🎯 Usage Examples

### Basic Assembly
```bash
# Simple assembly (creates timestamped output directory with all build artifacts)
python src/TASM.py hello.asm

# Specific output file and format (intermediates in output/, final binary at specified location)
python src/TASM.py -f bin -o hello.bin hello.asm
```

### TriCore Assembly
```assembly
; TriCore assembly example - complete_example.asm
.org 0x80000000

; Constants
BUFFER_SIZE  EQU 256
MAX_COUNTER  EQU 100

main:
    ; Initialize address register
    MOVH.A A[15], #HI:0xD0000000
    LEA A[15], [A[15]]LO:0xD0000000
    
    ; Arithmetic operations
    MOV D[0], #10                  ; Load immediate
    MOV D[1], #20                  ; Load immediate
    ADD D[2], D[0], D[1]           ; D[2] = D[0] + D[1] = 30
    SUB D[3], D[2], #5             ; D[3] = D[2] - 5 = 25
    MUL D[4], D[0], D[1]           ; D[4] = D[0] * D[1] = 200
    
    ; Logical operations  
    AND D[5], D[2], #0x0F          ; Mask lower nibble
    OR D[6], D[5], #0xF0           ; Set upper nibble
    XOR D[7], D[6], #0xFF          ; Invert all bits
    
    ; Load/store operations
    LD.W D[8], [A[15]]0            ; Load word from address
    ST.W [A[15]]4, D[2]            ; Store word to address+4
    LD.B D[9], [A[15]]8            ; Load byte from address+8
    ST.H [A[15]]12, D[3]           ; Store halfword to address+12
    
    ; Comparison and branching
    MOV D[10], #MAX_COUNTER
    
loop_start:
    SUB D[10], #1                  ; Decrement counter
    JNED D[10], #0, loop_start     ; Jump if not equal to zero
    
    ; Conditional operations
    CMOV D[11], D[0], D[1], D[2]   ; Conditional move
    SEL D[12], D[3], D[4], D[5]    ; Select based on condition
    
    ; Function call
    CALL calculate_checksum
    
    ; End program
    DEBUG                          ; Breakpoint
    J main                         ; Infinite loop

calculate_checksum:
    ; Function example
    MOV D[15], #0                  ; Initialize result
    ADD D[15], D[0]                ; Add parameters
    ADD D[15], D[1]
    RET                            ; Return

; Data section
data_section:
    DB "TriCore", 0                ; String data
    DW 0x1234, 0x5678              ; Word data
    DD 0x12345678                  ; Doubleword data
    
buffer:
    RESB BUFFER_SIZE               ; Reserve buffer space

end_program:
```

```bash
# Assemble TriCore program
python src/TASM.py -f bin -o tricore_app.bin complete_example.asm

# With listing file
python src/TASM.py -f bin -o tricore_app.bin -l tricore_app.lst complete_example.asm
```

### Cross-Platform Object Files (Planned)
```bash
# Linux ELF64 (PLANNED - not yet implemented)
# python src/TASM.py -f elf64 -o module.o source.asm

# Windows PE/COFF Object (PLANNED - not yet implemented)
# python src/TASM.py -f obj -o module.obj source.asm

# Note: macOS Mach-O format is not planned for implementation
```

## Development Workflow

### Edit-Assemble-Test Cycle
```bash
# 1. Edit source file
nano program.asm

# 2. Preprocess to check macro expansion (outputs to stdout)
python src/TASM.py -E program.asm

# 3. Assemble with verbose output for debugging
python src/TASM.py --verbose -f bin -o program.bin program.asm

# 4. Check build logs (in timestamped build directory)
cat output/assembly_build_*/build.log

# 5. View JSON build summary
cat output/assembly_build_*/build_summary.json | python -m json.tool
```

### Different Output Formats
```bash
# Binary file (for embedded systems) - IMPLEMENTED
python src/TASM.py -f bin -o firmware.bin source.asm

# Intel HEX file (for programmers) - IMPLEMENTED
python src/TASM.py -f hex -o firmware.hex source.asm

# Plain text format (for analysis) - IMPLEMENTED
python src/TASM.py -f txt -o firmware.txt source.asm

# Planned formats (not yet implemented):
# ELF object file (for Linux) - PLANNED
# python src/TASM.py -f elf64 -o module.o source.asm

# Windows PE/COFF object file - PLANNED
# python src/TASM.py -f obj -o module.obj source.asm
```

### Preprocessing and Macros
```bash
# Define macros on command line
python src/TASM.py -D DEBUG=1 -D VERSION=2 source.asm

# Include additional directories
python src/TASM.py -I ./includes -I ./common source.asm

# Preprocess only (useful for debugging)
python src/TASM.py -E source.asm > expanded.asm

# Skip macro expansion phase
python src/TASM.py --no-macros source.asm
```

## 🏗️ Build System Integration

TASM integrates seamlessly with popular build systems:

### Makefile Integration

```makefile
# Basic Makefile for TASM projects
TASM = python src/TASM.py
ASM_FILES = $(wildcard *.asm)
OBJ_FILES = $(ASM_FILES:.asm=.o)

# Default target
all: program

# Assemble .asm files to object files
%.o: %.asm
	$(TASM) -f elf64 -o $@ $<

# Link object files
program: $(OBJ_FILES)
	ld -o program $(OBJ_FILES)

# Clean build artifacts
clean:
	rm -f $(OBJ_FILES) program
	rm -rf output/

# Preprocess for debugging
preprocess: $(ASM_FILES)
	$(TASM) -E $(ASM_FILES) > preprocessed.asm

.PHONY: all clean preprocess
```

### CMake Integration

```cmake
# CMakeLists.txt for TASM projects
cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Find TASM
find_program(TASM_EXECUTABLE 
    NAMES python
    PATHS ${CMAKE_SOURCE_DIR}/src
)

# Custom command for assembly
function(add_assembly_target target_name source_file)
    add_custom_command(
        OUTPUT ${target_name}.o
        COMMAND ${TASM_EXECUTABLE} TASM.py -f elf64 -o ${target_name}.o ${source_file}
        DEPENDS ${source_file}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/src
    )
    add_custom_target(${target_name} DEPENDS ${target_name}.o)
endfunction()

# Use the function
add_assembly_target(main main.asm)
```

### Batch Processing (Windows)

Create `build.bat`:
```batch
@echo off
setlocal

set TASM=python src\TASM.py
set OUTPUT_DIR=output

if not exist %OUTPUT_DIR% mkdir %OUTPUT_DIR%

echo Building assembly files...
for %%f in (*.asm) do (
    echo Assembling %%f...
    %TASM% -f bin -o %OUTPUT_DIR%\%%~nf.bin %%f
    if errorlevel 1 (
        echo Error assembling %%f
        exit /b 1
    )
)

echo Build completed successfully!
```

### Shell Script (Linux/macOS)

Create `build.sh`:
```bash
#!/bin/bash
set -e

TASM="python src/TASM.py"
OUTPUT_DIR="output"

mkdir -p "$OUTPUT_DIR"

echo "Building assembly files..."
for asm_file in *.asm; do
    if [ -f "$asm_file" ]; then
        echo "Assembling $asm_file..."
        base_name=$(basename "$asm_file" .asm)
        $TASM -f bin -o "$OUTPUT_DIR/${base_name}.bin" "$asm_file"
    fi
done

echo "Build completed successfully!"
```

## 🔍 Three-Phase Architecture

TASM's unique three-phase design provides robust compilation:

### Phase 1 - Macro Expansion
- **Process**: Expands macros, includes, and conditional directives
- **Input**: Source `.asm` file with macros
- **Output**: Expanded `.asm` file with all macros resolved
- **Features**:
  - C-style macro definitions with parameters
  - Recursive macro expansion
  - Include file processing
  - Conditional assembly (`%if`, `%ifdef`, `%else`, `%endif`)
  - Symbol definitions (`%define`, `EQU`)

### Phase 2 - Assembly
- **Process**: Two-pass assembly for symbol resolution
- **Input**: Expanded `.asm` file
- **Output**: Object `.obj` file with relocatable code
- **Features**:
  - Pass 1: Symbol table creation and address calculation
  - Pass 2: Code generation and encoding
  - Instruction variant selection (16-bit vs 32-bit optimization)
  - Label and symbol resolution
  - Data directive processing

### Phase 3 - Linking
- **Process**: Two-pass linking with iterative instruction size optimization
- **Input**: Object `.obj` file(s)
- **Output**: Final binary, HEX, or text file plus listing and map files
- **Features**:
  - **Pass 1 - Symbol Resolution**: Resolves all external symbols and builds global symbol table
  - **Pass 2 - Optimization**: Multi-pass iterative re-encoding to optimize instruction sizes (16-bit vs 32-bit)
  - **Listing Generation**: Creates preliminary `.ls1` file, then updates to final `.lst` with linked addresses
  - **Output Formats**: Binary (`.bin`), Intel HEX (`.hex`), Plain Text (`.txt`)
  - **Map File**: Generates `.map` file with symbol addresses and memory layout
  - **Address Conflict Detection**: Validates no overlapping code/data regions

### Example Flow

```
hello.asm
    ↓ Phase 1: Macro Expansion
hello_expanded.asm
    ↓ Phase 2: Assembly
hello.obj
    ↓ Phase 3: Linking
hello.bin
```

## 📁 Project Structure

```
TASM/
├── config/                     # Configuration files
│   └── tasm_config.json       # Main config (endianness, paths, output)
├── src/                        # Core assembler source code
│   ├── TASM.py                # Main entry point (NASM-compatible CLI)
│   ├── config_loader.py       # Configuration manager
│   ├── macro.py               # Phase 1: Macro expansion
│   ├── assembler.py           # Phase 2: Assembly engine  
│   ├── linker.py              # Phase 3: Linking
│   ├── instruction_loader.py  # External instruction set loader
│   ├── instruction_encoder.py # Instruction encoding engine
│   ├── compiler_logger.py     # Logging system
│   └── utils.py               # Utility functions
├── documentation/              # Comprehensive documentation
│   ├── README.md              # This file (complete guide)
│   ├── command-line.md        # Complete CLI reference (1200+ lines)
│   ├── architecture.md        # Technical architecture
│   ├── instruction_encoder.md # Encoder internals documentation
│   ├── MACRO_EXPANDER_GUIDE.md # Macro system guide
│   ├── tricore_tc1.6.md       # TriCore 1.6 reference (2100+ lines)
│   └── tricore_tc1.8.md       # TriCore 1.8 reference (3600+ lines)
├── tests/                      # Comprehensive test suite
│   ├── run_all_tests.bat      # Main test suite (16 tests)
│   ├── 0_test.bat through 6_test_macros.bat  # Individual test suites
│   ├── test_*.py              # Python unit tests
│   └── test_*.asm             # Assembly test files
├── Processors/                 # Processor-specific data
│   └── tricore/
│       └── data/
│           ├── languages/     # Instruction set definitions (.xlsx)
│           └── manuals/       # Reference manuals (.pdf)
├── output/                     # Organized build outputs
│   └── assembly_build_*/      # Timestamped build directories
│       ├── *_expanded.asm     # Phase 1: Expanded source
│       ├── *.obj              # Phase 2: Object files
│       ├── *.bin/*.hex/*.txt  # Phase 3: Output files
│       ├── build.log          # Detailed build logs
│       └── build_summary.json # JSON build reports
├── data/                       # Example assembly files
│   ├── macros/                # C-macro definition files
│   └── *.asm                  # Test and example programs
└── scripts/                    # Utility scripts
```

## 🧪 Testing

TASM includes a comprehensive test suite with 6 individual test suites covering all features:

### Run All Tests
```bash
# Windows - Run all test suites
.\tests\run_all_tests.bat

# Verbose mode (see detailed output)
.\tests\run_all_tests.bat --verbose
.\tests\run_all_tests.bat -v

# Linux/macOS
pytest tests/
```

### Individual Test Suites
```bash
# Test Suite 0: Basic instruction encoding tests (7 tests)
.\tests\0_test.bat

# Test Suite 1: Register encoding tests (19 tests)
.\tests\1_test.bat

# Test Suite 2: Advanced encoding tests (13 tests)
.\tests\2_test.bat

# Test Suite 3: Operand format tests (12 tests)
.\tests\3_test.bat

# Test Suite 4: Encoder validation (4617 instructions)
.\tests\4_test.bat

# Test Suite 6: Macro expansion tests (3 tests)
.\tests\6_test_macros.bat
```

### Test Coverage
- **Basic Instructions**: MOV, ADD, SUB, JMP, CALL, RET
- **Register Encoding**: All register types (D, A, E, P)
- **Addressing Modes**: Direct, indirect, indexed, PC-relative
- **Data Directives**: DB, DW, DD, DQ, RESB, RESW
- **Numeric Constants**: All NASM formats (decimal, hex, octal, binary)
- **Macros**: C-style macros with parameters and recursion
- **Optimization**: 16-bit vs 32-bit instruction selection
- **Error Handling**: Invalid instructions, operands, and syntax

### Test Results
The consolidated test suite provides:
- **Pass/Fail Status**: Each test suite reports individual results
- **Statistics**: Total tests, passed, failed, pass rate
- **Detailed Logs**: `tests/output/test_suite_results.log`
- **Exit Codes**: 0 for success, 1 for failures

## Troubleshooting

### Common Issues

#### 1. "TASM: error: no input files"
**Problem**: No assembly file specified  
**Solution**: 
```bash
# Wrong
python src/TASM.py -f bin

# Correct  
python src/TASM.py -f bin source.asm
```

#### 2. "TASM: error: source file not found"
**Problem**: File path is incorrect  
**Solution**:
```bash
# Check file exists
ls -la source.asm

# Use correct path
python src/TASM.py ./data/source.asm
```

#### 3. PowerShell Token Splitting
**Problem**: PowerShell splits arguments with dots  
**Solution**:
```powershell
# Wrong (may cause issues)
python src\TASM.py -otest.bin source.asm

# Correct
python src\TASM.py "-otest.bin" source.asm
```

#### 4. Permission Errors
**Problem**: Cannot write to output directory  
**Solution**:
```bash
# Check permissions
ls -la output/

# Create directory with correct permissions
mkdir -p output
chmod 755 output
```

#### 5. Build Artifacts in Root Directory
**Problem**: Old intermediate files in root (from previous versions)  
**Solution**:
```bash
# Clean up old files (TASM now contains all files in output/)
rm -f *.obj *_expanded.asm *.bin

# Current TASM behavior: all build files go to output/assembly_build_*/
```

### Debug Mode

Enable verbose logging for detailed information:
```bash
python src/TASM.py --verbose -f bin -o debug.bin source.asm
```

Check build logs (located in timestamped build directories):
```bash
# View latest build log
cat output/assembly_build_*/build.log | tail

# View JSON summary with pretty formatting
cat output/assembly_build_*/build_summary.json | python -m json.tool

# Find build logs by timestamp
ls -la output/assembly_build_*/
```

### Error Types

```
UNKNOWN_INSTRUCTION      - Invalid mnemonic
INVALID_OPERAND         - Wrong operand format
DATA_DIRECTIVE_ERROR    - Data value out of range
INVALID_ORG             - Malformed .ORG directive
UNRESOLVED_SYMBOL       - Undefined label/constant
MACRO_EXPANSION_ERROR   - Macro processing failed
ENCODING_ERROR          - Instruction encoding failed
```

### Getting Help

1. **Built-in Help**: `python src/TASM.py -h`
2. **Check Version**: `python src/TASM.py -v` 
3. **Documentation**: See `documentation/` directory
4. **Test Files**: See `data/` directory for assembly examples
5. **Verbose Mode**: Use `--verbose` flag for detailed output

## 📦 File Organization

TASM maintains a clean and organized workspace:

### Build Directory Structure
```
PROJECT_ROOT/
├── src/                    # Source code (never modified)
├── data/                   # Input assembly files  
└── output/                 # All build artifacts
    └── assembly_build_TIMESTAMP/
        ├── *_expanded.asm  # Phase 1: Macro expansion
        ├── *.obj          # Phase 2: Assembly output
        ├── *.bin          # Phase 3: Final binary
        ├── build.log      # Detailed build log
        └── build_summary.json  # Structured report
```

### Benefits
- **Clean Root Directory**: No intermediate files clutter your workspace
- **Build Traceability**: Each build gets timestamped directory
- **Parallel Builds**: Multiple builds won't interfere with each other
- **Easy Cleanup**: Delete entire `output/` directory to clean all builds

## 📊 Professional Logging

TASM includes compiler-grade logging with detailed reports:

- **Structured Error Messages**: File locations and error codes
- **Build Statistics**: Comprehensive compilation metrics
- **JSON Reports**: Machine-readable build summaries in each build directory
- **Verbose Debug Mode**: Detailed internal processing info

### Example Output
```
info: TASM 1.0.0 - Three-Phase Assembler
info: === COMPILATION COMPLETED SUCCESSFULLY ===
============================================================
COMPILATION SUMMARY  
============================================================
Build started: 2025-12-27 12:00:00
Build finished: 2025-12-27 12:00:01
Duration: 0.15 seconds

STATISTICS:
  Errors:        0
  Warnings:      1
  Info:         26
  Debug:         0

BUILD SUCCEEDED
============================================================
```

### Message Format

Messages are formatted like compiler output:
```
file.py:line:column: level: message [ERROR_CODE]
```

Examples:
```
source.asm:45:23: error: Syntax error: missing semicolon [SYNTAX_ERROR]
source.asm:128: warning: Deprecated instruction usage [DEPRECATED]
info: Processing completed successfully
```

## ⚙️ Configuration

### tasm_config.json

TASM uses a JSON configuration file for customization:

```json
{
  "endianness": "little",
  "default_format": "bin",
  "listing_enabled": true,
  "output_directory": "output/assembly_build",
  "instruction_set": "Processors/tricore/data/languages/tricore_instruction_set.json",
  "optimization": {
    "prefer_16bit": true,
    "implicit_optimization": true
  }
}
```

### Configuration Options

- **endianness**: `"little"` or `"big"` - byte order for multi-byte values
- **default_format**: Default output format when `-f` not specified
- **listing_enabled**: Auto-generate listing files
- **output_directory**: Base directory for build artifacts
- **instruction_set**: Path to instruction set definition file
- **optimization**: Code optimization settings

## 🔧 Requirements

- **Python 3.8+** (Python 3.13 recommended)
- **Operating Systems**: Windows, Linux, macOS
- **Dependencies**: Standard library only (no external packages required)

## 📖 Additional Documentation

### Core Documentation
- **[Command-Line Interface](command-line.md)** - Complete NASM-compatible command reference with all options (1200+ lines)
- **[Architecture Overview](architecture.md)** - Three-phase compilation, instruction loading, and configuration

### Technical Documentation  
- **[Instruction Encoder](instruction_encoder.md)** - Encoder internals, operand parsing, variant selection
- **[Macro Guide](MACRO_EXPANDER_GUIDE.md)** - Macro system and expansion templates
- **[Testing Guide](TRICORE_TESTING_GUIDE.md)** - Comprehensive test suite documentation

### Processor Documentation
- **[TriCore TC1.6](tricore_tc1.6.md)** - TriCore 1.6 instruction set reference (2100+ lines)
- **[TriCore TC1.8](tricore_tc1.8.md)** - TriCore 1.8 instruction set reference (3600+ lines)

## 🎓 Best Practices

1. **Use underscores** for large numbers: `1_000_000` instead of `1000000`
2. **Be explicit** with hex: `0abh` not `abh` (needs leading 0)
3. **Define constants** with EQU for magic numbers
4. **Comment your code** - assembly is cryptic without comments
5. **Use meaningful labels** - `loop_start` better than `l1`
6. **Organize data sections** - separate code and data
7. **Use TIMES** for repeated patterns - cleaner than manual repetition
8. **Check listing files** to verify byte layout and encoding
9. **Respect endianness** - configure in tasm_config.json
10. **Test incrementally** - assemble frequently during development

## 📄 License

This project is available under the MIT License. See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please see the documentation for development guidelines.

## 📈 Version History

- **v1.0.0** (2025-11-01): Initial release with NASM-compatible interface
  - Three-phase compilation architecture
  - NASM-compatible command-line interface  
  - Multiple output format support
  - Professional logging and error handling
  - Comprehensive documentation
  - TriCore TC1.6/1.8 support with 526 instruction variants

---

**TASM** provides professional assembly development with industry-standard compatibility, making it ideal for both education and production use with the TriCore architecture.

*For detailed command-line reference and advanced features, see [command-line.md](command-line.md).*

*Last updated: December 27, 2025*
