"""
Tricore Instruction Encoder

This module implements the instruction encoding logic for the TASM assembler.
It parses assembly instructions, matches them with the loaded instruction set,
validates operand counts, and encodes them to 32-bit binary values.

Encoding process:
1. Parse source ASM instruction (e.g., "ABS d1, d3")
2. Match with instruction set (e.g., ABS D[c],D[b])
3. Validate operand count matches expected
4. Calculate operand bit fields using position and length
5. Combine opcode with operand fields to create final 32-bit value
"""

import re
import logging
from typing import List, Optional, Dict, Tuple, Union
from dataclasses import dataclass

# Handle both direct execution and module import
try:
    from .instruction_loader import InstructionDefinition, InstructionSetLoader
except ImportError:
    from instruction_loader import InstructionDefinition, InstructionSetLoader

logger = logging.getLogger(__name__)


@dataclass
class ParsedOperand:
    """Represents a parsed operand with type information."""
    text: str  # Original operand text (e.g., "d4", "#1", "[a15]")
    type: str  # Operand type: 'reg_d', 'reg_a', 'reg_e', 'reg_p', 'imm'
    
    def __str__(self):
        return f"{self.text}:{self.type}"


@dataclass
class ParsedInstruction:
    """Represents a parsed assembly instruction."""
    mnemonic: str  # Instruction mnemonic (e.g., "ABS")
    operands: List[ParsedOperand]  # List of typed operands
    original_line: str  # Original assembly line
    line_number: int  # Line number in source file
    
    @property
    def operand_count(self) -> int:
        """Get the number of operands."""
        return len(self.operands)
    
    def get_operand_texts(self) -> List[str]:
        """Get list of operand text strings (for backward compatibility)."""
        return [op.text for op in self.operands]
    
    def get_operand_types(self) -> List[str]:
        """Get list of operand types."""
        return [op.type for op in self.operands]


@dataclass
class EncodedInstruction:
    """Represents an encoded instruction with binary value."""
    parsed: ParsedInstruction
    definition: InstructionDefinition
    binary_value: int  # 32-bit encoded value
    hex_value: str  # Hex representation
    
    def __str__(self) -> str:
        return f"{self.parsed.mnemonic} -> {self.hex_value} ({self.binary_value:032b})"


