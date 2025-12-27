#!/usr/bin/env python3
"""
TASM - Three-Phase Assembler

A NASM-compatible assembler with three-phase compilation:
1. Macro Expansion
2. Assembly 
3. Linking

Compatible command-line interface with NASM for seamless integration.
"""

import sys
import os
from pathlib import Path
import argparse
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from logger import (
    initialize_logger, log_info, log_error, log_warning, log_debug, log_abort, log_fatal,
    print_build_summary, export_build_summary_json, get_logger, LogLevel
)
from utils import create_output_dir
from macro import MacroExpander
from assembler import AssemblerEngine
from linker import Linker
from config_loader import get_config

# Version information
TASM_VERSION = "1.0.0"
TASM_DATE = "2025-11-01"

# Console output functions
def print_header():
    """Print custom TASM header"""
    print(f"TASM version {TASM_VERSION} compiled on {TASM_DATE}-- Created by Gino Latino")
    print()

def print_phase(phase_name: str, details: str = ""):
    """Print phase progress"""
    if details:
        print(f"{phase_name}... {details}")
    else:
        print(f"{phase_name}...")

def print_enhanced_summary(output_file_path: Optional[Path] = None, instruction_count: int = 0,
                          linker: Optional['Linker'] = None, output_format: str = 'bin'):
    """Print enhanced build summary"""
    logger = get_logger()
    
    # Get timing information
    start_time = getattr(logger, 'start_time', datetime.now())
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("============================================================")
    print("COMPILATION SUMMARY") 
    print("============================================================")
    
    # Calculate stats
    stats = logger.stats
    total_messages = sum(stats.values())
    
    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    # Build status
    error_count = stats[LogLevel.ERROR] + stats[LogLevel.ABORT] + stats[LogLevel.FATAL]
    
    if error_count == 0:
        print(f"{GREEN}BUILD SUCCEEDED{RESET}")
        
        # Get file size information
        file_size = 0
        if output_file_path and output_file_path.exists():
            file_size = output_file_path.stat().st_size
        
        # Calculate performance metrics
        msec_per_byte = (duration * 1000 / file_size) if file_size > 0 else 0
        msec_per_opcode = (duration * 1000 / instruction_count) if instruction_count > 0 else 0
        
        print(f"Size: {file_size} bytes in {duration:.3f}s ({msec_per_byte:.1f} msec/byte)")
        print(f"Opcodes: {instruction_count} opcodes in {duration:.3f}s ({msec_per_opcode:.1f} msec/opcode)")
        print()
        
        # Print linker information if available
        if linker:
            print(f"Memory range: 0x{linker.min_addr:08X} - 0x{linker.max_addr:08X}")
            print(f"Instructions: {linker.instruction_count}")
            if linker.map_file_path:
                print(f"Map file generated: {linker.map_file_path}")
            # Print output file information
            if output_file_path:
                format_name = output_format.upper() if output_format != 'bin' else 'Binary'
                print(f"Output ({format_name}) file generated: {output_file_path}")
    else:
        print(f"{RED}BUILD FAILED{RESET}")
    
    print()
    print("STATISTICS:")
    print(f"  Errors:        {stats[LogLevel.ERROR]}")
    print(f"  Warnings:      {stats[LogLevel.WARNING]}")  
    print(f"  Info:          {stats[LogLevel.INFO]}")
    print(f"  Debug:         {stats[LogLevel.DEBUG]}")
    print(f"  Aborts:        {stats[LogLevel.ABORT]}")
    print(f"  Fatal:         {stats[LogLevel.FATAL]}")
    print(f"  Total:         {total_messages}")
    print()

# Output format mapping (NASM-compatible)
OUTPUT_FORMATS = {
    'bin': 'Binary flat file',
    'hex': 'Intel HEX format',
    'txt': 'Plain text with addresses and opcodes'
}

def check_for_errors() -> bool:
    """Check if there are any errors that should stop compilation"""
    logger = get_logger()
    error_count = (logger.stats[LogLevel.ERROR] + 
                  logger.stats[LogLevel.ABORT] + 
                  logger.stats[LogLevel.FATAL])
    return error_count == 0

