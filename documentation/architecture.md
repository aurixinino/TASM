# TASM Architecture Overview

**TASM** (Three-Phase Assembler) implements a sophisticated three-phase compilation architecture with **external instruction set support**. The system provides robust assembly processing with comprehensive error handling, NASM-compatible interface, and flexible instruction set loading from multiple file formats.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [External Instruction Set System](#external-instruction-set-system)
- [Phase 1: Macro Expansion](#phase-1-macro-expansion)
- [Phase 2: Assembly with External Encoding](#phase-2-assembly-with-external-encoding)
- [Phase 3: Linking](#phase-3-linking)
- [Core Components](#core-components)
- [Error Handling](#error-handling)
- [Logging System](#logging-system)

## Architecture Overview

```
External Instruction Set (.xlsx/.json/.xml)
       ↓
┌──────────────────┐
│ Instruction Set  │
│     Loader       │ → In-Memory Instruction Database
└──────────────────┘
       ↓
Source File (.asm) + Macro Files (.h/.asm)
       ↓
┌──────────────────┐
│  Phase 1: Macro  │ → Expanded Source (.asm)
│    Expansion     │
└──────────────────┘
       ↓
┌──────────────────┐
│  Phase 2: External│ → Object File (.obj)
│  Instruction     │
│    Encoding      │
└──────────────────┘
       ↓
┌──────────────────┐
│  Phase 3: Linking│ → Binary/Executable
│                  │
└──────────────────┘

Enhanced TriCore Instruction Set: 589 instructions
Valid Opcodes: 513/589 (87.1%)
Enhanced Syntax: 449/589 (76.2%)
```

## Phase 1: Macro Expansion

The macro expansion phase processes assembly source files to expand macros, handle includes, and prepare clean assembly code for the assembler.

### Responsibilities:
- **Macro Definition Processing**: Collect and validate macro definitions
- **Macro Expansion**: Replace macro calls with expanded code
- **Include File Processing**: Handle file inclusions and path resolution
- **Conditional Assembly**: Process conditional directives
- **Comment Preservation**: Maintain source comments for debugging

### Input/Output:
- **Input**: Source assembly files (`.asm`)
- **Output**: Expanded assembly files (`*_expanded.asm`) in timestamped build directory

## External Instruction Set System

TASM now implements a revolutionary **external instruction set architecture** that completely replaces hardcoded instruction encoding with a flexible, file-based approach. This system supports multiple file formats and enables easy processor architecture changes without recompilation.

### Supported Instruction Set Formats:
- **Excel (.xlsx)**: Primary format using `Processors/tricore/data/languages/tricore_tc1.6_instruction_set.xlsx`
- **JSON (.json)**: Structured data format for programmatic access
- **XML (.xml)**: Hierarchical format for complex instruction definitions
- **CSV (.csv)**: Legacy format (still supported for backward compatibility)

### Default Instruction Set:
`Processors/tricore/data/languages/tricore_tc1.6_instruction_set.xlsx`
- **120 Instructions**: Tricore reduced instruction set (tricore_reduced_instruction_set sheet)
- **Complete Operand Mapping**: Position and length data for all 5 operand fields
- **32-bit Instruction Encoding**: Full support for Tricore's 32-bit instruction format

### Instruction Definition Structure:
Each instruction contains:
- **OpCode**: 32-bit hex value (e.g., `0x01C0000B`)
- **Syntax**: Assembly syntax pattern (e.g., `ABS D[c],D[b]`)
- **OperandCount**: Number of operands (0-5)
- **Operand Fields**: Position and length for each operand (op1_pos, op1_len, etc.)

### Encoding Algorithm:
1. **Parse** assembly instruction (e.g., `ABS d1, d3` → `ABS 1, 3` after macro expansion)
2. **Match** with instruction set by mnemonic and operand count
3. **Validate** operand count matches expected
4. **Calculate** operand bit fields:
   - `Op1_mask = (1 << op1_len) - 1`
   - `Op1 = (operand_value & Op1_mask) << op1_pos`
5. **Combine** final instruction: `OpCode | Op1 | Op2 | ... | Op5`

### Example Encoding:
```
ABS d1, d3  (after macro expansion: ABS 1, 3)
├─ Base OpCode: 0x01C0000B
├─ Op1 (d1=1): (1 & 0xF) << 28 = 0x10000000  
├─ Op2 (d3=3): (3 & 0xF) << 12 = 0x00003000
└─ Final: 0x01C0000B | 0x10000000 | 0x00003000 = 0x11C0300B
```

### Instruction Categories:
- **Arithmetic**: 214 instructions (ADD, SUB, MUL, DIV, MADD, MSUB)
- **Logical**: 55 instructions (AND, OR, XOR, NOT, NAND, NOR)
- **Memory**: 99 instructions (LD, ST, LEA, SWAP, CACHE)
- **Control**: 40 instructions (J, CALL, RET, LOOP, BR)
- **System**: 7 instructions (RFE, RFM, TRAP, NOP)
- **Floating Point**: 6 instructions (.F, .DF variants)
- **Packed**: 21 instructions (.B, .H, .W, PACK, UNPACK)

### Opcode Validation:
TASM includes comprehensive opcode testing capabilities through:
- `scripts/tasm_opcode_comprehensive_test.py`: Full instruction set analysis
- `scripts/tasm_integration_test.py`: Real assembly validation testing

### Key Features:
- Recursive macro expansion support
- Include path resolution
- Macro parameter substitution
- Line number tracking for error reporting
- Clean workspace management (all outputs in `output/assembly_build_*/`)

## Phase 2: Assembly with External Encoding

The assembly phase uses the **external instruction set system** to convert expanded assembly source into precise binary object code with comprehensive instruction validation.

### New External Encoding Responsibilities:
- **Instruction Set Loading**: Load instruction definitions from Excel/JSON/XML files
- **Smart Instruction Parsing**: Parse assembly with flexible operand formats
- **Precise Instruction Matching**: Match by mnemonic and operand count
- **Bitfield Calculation**: Calculate precise operand bit positions and masks
- **32-bit Binary Generation**: Generate accurate 32-bit instruction encodings

### Core Components:

#### InstructionSetLoader (`src/instruction_loader.py`)
- Loads instruction sets from multiple formats (.xlsx, .json, .xml)
- Creates in-memory instruction database with 120+ instruction definitions
- Supports instruction lookup by mnemonic and operand count
- Provides format conversion capabilities (Excel → JSON export)

#### InstructionEncoder (`src/instruction_encoder.py`)
- Parses assembly lines into structured instruction objects
- Validates operand counts against instruction set requirements
- Handles multiple operand formats: registers (d1, D[1]), immediates (#255, 0xFF)
- Calculates precise bit field encoding using position/length metadata
- Combines base opcode with encoded operands for final 32-bit value

### Two-Pass Assembly Process:

#### Pass 1: Symbol Collection & Instruction Validation
- Scan source for labels and symbols
- Calculate addresses and build symbol table
- **Pre-validate all instructions** against external instruction set
- Check operand counts and syntax compatibility
- Report detailed encoding errors with line numbers

#### Pass 2: Precision Code Generation
- **Load external instruction set** into memory (120 Tricore instructions)
- Generate machine code using **exact bit field calculations**
- Resolve symbol references where possible
- Create relocation entries for external symbols
- **Output verified object file** with validated instruction encodings

### Input/Output:
- **Input**: Expanded assembly files (`*_expanded.asm`) from build directory
- **Output**: Object files (`.obj`) with symbol tables in same build directory

## Phase 3: Linking

The linking phase combines object files, resolves external symbols, and generates the final executable or library.

### Responsibilities:
- **Object File Loading**: Load and parse object files
- **Symbol Resolution**: Resolve external symbol references
- **Address Relocation**: Adjust addresses for final memory layout
- **Binary Generation**: Create final executable or object file

### Linking Process:
1. **Load Object Files**: Parse object files and extract symbols
2. **Build Global Symbol Table**: Merge symbol tables from all objects
3. **Resolve References**: Match symbol references with definitions
4. **Apply Relocations**: Adjust addresses based on final layout
5. **Generate Output**: Create final binary or executable file

### Input/Output:
- **Input**: Object files (`.obj`) from build directory
- **Output**: Binary files (`.bin`) or executables in build directory (copied to user-specified location if `-o` used)

## Core Components

### `TASM.py` - Main Entry Point
- NASM-compatible command-line interface
- Argument parsing and validation
- Compilation orchestration
- Error handling and reporting

### `macro.py` - MacroExpander
```python
class MacroExpander:
    def process_file(source_file, output_file) -> bool
    def collect_macros(lines) -> Dict[str, Macro]
    def expand_macros(lines, macros) -> List[str]
```

### `assembler.py` - AssemblerEngine  
```python
class AssemblerEngine:
    def assemble_file(source_file, object_file) -> bool
    def first_pass(lines) -> Dict[str, int]
    def second_pass(lines, symbols) -> bytes
```

### `linker.py` - Linker
```python
class Linker:
    def link_files(object_files, output_file, base_address) -> bool
    def load_object_file(obj_file) -> ObjectInfo
    def resolve_symbols(objects) -> Dict[str, int]
```

### `compiler_logger.py` - Logging System
```python
def initialize_logger(log_file, console_output=True) -> Logger
def log_info(message, **kwargs)
def log_error(message, error_code=None, **kwargs)
def print_build_summary()
```

### `utils.py` - Utility Functions
```python
def create_output_dir(prefix) -> Path
def parse_number(value) -> int
def validate_identifier(name) -> bool
```

## TriCore Instruction Set Architecture

TASM now supports the **TriCore instruction set architecture**, providing comprehensive assembly for TriCore processors used in automotive and industrial applications.

### TriCore Instruction Set Features:
- **526 Instruction Variants**: Supporting 209 unique mnemonics across the full TriCore instruction set
- **External CSV Configuration**: Instruction set loaded dynamically from `data/tricore_instruction_set.csv`
- **Variable Instruction Sizes**: Supporting both 16-bit and 32-bit instruction formats
- **Complex Operand Syntax**: Advanced operand patterns with register addressing, immediate values, and scaled indexing
- **Pandas-Based Loading**: Efficient CSV parsing and instruction set management

### Instruction Set Structure:
The TriCore instruction set is defined in `data/tricore_instruction_set.csv` with the following format:
```csv
OpCode,OpCodeSize,Instruction,LongName,Syntax,LongDescription,Reference
0x01C0000B,32,"ABS","Absolute Value","ABS D[c],D[b]","See pag.49",
0x0000008B,32,"ADD","Add","ADD D[c],D[a],const9","See pag.59",
0x42,16,"ADD","Add","ADD D[a],D[b]","See pag.60",
```

### Key Fields:
- **OpCode**: Hexadecimal instruction opcode (16-bit or 32-bit)
- **OpCodeSize**: Instruction size in bits (16 or 32)
- **Instruction**: Assembly mnemonic (e.g., ADD, ABS, ADDI)
- **Syntax**: Full instruction syntax pattern with operands
- **LongName/LongDescription**: Human-readable instruction documentation

### Instruction Categories:
- **Arithmetic**: ADD, SUB, MUL, DIV variants with saturation support
- **Logical**: AND, OR, XOR, NOT operations with bit manipulation
- **Load/Store**: Memory access with various addressing modes
- **Branch/Jump**: Conditional and unconditional control flow
- **System**: Processor control and status operations
- **Special**: Packed operations for SIMD-style processing

### Syntax Matching:
TASM implements intelligent syntax matching to automatically select the correct instruction variant:
```assembly
ADD D[0],D[1]           ; Matches 16-bit ADD D[a],D[b] format
ADD D[c],D[a],const9    ; Matches 32-bit ADD with immediate format
ABS D[c],D[b]           ; Matches ABS instruction syntax
```

## Error Handling

TASM implements comprehensive error handling across all phases:

### Error Categories:
- **Syntax Errors**: Invalid instruction syntax or operands
- **Symbol Errors**: Undefined symbols or duplicate definitions
- **File Errors**: Missing files or I/O failures
- **Macro Errors**: Invalid macro definitions or expansions
- **Linking Errors**: Unresolved symbols or address conflicts

### Error Reporting:
- **File and Line Information**: Precise error location reporting
- **Error Codes**: Structured error identification
- **Context Information**: Relevant code context for debugging
- **NASM-Compatible Messages**: Industry-standard error formats

### Example Error Output:
```
data\simple_test.asm:15: error: undefined symbol 'unknown_label' [UNDEFINED_SYMBOL]
TASM: error: assembly failed
```

## Logging System

TASM provides comprehensive logging with multiple output formats:

### Log Levels:
- **ERROR**: Compilation errors that prevent success
- **WARNING**: Issues that don't prevent compilation
- **INFO**: General compilation progress information
- **DEBUG**: Detailed internal processing information

### Output Formats:
- **Console Output**: Real-time compilation feedback
- **Log Files**: Detailed build logs for analysis
- **JSON Reports**: Structured build summaries for tools

### Build Summary Example:
```json
{
  "build_info": {
    "start_time": "2025-11-01 10:55:53",
    "end_time": "2025-11-01 10:55:53",
    "duration": 0.11,
    "success": true
  },
  "statistics": {
    "errors": 0,
    "warnings": 1,
    "info": 40,
    "debug": 24
  },
  "files_processed": [
    "data\\simple_test.asm"
  ]
}
```

## File Organization and Workspace Management

TASM implements clean workspace management to maintain organized development environments:

### Build Directory Structure
```
output/
└── assembly_build_YYYYMMDD_HHMMSS/    # Timestamped builds
    ├── source_expanded.asm             # Phase 1 output
    ├── source.obj                      # Phase 2 output
    ├── source.bin                      # Phase 3 output  
    ├── build.log                       # Detailed logs
    └── build_summary.json              # JSON reports
```

### Workspace Benefits:
- **Build Isolation**: Each compilation gets dedicated directory
- **Clean Root**: No intermediate files clutter workspace
- **Traceability**: Timestamped builds for debugging
- **Parallel Safe**: Multiple builds won't interfere

## Performance Considerations

### Optimization Strategies:
- **Single-Pass Parsing**: Efficient source file processing
- **Symbol Table Optimization**: Fast symbol lookup and resolution
- **Memory Management**: Efficient handling of large source files
- **Incremental Processing**: Support for partial recompilation
- **Contained Builds**: Efficient I/O with organized file structure

### Scalability Features:
- **Streaming Processing**: Handle large files without excessive memory usage
- **Modular Design**: Independent phase processing for parallel execution
- **Caching Support**: Symbol table and macro caching for faster rebuilds
- **Build Directory Management**: Automatic cleanup and organization

---

This architecture provides a solid foundation for professional assembly compilation with clean workspace management, maintaining compatibility with industry-standard tools and workflows.