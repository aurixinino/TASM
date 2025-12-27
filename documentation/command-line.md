# TASM Command-Line Interface

**TASM** (Three-Phase Assembler) provides a **NASM-compatible command-line interface** for seamless integration with existing build systems and workflows. TASM implements a complete three-phase compilation process: macro expansion, assembly, and linking.

## Table of Contents

- [Synopsis](#synopsis)
- [Configuration](#configuration)
  - [Configuration File Location](#configuration-file-location)
  - [Configuration Structure](#configuration-structure)
  - [Configuration Options](#configuration-options)
- [Options](#options)
- [Output Formats](#output-formats)
- [Usage Examples](#usage-examples)
  - [Plain Text Generation](#plain-text-generation)
  - [Console Output and Logging](#console-output-and-logging)
- [NASM Compatibility](#nasm-compatibility)
- [Exit Codes](#exit-codes)
- [Three-Phase Compilation](#three-phase-compilation)

## Synopsis

```bash
TASM [-@ response_file] [-f format] [-o outfile] [-l listfile] [options...] filename
TASM -h | --help
TASM -v | --version
```

## Configuration

TASM uses a centralized JSON configuration file to manage architecture settings, file paths, and output options. This eliminates hardcoded values and provides a single source of configuration for the entire project.

### Quick Reference

**Using Default Config:**
```bash
TASM source.asm  # Uses config/tasm_config.json automatically
```

**Using Custom Config:**
```bash
TASM -c path/to/custom.json source.asm
TASM --config=path/to/custom.json source.asm
```

**Config File Specifies:**
- ✅ Endianness (little/big)
- ✅ Word size (16/32 bits)
- ✅ Instruction set file path
- ✅ PDF manual path
- ✅ Output file generation flags

### Configuration File Location

**Default Location:**
```
<project_root>/config/tasm_config.json
```

**Custom Location:**
You can specify a custom configuration file using the `-c` or `--config` option:
```bash
TASM -c path/to/custom_config.json source.asm
TASM --config=path/to/custom_config.json source.asm
```

**Path Resolution:**
- **Default**: TASM automatically locates config file relative to installation directory
- **Custom**: When `-c` option is used, TASM uses the specified path (absolute or relative)
- The config loader searches from `src/` directory up to project root for default config
- Full path example: `C:\Users\Atti\Documents\TEST_AI\AI_4\config\tasm_config.json`
- Custom config must be specified before other options that depend on configuration

**File Structure:**
```
project_root/
├── config/
│   └── tasm_config.json          # Main configuration file
├── src/
│   ├── TASM.py                   # Main assembler
│   ├── config_loader.py          # Configuration parser
│   ├── assembler.py              # Uses config for paths
│   ├── linker.py                 # Uses config for endianness
│   └── instruction_loader.py     # Uses config for instruction set
├── Processors/
│   └── tricore/
│       └── data/
│           ├── languages/
│           │   └── tricore_tc1.6_instruction_set.xlsx
│           └── manuals/
│               └── infineon-tricore-tc1.8-architecture-volume2-usermanual-en.pdf
└── output/
    └── assembly_build/           # Build output directory
```

### Configuration Structure

The configuration file uses JSON format with the following main sections:

```json
{
  "architecture": {
    "endianness": "little",
    "word_size": 32,
    "comment": "Endianness: 'little' or 'big'. Word size: 16 or 32 bits"
  },
  "paths": {
    "pdf_manual": "C:\\Users\\Atti\\Documents\\TEST_AI\\AI_4\\Processors\\tricore\\data\\manuals\\infineon-tricore-tc1.8-architecture-volume2-usermanual-en.pdf",
    "instruction_set": "C:\\Users\\Atti\\Documents\\TEST_AI\\AI_4\\Processors\\tricore\\data\\languages\\tricore_tc1.6_instruction_set.xlsx",
    "comment": "Absolute paths to processor documentation and instruction set definitions"
  },
  "output": {
    "generate_lst": true,
    "generate_bin": true,
    "generate_hex": true,
    "generate_map": true,
    "comment": "Control which output files are generated"
  }
}
```

### Configuration Options

#### Architecture Settings

| Setting | Type | Values | Description |
|---------|------|--------|-------------|
| `endianness` | string | `"little"` or `"big"` | Byte ordering for binary output |
| `word_size` | integer | `16` or `32` | Architecture word size in bits |

**Endianness Impact:**
- **Little-endian** (TriCore): LSB at lower address (e.g., `0x0002003B` → `3B 00 02 00`)
- **Big-endian**: MSB at lower address (e.g., `0x0002003B` → `00 02 00 3B`)

#### Path Configuration

| Setting | Type | Description |
|---------|------|-------------|
| `pdf_manual` | string | Absolute path to processor reference manual (PDF) |
| `instruction_set` | string | Absolute path to instruction set definition file (.xlsx, .json, .xml, .csv) |
| `output_dir` | string | Relative or absolute path to default output directory for build artifacts |

**Path Requirements:**
- `pdf_manual` and `instruction_set` must be absolute paths (e.g., `C:\path\to\file`)
- `output_dir` can be relative to project root (e.g., `output/assembly_build`) or absolute
- Windows: Use double backslashes (`\\`) or forward slashes (`/`)
- Unix/Linux: Use standard forward slashes (`/`)
- File must exist and be readable by TASM
- Default `output_dir`: `output/assembly_build`

**Supported Instruction Set Formats:**
- Excel (.xlsx) - Recommended for TriCore
- JSON (.json) - Structured data format
- XML (.xml) - Markup format
- CSV (.csv) - Legacy format

#### Output Control

| Setting | Type | Description |
|---------|------|-------------|
| `generate_lst` | boolean | Generate listing files (.lst) |
| `generate_bin` | boolean | Generate binary files (.bin) |
| `generate_hex` | boolean | Generate Intel HEX files (.hex) |
| `generate_map` | boolean | Generate memory map files (.map) |
| `enable_macros` | boolean | Enable macro expansion (can be overridden with --no-macros flag) |

### Configuration Usage

**Loading Configuration:**
```python
from config_loader import get_config

config = get_config()  # Singleton instance

# Check endianness
if config.is_little_endian:
    print("Using little-endian byte order")

# Access paths
instruction_set_path = config.instruction_set_path
pdf_path = config.pdf_manual_path

# Check output settings
if config.generate_lst:
    print("Listing files will be generated")
```

**Configuration Properties:**
- `is_little_endian` - Boolean: True if architecture is little-endian
- `is_big_endian` - Boolean: True if architecture is big-endian
- `word_size` - Integer: Word size in bits (16 or 32)
- `instruction_set_path` - String: Path to instruction set file
- `pdf_manual_path` - String: Path to PDF manual
- `generate_lst`, `generate_bin`, `generate_hex`, `generate_map` - Boolean: Output file flags

**Configuration Fallback:**
If the config file is not found or cannot be parsed:
- TASM falls back to default hardcoded paths
- Default: Little-endian, 32-bit architecture
- Warning message logged to build log

**Modifying Configuration:**
1. Open `config/tasm_config.json` in a text editor
2. Edit desired settings (maintain JSON syntax)
3. Save the file
4. Configuration automatically reloaded on next TASM invocation

**Example Configuration Modifications:**

Change to big-endian:
```json
{
  "architecture": {
    "endianness": "big",
    "word_size": 32
  }
}
```

Update instruction set path:
```json
{
  "paths": {
    "instruction_set": "D:\\CustomProcessors\\my_processor_v2.xlsx"
  }
}
```

Disable hex file generation:
```json
{
  "output": {
    "generate_hex": false
  }
}
```

### Configuration Best Practices

1. **Use Absolute Paths**: Always use absolute paths for `pdf_manual` and `instruction_set`
2. **Validate JSON**: Use a JSON validator to check syntax after editing
3. **Backup Configuration**: Keep a backup copy before making changes
4. **Version Control**: Commit `tasm_config.json` to version control
5. **Team Coordination**: Ensure all team members use consistent paths (or use relative paths from a known location)
6. **Custom Configs**: Use `-c` option for project-specific or environment-specific configurations
7. **Config Naming**: Use descriptive names like `config_debug.json`, `config_release.json`, `config_test.json`
8. **Documentation**: Document custom configs and their intended use cases in project README

## Options

### Output Control

| Option | Description |
|--------|-------------|
| `-o outfile` | Specify output file name |
| `-f format` | Select output file format (see [Output Formats](#output-formats)) |
| `-l [listfile]` | Generate MASM-style listing file with addresses, opcodes, and source |
| `-D dir` | Specify output directory for build artifacts |
| `--output-dir dir` | Specify output directory for build artifacts (long form) |

### Preprocessing

| Option | Description |
|--------|-------------|
| `-E` | Preprocess only (writes output to stdout) |
| `-a` | Suppress preprocessor |
| `--no-macros` | Disable macro expansion (use source code as-is) |
| `-I path` | Add pathname to include file path |
| `-i path` | Add pathname to include file path |
| `-p file` | Pre-include a file |
| `-P file` | Pre-include a file |

### Macro Definitions

| Option | Description |
|--------|-------------|
| `-d symbol` | Pre-define a macro |
| `-d symbol=value` | Pre-define a macro with value |
| `-D symbol` | Pre-define a macro |
| `-D symbol=value` | Pre-define a macro with value |
| `-u symbol` | Undefine a macro |
| `-U symbol` | Undefine a macro |

### Macro Expansion Files

| Option | Description |
|--------|-------------|
| `-m file` | Include macro expansion file template |
| `-M file` | Include macro expansion file template |
| `--macro-file file` | Include macro expansion file template (long form) |
| `--macro-file=file` | Include macro expansion file template (combined syntax) |
| `--macros file` | Include macro expansion file template (alternative) |

### Configuration File

| Option | Description |
|--------|-------------|
| `-c file` | Specify custom configuration file (JSON format) |
| `--config file` | Specify custom configuration file (long form) |
| `--config=file` | Specify custom configuration file (combined syntax) |

### Debug and Analysis

| Option | Description |
|--------|-------------|
| `-g` | Generate debug information |
| `-F format` | Select debug info format |
| `-M` | Generate Makefile dependencies on stdout |
| `-MG` | Generate dependencies, missing files assumed generated |
| `-MF file` | Set Makefile dependency file |
| `-MD file` | Assemble and generate dependencies |
| `-MT target` | Change default target of rule emitted by -M |
| `-MQ target` | Same as -MT but quotes special chars |

### Logging and Verbosity

| Option | Description |
|--------|-------------|
| `--info` | Show informational messages in addition to errors and aborts |
| `--verbose` | Show all log messages (debug, info, warning, error, abort) |
| `--debug` | Show debug messages in addition to standard logging |

**Logging Levels:**
- **Standard** (default): Shows only error and abort messages (quiet console mode)
- **Info** (`--info`): Shows info, warning, error, and abort messages  
- **Verbose** (`--verbose`): Shows all message types including debug information
- **Debug** (`--debug`): Shows standard messages plus debug messages

**Console Output:**
- TASM displays a professional header with version and build information
- Phase progress is shown during compilation (pre-processing, compilation passes, linking)
- Build statistics include file size, opcode count, and timing information
- By default, console output is minimal (errors/aborts only) - use `--info` for detailed progress

### Warnings and Optimization

| Option | Description |
|--------|-------------|
| `-w+warning` | Enable specific warning |
| `-w-warning` | Disable specific warning |
| `-w` | Enable all warnings (same as -Wall) |
| `-W` | Same as -w |
| `-O0` | No optimization |
| `-O1` | Minimal optimization |
| `-O32` | Force 32-bit instruction variants (override 16-bit code size optimization) |
| `-Ono-implicit` | Disable implicit operand variants (no A[10]/A[15] shortcuts) |
| `-Ox` | Multipass optimization (default) |

### Instruction Set Configuration

| Option | Description |
|--------|-------------|
| `-s file` | Specify instruction set CSV file |
| `--instruction-set file` | Specify instruction set CSV file (long form) |
| `--instruction-set=file` | Specify instruction set CSV file (combined syntax) |

### Compatibility and Help

| Option | Description |
|--------|-------------|
| `-t` | Enable TASM compatibility mode |
| `-v`, `--version` | Show version information |
| `-h`, `--help` | Show help text |
| `--verbose` | Enable verbose debug logging |

## Output Formats

TASM supports the following output formats:

| Format | Description |
|--------|-------------|
| `bin` | Binary flat file (default) |
| `hex` | Intel HEX format |
| `txt` | Plain text format with ADDRESS OPCODE pairs |

## Usage Examples

### Basic Assembly

```bash
# Assemble to binary format (creates timestamped output directory)
TASM source.asm

# Specify output file and format (intermediate files in output/, final binary at specified location)
TASM -f bin -o program.bin source.asm

# Combined syntax (quote arguments with dots in PowerShell)
TASM -fbin "-oprogram.bin" source.asm
```

### Custom Configuration Files

```bash
# Use custom configuration file (relative path)
TASM -c config/tasm_config_test.json source.asm

# Use custom configuration file (absolute path)
TASM -c C:\Projects\configs\tricore_big_endian.json source.asm

# Long form syntax
TASM --config config/custom.json source.asm

# Combined syntax
TASM --config=config/custom.json source.asm

# Combine custom config with output options
TASM -c config/test.json -l -f hex -o program.hex source.asm

# Multiple projects with different configurations
TASM -c project_a/config.json -o build/project_a.bin project_a/main.asm
TASM -c project_b/config.json -o build/project_b.bin project_b/main.asm
```

**Use Cases for Custom Configs:**
- **Development vs Production**: Different endianness or word sizes
- **Multiple Processors**: Separate configs for different target architectures
- **Team Environments**: Personal config paths without modifying default
- **Testing**: Temporary configurations for validation
- **Build Variants**: Debug vs Release configurations

**Example Custom Configs:**

**config/big_endian.json** (Big-endian processor):
```json
{
  "architecture": {
    "endianness": "big",
    "word_size": 32
  },
  "paths": {
    "instruction_set": "C:\\Processors\\custom_big_endian.xlsx"
  }
}
```

**config/debug.json** (Debug build with all outputs):
```json
{
  "architecture": {
    "endianness": "little",
    "word_size": 32
  },
  "output": {
    "generate_lst": true,
    "generate_bin": true,
    "generate_hex": true,
    "generate_map": true
  }
}
```

**config/release.json** (Release build, binary only):
```json
{
  "output": {
    "generate_lst": false,
    "generate_bin": true,
    "generate_hex": false,
    "generate_map": false
  }
}
```

**Complete Workflow Example:**
```bash
# Development: Use debug config with all outputs and listing
TASM -c config/debug.json -l dev_build.lst -o dev_build.bin source.asm

# Testing: Use test config with specific instruction set
TASM -c config/test.json -s test_data/test_instruction_set.xlsx -l test.asm

# Production: Use release config for optimized binary only
TASM -c config/release.json -f bin -o release/firmware.bin source.asm

# Cross-platform: Different configs for different targets
TASM -c config/tricore_tc16.json -o build/tricore/app.bin source.asm
TASM -c config/tricore_tc18.json -o build/tricore18/app.bin source.asm
```

### Instruction Set Configuration

```bash
# Use default TriCore 1.8 instruction set (from config)
TASM source.asm

# Use custom instruction set CSV file (overrides config)
TASM -s data/custom_instruction_set.csv source.asm

# Long option for instruction set
TASM --instruction-set=data/legacy_tricore.csv source.asm

# Combine with output format
TASM -s data/tricore_1.8_instruction_set.csv -f bin -o program.bin source.asm

# Custom config with instruction set override
TASM -c config/custom.json -s data/alternate_set.xlsx source.asm
```

### Output Directory Configuration

```bash
# Use default output directory from config (output/assembly_build)
TASM source.asm

# Override output directory with custom path (relative to project root)
TASM -D output/custom_build source.asm

# Use absolute path for output directory
TASM -D C:\Projects\builds\release source.asm

# Long form syntax
TASM --output-dir output/debug_build source.asm

# Combined syntax
TASM --output-dir=output/test_build source.asm

# Combine with other output options
TASM -D output/release -f bin -o firmware.bin source.asm

# Multiple builds with different output directories
TASM -D output/build_v1 -o app_v1.bin source_v1.asm
TASM -D output/build_v2 -o app_v2.bin source_v2.asm
```

**Use Cases for Custom Output Directories:**
- **Build Isolation**: Separate builds for different configurations
- **CI/CD Pipelines**: Custom paths for automated builds
- **Team Workflows**: Personal build directories without conflicts
- **Testing**: Isolated test build artifacts
- **Version Management**: Keep builds organized by version

**Output Directory Behavior:**
- Config file specifies default: `"output_dir": "output/assembly_build"`
- Command-line `-D` or `--output-dir` overrides config setting
- All intermediate files (.obj, .map, .log, .lst) go to this directory
- Final output file location controlled by `-o` option (can be different)
- If `-o` not specified, final output also goes to output directory

**Example Workflow:**
```bash
# Configure default output directory in config/tasm_config.json
{
  "paths": {
    "output_dir": "output/assembly_build"
  }
}

# Use default output directory
TASM source.asm  # Outputs to: output/assembly_build/

# Override for specific build
TASM -D build/release source.asm  # Outputs to: build/release/

# Override and specify final output location
TASM -D build/temp -o dist/firmware.bin source.asm
# Intermediates in: build/temp/
# Final binary at: dist/firmware.bin
```

### Intel HEX Generation

```bash
# Generate Intel HEX format
TASM -f hex -o program.hex source.asm

# Intel HEX with verbose output
TASM -f hex --verbose -o program.hex source.asm

# Intel HEX automatically handles 32-bit addressing with extended records
TASM -f hex -o firmware.hex embedded_code.asm
```

**Endianness in Output Files:**

All output formats respect the configured endianness setting:

**Binary Files (.bin):**
- Raw bytes in configured byte order
- Little-endian: `DF 04 00 80 3B 00 02 00 ...`
- Big-endian: `80 00 04 DF 00 02 00 3B ...`

**Intel HEX Files (.hex):**
- Data records contain bytes in configured order
- Example line (little-endian): `:10800000DF0400803B0002001D0000003B00021089`
- The data portion `DF0400803B0002001D0000003B000210` shows little-endian bytes

**Memory Verification:**
```powershell
# PowerShell: View binary file in hex
Format-Hex -Path program.bin | Select-Object -First 5

# Example output (little-endian):
#          Offset Bytes                                           
#          ------ -----------------------------------------------
# 0000000000000000 DF 04 00 80 3B 00 02 00 1D 00 00 00 3B 00 02 10
# 0000000000000010 8F 01 01 00 91 30 00 0F D9 00 04 0A 74 00 00 90
```

### Plain Text Generation

```bash
# Generate plain text format with ADDRESS OPCODE pairs
TASM -f txt -o program.txt source.asm

# Plain text output shows 32-bit addresses and 16-bit or 32-bit opcodes
# Example output:
# 0000A000 8000
# 0000A002 D4001234
# 0000A006 0009

# Combine with informational output
TASM -f txt --info -o disassembly.txt source.asm
```

### Listing Files

```bash
# Generate listing file with automatic naming (source.lst)
TASM -l source.asm

# Generate listing file with custom name
TASM -l myprogram.lst source.asm

# Combine listing with binary output
TASM -l -f bin -o program.bin source.asm

# Generate detailed listing with debug info
TASM -l program.lst --debug source.asm
```

Listing files provide a human-readable representation of the assembly process, showing:
- **32-bit addresses** in hexadecimal format (e.g., `80000000`)
- **Machine code bytes** in configured endianness (e.g., `3B 00 02 00` for little-endian)
- **16-bit instructions** shown as 2 bytes (e.g., `74 00`)
- **32-bit instructions** shown as 4 bytes (e.g., `DF 04 00 80`)
- **Original source lines** with comments preserved
- **Symbol table** with labels and their addresses
- **MASM-compatible formatting** for integration with existing workflows

**Endianness in Listing Files:**

Little-endian example (TriCore):
```
80000030  3B 00 02 00         mov d0, #0x20
80000034  1D 00 00 00         j common
80000048  74 00               st.w [a0], d0
```

The byte sequence `3B 00 02 00` represents opcode `0x0002003B` with LSB first.

Big-endian example (hypothetical):
```
80000030  00 02 00 3B         mov d0, #0x20
80000034  00 00 00 1D         j common
80000048  00 74               st.w [a0], d0
```

The byte sequence `00 02 00 3B` represents opcode `0x0002003B` with MSB first.

### Preprocessing

```bash
# Preprocess only, output to stdout
TASM -E source.asm

# Preprocess to file
TASM -E -o preprocessed.asm source.asm

# Preprocess with macro definitions
TASM -E -DDEBUG=1 -DVERSION=2 source.asm
```

### Macro Expansion Files

```bash
# Include single macro file
TASM -m macros/system.asm -o program.bin source.asm

# Include multiple macro files  
TASM -m macros/system.asm -m macros/math.asm -o program.bin source.asm

# Long form syntax
TASM --macro-file macros/system.asm --macro-file macros/math.asm -o program.bin source.asm

# Combined syntax
TASM --macro-file=macros/system.asm --macros=macros/math.asm -o program.bin source.asm

# Include macro files with custom instruction set
TASM -s data/tricore_1.8_instruction_set.csv -m macros/tricore.asm -o program.bin source.asm

# Preprocess with macro files
TASM -E -m macros/system.asm -m macros/math.asm source.asm

# Disable macro expansion (use source code as-is)
TASM --no-macros -o program.bin source.asm

# Disable macros with macro files still available for reference (they won't be applied)
TASM --no-macros -m macros/system.asm -o program.bin source.asm
```

**Macro Expansion Control:**

By default, TASM performs macro expansion in Phase 1 of the three-phase compilation process. You can control this behavior:

**Enable (default):**
- Macros defined in source file are expanded
- Macros from `-m` files are included and expanded
- Config setting: `"enable_macros": true`

**Disable:**
- Use `--no-macros` flag to skip macro expansion completely
- Source code is used as-is without any macro processing
- Useful for: debugging, GCC-generated files, pre-expanded code
- Config setting: `"enable_macros": false` (overridden by `--no-macros`)

**Use Cases for Disabling Macros:**
- **GCC Integration**: Source files from GCC toolchain (already preprocessed)
- **Debugging**: Isolate issues unrelated to macro expansion
- **Pre-expanded Code**: Source already contains expanded code
- **Performance**: Skip macro phase for files without macros
- **Compatibility**: Work with assemblers that don't support TASM macro syntax

### Console Output and Logging

```bash
# Quiet mode (default) - shows only errors and aborts
TASM -f bin -o program.bin source.asm
# Output: Header, phase names, build summary (errors only)

# Informational output - shows progress messages
TASM --info -f bin -o program.bin source.asm  
# Output: Header, detailed phase progress, build summary

# Verbose output - shows all messages
TASM --verbose -f bin -o program.bin source.asm

# Debug output - shows debug information
TASM --debug -f bin -o program.bin source.asm
```

**Example Console Output:**
```
TASM version 1.0.0 compiled on 2025-11-01-- Crafted by Gino Latino
Pre-processing the source code file... 20 lines of code loaded
Compiling, 1st pass... Macro expansion and assembly
Linking, 1st pass... Resolving symbols
Linking, 2nd pass... Finalizing

Build completed successfully.
Size: 359 bytes ($0167) in 1.121s (3.1 msec/byte)
Opcodes: 6 opcodes ($06) in 1.121s (186.9 msec/opcode)
Output: output/assembly_build_20241101_143022/tricore_basic_test.bin
```

### Listing and Debug Information

```bash
# Generate listing file
TASM -f bin -o program.bin -l program.lst source.asm

# Generate with debug information
TASM -f elf64 -g -o program.o source.asm

# Verbose compilation
TASM --verbose -f bin -o program.bin source.asm
```

### Optimization Levels

TASM supports multiple optimization flags to control code generation and instruction selection:

```bash
# No optimization
TASM -O0 source.asm

# Minimal optimization  
TASM -O1 source.asm

# Force 32-bit instruction variants (override default 16-bit preference)
TASM -O32 source.asm

# Multipass optimization (default)
TASM -Ox source.asm
```

#### `-O32` Force 32-Bit Variants

The `-O32` flag forces the assembler to use 32-bit instruction variants when multiple encoding sizes are available, overriding the default code-size optimization that prefers 16-bit variants.

**When to Use `-O32`:**

1. **Matching Reference Compiler Output**
   ```bash
   # Generate binary that exactly matches reference compiler's encoding
   TASM -O32 -o firmware.bin source.asm
   ```
   When validating against a reference toolchain that uses 32-bit variants, `-O32` ensures bit-exact matching.

2. **Processor-Specific Requirements**
   ```bash
   # Some TriCore variants may have timing differences with 16-bit vs 32-bit instructions
   TASM -O32 -o embedded_code.bin source.asm
   ```
   Certain processor revisions or real-time applications may require consistent 32-bit instruction timing.

3. **Consistent Instruction Alignment**
   ```bash
   # All instructions aligned on 32-bit boundaries for cache optimization
   TASM -O32 -f bin -o aligned_code.bin source.asm
   ```
   32-bit alignment can improve instruction cache performance on some architectures.

4. **Debugging and Analysis**
   ```bash
   # Easier disassembly with uniform instruction sizes
   TASM -O32 -l debug.lst source.asm
   ```
   32-bit instructions are more predictable when analyzing machine code or debugging.

**Example: ST.W Instruction Variants**

Without `-O32` (default code-size optimization):
```assembly
st.w [a12], 176, d15    ; Assembles to: 0x0278 (16-bit)
```

With `-O32` flag:
```assembly
st.w [a12], 176, d15    ; Assembles to: 0x2930CF89 (32-bit)
```

**Trade-offs:**
- ✅ **Pros**: Exact reference matching, consistent timing, better alignment
- ❌ **Cons**: Larger code size (up to 2x for affected instructions), slightly slower compilation

**Technical Details:**

Many TriCore instructions have multiple encoding variants:
- **16-bit variants**: Limited register sets, smaller immediate ranges
- **32-bit variants**: Full register access, larger immediate values

By default, TASM selects the smallest variant that can encode the instruction. The `-O32` flag filters out 16-bit variants during instruction selection, ensuring only 32-bit (or larger) variants are used.

**Verification:**
```bash
# Compare output with and without -O32
TASM -f txt -o default.txt source.asm
TASM -O32 -f txt -o force32.txt source.asm

# PowerShell: Compare file sizes
(Get-Item default.bin).Length
(Get-Item force32.bin).Length
```

#### `-Ono-implicit` Disable Implicit Operands

The `-Ono-implicit` flag disables instruction variants that use implicit operands (`A[10]` or `A[15]`), forcing the assembler to select only explicit operand variants.

**When to Use `-Ono-implicit`:**

1. **Matching Reference Compiler Output**
   ```bash
   # Generate binary matching compiler that avoids implicit operands
   TASM -Ono-implicit -o firmware.bin source.asm
   ```
   Many reference compilers prefer explicit operands for clarity and consistency.

2. **Code Portability**
   ```bash
   # Ensure code doesn't rely on architecture-specific shortcuts
   TASM -Ono-implicit -f bin -o portable_code.bin source.asm
   ```
   Explicit operands make code more portable across processor variants.

3. **Encoding Validation**
   ```bash
   # Validate against test suites that use explicit operands
   TASM -Ono-implicit -f txt -o explicit_encoding.txt test.asm
   ```
   Useful when comparing against reference implementations.

**Example: LD.BU Instruction Variants**

Without `-Ono-implicit` (default - uses implicit A[15]):
```assembly
ld.bu d15,[a15], 4      ; Assembles to: 0xF40C (16-bit, uses implicit A[15])
```

With `-Ono-implicit` flag:
```assembly
ld.bu d15,[a15], 4      ; Assembles to: 0x08C4FF09 (32-bit, explicit operands)
```

**Trade-offs:**
- ✅ **Pros**: Matches reference output, explicit encoding, better portability
- ❌ **Cons**: Larger code size, may not use most efficient encoding

**Technical Details:**

TriCore instructions often have variants with implicit `A[10]` or `A[15]` operands that produce shorter encodings. The `-Ono-implicit` flag filters these variants during instruction selection, ensuring only explicit-operand variants are used.

**Verification:**
```bash
# Compare output with and without -Ono-implicit
TASM -f txt -o default.txt source.asm
TASM -Ono-implicit -f txt -o explicit.txt source.asm

# PowerShell: Compare file sizes
(Get-Item default.bin).Length
(Get-Item explicit.bin).Length
```

### Makefile Dependencies

```bash
# Generate dependencies
TASM -M source.asm

# Generate dependencies to file
TASM -MF deps.d source.asm
```

## NASM Compatibility

TASM provides high compatibility with NASM command-line syntax:

### ✅ **Compatible Features**

- **Command Syntax**: Identical to NASM command-line patterns
- **Option Parsing**: Supports both separated (`-f bin`) and combined (`-fbin`) syntax
- **Help System**: NASM-style help output with complete option listing
- **Version Display**: Standard version information format
- **Error Messages**: Follow NASM error message format (`TASM: error: message`)
- **Preprocess Mode**: Clean stdout output with `-E` option
- **Exit Codes**: Standard exit codes (0 = success, 1 = error)

### 🔄 **Enhanced Features**

- **Three-Phase Compilation**: TASM adds macro expansion and linking phases
- **Comprehensive Logging**: Detailed build logs and JSON summaries
- **Verbose Mode**: Extended debugging information
- **Build Summaries**: Automatic generation of build reports

### ⚠️ **Current Limitations**

- Multiple input files not yet supported
- Some advanced NASM-specific features may not be implemented
- Instruction set may differ from NASM (TASM uses custom instruction set)

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | Error (compilation failed, invalid arguments, file not found) |

## Macro File Templates

Macro files are reusable collections of macro definitions that can be included in multiple assembly projects. They allow you to create standard libraries of common operations and constants.

### Creating Macro Files

Macro files contain only macro definitions:

**macros/system.asm**:
```assembly
; System constants and macros
#define STACK_SIZE 0x2000
#define HEAP_SIZE 0x4000
#define ZERO_REG(reg) MOV reg, #0
#define SET_STACK(reg) MOV reg, #STACK_SIZE
```

**macros/math.asm**:
```assembly
; Mathematical operation macros
#define ABS_VALUE(result, input) \
    CMP input, #0 ; \
    JGE skip_abs ; \
    NEG result, input ; \
    JMP done_abs ; \
skip_abs: ; \
    MOV result, input ; \
done_abs:
```

### Using Multiple Macro Files

```bash
# Include both system and math macros
TASM -m macros/system.asm -m macros/math.asm -o program.bin main.asm
```

In **main.asm**:
```assembly
start:
    ZERO_REG(D[0])           ; From system.asm
    SET_STACK(A[14])         ; From system.asm
    ABS_VALUE(D[1], D[2])    ; From math.asm
```

### Macro File Processing Order

1. Macro files are processed in the order specified on command line
2. Later macro definitions override earlier ones with the same name
3. Source file macros override macro file definitions
4. All macro files are processed before the main source file

## Three-Phase Compilation

TASM implements a unique three-phase compilation process:

### Phase 1: Macro Expansion
- Processes macro definitions and expansions
- Handles include files and conditional assembly
- Generates expanded assembly source

### Phase 2: Assembly  
- Parses assembly instructions and directives
- Performs symbol resolution and address calculation
- Generates object code with symbol tables

### Phase 3: Linking
- Links multiple object files (when supported)
- Resolves external symbols and references
- Generates final executable or object file

Each phase includes comprehensive error checking and detailed logging.

## Version Information

```
TASM version 1.0.0 compiled on 2025-11-01
```

To check your version:
```bash
TASM -v
TASM --version
```

## Examples in Context

### Simple Program Assembly

```bash
# Source file: hello.asm
TASM -f bin -o hello.bin hello.asm
```

### Output Format Examples

```bash
# Binary format (default)
TASM -f bin -o program.bin source.asm

# Intel HEX format
TASM -f hex -o program.hex source.asm
```

### Build System Integration

```makefile
# Makefile example
%.o: %.asm
	TASM -f hex -o $@ $<

program: main.o module.o
	ld -o program main.o module.o
```

## File Organization and Output Management

TASM maintains clean workspace organization by containing all build artifacts in dedicated output directories:

### Project Directory Structure
```
project_root/
├── config/
│   └── tasm_config.json               # Configuration file
├── src/
│   ├── TASM.py                        # Main assembler
│   ├── config_loader.py               # Config parser (singleton)
│   ├── assembler.py                   # Assembly engine
│   ├── linker.py                      # Linker engine
│   └── instruction_encoder.py         # Instruction encoder
├── data/
│   └── *.asm                          # Source assembly files
├── Processors/
│   └── tricore/
│       └── data/
│           ├── languages/
│           │   └── *.xlsx             # Instruction set definitions
│           └── manuals/
│               └── *.pdf              # Reference manuals
└── output/
    └── assembly_build_*/              # Build output directories
```

### Build Directory Structure
```
output/
└── assembly_build_YYYYMMDD_HHMMSS/    # Timestamped build directories
    ├── source_expanded.asm             # Phase 1: Expanded source
    ├── source.obj                      # Phase 2: Object file  
    ├── source.bin                      # Phase 3: Binary output
    ├── source.hex                      # Intel HEX output (if enabled)
    ├── source.lst                      # Listing file (if -l specified)
    ├── source.map                      # Memory map file
    ├── build.log                       # Detailed build log
    └── build_summary.json              # JSON build report
```

### Output File Behavior
- **Intermediate Files**: Always created in `output/assembly_build_*/` directories
- **Final Output**: 
  - Default: Created in build directory with appropriate extension
  - With `-o`: Created at specified location, intermediates remain in build directory
- **Logs and Reports**: Always in build directory for traceability

### Clean Workspace
- **Root Directory**: Remains clean of build artifacts
- **Source Preservation**: Original source files never modified
- **Build Isolation**: Each build gets its own timestamped directory

### PowerShell Usage Notes

When using TASM in PowerShell, quote arguments containing dots to prevent token splitting:

```powershell
# Correct
TASM -fbin "-otest.bin" source.asm

# May cause issues (PowerShell splits .bin as separate token)
TASM -fbin -otest.bin source.asm
```

## Configuration Troubleshooting

### Common Configuration Issues

**Config File Not Found (Default):**
```
Error: Configuration file not found: C:\...\config\tasm_config.json
```
**Solution:** Create the default config file or specify a custom config with `-c` option.

**Custom Config File Not Found:**
```
Error: Configuration file not found: path/to/custom_config.json
```
**Solution:** 
- Verify the path is correct (check for typos)
- Use absolute path if relative path doesn't work
- Ensure file exists: `Test-Path path/to/custom_config.json` (PowerShell)
```bash
# Verify config file exists
TASM -c config/test.json source.asm  # Will fail if not found

# Use absolute path
TASM -c C:\Projects\config\test.json source.asm
```

**Invalid JSON Syntax:**
```
Error: Invalid JSON in configuration file: Expecting ',' delimiter
```
**Solution:** Validate JSON syntax using a JSON validator or editor with syntax checking.

**Instruction Set File Not Found:**
```
Warning: Instruction set file not found, using default
```
**Solution:** Update `paths.instruction_set` in config file with correct absolute path.

**Permission Denied:**
```
Error: Cannot read configuration file: Permission denied
```
**Solution:** Check file permissions and ensure TASM has read access.

### Configuration Verification

Verify your configuration is loaded correctly:

```bash
# Run TASM with verbose output to see config loading (default config)
TASM --verbose source.asm

# Run with custom config and verbose output
TASM -c config/test.json --verbose source.asm

# Look for these log messages:
# "Using instruction set from config: C:\path\to\instruction_set.xlsx"
# "Loaded N instructions from C:\path\to\file"
```

**Testing Custom Configs:**
```bash
# Test with different configs to verify behavior
TASM -c config/little_endian.json -l test.asm
TASM -c config/big_endian.json -l test.asm

# Compare listing files to verify endianness
# Little-endian: 3B 00 02 00
# Big-endian:    00 02 00 3B
```

### Configuration Reset

To reset to default configuration:

1. Backup current config: `copy config\tasm_config.json config\tasm_config.backup.json`
2. Delete config file: `del config\tasm_config.json`
3. Create new default config with little-endian, 32-bit settings
4. Update paths to match your installation

### Configuration for Different Processors

**TriCore TC1.6 (Default):**
```json
{
  "architecture": {
    "endianness": "little",
    "word_size": 32
  },
  "paths": {
    "instruction_set": "C:\\...\\tricore_tc1.6_instruction_set.xlsx"
  }
}
```

**Hypothetical Big-Endian 16-bit Processor:**
```json
{
  "architecture": {
    "endianness": "big",
    "word_size": 16
  },
  "paths": {
    "instruction_set": "C:\\...\\custom_processor_16bit.xlsx"
  }
}
```

---

**TASM** provides professional-grade assembly with industry-standard command-line compatibility, centralized configuration management, and clean workspace organization, making it suitable for integration into existing development workflows and build systems.