def compile_assembly_file(source_file: Path, output_file: Optional[Path] = None, 
                         base_address: int = 0x80000000, 
                         output_format: str = 'bin',
                         listing_file: Optional[Path] = None,
                         preprocess_only: bool = False,
                         output_dir: Optional[Path] = None,
                         instruction_set_file: Optional[Path] = None,
                         macro_files: Optional[List[str]] = None,
                         force_32bit: bool = False,
                         no_implicit: bool = False,
                         no_macros: bool = False) -> Tuple[bool, Optional['Linker']]:
    """
    Compile a single assembly file through all three phases
    
    Args:
        source_file: Source assembly file
        output_dir: Directory for intermediate and output files
        base_address: Base address for linking
        
    Returns:
        Tuple of (success status, linker instance or None)
    """
    log_info(f"=== COMPILATION STARTED ===")
    log_info(f"Source file: {source_file}")
    log_info(f"Output directory: {output_dir}")
    log_info(f"Base address: 0x{base_address:08X}")
    if instruction_set_file:
        log_info(f"Instruction set: {instruction_set_file}")
    else:
        log_info(f"Instruction set: (from config)")
    
    # File paths for intermediate stages
    expanded_file = output_dir / f"{source_file.stem}_expanded.asm"
    object_file = output_dir / f"{source_file.stem}.obj"
    
    # Set binary file extension based on output format
    if output_format == 'hex':
        binary_file = output_dir / f"{source_file.stem}.hex"
    elif output_format == 'txt':
        binary_file = output_dir / f"{source_file.stem}.txt"
    else:  # bin format
        binary_file = output_dir / f"{source_file.stem}.bin"
    
    # Phase 1: Macro Expansion
    log_info("=== PHASE 1: MACRO EXPANSION ===")
    macro_expander = MacroExpander()
    
    # Process macro files first (if any)
    if macro_files:
        log_info(f"Processing {len(macro_files)} macro file(s)")
        for macro_file in macro_files:
            macro_file_path = Path(macro_file)
            if not macro_file_path.exists():
                log_error(f"Macro file not found: {macro_file}", error_code="MACRO_FILE_NOT_FOUND")
                return False, None
            
            log_info(f"Loading macro file: {macro_file_path}")
            if not macro_expander.process_macro_file(macro_file_path):
                log_abort(f"Failed to process macro file: {macro_file}", error_code="MACRO_FILE_FAILED")
                log_error(f"Check macro definitions in {macro_file} for syntax errors")
                return False, None
    
    # Process main source file with accumulated macros (if enabled)
    if no_macros:
        log_info("Macro expansion disabled (--no-macros)")
        # Use source file directly without expansion
        expanded_file = source_file
    else:
        if not macro_expander.process_file(source_file, expanded_file):
            log_abort("Macro expansion failed", error_code="MACRO_EXPANSION_FAILED")
            return False, None
        
        if not check_for_errors():
            log_error("Compilation halted due to errors in macro expansion phase", 
                     error_code="COMPILATION_HALTED")
            return False, None
        
        log_info("Macro expansion completed successfully")
    
    # Phase 2: Assembly
    log_info("=== PHASE 2: ASSEMBLY ===")
    assembler = AssemblerEngine(instruction_set_file, force_32bit=force_32bit, no_implicit=no_implicit)
    
    # Generate listing file name if requested
    actual_listing_file = None
    if listing_file:
        if listing_file == True:  # Auto-generate name
            actual_listing_file = output_dir / f"{source_file.stem}.lst"
        else:
            actual_listing_file = Path(listing_file)
    
    if not assembler.assemble_file(expanded_file, object_file, actual_listing_file):
        log_fatal("Assembly failed - compilation terminated", error_code="ASSEMBLY_FATAL")
        return False, None
    
    if not check_for_errors():
        log_error("Compilation halted due to errors in assembly phase", 
                 error_code="COMPILATION_HALTED")
        return False, None
    
    log_info("Assembly completed successfully")
    
    # Phase 3: Linking
    log_info("=== PHASE 3: LINKING ===")
    linker = Linker()
    
    if not linker.link_files([object_file], binary_file, base_address, output_format, force_32bit=force_32bit, no_implicit=no_implicit):
        log_abort("Linking failed", error_code="LINKING_FAILED")
        return False, None
    
    if not check_for_errors():
        log_fatal("Compilation halted due to errors in linking phase", 
                 error_code="COMPILATION_HALTED")
        return False, None
    
    log_info("Linking completed successfully")
    log_info(f"=== COMPILATION COMPLETED SUCCESSFULLY ===")
    log_info(f"Final binary: {binary_file}")
    
    return True, linker

