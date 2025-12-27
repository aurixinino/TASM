# TASM
TriCore(TM) Assembler

# TASM Installation and Quick Start Guide

This guide will help you get started with **TASM** (Three-Phase Assembler) quickly and efficiently.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [First Program](#first-program)
- [Common Usage Patterns](#common-usage-patterns)
- [Integration with Build Systems](#integration-with-build-systems)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **Operating System**: Windows, Linux, or macOS

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

## Quick Start

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

## First Program

Let's create and assemble your first TASM program:

### 1. Create a Simple Assembly File

Create `hello.asm`:
```assembly
; hello.asm - Simple test program
; Demonstrates basic TASM assembly

.ORG $8000

start:
    LDA #$48        ; Load 'H'
    STA $0200       ; Store to screen memory
    
    LDA #$65        ; Load 'e'  
    STA $0201       ; Store to screen memory
    
    LDA #$6C        ; Load 'l'
    STA $0202       ; Store to screen memory
    
    LDA #$6C        ; Load 'l'
    STA $0203       ; Store to screen memory
    
    LDA #$6F        ; Load 'o'
    STA $0204       ; Store to screen memory
    
    BRK             ; Break (halt)

end_program:
```

### 2. Assemble the Program

```bash
# Basic assembly (creates timestamped output directory)
python src/TASM.py hello.asm

# Assembly with specific output location
python src/TASM.py -f bin -o hello.bin hello.asm

# Assembly with listing file
python src/TASM.py -f bin -o hello.bin -l hello.lst hello.asm
```

### 3. Check the Results

After successful assembly, you'll see organized output:
```
info: TASM 1.0.0 - Three-Phase Assembler
info: Input file: hello.asm
info: Output format: bin (Binary flat file)
info: Output directory: C:\path\to\output\assembly_build_20251101_111739
info: === COMPILATION COMPLETED SUCCESSFULLY ===
info: Final binary: output\assembly_build_20251101_111739\hello.bin

# All build artifacts contained in timestamped directory:
output\assembly_build_20251101_111739\
├── hello_expanded.asm      # Phase 1 output
├── hello.obj              # Phase 2 output  
├── hello.bin              # Phase 3 output
├── build.log              # Detailed logs
└── build_summary.json     # JSON report
```

## Common Usage Patterns

### Development Workflow

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
# Binary file (for embedded systems)
python src/TASM.py -f bin -o firmware.bin source.asm

# ELF object file (for Linux)
python src/TASM.py -f elf64 -o module.o source.asm

# Windows object file
python src/TASM.py -f obj -o module.obj source.asm

# macOS object file  
python src/TASM.py -f macho64 -o module.o source.asm
```

### Preprocessing and Macros

```bash
# Define macros on command line
python src/TASM.py -D DEBUG=1 -D VERSION=2 source.asm

# Include additional directories
python src/TASM.py -I ./includes -I ./common source.asm

# Preprocess only (useful for debugging)
python src/TASM.py -E source.asm > expanded.asm
```

## Integration with Build Systems

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
	rm -f $(OBJ_FILES) program output/*

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

## File Organization

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

### Getting Help

1. **Built-in Help**: `python src/TASM.py -h`
2. **Check Version**: `python src/TASM.py -v` 
3. **Documentation**: See `documentation/` directory
4. **Test Files**: See `data/` directory for assembly examples

---

You're now ready to start using TASM for your assembly projects! The combination of NASM-compatible syntax and three-phase compilation provides a powerful and flexible development environment.
