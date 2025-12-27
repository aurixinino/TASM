"""
Assembler Module

This module handles the assembly phase, converting assembly mnemonics
into machine code instructions and handling labels, addressing modes, and directives.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from logger import log_info, log_error, log_warning, log_debug, get_logger
from config_loader import get_config

# Import the new instruction system
from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction, EncodedInstruction
from data_directives import DataDirective
from numeric_parser import parse_numeric

class AddressingMode(Enum):
    """Supported addressing modes"""
    IMMEDIATE = "immediate"      # #value
    DIRECT = "direct"           # address
    INDIRECT = "indirect"       # (address)
    INDEXED = "indexed"         # address,X or address,Y
    RELATIVE = "relative"       # for branches

@dataclass
class Instruction:
    """Represents an assembled instruction"""
    address: int
    opcode: int
    operand: Optional[int]
    size: int
    source_line: int
    source_text: str

@dataclass
class Label:
    """Represents a label definition"""
    name: str
    address: int
    line_defined: int

@dataclass
class Symbol:
    """Represents a symbol reference"""
    name: str
    address: int
    line_referenced: int
    resolved: bool = False

class AssemblerEngine:
    """Main assembler engine with external instruction set support"""
    
    def __init__(self, instruction_set_file: Optional[Path] = None, force_32bit: bool = False, no_implicit: bool = False):
        """
        Initialize assembler engine with external instruction set loader
        
        Args:
            instruction_set_file: Path to instruction set file (.xlsx, .json, .xml, or .csv).
                                If None, uses path from config or default tricore Excel instruction set.
            force_32bit: If True, forces use of 32-bit instruction variants when available.
            no_implicit: If True, disables implicit operand variants (A[10]/A[15] shortcuts).
        """
        # Determine instruction set file path
        if instruction_set_file is None:
            # Get instruction set path from config
            try:
                config = get_config()
                config_path = config.instruction_set_path
                if not config_path:
                    log_error("Instruction set path not configured in config/tasm_config.json")
                    raise ValueError("Instruction set path not configured")
                
                instruction_set_file = Path(config_path)
                if not instruction_set_file.exists():
                    log_error(f"Instruction set file not found: {instruction_set_file}")
                    raise FileNotFoundError(f"Instruction set file not found: {instruction_set_file}")
                
                log_info(f"Using instruction set from config: {instruction_set_file}")
            except Exception as e:
                log_error(f"Failed to load instruction set path from config: {e}")
                raise
        
        # Load instruction set using new loader system
        self.instruction_loader = InstructionSetLoader(force_32bit=force_32bit, no_implicit=no_implicit)
        if not self.instruction_loader.load_instruction_set(instruction_set_file):
            log_error(f"Failed to load instruction set from {instruction_set_file}")
            raise ValueError(f"Cannot load instruction set from {instruction_set_file}")
        
        log_info(f"Loaded {self.instruction_loader.get_instruction_count()} instructions from {instruction_set_file}")
        log_info(f"Found {self.instruction_loader.get_mnemonic_count()} unique instruction mnemonics")
        
        # Assembly state (initialize first)
        self.labels: Dict[str, Label] = {}
        self.symbols: List[Symbol] = []
        self.instructions: List[Instruction] = []
        self.current_address = 0x80000000  # Default start address for TriCore
        self.current_file = ""
        
        # Store all source lines with their addresses for listing generation
        # Format: (line_num, address, opcode_bytes, source_text)
        self.source_listing: List[Tuple[int, Optional[int], Optional[bytes], str]] = []
        
        # Create instruction encoder
        self.instruction_encoder = InstructionEncoder(self.instruction_loader)
        
        # Create data directive handler (pass labels dict for symbol resolution)
        config = get_config()
        self.data_directive = DataDirective(
            endianness='little' if config.is_little_endian else 'big',
            labels=self.labels
        )
        
        # Legacy attributes for backward compatibility
        self.opcodes = {}  # Will be populated as needed for compatibility
        self.opcode_sizes = {}
        self.enhanced_encoder = None  # Not needed with new system
    

    def assemble_file(self, input_file: Path, output_file: Path, listing_file: Optional[Path] = None) -> bool:
        """
        Assemble the macro-expanded source file
        
        Args:
            input_file: Macro-expanded assembly file
            output_file: Output object file
            listing_file: Optional listing file for human-readable output
            
        Returns:
            True if successful, False if errors occurred
        """
        self.current_file = str(input_file)
        self.listing_file = listing_file
        # Set current file in instruction encoder for better error reporting
        self.instruction_encoder.set_current_file(self.current_file)
        log_info(f"Starting assembly of {input_file.name}", str(input_file))
        
        try:
            # Read expanded source
            if not input_file.exists():
                log_error(f"Expanded source file not found: {input_file.name}", 
                         str(input_file), error_code="FILE_NOT_FOUND")
                return False
            
            with open(input_file, 'r', encoding='utf-8') as f:
                source_lines = f.readlines()
            
            log_info(f"Read {len(source_lines)} lines from expanded source", str(input_file))
            
            # First pass: collect labels and calculate addresses
            if not self._first_pass(source_lines):
                return False
            
            # Second pass: generate machine code
            if not self._second_pass(source_lines):
                return False
            
            # Write object file
            if not self._write_object_file(output_file):
                return False
            
            # Generate preliminary listing file (.ls1) if requested
            # This contains all source lines with preliminary addresses
            # The linker will update this to .lst with final addresses
            if self.listing_file:
                ls1_file = self.listing_file.with_suffix('.ls1')
                if not self._write_preliminary_listing(ls1_file):
                    log_warning(f"Failed to write preliminary listing file", str(ls1_file))
            
            log_info(f"Assembly completed successfully")
            log_info(f"Generated {len(self.instructions)} instructions")
            log_info(f"Code size: {self._calculate_code_size()} bytes")
            
            return True
            
        except Exception as e:
            log_error(f"Unexpected error during assembly: {str(e)}", 
                     str(input_file), error_code="ASSEMBLY_ERROR")
            return False
    
    def _first_pass(self, source_lines: List[str]) -> bool:
        """First pass: collect labels and calculate addresses"""
        log_debug("Starting first pass - collecting labels")
        
        address = self.current_address
        label_count = 0
        
        for line_num, line in enumerate(source_lines, 1):
            original_line = line.strip()
            
            # Store ALL source lines for listing (including comments and blank lines)
            # Address will be None for comments/blank lines, filled in during second pass for instructions
            # Skip GCC line directives (e.g., # 670 "filename" 1) and regular comments (;)
            if not original_line or original_line.startswith(';') or original_line.startswith('#'):
                self.source_listing.append((line_num, None, None, original_line))
                continue
            
            # Handle origin directive
            if original_line.upper().startswith('.ORG'):
                self.source_listing.append((line_num, address, None, original_line))
                if not self._handle_org_directive(original_line, line_num):
                    return False
                address = self.current_address
                continue
            
            # Handle EQU directive (defines constants)
            # Must be at start of line (after optional label): SYMBOL EQU value
            line_upper = original_line.upper()
            equ_pattern = re.match(r'^\s*(\w+)\s+EQU\s+', line_upper)
            if equ_pattern:
                self.source_listing.append((line_num, None, None, original_line))
                try:
                    symbol, value = self.data_directive.process_equ(original_line)
                    log_debug(f"Defined constant {symbol} = {value}")
                    # EQU constants are stored only in data_directive.constants, NOT in labels
                    # This prevents them from being treated as code labels during linking
                    continue
                except Exception as e:
                    log_error(f"Invalid EQU directive: {e}", 
                             self.current_file, line_num, error_code="INVALID_EQU")
                    return False
            
            # Check for label (but ignore colons in comments)
            colon_pos = original_line.find(':')
            semicolon_pos = original_line.find(';')
            
            # Only treat as label if colon comes before any comment
            if colon_pos != -1 and (semicolon_pos == -1 or colon_pos < semicolon_pos):
                label_part, instruction_part = original_line.split(':', 1)
                label_name = label_part.strip()
                
                if not self._validate_label_name(label_name, line_num):
                    return False
                
                if label_name in self.labels:
                    log_error(f"Label '{label_name}' already defined", 
                             self.current_file, line_num, error_code="DUPLICATE_LABEL")
                    log_debug(f"Previous definition at line {self.labels[label_name].line_defined}")
                    return False
                
                self.labels[label_name] = Label(label_name, address, line_num)
                label_count += 1
                log_debug(f"Label '{label_name}' defined at address 0x{address:08X}")
                
                # Process instruction part if present
                instruction_part = instruction_part.strip()
                if instruction_part and not instruction_part.startswith(';'):
                    # Check if it's a data directive
                    if self.data_directive.is_data_directive(instruction_part):
                        try:
                            inst_size = self.data_directive.calculate_size(instruction_part, address)
                            self.source_listing.append((line_num, address, None, original_line))
                            log_debug(f"Data directive size: {inst_size} bytes at address 0x{address:08X}")
                        except Exception as e:
                            log_error(f"Error calculating data directive size: {e}", 
                                     self.current_file, line_num, error_code="DATA_DIRECTIVE_ERROR")
                            return False
                    else:
                        inst_size = self._calculate_instruction_size(instruction_part, line_num)
                        if inst_size is None:
                            return False
                        self.source_listing.append((line_num, address, None, original_line))
                    address += inst_size
                else:
                    # Label only (no instruction on same line)
                    self.source_listing.append((line_num, address, None, original_line))
            
            else:
                # Regular instruction or directive
                # Check if it's a data directive
                if self.data_directive.is_data_directive(original_line):
                    try:
                        inst_size = self.data_directive.calculate_size(original_line, address)
                        self.source_listing.append((line_num, address, None, original_line))
                        log_debug(f"Data directive size: {inst_size} bytes at address 0x{address:08X}")
                    except Exception as e:
                        log_error(f"Error calculating data directive size: {e}", 
                                 self.current_file, line_num, error_code="DATA_DIRECTIVE_ERROR")
                        return False
                else:
                    inst_size = self._calculate_instruction_size(original_line, line_num)
                    if inst_size is None:
                        return False
                    self.source_listing.append((line_num, address, None, original_line))
                address += inst_size
        
        log_info(f"First pass completed - found {label_count} labels")
        return True
    
    def _handle_org_directive(self, line: str, line_num: int) -> bool:
        """Handle .ORG directive"""
        # Remove comments first
        if ';' in line:
            line = line.split(';')[0].strip()
        
        parts = line.split()
        if len(parts) != 2:
            log_error("Invalid .ORG directive format", 
                     self.current_file, line_num, error_code="INVALID_ORG")
            return False
        
        try:
            if parts[1].startswith('$'):
                # Hexadecimal
                address = int(parts[1][1:], 16)
            elif parts[1].startswith('0x'):
                # Hexadecimal
                address = int(parts[1], 16)
            else:
                # Decimal
                address = int(parts[1])
            
            if address < 0 or address > 0xFFFFFFFF:
                log_error(f"Address out of range: 0x{address:X}", 
                         self.current_file, line_num, error_code="ADDRESS_OUT_OF_RANGE")
                return False
            
            self.current_address = address
            log_info(f"Origin set to 0x{address:08X}", self.current_file, line_num)
            return True
            
        except ValueError:
            log_error(f"Invalid address format: {parts[1]}", 
                     self.current_file, line_num, error_code="INVALID_ADDRESS")
            return False
    
    def _validate_label_name(self, label_name: str, line_num: int) -> bool:
        """Validate label name"""
        if not label_name:
            log_error("Empty label name", self.current_file, line_num, error_code="EMPTY_LABEL")
            return False
        
        # Allow:
        # 1. Standard labels: starting with letter, underscore, or dot (GCC .L labels)
        # 2. GCC numeric local labels: pure digits like 0, 1, 2, etc.
        if not (re.match(r'^[a-zA-Z_\.][a-zA-Z0-9_\.]*$', label_name) or 
                re.match(r'^\d+$', label_name)):
            log_error(f"Invalid label name: '{label_name}'", 
                     self.current_file, line_num, error_code="INVALID_LABEL_NAME")
            return False
        
        # Check if it conflicts with instruction names (skip for numeric labels)
        if not re.match(r'^\d+$', label_name) and label_name.upper() in self.opcodes:
            log_warning(f"Label '{label_name}' shadows instruction name", 
                       self.current_file, line_num, error_code="LABEL_SHADOWS_INSTRUCTION")
        
        return True
    
    def _calculate_instruction_size(self, line: str, line_num: int) -> Optional[int]:
        """Calculate the size of an instruction in bytes using external instruction set"""
        line = line.strip()
        
        if not line or line.startswith(';'):
            return 0
        
        # Remove comments first
        if ';' in line:
            line = line.split(';')[0].strip()
        
        # Handle directives
        if line.upper().startswith('.'):
            return self._calculate_directive_size(line, line_num)
        
        # Parse instruction using new encoder
        parsed = self.instruction_encoder.parse_instruction_line(line, line_num)
        if parsed is None:
            return 0  # Not a valid instruction line
        
        # Find matching instruction definition
        definition = self.instruction_loader.find_instruction(parsed.mnemonic, parsed.operand_count)
        if definition is None:
            log_error(f"Unknown instruction: '{parsed.mnemonic}' with {parsed.operand_count} operands", 
                     self.current_file, line_num, error_code="UNKNOWN_INSTRUCTION")
            return None
        
        # Convert bits to bytes (Tricore instructions are 32-bit = 4 bytes)
        size_bytes = definition.opcode_size // 8
        return size_bytes
    
    def _calculate_directive_size(self, line: str, line_num: int) -> Optional[int]:
        """Calculate size of assembler directives"""
        parts = line.split()
        directive = parts[0].upper()
        
        if directive == '.ORG':
            return 0  # ORG doesn't generate code
        elif directive == '.BYTE':
            return len(parts) - 1  # One byte per value
        elif directive == '.WORD':
            return (len(parts) - 1) * 2  # Two bytes per value
        else:
            log_warning(f"Unknown directive: {directive}", 
                       self.current_file, line_num, error_code="UNKNOWN_DIRECTIVE")
            return 0
    
    def _determine_addressing_mode(self, operand: str, mnemonic: str = None) -> AddressingMode:
        """Determine addressing mode from operand"""
        operand = operand.strip()
        
        if operand.startswith('#'):
            return AddressingMode.IMMEDIATE
        elif operand.startswith('(') and operand.endswith(')'):
            return AddressingMode.INDIRECT
        elif ',' in operand:
            return AddressingMode.INDEXED
        else:
            # Check if this is a branch instruction - they use relative addressing
            if mnemonic and mnemonic.upper() in ['BEQ', 'BNE', 'BCC', 'BCS', 'BPL', 'BMI', 'BVC', 'BVS']:
                return AddressingMode.RELATIVE
            else:
                return AddressingMode.DIRECT
    
    def _second_pass(self, source_lines: List[str]) -> bool:
        """Second pass: generate machine code"""
        log_debug("Starting second pass - generating machine code")
        
        address = self.current_address
        instruction_count = 0
        
        for line_num, line in enumerate(source_lines, 1):
            original_line = line.strip()
            
            # Skip empty lines and comments
            if not original_line or original_line.startswith(';'):
                continue
            
            # Handle origin directive
            if original_line.upper().startswith('.ORG'):
                self._handle_org_directive(original_line, line_num)
                address = self.current_address
                continue
            
            # Skip EQU directives (already processed in first pass)
            line_upper = original_line.upper()
            if re.match(r'^\s*(\w+)\s+EQU\s+', line_upper):
                continue
            
            # Remove label if present (but ignore colons in comments)
            colon_pos = original_line.find(':')
            semicolon_pos = original_line.find(';')
            
            if colon_pos != -1 and (semicolon_pos == -1 or colon_pos < semicolon_pos):
                _, instruction_part = original_line.split(':', 1)
                instruction_part = instruction_part.strip()
                
                if not instruction_part or instruction_part.startswith(';'):
                    continue
                
                original_line = instruction_part
            
            # Check if it's a data directive
            if self.data_directive.is_data_directive(original_line):
                instruction = self._assemble_data_directive(original_line, address, line_num)
                if instruction is None:
                    return False
                if instruction.size > 0:
                    self.instructions.append(instruction)
                    address += instruction.size
                    instruction_count += 1
            else:
                # Assemble instruction
                instruction = self._assemble_instruction(original_line, address, line_num)
                if instruction is None:
                    return False
                
                if instruction.size > 0:
                    self.instructions.append(instruction)
                    address += instruction.size
                    instruction_count += 1
        
        log_info(f"Second pass completed - generated {instruction_count} instructions")
        return True
    
    def _assemble_instruction(self, line: str, address: int, line_num: int) -> Optional[Instruction]:
        """Assemble a single instruction using the new external instruction set system"""
        # Remove comments first
        if ';' in line:
            line = line.split(';')[0]
        
        line = line.strip()
        if not line:
            return Instruction(address, 0, None, 0, line_num, line)
        
        # Check if this is a directive
        if line.startswith('.'):
            return self._assemble_directive(line, address, line_num)
        
        # Parse instruction using new encoder
        parsed = self.instruction_encoder.parse_instruction_line(line, line_num)
        if parsed is None:
            # Not a valid instruction line (maybe empty or comment)
            return Instruction(address, 0, None, 0, line_num, line)
        
        # Convert labels dict to address dict for encoder
        label_addresses = {name: label.address for name, label in self.labels.items()}
        
        # Encode instruction with label resolution support
        encoded = self.instruction_encoder.encode_instruction(parsed, address, label_addresses)
        if encoded is None:
            # Encoding failed - detailed error already logged by encoder
            return None
        
        # Calculate instruction size (Tricore instructions are 32-bit = 4 bytes)
        size_bytes = encoded.definition.opcode_size // 8
        
        log_debug(f"Encoded: {parsed.mnemonic} -> {encoded.hex_value} ({size_bytes} bytes)")
        
        return Instruction(
            address=address,
            opcode=encoded.binary_value,
            operand=None,  # Operands are encoded in the opcode
            size=size_bytes,
            source_line=line_num,
            source_text=line
        )
        
        return Instruction(address, opcode, None, size_bytes, line_num, line)
    
    def _assemble_directive(self, line: str, address: int, line_num: int) -> Optional[Instruction]:
        """Assemble assembler directives"""
        parts = line.split()
        directive = parts[0].upper()
        
        if directive == '.BYTE':
            if len(parts) < 2:
                log_error("Missing value for .BYTE directive", 
                         self.current_file, line_num, error_code="MISSING_DIRECTIVE_VALUE")
                return None
            
            # For simplicity, just store first byte value
            try:
                value = self._parse_numeric_value(parts[1])
                return Instruction(address, value & 0xFF, None, 1, line_num, line)
            except ValueError:
                log_error(f"Invalid byte value: {parts[1]}", 
                         self.current_file, line_num, error_code="INVALID_BYTE_VALUE")
                return None
        
        return Instruction(address, 0, None, 0, line_num, line)
    
    def _assemble_data_directive(self, line: str, address: int, line_num: int) -> Optional[Instruction]:
        """Assemble NASM-compatible data directives"""
        # Remove comments
        if ';' in line:
            line = line.split(';')[0].strip()
        
        parts = line.split(None, 1)
        if not parts:
            return Instruction(address, 0, None, 0, line_num, line)
        
        directive = parts[0].upper()
        
        try:
            # Handle TIMES directive
            if directive == 'TIMES':
                count, rest = self.data_directive.process_times(line, address)
                # For TIMES, we need to recursively process the repeated part
                # Simplified: just calculate size and store as data
                data_size = self.data_directive.calculate_size(line, address)
                # Create a pseudo-instruction for TIMES (will need special handling in linker)
                return Instruction(address, 0, None, data_size, line_num, line)
            
            # Handle RESB/RESW/etc (reserve space - no data)
            if directive in self.data_directive.RESERVE_SIZES:
                size = self.data_directive.calculate_size(line, address)
                # Reserve directives don't generate data, just reserve space
                return Instruction(address, 0, None, size, line_num, line)
            
            # Handle INCBIN
            if directive == 'INCBIN':
                operands = parts[1] if len(parts) > 1 else ''
                base_dir = Path(self.current_file).parent if self.current_file else None
                data = self.data_directive.process_incbin(operands, base_dir)
                # Store binary data as multi-byte opcode
                # For simplicity, store first 4 bytes as opcode, size is full length
                opcode_val = int.from_bytes(data[:4], 'little') if len(data) >= 4 else 0
                return Instruction(address, opcode_val, None, len(data), line_num, line)
            
            # Handle DB, DW, DD, etc
            if directive in self.data_directive.DATA_SIZES:
                operands = parts[1] if len(parts) > 1 else ''
                values = self.data_directive.parse_data_list(operands)
                data = self.data_directive.encode_data(directive, values)
                
                # Store data bytes as opcode (limited to 4 bytes for storage)
                # For larger data, we'll need to store it differently
                if len(data) <= 4:
                    opcode_val = int.from_bytes(data, 'little')
                else:
                    # Store first 4 bytes, full data will be in linker
                    opcode_val = int.from_bytes(data[:4], 'little')
                
                return Instruction(address, opcode_val, None, len(data), line_num, line)
            
        except Exception as e:
            log_error(f"Error assembling data directive: {e}", 
                     self.current_file, line_num, error_code="DATA_DIRECTIVE_ERROR")
            return None
        
        return Instruction(address, 0, None, 0, line_num, line)
    
    def _parse_operand(self, operand_str: str, addressing_mode: AddressingMode, 
                      current_addr: int, line_num: int) -> Optional[int]:
        """Parse operand value"""
        try:
            if addressing_mode == AddressingMode.IMMEDIATE:
                # Remove # prefix
                value_str = operand_str[1:]
                return self._parse_numeric_value(value_str)
            
            elif addressing_mode == AddressingMode.RELATIVE:
                # Branch instruction - calculate relative offset
                target = self._resolve_symbol(operand_str, line_num)
                if target is None:
                    return None
                
                offset = target - (current_addr + 2)  # +2 for instruction size
                
                if offset < -128 or offset > 127:
                    log_error(f"Branch target out of range: {offset}", 
                             self.current_file, line_num, error_code="BRANCH_OUT_OF_RANGE")
                    return None
                
                return offset & 0xFF
            
            else:
                # Direct addressing - resolve symbol or parse address
                return self._resolve_symbol(operand_str, line_num)
        
        except Exception as e:
            log_error(f"Error parsing operand '{operand_str}': {str(e)}", 
                     self.current_file, line_num, error_code="OPERAND_PARSE_ERROR")
            return None
    
    def _parse_numeric_value(self, value_str: str) -> int:
        """
        Parse numeric value using NASM-compatible format.
        Supports all NASM 3.4.1 numeric constant formats.
        """
        value_str = value_str.strip()
        
        # Support legacy '%' prefix for binary (non-NASM)
        if value_str.startswith('%'):
            return int(value_str[1:].replace('_', ''), 2)
        
        # Use NASM-compatible parser for all other formats
        try:
            return parse_numeric(value_str)
        except ValueError as e:
            raise ValueError(f"Invalid numeric value '{value_str}': {e}")
    
    def _resolve_symbol(self, symbol_str: str, line_num: int) -> Optional[int]:
        """Resolve symbol to address"""
        symbol_str = symbol_str.strip()
        
        # Check if it's a numeric value
        try:
            return self._parse_numeric_value(symbol_str)
        except ValueError:
            pass
        
        # Look up label
        if symbol_str in self.labels:
            return self.labels[symbol_str].address
        
        # Unresolved symbol - add to symbol table for linker
        self.symbols.append(Symbol(symbol_str, 0, line_num))
        log_warning(f"Unresolved symbol: '{symbol_str}' - will be resolved by linker", 
                   self.current_file, line_num, error_code="UNRESOLVED_SYMBOL")
        return 0  # Placeholder
    
    def _calculate_code_size(self) -> int:
        """Calculate total code size"""
        return sum(inst.size for inst in self.instructions)
    
    def _write_object_file(self, output_file: Path) -> bool:
        """Write object file with machine code and symbol information"""
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write binary object file
            with open(output_file, 'wb') as f:
                # Write TOBJ header (TASM Object format)
                f.write(b'TOBJ')  # Magic number
                f.write(b'\x01\x00')  # Version 1.0
                
                # Write source file name length and name
                source_name = str(self.current_file).encode('utf-8')
                f.write(len(source_name).to_bytes(2, 'little'))
                f.write(source_name)
                
                # Write instruction count
                f.write(len(self.instructions).to_bytes(4, 'little'))
                
                # Write instructions
                for instruction in self.instructions:
                    f.write(instruction.address.to_bytes(4, 'little'))  # Address
                    # Handle opcode - clamp to 4 bytes for object file format
                    # Data directives may have opcode=0 with size>4, which is fine
                    try:
                        # Handle both positive overflow and negative numbers
                        if instruction.opcode < 0:
                            # Negative number - convert to two's complement
                            opcode_bytes = (instruction.opcode & 0xFFFFFFFF).to_bytes(4, 'little')
                        else:
                            opcode_bytes = instruction.opcode.to_bytes(4, 'little')
                    except (OverflowError, ValueError) as e:
                        # Opcode too large for 4 bytes, store only lower 4 bytes
                        opcode_bytes = (instruction.opcode & 0xFFFFFFFF).to_bytes(4, 'little')
                    f.write(opcode_bytes)   # Machine code
                    # Handle size - clamp to 255 bytes max for object file format
                    size_byte = min(instruction.size, 255)
                    f.write(size_byte.to_bytes(1, 'little'))     # Size
                    # Write source line number
                    f.write(instruction.source_line.to_bytes(4, 'little'))  # Source line
                    # Write source text
                    source_text = instruction.source_text.strip().encode('utf-8')
                    f.write(len(source_text).to_bytes(2, 'little'))
                    f.write(source_text)
                
                # Write label count and labels
                f.write(len(self.labels).to_bytes(4, 'little'))
                for label_name, label in sorted(self.labels.items()):
                    name_bytes = label_name.encode('utf-8')
                    f.write(len(name_bytes).to_bytes(2, 'little'))
                    f.write(name_bytes)
                    f.write(label.address.to_bytes(4, 'little'))
                    f.write(label.line_defined.to_bytes(4, 'little'))  # Line number
                
                # Write symbol count and symbols
                f.write(len(self.symbols).to_bytes(4, 'little'))
                for symbol in self.symbols:
                    name_bytes = symbol.name.encode('utf-8')
                    f.write(len(name_bytes).to_bytes(2, 'little'))
                    f.write(name_bytes)
                    f.write(symbol.address.to_bytes(4, 'little'))
                    f.write(symbol.line_referenced.to_bytes(4, 'little'))
                
                # Write constant count and constants (for EQU)
                f.write(len(self.data_directive.constants).to_bytes(4, 'little'))
                for const_name, const_value in sorted(self.data_directive.constants.items()):
                    name_bytes = const_name.encode('utf-8')
                    f.write(len(name_bytes).to_bytes(2, 'little'))
                    f.write(name_bytes)
                    # Handle both signed and unsigned constants - convert to 32-bit representation
                    try:
                        if const_value < 0:
                            # Negative - use signed
                            f.write(const_value.to_bytes(4, 'little', signed=True))
                        else:
                            # Positive - use unsigned (allows full 32-bit range)
                            f.write(const_value.to_bytes(4, 'little', signed=False))
                    except (OverflowError, ValueError):
                        # Value out of range - clamp to 32 bits
                        f.write((const_value & 0xFFFFFFFF).to_bytes(4, 'little', signed=False))
            
            log_info(f"Object file written successfully", str(output_file))
            
            # Listing file is now generated by linker after all linking steps
            # This ensures addresses are stable and correct
            
            return True
            
        except Exception as e:
            log_error(f"Error writing object file: {str(e)}", 
                     str(output_file), error_code="OBJECT_FILE_WRITE_ERROR")
            return False
    
    def _write_listing_file(self, listing_file: Path) -> bool:
        """Write a MASM-style listing file with addresses, opcodes, and source"""
        try:
            listing_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(listing_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"TASM Assembler  Version 1.0.0  {datetime.now().strftime('%m/%d/%y  %H:%M:%S')}  Page 1\n\n")
                
                # Read original source lines for listing
                source_lines = []
                if self.current_file:
                    try:
                        with open(self.current_file, 'r', encoding='utf-8') as src_f:
                            source_lines = src_f.readlines()
                    except Exception:
                        pass
                
                # Create instruction map by address
                instruction_map = {instr.address: instr for instr in self.instructions}
                
                current_address = None
                for line_num, source_line in enumerate(source_lines, 1):
                    source_line = source_line.rstrip()
                    
                    # Check if this line has an instruction at any address
                    instruction = None
                    for instr in self.instructions:
                        if instr.source_line == line_num:
                            instruction = instr
                            break
                    
                    if instruction:
                        # Format opcode as bytes according to endianness and size
                        config = get_config()
                        opcode = instruction.opcode
                        
                        # Convert opcode to bytes based on instruction size
                        # For data directives (DB, DW, DD, etc.), show only the actual bytes
                        if instruction.size == 1:  # 1-byte (DB)
                            byte0 = opcode & 0xFF
                            opcode_str = f"{byte0:02X}            "
                        elif instruction.size == 2:  # 2-byte (DW or 16-bit instruction)
                            if config.is_little_endian:
                                byte0 = opcode & 0xFF
                                byte1 = (opcode >> 8) & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X}         "
                            else:
                                byte0 = (opcode >> 8) & 0xFF
                                byte1 = opcode & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X}         "
                        elif instruction.size == 3:  # 3-byte
                            if config.is_little_endian:
                                byte0 = opcode & 0xFF
                                byte1 = (opcode >> 8) & 0xFF
                                byte2 = (opcode >> 16) & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X}      "
                            else:
                                byte0 = (opcode >> 16) & 0xFF
                                byte1 = (opcode >> 8) & 0xFF
                                byte2 = opcode & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X}      "
                        elif instruction.size == 4:  # 4-byte (DD or 32-bit instruction)
                            if config.is_little_endian:
                                byte0 = opcode & 0xFF
                                byte1 = (opcode >> 8) & 0xFF
                                byte2 = (opcode >> 16) & 0xFF
                                byte3 = (opcode >> 24) & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X} {byte3:02X}"
                            else:
                                byte0 = (opcode >> 24) & 0xFF
                                byte1 = (opcode >> 16) & 0xFF
                                byte2 = (opcode >> 8) & 0xFF
                                byte3 = opcode & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X} {byte3:02X}"
                        else:
                            # For larger sizes, show only first 4 bytes for listing
                            # (Full data is in the binary, this is just for display)
                            if config.is_little_endian:
                                byte0 = opcode & 0xFF
                                byte1 = (opcode >> 8) & 0xFF
                                byte2 = (opcode >> 16) & 0xFF
                                byte3 = (opcode >> 24) & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X} {byte3:02X}+"
                            else:
                                byte0 = (opcode >> 24) & 0xFF
                                byte1 = (opcode >> 16) & 0xFF
                                byte2 = (opcode >> 8) & 0xFF
                                byte3 = opcode & 0xFF
                                opcode_str = f"{byte0:02X} {byte1:02X} {byte2:02X} {byte3:02X}+"
                        
                        # Format: Address  Machine Code (bytes)  Source Line
                        f.write(f"{instruction.address:08X}  {opcode_str}  {source_line}\n")
                    else:
                        # Source line without machine code
                        f.write(f"                                 {source_line}\n")
                
                # Write symbol table
                if self.labels:
                    f.write(f"\nTASM Assembler  Version 1.0.0  {datetime.now().strftime('%m/%d/%y  %H:%M:%S')}  Symbols:\n\n")
                    f.write("Symbol Table\n")
                    f.write("------------\n\n")
                    
                    for label_name, label in sorted(self.labels.items()):
                        f.write(f"{label_name:<15} {label.address:08X}h\n")
                
            return True
            
        except Exception as e:
            log_error(f"Error writing listing file: {str(e)}", 
                     str(listing_file), error_code="LISTING_FILE_WRITE_ERROR")
            return False
    
    def _write_preliminary_listing(self, listing_file: Path) -> bool:
        """
        Write preliminary listing file (.ls1) with ALL source lines.
        This includes comments, blank lines, directives - everything from the source.
        The linker will convert this to .lst with final addresses.
        """
        try:
            from datetime import datetime
            
            listing_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Get config for endianness
            config = get_config()
            
            # Create mapping from line number to instruction
            line_to_instruction = {}
            for instruction in self.instructions:
                line_to_instruction[instruction.source_line] = instruction
            
            with open(listing_file, 'w', encoding='utf-8') as f:
                # Write header
                timestamp = datetime.now().strftime('%m/%d/%y  %H:%M:%S')
                f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Page 1\n")
                f.write("\n")
                f.write("ADDR     CODE          LINE     SOURCE CODE\n")
                
                # Write all source lines from source_listing
                for line_num, address, opcode_bytes, source_text in self.source_listing:
                    # Try to get instruction for this line
                    instruction = line_to_instruction.get(line_num)
                    
                    if instruction and instruction.size > 0:
                        # Format address
                        addr_str = f"{instruction.address:08X}"
                        
                        # Format opcode bytes
                        opcode = instruction.opcode
                        size = instruction.size
                        code_bytes = []
                        
                        if size == 1:
                            code_bytes.append(f"{opcode:02X}")
                        elif size == 2:
                            if config.is_little_endian:
                                code_bytes.append(f"{opcode & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 8) & 0xFF:02X}")
                            else:
                                code_bytes.append(f"{(opcode >> 8) & 0xFF:02X}")
                                code_bytes.append(f"{opcode & 0xFF:02X}")
                        elif size == 4:
                            if config.is_little_endian:
                                code_bytes.append(f"{opcode & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 8) & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 16) & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 24) & 0xFF:02X}")
                            else:
                                code_bytes.append(f"{(opcode >> 24) & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 16) & 0xFF:02X}")
                                code_bytes.append(f"{(opcode >> 8) & 0xFF:02X}")
                                code_bytes.append(f"{opcode & 0xFF:02X}")
                        elif size > 4:
                            # Data directive with many bytes
                            for i in range(min(size, 8)):
                                code_bytes.append(f"{(opcode >> (i * 8)) & 0xFF:02X}")
                            if size > 8:
                                code_bytes.append("...")
                        
                        code_str = ' '.join(code_bytes)
                        code_str = f"{code_str:<12}"
                        
                        # Format line number
                        line_str = f"{line_num:5d}"
                        
                        # Write formatted line
                        f.write(f"{addr_str} {code_str} {line_str}    {source_text}\n")
                    
                    elif address is not None:
                        # Label or directive with address but no opcode yet
                        addr_str = f"{address:08X}"
                        code_str = " " * 12
                        line_str = f"{line_num:5d}"
                        f.write(f"{addr_str} {code_str} {line_str}    {source_text}\n")
                    
                    else:
                        # Comment, blank line, or EQU (no address)
                        addr_str = " " * 8
                        code_str = " " * 12
                        line_str = f"{line_num:5d}"
                        f.write(f"{addr_str} {code_str} {line_str}    {source_text}\n")
                
                # Write symbol table on Page 2
                f.write(f"\n")
                f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Symbols - Page 2\n")
                f.write("\n")
                f.write("ADDR     LABEL\n")
                
                # Write symbols sorted by address (low to high)
                for name, label in sorted(self.labels.items(), key=lambda x: x[1].address):
                    f.write(f"{label.address:08X} {name}\n")
            
            log_info(f"Preliminary listing file generated: {listing_file}")
            return True
            
        except Exception as e:
            log_warning(f"Could not generate preliminary listing file: {e}")
            import traceback
            traceback.print_exc()
            return False