def show_help():
    """Show NASM-compatible help message"""
    help_text = f"""TASM version {TASM_VERSION} compiled on {TASM_DATE}

usage: TASM [-@ response_file] [-f format] [-o outfile] [-l listfile]
            [options...] filename

    or TASM -h for help

 -o outfile      output file name (only if single input file)
 -f format       select output file format

 -l listfile     generate listing

 -g              generate debug information
 -F format       select a debug info format

 -I path         add a pathname to the include file path
 -i path         add a pathname to the include file path
 -p file         pre-include a file
 -P file         pre-include a file

 -d symbol       pre-define a macro
 -d symbol=value pre-define a macro
 -D symbol       pre-define a macro
 -D symbol=value pre-define a macro
 -u symbol       undefine a macro
 -U symbol       undefine a macro

 -m file         include macro expansion file
 --macro-file file    include macro expansion file
 --macros file   include macro expansion file

 -c file         specify custom configuration file
 --config file   specify custom configuration file

 -D dir          specify output directory for build artifacts
 --output-dir dir specify output directory for build artifacts

 -E              preprocess only (writes output to stdout)
 -a              suppress preprocessor
 --no-macros     disable macro expansion (use source as-is)

 -M              generate Makefile dependencies on stdout
 -MG             d:o, missing files assumed generated
 -MF file        set Makefile dependency file
 -MD file        assemble and generate dependencies
 -MT target      change the default target of the rule emitted by -M
 -MQ target      same as -MT but quotes special chars

 -w+warning      enables warning
 -w-warning      disable warning
 -w              all warnings (same as -Wall)
 -W              same as -w

 -O0             no optimization
 -O1             minimal optimization
 -O32            force 32-bit instruction variants
 -Ono-implicit   disable implicit operand variants (no A[10]/A[15] shortcuts)
 -Ox             multipass optimization (default)

 -t              enable TASM compatibility mode
 -s file         specify instruction set CSV file
 --instruction-set file  specify instruction set CSV file
 --verbose       show all log messages (debug, info, warning, error, abort)
 --info          show info messages in addition to standard logging
 --debug         show debug messages in addition to standard logging
 -v              show version info
 -h              show this text
 --help          show this text

 Warnings:       label-redef, macro-params, number-overflow, gnu-elf-extensions,
                 float-denorm, float-overflow, float-toolong, float-underflow,
                 user

 Output formats: """ + ", ".join(OUTPUT_FORMATS.keys()) + "\n"
    
    print(help_text)

