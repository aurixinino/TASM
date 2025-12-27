"""
Linker Module

This module handles the linking phase, resolving external symbols,
combining object files, and generating the final executable binary.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import re

from logger import log_info, log_error, log_warning, log_debug, log_abort, get_logger
from config_loader import get_config

try:
    from intelhex import IntelHex
    INTELHEX_AVAILABLE = True
except ImportError:
    INTELHEX_AVAILABLE = False
    log_warning("intelhex library not available, falling back to custom implementation")

@dataclass
class ObjectFile:
    """Represents an object file"""
    filename: str
    instructions: List[Tuple[int, int, Optional[int], str, int]]  # address, opcode, operand, source, size (line_num stored separately)
    instruction_lines: List[int]  # Line numbers corresponding to each instruction
    labels: Dict[str, int]  # label_name -> address  
    label_lines: Dict[str, int]  # label_name -> line_num
    constants: Dict[str, int]  # EQU constants: name -> value
    unresolved_symbols: List[Tuple[str, int]]  # symbol_name, line_number
    code_size: int

@dataclass 
class LinkedSymbol:
    """Represents a symbol that has been linked"""
    name: str
    address: int
    defined_in: str
    references: List[Tuple[str, int]]  # (file, line) where referenced

class Linker:
    """Main linker engine"""
    
    def __init__(self):
        self.object_files: List[ObjectFile] = []
        self.global_symbols: Dict[str, LinkedSymbol] = {}
        self.unresolved_symbols: Set[str] = set()
        self.base_address = 0x8000
        self.current_address = 0x8000
        self.force_32bit = False  # Default to 16-bit optimization
        # Statistics for console output
        self.min_addr = 0
        self.max_addr = 0
        self.instruction_count = 0
        self.map_file_path = None
        
    def link_files(self, object_files: List[Path], output_file: Path, 
                  base_address: int = 0x8000, output_format: str = 'bin', force_32bit: bool = False,
                  no_implicit: bool = False) -> bool:
        """
        Link multiple object files into final executable
        
        Args:
            object_files: List of object file paths
            output_file: Output executable file path
            base_address: Base loading address
            output_format: Output format ('bin' or 'hex')
            force_32bit: If True, force 32-bit instruction variants during optimization
            
        Returns:
            True if successful, False if errors occurred
        """
        self.base_address = base_address
        self.current_address = base_address
        self.force_32bit = force_32bit  # Store for use in optimization
        
        log_info(f"Starting linking process with {len(object_files)} object files")
        log_info(f"Base address: 0x{base_address:04X}")
        
        # Load all object files
        if not self._load_object_files(object_files):
            return False
        
        # Resolve symbols
        if not self._resolve_symbols():
            return False
        
        # Optimize instruction sizes through iterative re-encoding
        # This handles forward references where instruction size affects displacement
        if not self._optimize_instruction_sizes():
            return False
        
        # Fix label addresses: labels should point to the instruction that follows them in source order
        # Use line numbers to determine which instruction follows each label
        log_info("Fixing label addresses based on source line numbers")
        for obj_file in self.object_files:
            updated_labels = {}
            
            for label_name, label_addr in obj_file.labels.items():
                label_line = obj_file.label_lines[label_name]
                
                # Find the first instruction AFTER this label's line number
                next_inst_addr = None
                for idx, inst_line in enumerate(obj_file.instruction_lines):
                    if inst_line > label_line:
                        next_inst_addr = obj_file.instructions[idx][0]
                        log_info(f"  Label '{label_name}' (line {label_line}) -> instruction at line {inst_line}, address 0x{next_inst_addr:08X}")
                        break
                
                if next_inst_addr is not None:
                    updated_labels[label_name] = next_inst_addr
                else:
                    # No instruction after label - keep original address
                    updated_labels[label_name] = label_addr
                    log_debug(f"  Label '{label_name}' (line {label_line}) - no following instruction, keeping 0x{label_addr:08X}")
            
            obj_file.labels = updated_labels
        
        # Rebuild global symbol table with corrected addresses
        for obj_file in self.object_files:
            for label_name, address in obj_file.labels.items():
                if label_name in self.global_symbols:
                    self.global_symbols[label_name].address = address
        
        # Final re-encoding pass with stabilized label addresses
        # This ensures all jump/branch instructions use the correct final addresses
        if not self._final_reencoding_pass():
            return False
        
        # Generate final output
        if not self._generate_output(output_file, output_format):
            return False
        
        log_info("Linking completed successfully")
        log_info(f"Final executable size: {self._calculate_final_size()} bytes")
        
        return True
    
    def _load_object_files(self, object_files: List[Path]) -> bool:
        """Load and parse object files"""
        log_debug("Loading object files")
        
        for obj_file in object_files:
            if not self._load_single_object_file(obj_file):
                return False
        
        log_info(f"Loaded {len(self.object_files)} object files")
        return True
    
    def _load_single_object_file(self, obj_file: Path) -> bool:
        """Load a single binary object file"""
        log_debug(f"Loading object file: {obj_file.name}")
        
        if not obj_file.exists():
            log_error(f"Object file not found: {obj_file.name}", 
                     str(obj_file), error_code="OBJECT_FILE_NOT_FOUND")
            return False
        
        try:
            with open(obj_file, 'rb') as f:
                # Read TOBJ header
                magic = f.read(4)
                if magic != b'TOBJ':
                    log_error(f"Invalid object file format: {obj_file.name}", 
                             str(obj_file), error_code="INVALID_OBJECT_FORMAT")
                    return False
                
                version = f.read(2)
                if version != b'\x01\x00':
                    log_error(f"Unsupported object file version: {obj_file.name}", 
                             str(obj_file), error_code="UNSUPPORTED_VERSION")
                    return False
                
                # Read source file name
                name_len = int.from_bytes(f.read(2), 'little')
                source_name = f.read(name_len).decode('utf-8')
                
                # Read instruction count
                instruction_count = int.from_bytes(f.read(4), 'little')
                
                # Read instructions
                instructions = []
                instruction_lines = []
                for _ in range(instruction_count):
                    address = int.from_bytes(f.read(4), 'little')
                    opcode = int.from_bytes(f.read(4), 'little')
                    size = int.from_bytes(f.read(1), 'little')
                    line_num = int.from_bytes(f.read(4), 'little')  # Read source line number
                    
                    # Read source text
                    text_len = int.from_bytes(f.read(2), 'little')
                    source_text = f.read(text_len).decode('utf-8')
                    
                    # Store instruction and its line number separately
                    instructions.append((address, opcode, None, source_text, size))
                    instruction_lines.append(line_num)
                    log_debug(f"Loaded instruction at line {line_num}: 0x{address:08X} = 0x{opcode:08X} (size: {size} bytes)")
                
                # Read label count and labels
                label_count = int.from_bytes(f.read(4), 'little')
                labels = {}
                label_lines = {}
                for _ in range(label_count):
                    name_len = int.from_bytes(f.read(2), 'little')
                    label_name = f.read(name_len).decode('utf-8')
                    address = int.from_bytes(f.read(4), 'little')
                    line_num = int.from_bytes(f.read(4), 'little')  # Read label line number
                    labels[label_name] = address
                    label_lines[label_name] = line_num
                    log_debug(f"Found label '{label_name}' at line {line_num}: 0x{address:08X}")
                
                # Read symbol count and symbols
                symbol_count = int.from_bytes(f.read(4), 'little')
                unresolved_symbols = []
                for _ in range(symbol_count):
                    name_len = int.from_bytes(f.read(2), 'little')
                    symbol_name = f.read(name_len).decode('utf-8')
                    address = int.from_bytes(f.read(4), 'little')
                    line_ref = int.from_bytes(f.read(4), 'little')
                    unresolved_symbols.append((symbol_name, line_ref))
                    log_debug(f"Found unresolved symbol: {symbol_name}")
                
                # Read constant count and constants (EQU directives)
                constants = {}
                const_count = int.from_bytes(f.read(4), 'little')
                for _ in range(const_count):
                    name_len = int.from_bytes(f.read(2), 'little')
                    const_name = f.read(name_len).decode('utf-8')
                    # Read as unsigned, then convert to signed if needed (for Python compatibility)
                    const_value_unsigned = int.from_bytes(f.read(4), 'little', signed=False)
                    # If high bit is set, interpret as signed negative
                    if const_value_unsigned >= 0x80000000:
                        const_value = const_value_unsigned - 0x100000000
                    else:
                        const_value = const_value_unsigned
                    constants[const_name] = const_value
                    log_debug(f"Found constant '{const_name}' = {const_value}")
            
            # Calculate code size
            code_size = len(instructions)
            
            # Create object file record
            obj_record = ObjectFile(
                filename=str(obj_file),
                instructions=instructions,
                instruction_lines=instruction_lines,
                labels=labels,
                label_lines=label_lines,
                constants=constants,
                unresolved_symbols=unresolved_symbols,
                code_size=code_size
            )
            
            self.object_files.append(obj_record)
            
            log_info(f"Loaded object file: {obj_file.name}")
            log_debug(f"  Instructions: {len(instructions)}")
            log_debug(f"  Labels: {len(labels)}")
            log_debug(f"  Unresolved symbols: {len(unresolved_symbols)}")
            
            return True
            
        except Exception as e:
            log_error(f"Error loading object file {obj_file.name}: {str(e)}", 
                     str(obj_file), error_code="OBJECT_LOAD_ERROR")
            return False
    
    def _resolve_symbols(self) -> bool:
        """Resolve all symbols across object files"""
        log_debug("Resolving symbols")
        
        # First, collect all defined symbols (labels)
        symbol_definitions = {}
        
        for obj_file in self.object_files:
            for label_name, address in obj_file.labels.items():
                if label_name in symbol_definitions:
                    log_error(f"Symbol '{label_name}' multiply defined", 
                             obj_file.filename, error_code="MULTIPLY_DEFINED_SYMBOL")
                    log_debug(f"Previous definition in: {symbol_definitions[label_name][1]}")
                    return False
                
                symbol_definitions[label_name] = (address, obj_file.filename)
                log_debug(f"Symbol '{label_name}' defined at 0x{address:04X} in {obj_file.filename}")
        
        # Collect all symbol references
        symbol_references = {}
        
        for obj_file in self.object_files:
            for symbol_name, line_num in obj_file.unresolved_symbols:
                if symbol_name not in symbol_references:
                    symbol_references[symbol_name] = []
                symbol_references[symbol_name].append((obj_file.filename, line_num))
        
        # Check for unresolved symbols
        unresolved_count = 0
        for symbol_name, references in symbol_references.items():
            if symbol_name not in symbol_definitions:
                self.unresolved_symbols.add(symbol_name)
                unresolved_count += 1
                
                for file_ref, line_ref in references:
                    log_error(f"Unresolved external symbol: '{symbol_name}'", 
                             file_ref, line_ref, error_code="UNRESOLVED_SYMBOL")
        
        if unresolved_count > 0:
            log_error(f"Found {unresolved_count} unresolved symbols", 
                     error_code="UNRESOLVED_SYMBOLS")
            return False
        
        # Create linked symbol table
        for symbol_name, (address, defining_file) in symbol_definitions.items():
            references = symbol_references.get(symbol_name, [])
            
            self.global_symbols[symbol_name] = LinkedSymbol(
                name=symbol_name,
                address=address,
                defined_in=defining_file,
                references=references
            )
        
        log_info(f"Symbol resolution completed")
        log_info(f"Resolved {len(self.global_symbols)} symbols")
        
        # Log symbol table
        if self.global_symbols:
            log_debug("Global symbol table:")
            for name, symbol in sorted(self.global_symbols.items()):
                log_debug(f"  {name}: 0x{symbol.address:04X} (defined in {Path(symbol.defined_in).name})")
        
        return True
    
    def _optimize_instruction_sizes(self) -> bool:
        """
        Iteratively re-encode instructions to optimize sizes.
        
        This handles the chicken-and-egg problem where:
        - Instruction size affects displacement calculation
        - Displacement affects instruction variant selection  
        - Instruction variant affects instruction size
        
        Algorithm:
        1. Calculate addresses with current instruction sizes
        2. Re-encode each instruction with updated label addresses
        3. If any instruction size changed, recalculate and repeat
        4. Stop when addresses stabilize (no size changes)
        
        Returns:
            True if successful, False if errors occurred
        """
        from instruction_loader import InstructionSetLoader
        from instruction_encoder import InstructionEncoder
        
        log_info("Starting instruction size optimization (multi-pass linking)")
        
        # Load instruction set
        try:
            from config_loader import get_config
            config = get_config()
            instruction_set_file = config.instruction_set_path
            
            loader = InstructionSetLoader(force_32bit=self.force_32bit)
            if not loader.load_instruction_set(instruction_set_file):
                log_error("Failed to load instruction set for re-encoding")
                return False
            
            encoder = InstructionEncoder(loader)
        except Exception as e:
            log_error(f"Failed to initialize encoder for optimization: {e}")
            return False
        
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            log_debug(f"Optimization pass {iteration}")
            
            # Build global label map with current addresses
            global_labels = {}
            for obj_file in self.object_files:
                for label_name, address in obj_file.labels.items():
                    global_labels[label_name] = address
            
            if iteration <= 2:  # Show labels on first two iterations
                log_info(f"Pass {iteration} labels: " + ", ".join(f"{name}=0x{addr:08X}" for name, addr in sorted(global_labels.items())))
            
            # Try to re-encode each instruction
            sizes_changed = False
            
            for obj_file in self.object_files:
                # First, re-encode all instructions with current label addresses
                # Store the new encodings with OLD addresses
                new_instructions = []
                
                for address, opcode, operand, source_text, size in obj_file.instructions:
                    # Skip data directives (DB, DW, etc.) - they don't need re-encoding
                    if source_text.strip().upper().startswith(('DB', 'DW', 'DD', 'DQ', 'DT', 'DO', 'DY', 'DZ', 'RESB', 'TIMES')):
                        new_instructions.append((address, opcode, operand, source_text, size))
                        continue
                    
                    # Try to parse and re-encode instruction
                    parsed = encoder.parse_instruction_line(source_text, 0)
                    if parsed is None:
                        # Not an instruction (label, directive, etc.) - keep as is
                        new_instructions.append((address, opcode, operand, source_text, size))
                        continue
                    
                    # Re-encode with current global labels
                    encoded = encoder.encode_instruction(parsed, address, global_labels)
                    if encoded is None:
                        # Encoding failed - keep original
                        new_instructions.append((address, opcode, operand, source_text, size))
                        continue
                    
                    # Check if size changed
                    new_size = encoded.definition.opcode_size // 8
                    if new_size != size:
                        log_info(f"  Size changed for '{source_text.strip()}' at 0x{address:08X}: {size} -> {new_size} bytes")
                        sizes_changed = True
                    
                    # Update instruction with new encoding (keep old address for now)
                    new_instructions.append((address, encoded.binary_value, operand, source_text, new_size))
                
                # Now recalculate addresses based on new sizes, preserving .ORG gaps
                final_instructions = []
                cumulative_shift = 0
                prev_address = None
                
                for old_address, opcode, operand, source_text, new_size in new_instructions:
                    # Detect gaps from .ORG directives
                    if prev_address is not None:
                        # Get previous instruction's size from final_instructions
                        if final_instructions:
                            prev_final_addr, _, _, _, prev_size = final_instructions[-1]
                            expected_next = prev_final_addr + prev_size
                            # If there's a gap, reset cumulative shift
                            if old_address > prev_address + (final_instructions[-1][4] if final_instructions else 0):
                                # Gap detected - preserve it by not adding to shift
                                gap_size = old_address - (prev_address + (final_instructions[-1][4] if final_instructions else 0))
                                log_debug(f"  Preserving gap of {gap_size} bytes before 0x{old_address:08X}")
                                cumulative_shift = 0  # Reset shift after gap
                    
                    new_address = old_address + cumulative_shift
                    final_instructions.append((new_address, opcode, operand, source_text, new_size))
                    
                    # Update cumulative shift for next instruction
                    # (This accounts for size changes in THIS instruction affecting addresses of FOLLOWING instructions)
                    if prev_address is not None and final_instructions and len(final_instructions) >= 2:
                        # Compare new size vs original size
                        # We need to track original sizes... but they're in obj_file.instructions
                        # Let me rebuild this logic more cleanly
                        pass
                    
                    prev_address = old_address
                
                # Actually, this is getting too complicated. Let me use a simpler approach:
                # Just recalculate addresses sequentially, preserving gaps
                final_instructions = []
                for idx, (old_addr, opcode, operand, source_text, new_size) in enumerate(new_instructions):
                    if idx == 0:
                        # First instruction keeps its address
                        new_addr = old_addr
                    else:
                        # Check if there should be a gap
                        prev_old_addr = obj_file.instructions[idx-1][0]
                        prev_old_size = obj_file.instructions[idx-1][4]
                        prev_new_addr = final_instructions[-1][0]
                        prev_new_size = final_instructions[-1][4]
                        
                        # Expected address if contiguous
                        expected_old = prev_old_addr + prev_old_size
                        expected_new = prev_new_addr + prev_new_size
                        
                        # If there was a gap in original, preserve it
                        if old_addr > expected_old:
                            gap = old_addr - expected_old
                            new_addr = expected_new + gap
                        else:
                            new_addr = expected_new
                    
                    final_instructions.append((new_addr, opcode, operand, source_text, new_size))
                
                obj_file.instructions = final_instructions
                
                # Update label addresses based on instruction moves
                # Build mapping from old instruction addresses to new ones
                addr_map = {}
                for old_inst, new_inst in zip(new_instructions, final_instructions):
                    addr_map[old_inst[0]] = new_inst[0]
                
                updated_labels = {}
                for label_name, label_addr in obj_file.labels.items():
                    if label_addr in addr_map:
                        # Label matches an instruction address
                        # Check if this instruction is a branch/jump - if so, label probably belongs to NEXT instruction
                        inst_idx = None
                        for idx, (old_addr, _, _, source, _) in enumerate(new_instructions):
                            if old_addr == label_addr:
                                inst_idx = idx
                                break
                        
                        if inst_idx is not None:
                            source_upper = new_instructions[inst_idx][3].strip().upper()
                            # Check if it's a branch/jump instruction
                            is_branch = any(source_upper.startswith(prefix) for prefix in ['J', 'CALL', 'JNZ', 'JZ', 'JEQ', 'JNE', 'JL', 'LOOP'])
                            
                            # Don't move function entry points (typically at first instruction, or PascalCase with underscore and "Assembly")
                            is_likely_function = (inst_idx == 0 or  
                                                 ('_' in label_name and label_name.endswith('Assembly')))
                            
                            if is_branch and not is_likely_function and inst_idx + 1 < len(final_instructions):
                                # This is a branch target (not a function) - assign label to next instruction
                                updated_labels[label_name] = final_instructions[inst_idx + 1][0]
                                log_info(f"  Moved label '{label_name}' from branch at 0x{label_addr:08X} to next instruction at 0x{final_instructions[inst_idx + 1][0]:08X}")
                            else:
                                # Function entry point, not a branch, or no next instruction - keep at this address
                                updated_labels[label_name] = addr_map[label_addr]
                        else:
                            updated_labels[label_name] = addr_map[label_addr]
                    else:
                        # Label doesn't match - find nearest instruction before it and apply same shift
                        new_addr = label_addr
                        for old_addr in sorted(addr_map.keys(), reverse=True):
                            if old_addr <= label_addr:
                                shift = addr_map[old_addr] - old_addr
                                new_addr = label_addr + shift
                                break
                        updated_labels[label_name] = new_addr
                
                obj_file.labels = updated_labels
            
            # If no sizes changed and we've done at least 2 iterations, we're done
            # (First iteration might use wrong addresses from assembler's initial pass)
            if not sizes_changed and iteration >= 2:
                log_info(f"Instruction sizes stabilized after {iteration} iteration(s)")
                break
            elif not sizes_changed:
                log_info(f"No size changes on iteration {iteration}, forcing another pass to verify stability")
        
        if iteration >= max_iterations:
            log_warning(f"Instruction size optimization did not converge after {max_iterations} iterations")
        
        return True
    
    def _final_reencoding_pass(self) -> bool:
        """
        Perform final re-encoding of all instructions with stabilized label addresses.
        
        After address stabilization and label fixing, this ensures all jump/branch 
        instructions use the correct final addresses for their targets.
        
        Returns:
            True if successful, False if errors occurred
        """
        from instruction_loader import InstructionSetLoader
        from instruction_encoder import InstructionEncoder
        
        log_info("Performing final re-encoding with stabilized label addresses")
        
        # Load instruction set
        try:
            from config_loader import get_config
            config = get_config()
            instruction_set_file = config.instruction_set_path
            
            loader = InstructionSetLoader(force_32bit=self.force_32bit)
            if not loader.load_instruction_set(instruction_set_file):
                log_error("Failed to load instruction set for final re-encoding")
                return False
            
            encoder = InstructionEncoder(loader)
        except Exception as e:
            log_error(f"Failed to initialize encoder for final re-encoding: {e}")
            return False
        
        # Build final global label map
        final_global_labels = {}
        for obj_file in self.object_files:
            for label_name, address in obj_file.labels.items():
                final_global_labels[label_name] = address
        
        log_info("Final label addresses: " + ", ".join(f"{name}=0x{addr:08X}" for name, addr in sorted(final_global_labels.items())))
        
        # Re-encode all instructions one last time with final addresses
        for obj_file in self.object_files:
            final_instructions = []
            
            for address, opcode, operand, source_text, size in obj_file.instructions:
                # Skip data directives
                if source_text.strip().upper().startswith(('DB', 'DW', 'DD', 'DQ', 'DT', 'DO', 'DY', 'DZ', 'RESB', 'TIMES')):
                    final_instructions.append((address, opcode, operand, source_text, size))
                    continue
                
                # Try to parse and re-encode instruction
                parsed = encoder.parse_instruction_line(source_text, 0)
                if parsed is None:
                    final_instructions.append((address, opcode, operand, source_text, size))
                    continue
                
                # Re-encode with final global labels
                encoded = encoder.encode_instruction(parsed, address, final_global_labels)
                if encoded is None:
                    # Encoding failed - keep original
                    final_instructions.append((address, opcode, operand, source_text, size))
                    continue
                
                # Use the new encoding
                final_instructions.append((address, encoded.binary_value, operand, source_text, size))
                
                # Log if encoding changed (for debugging jump/branch instructions)
                if encoded.binary_value != opcode:
                    log_info(f"  Final re-encode: '{source_text.strip()}' at 0x{address:08X}: 0x{opcode:04X} -> 0x{encoded.binary_value:04X}")
            
            obj_file.instructions = final_instructions
        
        return True
    
    def _recalculate_addresses(self) -> None:
        """Recalculate instruction and label addresses after size changes
        
        This preserves address gaps created by .ORG directives by only adjusting
        addresses based on cumulative size changes, not by making them contiguous.
        """
        log_debug("Recalculating addresses")
        
        for obj_file in self.object_files:
            # Build mapping from old addresses to new addresses
            address_map = {}
            new_instructions = []
            
            # Track cumulative address shift (positive = addresses move up, negative = move down)
            cumulative_shift = 0
            prev_address = 0
            prev_size = 0
            
            for old_address, opcode, operand, source_text, size in obj_file.instructions:
                # Check if there's a gap before this instruction (e.g., from .ORG directive)
                # If current instruction's address jumped (not contiguous), preserve the gap
                if prev_address > 0:
                    expected_address = prev_address + prev_size
                    if old_address != expected_address:
                        # There's a gap - reset cumulative shift to maintain it
                        gap_size = old_address - expected_address
                        log_debug(f"  Preserving gap of {gap_size} bytes before 0x{old_address:08X}")
                        # Don't modify cumulative_shift - the gap is intentional
                
                # Calculate new address by applying cumulative shift
                new_address = old_address + cumulative_shift
                address_map[old_address] = new_address
                
                # Update cumulative shift if size changed
                # (This will affect all subsequent instructions)
                old_size = prev_size if prev_address == old_address else size  # Get old size from previous pass
                # Actually, we don't know the old size here - this is the NEW size after re-encoding
                # The shift has already been applied by updating the instruction tuples
                # So we don't need to calculate shift here - just preserve gaps
                
                # Update instruction address
                new_instructions.append((new_address, opcode, operand, source_text, size))
                
                prev_address = old_address
                prev_size = size
            
            obj_file.instructions = new_instructions
            
            # Update label addresses using the address map
            updated_labels = {}
            for label_name, old_address in obj_file.labels.items():
                if old_address in address_map:
                    updated_labels[label_name] = address_map[old_address]
                    log_debug(f"  Label '{label_name}': 0x{old_address:08X} -> 0x{address_map[old_address]:08X}")
                else:
                    # Label doesn't match any instruction address
                    # Apply the same shift as nearby instructions
                    # Find the closest instruction address before this label
                    closest_shift = 0
                    for inst_old_addr, inst_new_addr in address_map.items():
                        if inst_old_addr <= old_address:
                            closest_shift = inst_new_addr - inst_old_addr
                    
                    new_address = old_address + closest_shift
                    updated_labels[label_name] = new_address
                    log_debug(f"  Label '{label_name}': 0x{old_address:08X} -> 0x{new_address:08X} (interpolated)")
            
            obj_file.labels = updated_labels
    
    def _generate_output(self, output_file: Path, output_format: str) -> bool:
        """Generate final output in specified format"""
        if output_format == 'hex':
            log_debug("Generating Intel HEX output")
        elif output_format == 'txt':
            log_debug("Generating plain text output")
        else:
            log_debug("Generating binary output")
        
        try:
            # Collect all instructions sorted by address
            all_instructions = []
            
            for obj_file in self.object_files:
                for address, opcode, operand, source_text, size in obj_file.instructions:
                    all_instructions.append((address, opcode, operand, source_text, obj_file.filename, size))
            
            # Sort by address
            all_instructions.sort(key=lambda x: x[0])
            
            if not all_instructions:
                log_abort("No instructions to link", error_code="NO_INSTRUCTIONS")
                # Still generate empty output file for the requested format
                memory_image = {}
                if output_format == 'hex':
                    return self._generate_intel_hex(memory_image, output_file)
                elif output_format == 'txt':
                    # Generate empty text file
                    try:
                        with open(output_file, 'w') as f:
                            pass  # Create empty file
                        return True
                    except Exception as e:
                        log_error(f"Failed to create empty output file: {e}", error_code="FILE_CREATION_ERROR")
                        return False
                else:
                    # Generate empty binary file
                    try:
                        with open(output_file, 'wb') as f:
                            pass  # Create empty file
                        return True
                    except Exception as e:
                        log_error(f"Failed to create empty output file: {e}", error_code="FILE_CREATION_ERROR")
                        return False
            
            # Check for address conflicts
            if not self._check_address_conflicts(all_instructions):
                return False
            
            # Generate memory image
            memory_image = {}
            config = get_config()
            
            # Import data directive handler for re-encoding data directives
            from data_directives import DataDirective
            endianness = 'little' if config.is_little_endian else 'big'
            data_handler = DataDirective(endianness=endianness, labels=self.global_symbols)
            
            # Collect all constants from object files and add to data handler
            for obj_file in self.object_files:
                data_handler.constants.update(obj_file.constants)
            
            for address, opcode, operand, source_text, source_file, size in all_instructions:
                # Check if this is a data directive by looking at the source
                parts = source_text.strip().split(maxsplit=1)
                directive = parts[0].upper() if parts else ''
                
                # Check if it's a data directive (DB, DW, DD, etc., RESB, TIMES, INCBIN)
                is_data_directive = (directive in data_handler.DATA_SIZES or 
                                    directive in data_handler.RESERVE_SIZES or
                                    directive in ['TIMES', 'INCBIN'])
                
                if is_data_directive:
                    # Re-encode the data directive to get full data
                    try:
                        # Calculate size first
                        size = data_handler.calculate_size(source_text, address)
                        
                        # Handle different directive types
                        if directive in data_handler.RESERVE_SIZES:
                            # RESB/RESW etc - write zeros
                            if size > 10000000:  # Safety check for huge allocations (10MB)
                                log_error(f"RESB size too large: {size} bytes at 0x{address:08X}")
                                return False
                            for i in range(size):
                                memory_image[address + i] = 0
                        elif directive == 'TIMES':
                            # TIMES - parse count and data, then repeat
                            count, rest = data_handler.process_times(source_text, address)
                            # Parse the repeated directive
                            rest_parts = rest.strip().split(maxsplit=1)
                            rest_directive = rest_parts[0].upper() if rest_parts else ''
                            if rest_directive in data_handler.DATA_SIZES:
                                rest_operands = rest_parts[1] if len(rest_parts) > 1 else ''
                                values = data_handler.parse_data_list(rest_operands)
                                single_data = data_handler.encode_data(rest_directive, values)
                                # Repeat the data 'count' times
                                offset = 0
                                for _ in range(count):
                                    for byte_val in single_data:
                                        memory_image[address + offset] = byte_val
                                        offset += 1
                            else:
                                # Can't encode, fill with zeros
                                for i in range(size):
                                    memory_image[address + i] = 0
                        elif directive in data_handler.DATA_SIZES:
                            # DB, DW, DD etc - re-encode the data
                            operands = parts[1] if len(parts) > 1 else ''
                            values = data_handler.parse_data_list(operands)
                            data = data_handler.encode_data(directive, values)
                            for i, byte_val in enumerate(data):
                                memory_image[address + i] = byte_val
                        elif directive == 'INCBIN':
                            # INCBIN - read the binary file
                            from pathlib import Path
                            operands = parts[1] if len(parts) > 1 else ''
                            # Determine base directory from source file
                            source_path = Path(source_file) if source_file else None
                            base_dir = source_path.parent if source_path and source_path.is_absolute() else None
                            data = data_handler.process_incbin(operands, base_dir)
                            for i, byte_val in enumerate(data):
                                memory_image[address + i] = byte_val
                    except Exception as e:
                        log_warning(f"Failed to re-encode data directive at 0x{address:08X}: {e}")
                        # Fall back to opcode-based encoding
                        is_data_directive = False
                
                if not is_data_directive:
                    # Regular instruction - store opcode bytes according to configured endianness
                    # For TriCore and little-endian architectures, the LSB comes first
                    if config.is_little_endian:
                        # Little-endian: LSB at lower address
                        memory_image[address] = opcode & 0xFF
                        memory_image[address + 1] = (opcode >> 8) & 0xFF
                        memory_image[address + 2] = (opcode >> 16) & 0xFF
                        memory_image[address + 3] = (opcode >> 24) & 0xFF
                    else:
                        # Big-endian: MSB at lower address
                        memory_image[address] = (opcode >> 24) & 0xFF
                        memory_image[address + 1] = (opcode >> 16) & 0xFF
                        memory_image[address + 2] = (opcode >> 8) & 0xFF
                        memory_image[address + 3] = opcode & 0xFF
                
                # Note: TriCore instructions don't use separate operands, 
                # everything is encoded in the 32-bit opcode
            
            # Write binary file
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if output_format == 'hex':
                # Generate Intel HEX format
                if not self._generate_intel_hex(memory_image, output_file):
                    return False
                    
                # Write map file
                map_file = output_file.with_suffix('.map')
                self._write_map_file(map_file, all_instructions)
                
                min_addr = min(memory_image.keys())
                max_addr = max(memory_image.keys())
                
                # Store statistics for console output
                self.min_addr = min_addr
                self.max_addr = max_addr
                self.instruction_count = len(all_instructions)
                self.map_file_path = str(map_file)
                
                log_info(f"Memory range: 0x{min_addr:08X} - 0x{max_addr:08X}")
                log_info(f"Data bytes: {len(memory_image)} bytes")
                log_info(f"Map file generated: {map_file}")
                
                # Generate listing file with final linked addresses
                listing_file = output_file.parent / (output_file.stem + '.lst')
                self._generate_listing_file(listing_file, all_instructions)
            elif output_format == 'txt':
                # Generate plain text format with ADDRESS INSTRUCTION
                if not self._generate_plain_text(all_instructions, output_file):
                    return False
                    
                # Write map file
                map_file = output_file.with_suffix('.map')
                self._write_map_file(map_file, all_instructions)
                
                min_addr = all_instructions[0][0]
                max_addr = all_instructions[-1][0] + 3  # Add 4 bytes for last instruction
                
                # Store statistics for console output
                self.min_addr = min_addr
                self.max_addr = max_addr
                self.instruction_count = len(all_instructions)
                self.map_file_path = str(map_file)
                
                log_info(f"Text file generated: {output_file}")
                log_info(f"Memory range: 0x{min_addr:08X} - 0x{max_addr:08X}")
                log_info(f"Instructions: {len(all_instructions)}")
                log_info(f"Map file generated: {map_file}")
                
                # Generate listing file with final linked addresses
                listing_file = output_file.parent / (output_file.stem + '.lst')
                self._generate_listing_file(listing_file, all_instructions)
            else:
                # Generate binary format
                min_addr = min(memory_image.keys())
                max_addr = max(memory_image.keys())
                
                binary_data = bytearray(max_addr - min_addr + 1)
                
                for addr, byte_val in memory_image.items():
                    binary_data[addr - min_addr] = byte_val
                
                with open(output_file, 'wb') as f:
                    f.write(binary_data)
                
                # Write map file
                map_file = output_file.with_suffix('.map')
                self._write_map_file(map_file, all_instructions)
                
                # Store statistics for console output
                self.min_addr = min_addr
                self.max_addr = max_addr
                self.instruction_count = len(all_instructions)
                self.map_file_path = str(map_file)
                
                log_info(f"Binary file generated: {output_file}")
                log_info(f"Memory range: 0x{min_addr:08X} - 0x{max_addr:08X}")
                log_info(f"Binary size: {len(binary_data)} bytes")
                log_info(f"Map file generated: {map_file}")
                
                # Generate listing file with final linked addresses
                listing_file = output_file.parent / (output_file.stem + '.lst')
                self._generate_listing_file(listing_file, all_instructions)
            
            return True
            
        except Exception as e:
            log_error(f"Error generating binary: {str(e)}", 
                     str(output_file), error_code="BINARY_GENERATION_ERROR")
            return False
    
    def _check_address_conflicts(self, instructions: List[Tuple]) -> bool:
        """Check for overlapping addresses"""
        log_debug("Checking for address conflicts")
        
        occupied_addresses = set()
        conflicts = []
        
        for address, opcode, operand, source_text, source_file, size in instructions:
            # Size is now provided in the tuple
            # Keep existing logic as fallback
            if size == 0:
                size = 1
                if operand is not None:
                    if operand <= 0xFF:
                        size = 2
                    else:
                        size = 3
            
            # Check each byte of the instruction
            for offset in range(size):
                addr = address + offset
                if addr in occupied_addresses:
                    conflicts.append((addr, source_file, source_text))
                else:
                    occupied_addresses.add(addr)
        
        if conflicts:
            log_error("Address conflicts detected:", error_code="ADDRESS_CONFLICTS")
            for addr, source_file, source_text in conflicts:
                log_error(f"  Address 0x{addr:04X} conflict in {Path(source_file).name}: {source_text}", 
                         source_file, error_code="ADDRESS_CONFLICT")
            return False
        
        return True
    
    def _update_listing_from_ls1(self, ls1_file: Path, listing_file: Path, all_instructions: List[Tuple]) -> bool:
        """
        Update preliminary listing (.ls1) with final linked addresses to create final .lst file.
        
        The .ls1 file contains all source lines (comments, directives, etc.) with preliminary addresses.
        We update the addresses and opcodes for instructions that were re-encoded during linking.
        
        Args:
            ls1_file: Input preliminary listing file
            listing_file: Output final listing file
            all_instructions: List of final instructions with linked addresses
        """
        try:
            from datetime import datetime
            
            # Build mapping from line number to final instruction
            # Format: line_num -> (address, opcode, size)
            line_to_final_instruction = {}
            
            for obj_file in self.object_files:
                for idx, (address, opcode, operand, source_text, size) in enumerate(obj_file.instructions):
                    if idx < len(obj_file.instruction_lines):
                        line_num = obj_file.instruction_lines[idx]
                        line_to_final_instruction[line_num] = (address, opcode, size)
            
            # Get config for endianness
            config = get_config()
            
            # Read the .ls1 file
            with open(ls1_file, 'r', encoding='utf-8') as f:
                ls1_lines = f.readlines()
            
            # Write updated .lst file
            with open(listing_file, 'w', encoding='utf-8') as f:
                # Update timestamp but keep same format
                timestamp = datetime.now().strftime('%m/%d/%y  %H:%M:%S')
                
                in_symbol_table = False
                symbol_table_written = False
                
                for line in ls1_lines:
                    # Update timestamps
                    if 'TASM Assembler  Version' in line:
                        if 'Symbols' in line:
                            # Start of symbol table - write header and then regenerate table
                            f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Symbols - Page 2\n")
                            in_symbol_table = True
                        else:
                            f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Page 1\n")
                        continue
                    
                    # When we hit symbol table, regenerate it completely sorted by address
                    if in_symbol_table:
                        if not symbol_table_written:
                            f.write("\n")
                            f.write("ADDR     LABEL\n")
                            # Write symbols sorted by address (low to high)
                            for name, symbol in sorted(self.global_symbols.items(), key=lambda x: x[1].address):
                                f.write(f"{symbol.address:08X} {name}\n")
                            symbol_table_written = True
                        # Skip all remaining lines (old symbol table)
                        continue
                    
                    # Pass through header lines
                    if line.strip() in ['', 'ADDR     CODE          LINE     SOURCE CODE', 'ADDR     LABEL']:
                        f.write(line)
                        continue
                    
                    # Update instruction lines with final addresses and opcodes
                    if not in_symbol_table and len(line) > 30:
                        # Parse line: "ADDR     CODE          LINE     SOURCE CODE"
                        # Extract line number (columns 23-27)
                        try:
                            line_num_str = line[23:28].strip()
                            if line_num_str.isdigit():
                                line_num = int(line_num_str)
                                
                                # Check if we have a final instruction for this line
                                if line_num in line_to_final_instruction:
                                    address, opcode, size = line_to_final_instruction[line_num]
                                    
                                    # Extract source code (starts at column 31 after 4 spaces following line number)
                                    source_text = line[31:].rstrip('\n')
                                    
                                    # Format address
                                    addr_str = f"{address:08X}"
                                    
                                    # Format opcode bytes
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
                                    
                                    code_str = ' '.join(code_bytes)
                                    code_str = f"{code_str:<12}"
                                    
                                    line_str = f"{line_num:5d}"
                                    
                                    # Write updated line
                                    f.write(f"{addr_str} {code_str} {line_str}    {source_text}\n")
                                    continue
                        except (ValueError, IndexError):
                            pass
                    
                    # Pass through unchanged
                    f.write(line)
            
            log_info(f"Final listing file generated from {ls1_file.name}: {listing_file}")
            return True
            
        except Exception as e:
            log_warning(f"Could not update listing from .ls1: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _generate_listing_file(self, listing_file: Path, all_instructions: List[Tuple]) -> bool:
        """
        Generate final listing file (.lst) after linking with correct addresses.
        
        This function reads the preliminary .ls1 file generated by the assembler
        (which contains ALL source lines including comments) and updates the addresses
        with the final linked addresses.
        
        Format:
        - Header: TASM Assembler Version xxx Date Time ... Page 1
        - Empty line
        - Column header: ADDR     CODE      LINE     SOURCE CODE
        - All source lines with final addresses
        - Page 2: Symbol table with ADDR and LABEL columns
        
        Args:
            listing_file: Path to output .lst file
            all_instructions: List of (address, opcode, operand, source_text, source_file, size)
        """
        try:
            from datetime import datetime
            
            listing_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if preliminary .ls1 file exists
            ls1_file = listing_file.with_suffix('.ls1')
            if ls1_file.exists():
                # Read and update the .ls1 file with final addresses
                return self._update_listing_from_ls1(ls1_file, listing_file, all_instructions)
            
            # If no .ls1 file, generate listing from instructions only (old behavior)
            # Build mapping from instructions to line numbers
            instruction_line_map = {}  # (address, opcode) -> line_num
            
            for obj_file in self.object_files:
                for idx, (address, opcode, operand, source_text, size) in enumerate(obj_file.instructions):
                    if idx < len(obj_file.instruction_lines):
                        line_num = obj_file.instruction_lines[idx]
                        instruction_line_map[(address, opcode)] = line_num
            
            # Get config for endianness
            config = get_config()
            
            with open(listing_file, 'w', encoding='utf-8') as f:
                # Page 1: Code Listing
                timestamp = datetime.now().strftime('%m/%d/%y  %H:%M:%S')
                f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Page 1\n")
                f.write("\n")
                f.write("ADDR     CODE          LINE     SOURCE CODE\n")
                
                # Write instructions
                for instr in all_instructions:
                    address, opcode, operand, source_text, source_file, size = instr
                    
                    # Look up line number from mapping
                    line_num = instruction_line_map.get((address, opcode), 0)
                    
                    # Format address (8 hex digits)
                    addr_str = f"{address:08X}"
                    
                    # Format code bytes based on size and endianness
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
                    
                    # Format code string (up to 12 characters for alignment)
                    code_str = ' '.join(code_bytes)
                    code_str = f"{code_str:<12}"
                    
                    # Format line number (5 digits)
                    line_str = f"{line_num:5d}" if line_num else "     "
                    
                    # Write formatted line
                    f.write(f"{addr_str} {code_str} {line_str}    {source_text}\n")
                
                # Page 2: Symbol Table
                f.write(f"\n")
                f.write(f"TASM Assembler  Version 1.0.0  {timestamp}  Symbols - Page 2\n")
                f.write("\n")
                f.write("ADDR     LABEL\n")
                
                # Write symbols sorted by address (low to high)
                for name, symbol in sorted(self.global_symbols.items(), key=lambda x: x[1].address):
                    f.write(f"{symbol.address:08X} {name}\n")
            
            log_info(f"Listing file generated: {listing_file}")
            return True
            
        except Exception as e:
            log_warning(f"Could not generate listing file: {e}")
            import traceback
            traceback.print_exc()
            return True  # Non-fatal
    
    def _write_map_file(self, map_file: Path, instructions: List[Tuple]) -> bool:
        """Write linker map file"""
        try:
            with open(map_file, 'w', encoding='utf-8') as f:
                f.write("Linker Map File\n")
                f.write("===============\n\n")
                
                # Memory layout
                f.write("Memory Layout:\n")
                f.write("--------------\n")
                
                for address, opcode, operand, source_text, source_file, size in instructions:
                    f.write(f"0x{address:04X}: {opcode:02X}")
                    
                    if operand is not None:
                        if operand <= 0xFF:
                            f.write(f" {operand:02X}")
                        else:
                            f.write(f" {operand & 0xFF:02X} {(operand >> 8) & 0xFF:02X}")
                    
                    f.write(f"  ; {source_text} ({Path(source_file).name})\n")
                
                # Symbol table
                f.write(f"\nGlobal Symbol Table:\n")
                f.write("--------------------\n")
                
                for name, symbol in sorted(self.global_symbols.items()):
                    f.write(f"{name:<20} 0x{symbol.address:04X}  {Path(symbol.defined_in).name}\n")
                    
                    if symbol.references:
                        for ref_file, ref_line in symbol.references:
                            f.write(f"{'':20}        referenced in {Path(ref_file).name}:{ref_line}\n")
                
                # Statistics
                f.write(f"\nStatistics:\n")
                f.write("----------\n")
                f.write(f"Object files processed: {len(self.object_files)}\n")
                f.write(f"Instructions linked: {len(instructions)}\n")
                f.write(f"Symbols resolved: {len(self.global_symbols)}\n")
                f.write(f"Final binary size: {self._calculate_final_size()} bytes\n")
            
            return True
            
        except Exception as e:
            log_error(f"Error writing map file: {str(e)}", 
                     str(map_file), error_code="MAP_FILE_ERROR")
            return False
    
    def _calculate_final_size(self) -> int:
        """Calculate final binary size"""
        if not self.object_files:
            return 0
        
        total_size = 0
        for obj_file in self.object_files:
            total_size += obj_file.code_size
        
        return total_size
    
    def _generate_intel_hex(self, memory_image: Dict[int, int], output_file: Path) -> bool:
        """Generate Intel HEX format output using custom implementation with proper 32-bit addressing"""
        try:
            # Always use custom implementation for proper Extended Linear Address support
            # The intelhex library defaults to segmented addressing which doesn't work well
            # for 32-bit addresses like 0x08000000 or 0x80000000
            return self._generate_intel_hex_custom(memory_image, output_file)
                
        except Exception as e:
            log_error(f"Failed to write Intel HEX file: {e}", 
                     error_code="HEX_WRITE_ERROR")
            return False
    
    def _generate_intel_hex_custom(self, memory_image: Dict[int, int], output_file: Path) -> bool:
        """Custom Intel HEX generator (fallback when intelhex library not available)"""
        try:
            with open(output_file, 'w') as f:
                # Group consecutive bytes into records
                addresses = sorted(memory_image.keys())
                if not addresses:
                    log_warning("No data to write to Intel HEX file")
                    # Write empty hex file with end record
                    f.write(":00000001FF\n")
                    return True
                
                current_extended_addr = None
                current_address = None
                current_data = []
                
                for addr in addresses:
                    # Check if we need to write an Extended Linear Address record
                    extended_addr = (addr >> 16) & 0xFFFF
                    if extended_addr != current_extended_addr:
                        # Write any pending data first
                        if current_data:
                            self._write_hex_record(f, current_address, current_data)
                            current_data = []
                        
                        # Write Extended Linear Address Record (type 04)
                        self._write_extended_address_record(f, extended_addr)
                        current_extended_addr = extended_addr
                        current_address = None
                    
                    if current_address is None:
                        current_address = addr
                        current_data = [memory_image[addr]]
                    elif addr == current_address + len(current_data):
                        # Consecutive address
                        current_data.append(memory_image[addr])
                        
                        # Write record if we have 16 bytes (max record size)
                        if len(current_data) >= 16:
                            self._write_hex_record(f, current_address, current_data)
                            current_address = None
                            current_data = []
                    else:
                        # Non-consecutive, write current record and start new one
                        if current_data:
                            self._write_hex_record(f, current_address, current_data)
                        current_address = addr
                        current_data = [memory_image[addr]]
                
                # Write final record if any data remains
                if current_data:
                    self._write_hex_record(f, current_address, current_data)
                
                # Write end-of-file record
                f.write(":00000001FF\n")
                
            log_info(f"Intel HEX file written using custom implementation: {output_file}")
            return True
            
        except Exception as e:
            log_error(f"Failed to write Intel HEX file: {e}", 
                     error_code="HEX_WRITE_ERROR")
            return False
    
    def _write_extended_address_record(self, f, extended_addr: int) -> None:
        """Write Extended Linear Address Record (type 04)"""
        byte_count = 0x02
        address = 0x0000
        record_type = 0x04
        data_high = (extended_addr >> 8) & 0xFF
        data_low = extended_addr & 0xFF
        
        # Calculate checksum
        checksum = byte_count + (address >> 8) + (address & 0xFF) + record_type + data_high + data_low
        checksum = (-checksum) & 0xFF
        
        # Write record
        record = f":{byte_count:02X}{address:04X}{record_type:02X}{data_high:02X}{data_low:02X}{checksum:02X}\n"
        f.write(record)
    
    def _write_hex_record(self, f, address: int, data: List[int]) -> None:
        """Write a single Intel HEX data record (type 00)"""
        byte_count = len(data)
        # Use only lower 16 bits of address (upper 16 bits set by Extended Linear Address Record)
        address_16bit = address & 0xFFFF
        address_high = (address_16bit >> 8) & 0xFF
        address_low = address_16bit & 0xFF
        record_type = 0x00  # Data record
        
        # Calculate checksum
        checksum = byte_count + address_high + address_low + record_type
        for byte_val in data:
            checksum += byte_val
        checksum = (-checksum) & 0xFF
        
        # Write record
        record = f":{byte_count:02X}{address_16bit:04X}{record_type:02X}"
        for byte_val in data:
            record += f"{byte_val:02X}"
        record += f"{checksum:02X}\n"
        
        f.write(record)
    
    def _generate_plain_text(self, instructions: List[Tuple], output_file: Path) -> bool:
        """Generate plain text format with ADDRESS INSTRUCTIONS"""
        log_debug(f"_generate_plain_text called with {len(instructions)} instructions")
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            log_debug(f"Writing plain text to: {output_file}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for address, opcode, operand, source_text, source_file, size in instructions:
                    # Format based on actual size from instruction record
                    if size == 1:
                        # DB - 8-bit (1 byte)
                        f.write(f"{address:08X}  {opcode:02X}\n")
                    elif size == 2:
                        # DW or 16-bit instruction (2 bytes)
                        f.write(f"{address:08X}  {opcode:04X}\n")
                    elif size == 4:
                        # DD or 32-bit instruction (4 bytes)
                        f.write(f"{address:08X}  {opcode:08X}\n")
                    elif size == 8:
                        # DQ - 64-bit (8 bytes)
                        f.write(f"{address:08X}  {opcode:016X}\n")
                    else:
                        # Default: use minimum hex digits needed
                        hex_digits = size * 2  # 2 hex digits per byte
                        format_str = f"{{:0{hex_digits}X}}"
                        f.write(f"{address:08X}  {format_str.format(opcode)}\n")
                        
            log_debug("Plain text file written successfully")
            return True
            
        except Exception as e:
            log_error(f"Error generating plain text: {str(e)}", 
                     str(output_file), error_code="TEXT_GENERATION_ERROR")
            return False