class InstructionEncoder:
    """Encodes assembly instructions to binary based on loaded instruction set."""
    
    def __init__(self, instruction_loader: InstructionSetLoader):
        self.loader = instruction_loader
        self.encoding_errors: List[str] = []
        self.current_file: Optional[str] = None
        
        # Regular expressions for parsing
        self.instruction_pattern = re.compile(
            r'^\s*([A-Z][A-Z0-9._]*)\s*(.*?)(?:;.*)?$',  # instruction operands ;comment
            re.IGNORECASE
        )
        self.operand_pattern = re.compile(r'[,\s]+')  # Split on commas and whitespace
    
    def set_current_file(self, file_path: str) -> None:
        """Set the current source file being processed for better error reporting."""
        self.current_file = file_path
    
    def parse_instruction_line(self, line: str, line_number: int) -> Optional[ParsedInstruction]:
        """
        Parse a single assembly instruction line.
        
        Args:
            line: Assembly instruction line
            line_number: Line number in source file
            
        Returns:
            ParsedInstruction if valid, None if not an instruction
        """
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith(';') or stripped.startswith('#'):
            return None
        
        # Skip labels (lines ending with :)
        if stripped.endswith(':'):
            return None
        
        # Skip directives (lines starting with .)
        if stripped.startswith('.'):
            return None
        
        # Match instruction pattern
        match = self.instruction_pattern.match(stripped)
        if not match:
            return None
        
        mnemonic = match.group(1).upper()
        operands_str = match.group(2).strip()
        
        # Strip GCC-style annotations (e.g., #function_name or whitespace#function_name)
        # These are not immediate values like #10, but metadata annotations
        # Pattern: optional whitespace/comma, followed by # and identifier (not a number)
        # This handles both "ret #func" and "add d2, #5 #annotation"
        operands_str = re.sub(r'[,\s]*#[a-zA-Z_][a-zA-Z0-9_\.]*\s*$', '', operands_str)
        
        # Parse operands with tolerant splitting
        operands = []
        if operands_str:
            # Use tolerant splitting for compound operands
            split_ops = self.loader.split_compound_operands(operands_str)
            for op_text in split_ops:
                if op_text:
                    op_type = self._classify_operand_type(op_text)
                    operands.append(ParsedOperand(text=op_text, type=op_type))
        
        return ParsedInstruction(
            mnemonic=mnemonic,
            operands=operands,
            original_line=line,
            line_number=line_number
        )
    
    def _classify_operand_type(self, operand: str) -> str:
        """
        Classify operand type at parse time.
        
        Rules:
        - D[x], d[x], dx, Dx -> 'reg_d' (data register)
        - A[x], a[x], ax, Ax -> 'reg_a' (address register)  
        - E[x], e[x], ex, Ex -> 'reg_e' (extended register)
        - P[x], p[x], px, Px -> 'reg_p' (pointer register)
        - Everything else -> 'imm' (immediate/constant/label/memory)
        
        Args:
            operand: Raw operand string
            
        Returns:
            Type string: 'reg_d', 'reg_a', 'reg_e', 'reg_p', or 'imm'
        """
        # Clean the operand (remove brackets, whitespace)
        clean = operand.strip().replace('[', '').replace(']', '').lower()
        
        # Check first character to determine register type
        if clean and len(clean) >= 2:
            first_char = clean[0]
            # Must be followed by a digit or closing bracket
            if first_char == 'd' and (clean[1].isdigit() or len(clean) == 1):
                return 'reg_d'
            elif first_char == 'a' and (clean[1].isdigit() or len(clean) == 1):
                return 'reg_a'
            elif first_char == 'e' and (clean[1].isdigit() or len(clean) == 1):
                return 'reg_e'
            elif first_char == 'p' and (clean[1].isdigit() or len(clean) == 1):
                return 'reg_p'
        
        # Everything else is immediate (numbers, labels, constants, etc.)
        return 'imm'
    
    def parse_operand_value(self, operand: str, current_address: Optional[int] = None, 
                           labels: Optional[Dict[str, int]] = None,
                           instruction_size: int = 0) -> int:
        """
        Parse operand string to numeric value.
        
        Handles various formats:
        - Register names: d1, D1, D[1] -> 1
        - Immediate values: #5, 0x10, 255 -> numeric value
        - Constants: STACK_SIZE (after macro expansion) -> numeric value
        - Labels: common, loop_start -> resolved address (relative if needed)
        
        Args:
            operand: Operand string
            current_address: Current instruction address (for relative addressing)
            labels: Label dictionary for label resolution
            instruction_size: Size of current instruction in bytes (for PC-relative calculation)
            
        Returns:
            Numeric value of the operand
            
        Raises:
            ValueError: If operand cannot be parsed
        """
        operand = operand.strip()
        
        # Handle GCC post-increment addressing: [%a2+], [a0+], etc.
        postinc_match = re.match(r'^\[%?([dDaAeEpP])(\d+)\+\]$', operand)
        if postinc_match:
            # Return the register number - the + indicates post-increment mode
            # The encoder will handle this based on the instruction definition
            return int(postinc_match.group(2))
        
        # Handle memory indirect addressing: [a0], [d1], [%a0] (GCC), etc.
        indirect_match = re.match(r'^\[%?([dDaAeEpP])(\d+)\]$', operand)
        if indirect_match:
            # Return the register number - the register number is the operand value
            return int(indirect_match.group(2))
        
        # Handle complex addressing modes like [a0]+0x7000, [a0+0x10], etc.
        # For now, extract the numeric part - full addressing mode support needs more work
        addressing_match = re.match(r'^\[([a-zA-Z0-9_]+)\]\s*\+\s*(.+)$', operand)
        if addressing_match:
            # Extract the offset part
            offset_str = addressing_match.group(2)
            return self.parse_operand_value(offset_str)  # Recursively parse the offset
        
        # Handle register formats: d1, D1, D[1], A[2], E[4], P[0], etc.
        # Also support GCC syntax with % prefix: %d1, %a2, %e4, etc.
        reg_patterns = [
            r'^%?[dDaAeEpP](\d+)$',           # d1, D1, a2, A2, %d1, %a2 (GCC)
            r'^%?[dDaAeEpP]\[(\d+)\]$',       # D[1], A[2], %d[1] (GCC)
            r'^%?[dDaAeEpP]\s*\[\s*(\d+)\s*\]$'  # D[ 1 ], A[ 2 ], %d[ 1 ] (GCC)
        ]
        
        for pattern in reg_patterns:
            match = re.match(pattern, operand, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Handle immediate values with # prefix
        if operand.startswith('#'):
            operand = operand[1:]
        
        # Try to parse as NASM-compatible numeric constant
        try:
            from numeric_parser import parse_numeric
            return parse_numeric(operand)
        except (ValueError, ImportError):
            pass
        
        # Try simple integer parsing as fallback
        try:
            # Handle hex (0x), binary (0b), octal (0o)
            if operand.lower().startswith('0x'):
                return int(operand, 16)
            elif operand.lower().startswith('0b'):
                return int(operand, 2)
            elif operand.lower().startswith('0o'):
                return int(operand, 8)
            else:
                # Try decimal
                return int(operand, 10)
        except ValueError:
            pass
        
        # Handle GCC local label references: 0f, 1f, 2f (forward), 0b, 1b, 2b (backward)
        gcc_local_ref = re.match(r'^(\d+)([fb])$', operand)
        if gcc_local_ref and labels:
            label_num = gcc_local_ref.group(1)
            direction = gcc_local_ref.group(2)
            
            # Find the appropriate numeric label
            if direction == 'f':  # forward reference
                # Find the next occurrence of this numeric label after current address
                target_address = None
                if current_address is not None:
                    for label_name, label_addr in labels.items():
                        if label_name == label_num and label_addr > current_address:
                            if target_address is None or label_addr < target_address:
                                target_address = label_addr
                else:
                    # First pass - use placeholder
                    target_address = None
                    
                if target_address is not None:
                    if current_address is not None:
                        displacement_bytes = target_address - current_address
                        logger.debug(
                            f"GCC forward local label {operand}: target=0x{target_address:X}, "
                            f"current=0x{current_address:X}, disp={displacement_bytes}"
                        )
                        return displacement_bytes
                    else:
                        return target_address
                        
            else:  # 'b' - backward reference
                # Find the most recent occurrence of this numeric label before current address
                target_address = None
                if current_address is not None:
                    for label_name, label_addr in labels.items():
                        if label_name == label_num and label_addr < current_address:
                            if target_address is None or label_addr > target_address:
                                target_address = label_addr
                else:
                    # First pass - use placeholder
                    target_address = None
                    
                if target_address is not None:
                    if current_address is not None:
                        displacement_bytes = target_address - current_address
                        logger.debug(
                            f"GCC backward local label {operand}: target=0x{target_address:X}, "
                            f"current=0x{current_address:X}, disp={displacement_bytes}"
                        )
                        return displacement_bytes
                    else:
                        return target_address
            
            # If we couldn't resolve it, use placeholder
            if current_address is not None:
                # For forward refs, assume far; for backward, assume near
                placeholder = 254 if direction == 'f' else -254
                logger.debug(f"GCC local label {operand} placeholder: {placeholder}")
                return placeholder
            else:
                return 0
        
        # Try to resolve as a label
        if labels and operand in labels:
            label_address = labels[operand]
            if current_address is not None:
                # Calculate relative displacement for PC-relative branch instructions
                # TriCore PC-relative addressing:
                # - Displacement is relative to CURRENT instruction address, not next PC
                # - Return displacement in BYTES
                # - The /2 division will be applied during encoding based on syntax
                displacement_bytes = label_address - current_address
                logger.debug(
                    f"PC-relative: target=0x{label_address:X}, current=0x{current_address:X}, "
                    f"disp_bytes={displacement_bytes}"
                )
                return displacement_bytes
            else:
                return label_address
        
        # Check if this might be a label (alphanumeric identifier starting with letter or underscore)
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', operand):
            # This is likely a label that will be resolved later
            # For PC-relative addressing, use maximum displacement as placeholder
            # This ensures we use the largest instruction variant during first pass
            # The linker will fix this with multi-pass optimization
            if current_address is not None:
                # Return large positive displacement (assumes forward reference)
                # Use 254 bytes (max disp8) to force selection of largest variant
                logger.debug(f"Forward reference placeholder for '{operand}': returning 254 bytes")
                return 254
            else:
                # Absolute addressing - return 0 as placeholder
                logger.debug(f"Forward reference placeholder for '{operand}': returning 0")
                return 0
        
        # If all else fails, treat as macro-expanded constant
        # This should have been resolved during macro expansion
        raise ValueError(f"Cannot parse operand value: {operand}")
    
    
    def _log_encoding_error(self, parsed: ParsedInstruction, message: str, 
                           error_token_index: Optional[int] = None, 
                           file_path: Optional[str] = None,
                           definition: Optional['InstructionDefinition'] = None) -> None:
        """Log an enhanced encoding error with full context."""
        # Import here to avoid circular imports
        try:
            from logger import log_error, log_abort
        except ImportError:
            # Fallback if logger module isn't available (e.g., in tests)
            import logging
            logger = logging.getLogger(__name__)
            log_error = lambda msg, *args, **kwargs: logger.error(msg)
            log_abort = lambda msg, *args, **kwargs: logger.error(f"ABORT: {msg}")
        
        # Create token list from the instruction
        tokens = [parsed.mnemonic]
        if parsed.operands:
            tokens.extend(parsed.operands)
        
        # First log as ERROR with details
        error_details = f"{message}\n"
        error_details += f"  Instruction: {parsed.mnemonic}\n"
        operand_strs = [op.text if hasattr(op, 'text') else str(op) for op in parsed.operands]
        error_details += f"  Operands provided: {', '.join(operand_strs) if parsed.operands else '(none)'}\n"
        error_details += f"  Operand count: {len(parsed.operands)}\n"
        error_details += f"  Original line: {parsed.original_line.strip()}\n"
        
        # Add instruction definition details if available
        if definition:
            error_details += f"\n  Expected syntax: {definition.syntax}\n"
            error_details += f"  Expected operands: {definition.operand_count}\n"
            error_details += f"  Instruction variant: {definition.long_name}\n"
            error_details += f"  OpCode: {definition.opcode}\n"
        
        if error_token_index is not None and error_token_index < len(tokens):
            error_details += f"\n  Problem token: {tokens[error_token_index]}\n"
        
        log_error(
            error_details,
            file_path=file_path or getattr(self, 'current_file', None),
            line_number=parsed.line_number
        )
        
        # Then log as ABORT to stop compilation
        log_abort(
            message,
            file_path=file_path or getattr(self, 'current_file', None),
            line_number=parsed.line_number
        )
    
    def _extract_operand_patterns(self, syntax: str) -> List[str]:
        """
        Extract operand patterns from instruction syntax.
        
        Examples:
        - "JNZ D[b], disp4/2" -> ["D[b]", "disp4/2"]
        - "J disp8/2" -> ["disp8/2"]
        - "MOV D[a], D[b]" -> ["D[a]", "D[b]"]
        
        Returns:
            List of operand pattern strings (including any /2 modifiers)
        """
        # Remove the mnemonic (first word)
        parts = syntax.split(None, 1)
        if len(parts) < 2:
            return []
        
        operands_part = parts[1].strip()
        
        # Remove any {} split operand specifications
        operands_part = re.sub(r'\{[^\}]+\}', '', operands_part)
        
        # Split by comma to get individual operands
        operands = [op.strip() for op in operands_part.split(',')]
        
        return operands
    
    def _parse_split_operand_syntax(self, syntax: str) -> tuple[int, List[tuple[int, int]]]:
        """
        Parse split operand syntax to extract bitfield ranges and determine which operand is split.
        
        New syntax format (as of Nov 2025):
            "J disp24 {[15:0],[23:16]}" -> operand 1, [(15, 0), (23, 16)]
            "ST.W A[b], off10 {[9:6][5:0]}, D[a]" -> operand 2, [(9, 6), (5, 0)]
            "LEA A[a],A[b],off16 {[9:6][15:10][5:0]}" -> operand 3, [(9, 6), (15, 10), (5, 0)]
        
        The {} is now adjacent to the operand that needs special encoding.
        
        Args:
            syntax: Instruction syntax string
            
        Returns:
            Tuple of (split_operand_position, bitfield_ranges)
            - split_operand_position: 1-based operand number that is split
            - bitfield_ranges: List of (high, low) tuples representing bitfield ranges
        """
        # Find content within curly braces
        match = re.search(r'\{([^\}]+)\}', syntax)
        if not match:
            return (0, [])
        
        content = match.group(1)
        
        # Extract all [n:m] patterns
        bitfield_pattern = r'\[(\d+):(\d+)\]'
        matches = re.findall(bitfield_pattern, content)
        bitfield_ranges = [(int(high), int(low)) for high, low in matches]
        
        # Determine which operand has the {} attached
        # Split the syntax by commas to count operands before the {}
        before_brace = syntax[:match.start()]
        
        # Count commas before the {} to determine operand position
        # Note: This is a simplified approach; more robust parsing might be needed
        operand_count = before_brace.count(',') + 1
        
        return (operand_count, bitfield_ranges)
    
    def _encode_split_operand_instruction(self, parsed: ParsedInstruction, 
                                         definition: InstructionDefinition, 
                                         base_opcode: int,
                                         current_address: Optional[int] = None,
                                         labels: Optional[Dict[str, int]] = None,
                                         instruction_size_bytes: int = 0) -> Optional[int]:
        """
        Encode instructions with split operands.
        
        Examples:
        1) J instruction with syntax "J disp24 {[15:0],[23:16]}":
           - The disp24 operand is split into two parts
           - Part 1: bits [15:0] of disp24 -> op1_pos for op1_len bits
           - Part 2: bits [23:16] of disp24 -> op2_pos for op2_len bits
           - Total size: 16 + 8 = 24 bits
        
        2) LEA instruction with syntax "LEA A[a],A[b],off16 {[9:6][15:10][5:0]}":
           - First two operands are regular registers
           - Third operand off16 is split into three parts
           - Part 1: bits [9:6] -> op3_pos for op3_len bits (4 bits)
           - Part 2: bits [15:10] -> op4_pos for op4_len bits (6 bits)
           - Part 3: bits [5:0] -> op5_pos for op5_len bits (6 bits)
           - Total size: 4 + 6 + 6 = 16 bits
        
        The algorithm:
        1. Parse the syntax to find which operand is split and its bitfield ranges
        2. Calculate total operand size from all parts
        3. Parse the operand value
        4. Extract and position each bitfield part
        
        Args:
            parsed: Parsed instruction
            definition: Instruction definition
            current_address: Current instruction address (for PC-relative addressing)
            labels: Label dictionary for label resolution
            instruction_size_bytes: Size of instruction in bytes
            base_opcode: Base opcode value
            
        Returns:
            Encoded binary value or None if encoding failed
        """
        try:
            # Parse the syntax to determine which operand is split
            split_operand_pos, bitfield_ranges = self._parse_split_operand_syntax(definition.syntax)
            
            if not bitfield_ranges or split_operand_pos == 0:
                try:
                    from logger import log_error
                except ImportError:
                    import logging
                    log_error = logging.getLogger(__name__).error
                log_error(
                    f"Failed to parse split operand syntax: {definition.syntax}"
                )
                self._log_encoding_error(
                    parsed,
                    f"Invalid split operand syntax in instruction definition",
                    error_token_index=1,
                    definition=definition
                )
                return None
            
            # The split operand is at position split_operand_pos (1-based)
            # It occupies multiple bitfield slots in the instruction definition
            num_split_parts = len(bitfield_ranges)
            split_operand_index = split_operand_pos - 1  # Convert to 0-based index for parsed.operands
            
            logger.debug(
                f"Split operand detected at position {split_operand_pos} "
                f"with {num_split_parts} parts: {bitfield_ranges}"
            )
            
            # Start with base opcode
            binary_value = base_opcode
            
            # Track which instruction bitfield we're on
            # In the instruction definition, operands are numbered sequentially
            # But in the parsed instruction, split operand is just ONE operand
            instr_def_operand_num = 1
            parsed_operand_index = 0
            
            # Iterate through all parsed operands
            for parsed_idx in range(len(parsed.operands)):
                if parsed_idx == split_operand_index:
                    # This is the split operand - encode it across multiple bitfields
                    operand = parsed.operands[parsed_idx]
                    split_operand_str = operand.text if hasattr(operand, 'text') else operand
                    split_operand_value = self.parse_operand_value(
                        split_operand_str, current_address, labels, instruction_size_bytes
                    )
                    
                    # Check if this operand has /2 modifier in syntax
                    syntax_operands = self._extract_operand_patterns(definition.syntax)
                    if parsed_idx < len(syntax_operands) and '/2' in syntax_operands[parsed_idx]:
                        logger.debug(f"Split operand has /2 modifier, dividing {split_operand_value} by 2")
                        split_operand_value = split_operand_value // 2
                    
                    # Calculate total size of split operand
                    total_bits = 0
                    part_info = []
                    
                    for i, (high_bit, low_bit) in enumerate(bitfield_ranges):
                        # Get bitfield info from instruction definition
                        op_pos, op_len = definition.get_operand_info(instr_def_operand_num)
                        
                        # Bitfield size from syntax
                        bitfield_size = high_bit - low_bit + 1
                        total_bits += bitfield_size
                        
                        part_info.append({
                            'operand_num': instr_def_operand_num,
                            'high_bit': high_bit,
                            'low_bit': low_bit,
                            'size': bitfield_size,
                            'position': op_pos,
                            'length': op_len
                        })
                        
                        instr_def_operand_num += 1
                    
                    # Validate operand fits in total size
                    max_value = (1 << total_bits) - 1
                    if split_operand_value > max_value and split_operand_value < (1 << 32):
                        try:
                            from logger import log_error
                        except ImportError:
                            import logging
                            log_error = logging.getLogger(__name__).error
                        log_error(
                            f"Split operand value 0x{split_operand_value:X} exceeds {total_bits}-bit total field (max: 0x{max_value:X})"
                        )
                        self._log_encoding_error(
                            parsed,
                            f"Split operand value 0x{split_operand_value:X} does not fit in {total_bits}-bit field (max: 0x{max_value:X})",
                            error_token_index=parsed_idx,
                            definition=definition
                        )
                        return None
                    
                    # Extract and encode each bitfield part
                    debug_parts = []
                    for part in part_info:
                        # Extract bits [high:low] from the operand value
                        shift_amount = part['low_bit']
                        mask = (1 << part['size']) - 1
                        part_value = (split_operand_value >> shift_amount) & mask
                        
                        # Encode into instruction at op_pos for op_len bits
                        op_pos = part['position']
                        op_len = part['length']
                        op_mask = (1 << op_len) - 1
                        
                        binary_value |= (part_value & op_mask) << op_pos
                        
                        debug_parts.append(
                            f"  Part {part['operand_num']}: bits[{part['high_bit']}:{part['low_bit']}] "
                            f"= 0x{part_value:X} -> pos {op_pos}, len {op_len}"
                        )
                    
                    logger.debug(
                        f"Split operand encoding: {split_operand_str} -> 0x{split_operand_value:X} ({total_bits} bits total)\n"
                        + "\n".join(debug_parts)
                    )
                    
                else:
                    # Regular operand - encode normally
                    operand = parsed.operands[parsed_idx]
                    operand_str = operand.text if hasattr(operand, 'text') else operand
                    operand_value = self.parse_operand_value(
                        operand_str, current_address, labels, instruction_size_bytes
                    )
                    
                    op_pos, op_len = definition.get_operand_info(instr_def_operand_num)
                    if op_len > 0:
                        mask = (1 << op_len) - 1
                        if operand_value > mask:
                            try:
                                from logger import log_error
                            except ImportError:
                                import logging
                                log_error = logging.getLogger(__name__).error
                            log_error(
                                f"Operand {instr_def_operand_num} value 0x{operand_value:X} exceeds {op_len}-bit field (max: 0x{mask:X})"
                            )
                            self._log_encoding_error(
                                parsed,
                                f"Operand {instr_def_operand_num} value 0x{operand_value:X} does not fit in {op_len}-bit field (max: 0x{mask:X})",
                                error_token_index=parsed_idx,
                                definition=definition
                            )
                            return None
                        
                        binary_value |= (operand_value & mask) << op_pos
                    
                    instr_def_operand_num += 1
            
            logger.debug(f"Final encoded value: 0x{binary_value:08X}")
            
            return binary_value
            
        except ValueError as e:
            try:
                from logger import log_error
            except ImportError:
                import logging
                log_error = logging.getLogger(__name__).error
            log_error(
                f"Cannot parse operand in split operand instruction: {e}\n"
                f"  Expected syntax: {definition.syntax}\n"
                f"  Instruction variant: {definition.long_name}\n"
                f"  Operand count expected: {definition.operand_count}"
            )
            self._log_encoding_error(
                parsed,
                f"Cannot parse operand: {e}\n"
                f"  Expected syntax: {definition.syntax}",
                error_token_index=1,
                definition=definition
            )
            return None
    
    def encode_instruction(self, parsed: ParsedInstruction, 
                          current_address: Optional[int] = None,
                          labels: Optional[Dict[str, int]] = None) -> Optional[EncodedInstruction]:
        """
        Encode a parsed instruction to binary.
        
        Args:
            parsed: Parsed instruction
            current_address: Current instruction address (for PC-relative addressing)
            labels: Label dictionary for label resolution
            
        Returns:
            EncodedInstruction if successful, None if encoding failed
        """
        try:
            # Always normalize operands before matching
            normalized_operands = []
            for op in parsed.operands:
                # Remove brackets and split compound operands
                split_ops = self.loader.split_compound_operands(op.text if hasattr(op, 'text') else str(op))
                for split_op in split_ops:
                    # Normalize bracketed register forms: [a[2]] -> a2, [A[2]] -> A2
                    # Robust normalization: strip all outer brackets from register operands
                    bracketed = split_op
                    # Remove all outer brackets
                    while True:
                        # Remove leading/trailing brackets
                        bracketed = bracketed.strip()
                        if bracketed.startswith('[') and bracketed.endswith(']'):
                            bracketed = bracketed[1:-1].strip()
                        else:
                            break
                    # Now match register pattern: a[2], A[2], etc.
                    reg_match = re.match(r'^([aAeEdDpP])\[(\d+)\]$', bracketed)
                    if reg_match:
                        bracketed = f"{reg_match.group(1)}{reg_match.group(2)}"
                    split_op = bracketed
                    op_type = self._classify_operand_type(split_op)
                    normalized_operands.append(ParsedOperand(text=split_op, type=op_type))

            definition = self.loader.find_instruction(
                parsed.mnemonic,
                len(normalized_operands),
                normalized_operands  # Pass normalized operands for type-based matching
            )
            logger.info(f"[ENCODE] find_instruction returned: {definition.syntax if definition else 'None'} for {parsed.mnemonic}")
            if not definition:
                # Try to find other variants to show available options
                all_variants = self.loader.get_instruction_variants(parsed.mnemonic)
                variant_info = ""
                if all_variants:
                    variant_info = f"\n  Available variants for {parsed.mnemonic}:\n"
                    for var in all_variants:
                        variant_info += f"    - {var.syntax} ({var.operand_count} operands)\n"
                
                self._log_encoding_error(
                    parsed, 
                    f"Unknown instruction '{parsed.mnemonic}' with {parsed.operand_count} operands{variant_info}",
                    error_token_index=0  # Error is in the mnemonic (first token)
                )
                return None
            
            # Start with base opcode
            opcode_value = definition.get_opcode_value()
            binary_value = opcode_value
            
            # Check if this instruction has split operand encoding (like J instruction)
            # Syntax format: "J disp24 {[15:0],[23:16]}" or "ST.W off10 {[9:6][5:0]}, D[a]"
            # Use regex to match the specific pattern: {[n:m]...}
            split_operand_pattern = r'\{\s*\[\d+:\d+\]'
            has_split_operand = re.search(split_operand_pattern, definition.syntax) is not None
            
            # Get instruction size for PC-relative calculations
            instruction_size_bytes = definition.opcode_size // 8
            
            if has_split_operand:
                # Handle split operand encoding (e.g., J instruction with disp24 split into two parts)
                logger.debug(f"Instruction {parsed.mnemonic} has split operands - using split operand encoding")
                binary_value = self._encode_split_operand_instruction(
                    parsed, definition, binary_value, current_address, labels, instruction_size_bytes
                )
                if binary_value is None:
                    return None
            else:
                logger.debug(f"Instruction {parsed.mnemonic} using standard operand encoding")
                # Standard operand encoding
                # Extract operand patterns from syntax to check for /2 modifier
                syntax_operands = self._extract_operand_patterns(definition.syntax)
                
                # First, parse all operand values to check if a smaller variant would fit
                # BUT: Skip register operands - only check immediate/offset operands
                parsed_operand_values = []
                operand_is_register = []  # Track which operands are registers vs immediates
                
                for i, operand in enumerate(parsed.operands):
                    operand_str = operand.text if hasattr(operand, 'text') else operand
                    
                    # Check if this operand is a register
                    is_reg = False
                    reg_patterns = [
                        r'^%?[dDaAeEpP](\d+)$',           # d1, D1, a2, A2, %d1, %a2
                        r'^%?[dDaAeEpP]\[(\d+)\]$',       # D[1], A[2]
                    ]
                    for pattern in reg_patterns:
                        if re.match(pattern, operand_str.strip()):
                            is_reg = True
                            break
                    
                    operand_is_register.append(is_reg)
                    
                    try:
                        # Parse operand value with label/PC-relative support
                        operand_value = self.parse_operand_value(
                            operand_str, current_address, labels, instruction_size_bytes
                        )
                        
                        # Apply scaling modifiers
                        if i < len(syntax_operands):
                            syntax_op = syntax_operands[i]
                            if '/4' in syntax_op:
                                operand_value = operand_value // 4
                            elif '/2' in syntax_op:
                                operand_value = operand_value // 2
                            elif 'off' in syntax_op.lower() and '/4' not in syntax_op:
                                word_aligned_mnemonics = {'LD.W', 'ST.W', 'LD.A', 'LEA'}
                                if definition.instruction in word_aligned_mnemonics:
                                    match = re.search(r'\boff\d+\b', syntax_op, re.IGNORECASE)
                                    if match:
                                        operand_value = operand_value // 4
                        
                        parsed_operand_values.append(operand_value)
                    except ValueError as e:
                        self._log_encoding_error(
                            parsed,
                            f"Cannot parse operand '{operand_str}': {e}",
                            error_token_index=i + 1,
                            definition=definition
                        )
                        return None
                
                # Check if there are smaller instruction variants that can fit these operand values
                # Optimize for:
                # - PC-relative branch/loop instructions (J, LOOP, JNZ, JEQ, etc.)
                # - MOV instructions with immediate values or register operands
                # - MOV.AA address register move instructions
                # - Instructions with multiple size variants where smaller encoding is possible
                optimize_mnemonics = {'J', 'LOOP', 'JNZ', 'JEQ', 'JNE', 'JGE', 'JL', 'JLT', 'JGEU', 'JLTU', 'CALL', 'MOV', 'MOV.AA', 'ADD', 'SUB'}
                all_variants = self.loader.get_instruction_variants(parsed.mnemonic)
                if len(all_variants) > 1 and parsed.mnemonic.upper() in optimize_mnemonics:
                    # Filter variants that match operand count
                    matching_variants = [v for v in all_variants 
                                       if v.operand_count == len(normalized_operands)]
                    
                    # Additional filtering: remove variants with specific register constraints
                    # that don't match the actual operand registers
                    # Example: MOV D[15], const8 should only match if operand is actually D15
                    # Also filter by register TYPE: E register syntax should only match E register operands
                    # IMPORTANT: Also filter by operand KIND: register vs immediate
                    # Example: MOV D[a], const4 should NOT match MOV D4, D2 (D2 is register, not immediate)
                    filtered_variants = []
                    for variant in matching_variants:
                        variant_syntax_operands = self._extract_operand_patterns(variant.syntax)
                        is_compatible = True
                        
                        for i, syntax_op in enumerate(variant_syntax_operands):
                            if i >= len(normalized_operands):
                                break
                            
                            # Extract actual operand
                            actual_operand_obj = normalized_operands[i]
                            actual_operand = actual_operand_obj.text if hasattr(actual_operand_obj, 'text') else str(actual_operand_obj)
                            actual_reg_match = re.match(r'^([DAEP])(\d+)$', actual_operand.upper())
                            
                            # Check if syntax expects a register
                            syntax_reg_match = re.match(r'^([DAEP])\[', syntax_op.upper())
                            
                            # Case 1: Syntax expects a register, operand IS a register
                            if syntax_reg_match and actual_reg_match:
                                syntax_type = syntax_reg_match.group(1)
                                actual_type = actual_reg_match.group(1)
                                actual_num = int(actual_reg_match.group(2))
                                
                                # Check TYPE match (D vs E vs A vs P)
                                if actual_type != syntax_type:
                                    is_compatible = False
                                    logger.debug(
                                        f"Variant '{variant.syntax}' incompatible: "
                                        f"requires {syntax_type} register but operand is {actual_type}{actual_num}"
                                    )
                                    break
                                
                                # Check NUMBER match (if syntax specifies specific number)
                                spec_num_match = re.match(r'^[DAEP]\[(\d+)\]', syntax_op.upper())
                                if spec_num_match:
                                    spec_num = int(spec_num_match.group(1))
                                    if actual_num != spec_num:
                                        is_compatible = False
                                        logger.debug(
                                            f"Variant '{variant.syntax}' incompatible: "
                                            f"requires {syntax_type}[{spec_num}] but operand is {actual_type}{actual_num}"
                                        )
                                        break
                            
                            # Case 2: Syntax expects immediate (const, off, disp), operand IS a register
                            # This is INCOMPATIBLE - filter out
                            elif not syntax_reg_match and actual_reg_match:
                                # Syntax expects immediate but operand is a register
                                is_compatible = False
                                logger.debug(
                                    f"Variant '{variant.syntax}' incompatible: "
                                    f"operand {i+1} expects immediate ('{syntax_op}') but got register '{actual_operand}'"
                                )
                                break
                            
                            # Case 3: Syntax expects register, operand is NOT a register
                            # This is INCOMPATIBLE - filter out
                            elif syntax_reg_match and not actual_reg_match:
                                # Syntax expects register but operand is immediate/label
                                is_compatible = False
                                logger.debug(
                                    f"Variant '{variant.syntax}' incompatible: "
                                    f"operand {i+1} expects register ('{syntax_op}') but got immediate '{actual_operand}'"
                                )
                                break
                        
                        if is_compatible:
                            filtered_variants.append(variant)
                    
                    matching_variants = filtered_variants
                    
                    # Always check if values fit, even if there's only 1 matching variant
                    # This handles cases where find_instruction returned a variant that doesn't fit
                    # Check which variants can accommodate the parsed values
                    suitable_variants = []
                    for variant in matching_variants:
                        can_fit = True
                        variant_syntax_operands = self._extract_operand_patterns(variant.syntax)
                        
                        for i, value in enumerate(parsed_operand_values):
                            # Skip checking register operands - they don't have bit width constraints
                            # Only check immediate/offset operands
                            if i < len(operand_is_register) and operand_is_register[i]:
                                continue
                            
                            op_num = i + 1
                            op_pos, op_len = variant.get_operand_info(op_num)
                            
                            if op_len == 0:
                                continue
                            
                            # Check if value fits in this variant's bit field
                            max_signed = (1 << (op_len - 1)) - 1
                            min_signed = -(1 << (op_len - 1))
                            max_unsigned = (1 << op_len) - 1
                            
                            if not ((min_signed <= value <= max_signed) or (0 <= value <= max_unsigned)):
                                can_fit = False
                                logger.debug(
                                    f"Variant '{variant.syntax}' ({variant.opcode_size}-bit): "
                                    f"operand {i+1} value {value} doesn't fit in {op_len} bits"
                                )
                                break
                        
                        if can_fit:
                            suitable_variants.append(variant)
                    
                    logger.info(f"[OPT] After value-fit check: {len(suitable_variants)} suitable variant(s) for {parsed.mnemonic}")
                    if suitable_variants:
                        for v in suitable_variants:
                            logger.info(f"[OPT]   - {v.syntax} ({v.opcode_size}-bit)")
                        
                        # Select the smallest suitable variant (code size optimization)
                        if suitable_variants:
                            suitable_variants.sort(key=lambda v: v.opcode_size)
                            best_variant = suitable_variants[0]
                            
                            if best_variant.opcode != definition.opcode:
                                logger.debug(
                                    f"Optimizing: switching from {definition.syntax} ({definition.opcode_size}-bit) "
                                    f"to {best_variant.syntax} ({best_variant.opcode_size}-bit)"
                                )
                                definition = best_variant
                                opcode_value = definition.get_opcode_value()
                                binary_value = opcode_value
                                instruction_size_bytes = definition.opcode_size // 8
                                syntax_operands = self._extract_operand_patterns(definition.syntax)
                        else:
                            # No variants fit the operand values - fall back to largest variant
                            # (most likely to accommodate the values)
                            logger.info(f"No suitable variant found for {parsed.mnemonic} - attempting fallback to largest variant")
                            all_variants.sort(key=lambda v: v.opcode_size, reverse=True)
                            fallback_variant = all_variants[0]
                            
                            logger.info(
                                f"Falling back from {definition.syntax} ({definition.opcode_size}-bit) "
                                f"to {fallback_variant.syntax} ({fallback_variant.opcode_size}-bit)"
                            )
                            definition = fallback_variant
                            opcode_value = definition.get_opcode_value()
                            binary_value = opcode_value
                            instruction_size_bytes = definition.opcode_size // 8
                            syntax_operands = self._extract_operand_patterns(definition.syntax)
                
                # Now encode operands with the selected (possibly optimized) variant
                # Process each operand
                for i, operand in enumerate(parsed.operands):
                    operand_num = i + 1  # 1-based operand numbering
                    operand_str = operand.text if hasattr(operand, 'text') else operand
                    
                    operand_value = parsed_operand_values[i]  # Use already-parsed value
                    
                    # Get position and length for this operand
                    op_pos, op_len = definition.get_operand_info(operand_num)
                    
                    if op_len == 0:
                        # This is an implicit operand (like D[15] in CMOV) - skip encoding
                        logger.debug(
                            f"Operand {operand_num}: {operand_str} -> implicit (not encoded, len=0)"
                        )
                        continue
                    
                    # Calculate operand mask and encoded value
                    op_mask = (1 << op_len) - 1  # e.g., 0xF for 4-bit field
                    
                    # Check if operand value fits in the field
                    # For signed values (negative displacements), check after masking
                    if operand_value < 0:
                        # Negative value - check if it fits as signed value
                        # Convert to unsigned by masking, then check range
                        signed_min = -(1 << (op_len - 1))  # e.g., -128 for 8-bit
                        if operand_value < signed_min:
                            self._log_encoding_error(
                                parsed,
                                f"Operand {operand_num} value {operand_value} is too negative for {op_len}-bit signed field (min: {signed_min})",
                                error_token_index=i + 1,
                                definition=definition
                            )
                            return None
                    elif operand_value > op_mask:
                        self._log_encoding_error(
                            parsed,
                            f"Operand {operand_num} value 0x{operand_value:X} does not fit in {op_len}-bit field (max: 0x{op_mask:X})",
                            error_token_index=i + 1,  # +1 because mnemonic is token 0
                            definition=definition
                        )
                        return None
                    
                    # Encode operand into binary value (masking handles negative values as two's complement)
                    encoded_operand = (operand_value & op_mask) << op_pos
                    binary_value |= encoded_operand
                    
                    logger.debug(
                        f"Operand {operand_num}: {operand_str} -> {operand_value} "
                        f"@ pos {op_pos}, len {op_len} -> 0x{encoded_operand:08X}"
                    )
            
            # Create encoded instruction with proper size formatting
            size_bytes = definition.opcode_size // 8
            if size_bytes == 2:  # 16-bit instruction
                hex_value = f"0x{binary_value:04X}"
            elif size_bytes == 4:  # 32-bit instruction
                hex_value = f"0x{binary_value:08X}"
            else:  # Other sizes (future-proofing)
                hex_chars = size_bytes * 2
                hex_value = f"0x{binary_value:0{hex_chars}X}"
            
            operand_strs = [op.text if hasattr(op, 'text') else str(op) for op in parsed.operands]
            logger.debug(
                f"Encoded {parsed.mnemonic} {', '.join(operand_strs)} -> {hex_value} ({size_bytes} bytes)"
            )
            
            return EncodedInstruction(
                parsed=parsed,
                definition=definition,
                binary_value=binary_value,
                hex_value=hex_value
            )
            
        except Exception as e:
            self._log_encoding_error(
                parsed,
                f"Unexpected encoding error: {e}",
                error_token_index=None
            )
            return None
    
    def encode_assembly_file(self, lines: List[str]) -> List[EncodedInstruction]:
        """
        Encode an entire assembly file.
        
        Args:
            lines: List of assembly source lines
            
        Returns:
            List of successfully encoded instructions
        """
        encoded_instructions = []
        self.encoding_errors.clear()
        
        for line_num, line in enumerate(lines, 1):
            parsed = self.parse_instruction_line(line, line_num)
            if parsed:
                encoded = self.encode_instruction(parsed)
                if encoded:
                    encoded_instructions.append(encoded)
        
        return encoded_instructions
    
    def get_encoding_errors(self) -> List[str]:
        """Get list of encoding errors from last encoding operation."""
        return self.encoding_errors.copy()
    
    def validate_instruction_syntax(self, mnemonic: str, operands: List[str]) -> Tuple[bool, str]:
        """
        Validate instruction syntax against loaded instruction set.
        
        Args:
            mnemonic: Instruction mnemonic
            operands: List of operands
            
        Returns:
            (is_valid, error_message)
        """
        variants = self.loader.get_instruction_variants(mnemonic)
        
        if not variants:
            return False, f"Unknown instruction: {mnemonic}"
        
        # Check if any variant matches the operand count
        operand_count = len(operands)
        for variant in variants:
            if variant.operand_count == operand_count:
                return True, ""
        
        # No matching variant found
        valid_counts = [v.operand_count for v in variants]
        return False, f"Invalid operand count for {mnemonic}: got {operand_count}, expected {valid_counts}"
    
    def get_instruction_info(self, mnemonic: str) -> List[Dict]:
        """Get detailed information about instruction variants."""
        variants = self.loader.get_instruction_variants(mnemonic)
        
        info_list = []
        for variant in variants:
            info_list.append({
                'mnemonic': variant.instruction,
                'syntax': variant.syntax,
                'operand_count': variant.operand_count,
                'opcode': variant.opcode,
                'description': variant.long_name
            })
        
        return info_list


def main():
    """Test the instruction encoder with sample instructions."""
    logging.basicConfig(level=logging.DEBUG)
    
    # Load instruction set
    from pathlib import Path
    from config_loader import get_config
    
    loader = InstructionSetLoader()
    config = get_config()
    excel_path = Path(config.instruction_set_path)
    
    if not loader.load_instruction_set(excel_path):
        print("❌ Failed to load instruction set")
        return
    
    # Create encoder
    encoder = InstructionEncoder(loader)
    
    # Test with sample instructions (after macro expansion)
    test_lines = [
        "ABS 1, 3",        # ABS d1, d3 after macro expansion
        "ADD 2, 4, 5",     # ADD instruction
        "MOV 1, #0xFF",    # MOV with immediate
        "NOP",             # No operands
        "; This is a comment",  # Should be ignored
        "INVALID_INSTR 1, 2",  # Should fail
    ]
    
    print("🧪 Testing instruction encoding:")
    print("=" * 50)
    
    for line_num, line in enumerate(test_lines, 1):
        print(f"\nLine {line_num}: {line}")
        parsed = encoder.parse_instruction_line(line, line_num)
        
        if parsed:
            print(f"  Parsed: {parsed.mnemonic} {parsed.operands}")
            encoded = encoder.encode_instruction(parsed)
            
            if encoded:
                print(f"  ✅ Encoded: {encoded}")
            else:
                print(f"  ❌ Encoding failed")
        else:
            print(f"  ⏭️  Skipped (not an instruction)")
    
    # Show any errors
    errors = encoder.get_encoding_errors()
    if errors:
        print(f"\n❌ Encoding errors ({len(errors)}):")
        for error in errors:
            print(f"  {error}")
    else:
        print(f"\n✅ No encoding errors")


if __name__ == '__main__':
    main()