def compile_multiple_files(source_files: List[Path], output_file: Optional[Path] = None,
                          base_address: int = 0x80000000, 
                          output_format: str = 'bin',
                          listing_file: Optional[Path] = None,
                          preprocess_only: bool = False,
                          output_dir: Optional[Path] = None,
                          instruction_set_file: Optional[Path] = None,
                          macro_files: Optional[List[str]] = None,
                          force_32bit: bool = False,
                          no_implicit: bool = False) -> Tuple[bool, Optional['Linker']]:
    """
    Compile multiple assembly files and link them together
    
    Args:
        source_files: List of source assembly files
        output_dir: Directory for intermediate and output files
        base_address: Base address for linking
        
    Returns:
        Tuple of (success: bool, linker: Optional[Linker])
    """
    log_info(f"=== MULTI-FILE COMPILATION STARTED ===")
    log_info(f"Source files: {[str(f) for f in source_files]}")
    log_info(f"Output directory: {output_dir}")
    log_info(f"Base address: 0x{base_address:08X}")
    if instruction_set_file:
        log_info(f"Instruction set: {instruction_set_file}")
    
    # Phase 1: Macro expansion for all files
    log_info("=== PHASE 1: MACRO EXPANSION ===")
    expanded_files = []
    
    if macro_files:
        log_info(f"Processing {len(macro_files)} macro file(s)")
    
    macro_expander = MacroExpander()
    
    # Load macro files first (shared across all source files)
    if macro_files:
        for macro_file in macro_files:
            macro_file_path = Path(macro_file)
            log_info(f"Loading macro file: {macro_file_path}")
            if not macro_expander.process_macro_file(macro_file_path):
                log_abort(f"Failed to process macro file: {macro_file}", error_code="MACRO_FILE_FAILED")
                return False, None
    
    # Expand each source file
    for source_file in source_files:
        log_info(f"Starting macro expansion for {source_file.name}")
        expanded_file = output_dir / f"{source_file.stem}_expanded.asm"
        
        if not macro_expander.process_file(source_file, expanded_file):
            log_abort(f"Macro expansion failed for {source_file}", error_code="MACRO_EXPANSION_FAILED")
            return False, None
            
        expanded_files.append(expanded_file)
        log_info(f"Macro expansion completed for {source_file.name}")
    
    log_info("Macro expansion completed for all files")
    
    # Phase 2: Assembly for all files
    log_info("=== PHASE 2: ASSEMBLY ===")
    object_files = []
    
    for i, expanded_file in enumerate(expanded_files):
        source_file = source_files[i]
        log_info(f"Starting assembly of {expanded_file.name}")
        object_file = output_dir / f"{source_file.stem}.obj"
        
        # Create a fresh assembler instance for each file to avoid state conflicts
        assembler = AssemblerEngine(instruction_set_file, force_32bit=force_32bit, no_implicit=no_implicit)
        
        # Generate listing file for this source file if requested (one .LST per .ASM)
        source_listing_file = None
        if listing_file:
            source_listing_file = output_dir / f"{source_file.stem}.lst"
        
        if not assembler.assemble_file(expanded_file, object_file, source_listing_file):
            log_abort(f"Assembly failed for {expanded_file}", error_code="ASSEMBLY_FAILED")
            return False, None
            
        object_files.append(object_file)
        log_info(f"Assembly completed for {expanded_file.name}")
    
    log_info("Assembly completed for all files")
    
    # Phase 3: Linking
    log_info("=== PHASE 3: LINKING ===")
    linker = Linker()
    
    # Set program file extension based on output format
    if output_format == 'hex':
        program_bin = output_dir / "program.hex"
    elif output_format == 'txt':
        program_bin = output_dir / "program.txt"
    else:  # bin format
        program_bin = output_dir / "program.bin"
    
    log_info(f"Starting linking process with {len(object_files)} object files")
    log_info(f"Base address: 0x{base_address:08X}")
    
    if not linker.link_files(object_files, program_bin, base_address, output_format, force_32bit=force_32bit, no_implicit=no_implicit):
        log_abort("Linking failed", error_code="LINKING_FAILED")
        return False, None
    
    log_info("Linking completed successfully")
    log_info(f"=== MULTI-FILE COMPILATION COMPLETED SUCCESSFULLY ===")
    
    return True, linker

def main():
    """Main entry point with NASM-compatible command line"""
    # Handle special cases before argument parsing
    if len(sys.argv) == 1:
        print("TASM: error: no input files", file=sys.stderr)
        return 1
    
    # Check for help or version without full parsing
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:
            show_help()
            return 0
        elif arg in ['-v', '--version']:
            print(f"TASM version {TASM_VERSION} compiled on {TASM_DATE}")
            return 0
    
    # Parse NASM-style arguments manually for maximum compatibility
    input_files = []
    output_file = None
    output_format = 'bin'
    listing_file = None
    preprocess_only = False
    verbose = "standard"  # "standard", "info", "verbose", or "debug"
    base_address = 0x80000000  # TriCore default base address
    user_specified_output = False
    instruction_set_file = None  # Default to None, will use instruction set from config
    macro_files = []  # List of macro files to include
    force_32bit = False  # Flag for -O32 optimization (force 32-bit variants)
    no_implicit = False  # Flag for -Ono-implicit optimization (disable implicit A[10]/A[15] operands)
    no_macros = False  # Flag for --no-macros (disable macro expansion)
    output_dir_override = None  # Override for output directory path
    
    # Debug: print arguments
    # print(f"DEBUG: sys.argv = {sys.argv}", file=sys.stderr)
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg.startswith('-'):
            if arg == '-o':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -o requires an argument", file=sys.stderr)
                    return 1
                output_file = sys.argv[i + 1]
                user_specified_output = True
                i += 2
            elif arg.startswith('-o'):
                output_file = arg[2:]  # -ofile.bin
                user_specified_output = True
                i += 1
            elif arg == '-f':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -f requires an argument", file=sys.stderr)
                    return 1
                output_format = sys.argv[i + 1]
                if output_format not in OUTPUT_FORMATS:
                    print(f"TASM: error: unknown output format '{output_format}'", file=sys.stderr)
                    return 1
                i += 2
            elif arg.startswith('-f'):
                output_format = arg[2:]  # -fbin
                if not output_format:  # Handle case where -f has no format attached
                    print("TASM: error: -f requires an argument", file=sys.stderr)
                    return 1
                if output_format not in OUTPUT_FORMATS:
                    print(f"TASM: error: unknown output format '{output_format}'", file=sys.stderr)
                    return 1
                i += 1
            elif arg == '-l':
                # Check if next argument is a listing filename (not an .asm file or option)
                if (i + 1 < len(sys.argv) and 
                    not sys.argv[i + 1].startswith('-') and 
                    not sys.argv[i + 1].endswith('.asm')):
                    listing_file = sys.argv[i + 1]
                    i += 2
                else:
                    # Auto-generate listing file name (will be set later based on input file)
                    listing_file = True
                    i += 1
            elif arg.startswith('-l'):
                listing_file = arg[2:]  # -lfile.lst
                i += 1
            elif arg == '-E':
                preprocess_only = True
                i += 1
            elif arg == '--verbose':
                verbose = "verbose"
                i += 1
            elif arg == '--info':
                verbose = "info"
                i += 1
            elif arg == '--debug':
                verbose = "debug"
                i += 1
            elif arg == '--no-macros':
                no_macros = True
                i += 1
            elif arg == '--instruction-set':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: --instruction-set requires an argument", file=sys.stderr)
                    return 1
                instruction_set_file = sys.argv[i + 1]
                i += 2
            elif arg.startswith('--instruction-set='):
                instruction_set_file = arg[18:]  # --instruction-set=file.csv
                i += 1
            elif arg == '-s':
                # Short option for instruction set specification
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -s requires an argument", file=sys.stderr)
                    return 1
                instruction_set_file = sys.argv[i + 1]
                i += 2
            elif arg.startswith('-s') and len(arg) > 2:
                instruction_set_file = arg[2:]  # -sfile.csv
                i += 1
            elif arg == '-m':
                # Short option for macro file
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -m requires an argument", file=sys.stderr)
                    return 1
                macro_files.append(sys.argv[i + 1])
                i += 2
            elif arg.startswith('-m') and len(arg) > 2:
                macro_files.append(arg[2:])  # -mfile.asm
                i += 1
            elif arg == '--macro-file':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: --macro-file requires an argument", file=sys.stderr)
                    return 1
                macro_files.append(sys.argv[i + 1])
                i += 2
            elif arg.startswith('--macro-file='):
                macro_files.append(arg[13:])  # --macro-file=file.asm
                i += 1
            elif arg == '--macros':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: --macros requires an argument", file=sys.stderr)
                    return 1
                macro_files.append(sys.argv[i + 1])
                i += 2
            elif arg.startswith('--macros='):
                macro_files.append(arg[9:])  # --macros=file.asm
                i += 1
            elif arg == '-c':
                # Short option for config file
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -c requires an argument", file=sys.stderr)
                    return 1
                config_file = sys.argv[i + 1]
                # Set custom config path before any config access
                from config_loader import set_config_path
                set_config_path(config_file)
                i += 2
            elif arg.startswith('-c') and len(arg) > 2:
                config_file = arg[2:]  # -cconfig.json
                from config_loader import set_config_path
                set_config_path(config_file)
                i += 1
            elif arg == '--config':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: --config requires an argument", file=sys.stderr)
                    return 1
                config_file = sys.argv[i + 1]
                from config_loader import set_config_path
                set_config_path(config_file)
                i += 2
            elif arg.startswith('--config='):
                config_file = arg[9:]  # --config=config.json
                from config_loader import set_config_path
                set_config_path(config_file)
                i += 1
            elif arg == '-O32':
                # Force 32-bit instruction variants (no 16-bit optimization)
                force_32bit = True
                i += 1
            elif arg == '-Ono-implicit':
                # Disable implicit operand variants (no A[10]/A[15] shortcuts)
                no_implicit = True
                i += 1
            elif arg == '-D':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: -D requires an argument", file=sys.stderr)
                    return 1
                output_dir_override = sys.argv[i + 1]
                i += 2
            elif arg.startswith('-D') and len(arg) > 2:
                output_dir_override = arg[2:]  # -Doutput/custom
                i += 1
            elif arg == '--output-dir':
                if i + 1 >= len(sys.argv):
                    print("TASM: error: --output-dir requires an argument", file=sys.stderr)
                    return 1
                output_dir_override = sys.argv[i + 1]
                i += 2
            elif arg.startswith('--output-dir='):
                output_dir_override = arg[13:]  # --output-dir=output/custom
                i += 1
            else:
                # Skip other options for now
                if arg in ['-g', '-a', '-t', '-M', '-MG', '-W', '--verbose']:
                    i += 1
                elif arg in ['-F', '-I', '-i', '-p', '-P', '-d', '-D', '-u', '-U',
                           '-MF', '-MD', '-MT', '-MQ', '-w', '-O', '-s', '-Z']:
                    # Options that take arguments
                    if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                        i += 2
                    else:
                        i += 1
                else:
                    print(f"TASM: warning: unknown option '{arg}'", file=sys.stderr)
                    i += 1
        else:
            # Input file
            input_files.append(arg)
            i += 1
    
    # Validate input
    if not input_files:
        print("TASM: error: no input files", file=sys.stderr)
        return 1
    
    # Convert all input files to Path objects and validate they exist
    source_files = []
    for input_file in input_files:
        source_file = Path(input_file)
        if not source_file.exists():
            print(f"TASM: error: source file not found: {source_file}", file=sys.stderr)
            return 1
        source_files.append(source_file)
    
    # Always use output directory for intermediate files
    # Create a dedicated output directory for build artifacts
    # Use command-line override if provided, otherwise use config default
    build_output_dir = create_output_dir(override_path=output_dir_override)
    build_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle final output file location
    if output_file:
        output_path = Path(output_file)
        if output_path.is_absolute():
            final_output_dir = output_path.parent
        else:
            # Relative path - use current directory as base
            final_output_dir = Path.cwd() / output_path.parent
        final_output_dir.mkdir(parents=True, exist_ok=True)
        final_output_file = output_path
    else:
        # Auto-generate output filename based on format in build directory
        # Use first source file name as base for multiple files
        primary_source = source_files[0]
        if output_format == 'bin':
            final_output_file = build_output_dir / primary_source.stem
        elif output_format == 'hex':
            final_output_file = build_output_dir / f"{primary_source.stem}.hex"
        elif output_format == 'txt':
            final_output_file = build_output_dir / f"{primary_source.stem}.txt"
        elif output_format in ['obj']:
            final_output_file = build_output_dir / f"{primary_source.stem}.obj"
        else:
            final_output_file = build_output_dir / f"{primary_source.stem}.out"
        output_file = str(final_output_file)
    
    # Use build_output_dir for all intermediate files
    output_dir = build_output_dir
    
    # Initialize logger with enhanced console control
    log_file = output_dir / "build.log"
    json_file = output_dir / "build_summary.json"
    
    console_output = not preprocess_only or user_specified_output
    logger = initialize_logger(log_file, console_output=console_output, verbosity_level=verbose)
    
    # Print custom header to console
    if console_output:
        print_header()
        
        # Count lines of code
        source_lines = 0
        try:
            with open(source_files[0], 'r', encoding='utf-8') as f:
                source_lines = len(f.readlines())
        except:
            source_lines = 0
            
        print_phase("Pre-processing the source code file", f"{source_lines} lines of code loaded")
    
    # Log detailed info to files only (unless --info or higher verbosity)
    if verbose in ["info", "verbose", "debug"]:
        log_debug(f"Logging verbosity: {verbose}")
        log_info(f"TASM {TASM_VERSION} - Three-Phase Assembler")
        log_info(f"Input file: {source_file}")
        log_info(f"Output format: {output_format} ({OUTPUT_FORMATS.get(output_format, 'Unknown')})")
        log_info(f"Output file: {output_file}")
    
    # Always log to files for build.log
    
    if listing_file:
        log_info(f"Listing file: {listing_file}")
    
    # Start compilation
    success = False
    output_file_path = None
    instruction_count = 0
    linker = None  # Will hold linker instance for statistics
    
    try:
        # Add start time to logger for duration calculation
        logger.start_time = datetime.now()
        
        if preprocess_only:
            # Only do macro expansion phase
            log_info("=== PREPROCESS ONLY MODE ===")
            macro_expander = MacroExpander()
            
            # Process macro files first (if any)
            if macro_files:
                log_info(f"Processing {len(macro_files)} macro file(s)")
                for macro_file in macro_files:
                    macro_file_path = Path(macro_file)
                    if not macro_file_path.exists():
                        print(f"TASM: error: macro file not found: {macro_file}", file=sys.stderr)
                        return 1
                    
                    log_info(f"Loading macro file: {macro_file_path}")
                    if not macro_expander.process_macro_file(macro_file_path):
                        print(f"TASM: error: failed to process macro file: {macro_file}", file=sys.stderr)
                        print(f"TASM: check the macro definitions in {macro_file} for syntax errors", file=sys.stderr)
                        print(f"TASM: use --verbose for detailed debugging information", file=sys.stderr)
                        return 1
            
            # Output to stdout or specified file
            if len(source_files) > 1:
                print("TASM: error: preprocessing multiple files not supported with -E", file=sys.stderr)
                return 1
                
            source_file = source_files[0]  # Only one file for preprocessing
            if user_specified_output and output_file and output_file != '-':
                expanded_file = Path(output_file)
                success = macro_expander.process_file(source_file, expanded_file)
            else:
                # Output to stdout (NASM -E behavior)
                expanded_file = output_dir / f"{source_file.stem}_expanded.asm"
                if macro_expander.process_file(source_file, expanded_file):
                    with open(expanded_file, 'r') as f:
                        print(f.read(), end='')
                    success = True
        else:
            # Full three-phase compilation
            # Get instruction set path from config if not specified
            if instruction_set_file:
                instruction_set_path = Path(instruction_set_file)
            else:
                # Use the instruction set from config
                config = get_config()
                instruction_set_path = Path(config.instruction_set_path)
                log_info(f"Using instruction set from config: {instruction_set_path}")
            
            if len(source_files) == 1:
                # Single file compilation
                if console_output:
                    print_phase("Compiling, 1st pass", "Macro expansion and Assembly")
                    
                success, linker = compile_assembly_file(source_files[0], base_address=base_address, 
                                              output_dir=output_dir, instruction_set_file=instruction_set_path,
                                              macro_files=macro_files, output_format=output_format,
                                              listing_file=listing_file, force_32bit=force_32bit,
                                              no_implicit=no_implicit, no_macros=no_macros)
                                              
                if console_output and success:
                    print_phase("Linking, 1st pass", "Resolving symbols")
                    print_phase("Linking, 2nd pass", "Finalizing")
                    
                # Set output file path for summary
                if success:
                    if output_format == 'hex':
                        output_file_path = output_dir / f"{source_files[0].stem}.hex"
                    elif output_format == 'txt':
                        output_file_path = output_dir / f"{source_files[0].stem}.txt"  
                    else:
                        output_file_path = output_dir / f"{source_files[0].stem}.bin"
                    
                    # Get instruction count from linker
                    instruction_count = linker.instruction_count if linker else 0
            else:
                # Multiple file compilation
                if console_output:
                    print_phase("Compiling, 1st pass", "Multiple files macro expansion and Assembly")
                    
                success, linker = compile_multiple_files(source_files, base_address=base_address,
                                               output_dir=output_dir, instruction_set_file=instruction_set_path,
                                               macro_files=macro_files, output_format=output_format,
                                               listing_file=listing_file, force_32bit=force_32bit,
                                               no_implicit=no_implicit)
                                               
                if console_output and success:
                    print_phase("Linking, 1st pass", "Resolving symbols")
                    print_phase("Linking, 2nd pass", "Finalizing")
                    
                # Set output file path for summary  
                if success:
                    if output_format == 'hex':
                        output_file_path = output_dir / "program.hex"
                    elif output_format == 'txt':
                        output_file_path = output_dir / "program.txt"
                    else:
                        output_file_path = output_dir / "program.bin"
                        
                    # Get instruction count from linker
                    instruction_count = linker.instruction_count if linker else 0
            
            # Move final binary to specified output location if different from build directory
            if success and output_file and user_specified_output:
                final_output_path = Path(output_file)
                output_file_path = final_output_path  # Store for summary
                program_bin = output_dir / "program.bin"
                
                # If output file is different from where program.bin is created
                if final_output_path != program_bin:
                    if program_bin.exists():
                        # Copy/move to final location
                        import shutil
                        shutil.copy2(program_bin, final_output_path)
                        log_info(f"Output copied to: {final_output_path}")
                    else:
                        # Look for the actual output file that was created
                        # Use first source file name as base for multiple files
                        primary_source = source_files[0]
                        
                        # Choose correct file extension based on format
                        if output_format == 'hex':
                            binary_file = output_dir / f"{primary_source.stem}.hex"
                        elif output_format == 'txt':
                            binary_file = output_dir / f"{primary_source.stem}.txt"
                        else:  # bin format
                            binary_file = output_dir / f"{primary_source.stem}.bin"
                            
                        if binary_file.exists():
                            import shutil
                            shutil.copy2(binary_file, final_output_path)
                            log_info(f"Output copied to: {final_output_path}")
        
    except KeyboardInterrupt:
        log_error("Compilation interrupted by user", error_code="USER_INTERRUPT")
        success = False
    except Exception as e:
        log_error(f"Unexpected error during compilation: {str(e)}", 
                 error_code="UNEXPECTED_ERROR")
        log_debug(f"Exception details: {type(e).__name__}: {str(e)}")
        success = False
    
    # Generate final report (unless preprocess-only to stdout)
    if not (preprocess_only and (not output_file or output_file == '-')):
        if console_output:
            # Print enhanced console summary
            print_enhanced_summary(output_file_path, instruction_count, linker, output_format)
        
        # Always export files (logs are automatically saved during execution)
        export_build_summary_json(json_file)
        
        if verbose in ["info", "verbose", "debug"]:
            log_info(f"Build log: {log_file}")
            log_info(f"Build summary: {json_file}")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)