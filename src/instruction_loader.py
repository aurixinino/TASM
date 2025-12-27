"""
Tricore Instruction Set Loader

This module loads and parses instruction set definitions from external files.
Supports multiple formats: Excel (.xlsx), JSON (.json), and XML (.xml).

The loader creates an in-memory representation of the instruction set that can be
used by the instruction encoder for efficient lookup and encoding operations.
"""

import pandas as pd
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

try:
    from config_loader import get_config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False


@dataclass
class InstructionDefinition:
    """Represents a single instruction definition from the instruction set."""
    
    opcode: str  # Hex string like "0x01C0000B"
    opcode_size: int  # Size in bits (e.g., 32)
    instruction: str  # Mnemonic like "ABS"
    long_name: str  # Full name like "Absolute Value"
    syntax: str  # Syntax pattern like "ABS D[c],D[b]"
    reference: str  # Reference documentation
    operand_count: int  # Number of operands
    
    # Operand position and length information
    op1_pos: int = 0
    op1_len: int = 0
    op2_pos: int = 0
    op2_len: int = 0
    op3_pos: int = 0
    op3_len: int = 0
    op4_pos: int = 0
    op4_len: int = 0
    op5_pos: int = 0
    op5_len: int = 0
    
    # Syntax operand types (computed at load time)
    _syntax_operand_types: Optional[List[str]] = None
    
    @property
    def syntax_operand_types(self) -> List[str]:
        """Get cached syntax operand types (computed once)."""
        if self._syntax_operand_types is None:
            self._syntax_operand_types = self._parse_syntax_operand_types()
        return self._syntax_operand_types
    
    def _parse_syntax_operand_types(self) -> List[str]:
        import re
        # Extract operands from syntax (everything after mnemonic)
        parts = self.syntax.split(None, 1)
        if len(parts) < 2:
            return []
        
        operands_str = parts[1]
        
        # Remove split field markers like {[15:0]}
        operands_str = re.sub(r'\{[^\}]+\}', '', operands_str)
        
        # Split by comma
        operand_patterns = [op.strip() for op in operands_str.split(',')]
        
        types = []
        for pattern in operand_patterns:
            # Check if this is a register pattern (D[x], A[x], E[x], P[x])
            # Must have brackets OR be single letter followed by digit
            is_register = False
            pattern_upper = pattern.strip().upper()
            
            # Check for [A[15]] pattern (fixed register with memory addressing)
            # This should be treated as reg_a for matching purposes
            fixed_reg_match = re.match(r'^\[([DAEP])\[(\d+)\]\]', pattern_upper)
            if fixed_reg_match:
                reg_type = fixed_reg_match.group(1)
                if reg_type == 'D':
                    types.append('reg_d')
                elif reg_type == 'A':
                    types.append('reg_a')
                elif reg_type == 'E':
                    types.append('reg_e')
                elif reg_type == 'P':
                    types.append('reg_p')
                is_register = True
            
            if not is_register:
                # Check for D[x], A[x], E[x], P[x] pattern
                reg_match = re.match(r'^([DAEP])\s*\[', pattern_upper)
                if reg_match:
                    reg_type = reg_match.group(1)
                    if reg_type == 'D':
                        types.append('reg_d')
                    elif reg_type == 'A':
                        types.append('reg_a')
                    elif reg_type == 'E':
                        types.append('reg_e')
                    elif reg_type == 'P':
                        types.append('reg_p')
                    is_register = True
            
            if not is_register:
                # Not a register pattern - it's an immediate (disp, off, const, etc.)
                types.append('imm')
        
        return types
    
    def get_opcode_value(self) -> int:
        if isinstance(self.opcode, str) and self.opcode.startswith('0x'):
            return int(self.opcode, 16)
        elif isinstance(self.opcode, (int, float)):
            return int(self.opcode)
        else:
            raise ValueError(f"Invalid opcode format: {self.opcode}")
    
    def get_operand_info(self, operand_num: int) -> tuple[int, int]:
        """Get position and length for specified operand (1-based)."""
        operand_map = {
            1: (self.op1_pos, self.op1_len),
            2: (self.op2_pos, self.op2_len),
            3: (self.op3_pos, self.op3_len),
            4: (self.op4_pos, self.op4_len),
            5: (self.op5_pos, self.op5_len)
        }
        return operand_map.get(operand_num, (0, 0))
    
    def get_operand_bit_width(self, operand_num: int) -> int:
        """
        Get total bit width for specified operand, handling split fields.
        
        For operands with split encoding like off16 {[9:6][15:10][5:0]},
        calculates the total width by parsing the bitfield specification.
        
        Args:
            operand_num: Operand number (1-based)
            
        Returns:
            Total bit width for the operand
        """
        import re
        
        # First try to get from syntax if it contains a split field spec
        # Parse syntax to find the operand
        parts = self.syntax.split(None, 1)
        if len(parts) < 2:
            # No operands in syntax
            _, op_len = self.get_operand_info(operand_num)
            return op_len
        
        operands_str = parts[1]
        
        # Split by comma to get individual operand patterns
        operand_patterns = [op.strip() for op in operands_str.split(',')]
        
        if operand_num > len(operand_patterns):
            # Operand number out of range
            _, op_len = self.get_operand_info(operand_num)
            return op_len
        
        # Get the pattern for this operand (0-based index)
        pattern = operand_patterns[operand_num - 1]
        
        # Check if this pattern contains a split field specification {...}
        split_match = re.search(r'\{([^\}]+)\}', pattern)
        if split_match:
            # Parse split fields: [9:6][15:10][5:0] -> [(9,6), (15,10), (5,0)]
            fields_str = split_match.group(1)
            field_matches = re.findall(r'\[(\d+):(\d+)\]', fields_str)
            
            # Calculate total width by summing all field widths
            total_width = 0
            for high, low in field_matches:
                width = int(high) - int(low) + 1
                total_width += width
            
            return total_width
        
        # Check if pattern has explicit bit width (e.g., off16, imm8, disp24)
        width_match = re.search(r'(off|imm|disp|const|rel)(\d+)', pattern, re.IGNORECASE)
        if width_match:
            return int(width_match.group(2))
        
        # Fallback to stored length
        _, op_len = self.get_operand_info(operand_num)
        return op_len


class InstructionSetLoader:
    def __init__(self, force_32bit: bool = False, no_implicit: bool = False):
        self.force_32bit = force_32bit
        self.no_implicit = no_implicit
        self.instructions = {}
        self._instruction_list = []

    def load_instruction_set(self, file_path: Union[str, Path]) -> bool:
        """
        Delegates to the appropriate private loader based on file extension.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        try:
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                return self._load_excel(file_path)
            elif file_path.suffix.lower() == '.csv':
                return self._load_csv(file_path)
            elif file_path.suffix.lower() == '.json':
                return self._load_json(file_path)
            elif file_path.suffix.lower() == '.xml':
                return self._load_xml(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path.suffix}")
                return False
        except Exception as e:
            logger.error(f"Failed to load instruction set from {file_path}: {e}")
            return False

    def split_compound_operands(self, operand_str: str) -> List[str]:
        """
        Split compound operands (e.g., [A[15]], 4, D0) into individual operand strings.
        Handles tolerant parsing for bracketed and vendor-specific forms.
        Also splits compound patterns like [a15]14 into ['a15', '14'].
        """
        # Split by comma, but keep brackets together
        parts = []
        buf = ''
        depth = 0
        for c in operand_str:
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
            if c == ',' and depth == 0:
                if buf.strip():
                    parts.append(buf.strip())
                buf = ''
            else:
                buf += c
        if buf.strip():
            parts.append(buf.strip())
        
        # Tolerant normalization: convert bracketed register forms to canonical
        # AND split compound patterns like [a15]14 into ['a15', '14']
        normalized = []
        for op in parts:
            op = op.strip()
            
            # Check for compound pattern: [register]offset or [register+]offset (e.g., [a15]14, [%a2+]1)
            # This should be split into register part and offset part
            # Support GCC post-increment: [%a2+]1 means use a2, then increment by 1
            compound_match = re.match(r'^\[([^\]]+)\](\d+)$', op)
            if compound_match:
                # Split into register part and offset part
                reg_part = compound_match.group(1)  # e.g., "a15" or "A[2]" or "%a2+"
                offset_part = compound_match.group(2)  # e.g., "14" or "1"
                
                # Check if this is GCC post-increment syntax (%reg+ inside brackets)
                gcc_postinc = re.match(r'^%?([aAeEdDpP])(\d+)\+$', reg_part)
                if gcc_postinc:
                    # Keep the brackets and + for GCC post-increment: [%a2+]
                    normalized.append(f"[{reg_part}]")
                    normalized.append(offset_part)
                    continue
                
                # Normalize the register part (remove brackets, convert a[2] to a2)
                # Remove all outer brackets from register part
                while True:
                    reg_part = reg_part.strip()
                    if reg_part.startswith('[') and reg_part.endswith(']'):
                        reg_part = reg_part[1:-1].strip()
                    else:
                        break
                
                # Convert a[2], A[2], etc. to a2/A2
                reg_match = re.match(r'^([aAeEdDpP])\[(\d+)\]$', reg_part)
                if reg_match:
                    reg_part = f"{reg_match.group(1)}{reg_match.group(2)}"
                
                # Add both parts separately
                normalized.append(reg_part)
                normalized.append(offset_part)
                continue
            
            # Not a compound pattern, process normally
            # Remove all outer brackets
            while True:
                op = op.strip()
                if op.startswith('[') and op.endswith(']'):
                    op = op[1:-1].strip()
                else:
                    break
            # Convert a[2], A[2], etc. to a2/A2
            reg_match = re.match(r'^([aAeEdDpP])\[(\d+)\]$', op)
            if reg_match:
                op = f"{reg_match.group(1)}{reg_match.group(2)}"
            normalized.append(op)
        return normalized
        try:
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                return self._load_excel(file_path)
            elif file_path.suffix.lower() == '.csv':
                return self._load_csv(file_path)
            elif file_path.suffix.lower() == '.json':
                return self._load_json(file_path)
            elif file_path.suffix.lower() == '.xml':
                return self._load_xml(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path.suffix}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to load instruction set from {file_path}: {e}")
            return False
    
    def _load_excel(self, file_path: Path) -> bool:
        """Load instruction set from Excel file."""
        logger.info(f"Loading instruction set from Excel file: {file_path}")
        
        try:
            # Read the Excel file and get sheet names
            xl_file = pd.ExcelFile(file_path)
            logger.debug(f"Available sheets: {xl_file.sheet_names}")
            
            # Look for the tricore_reduced_instruction_set sheet
            sheet_name = 'tricore_reduced_instruction_set'
            if sheet_name not in xl_file.sheet_names:
                # Fall back to first sheet
                sheet_name = xl_file.sheet_names[0]
                logger.warning(f"Sheet 'tricore_reduced_instruction_set' not found, using '{sheet_name}'")
            
            # Read the data
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} instructions from sheet '{sheet_name}'")
            
            # Convert DataFrame to instruction definitions
            instructions_loaded = 0
            for _, row in df.iterrows():
                try:
                    # Skip rows with missing critical fields (OpCode or Instruction)
                    if pd.isna(row['OpCode']) or pd.isna(row['Instruction']):
                        continue
                    
                    instruction = InstructionDefinition(
                        opcode=str(row['OpCode']) if pd.notna(row['OpCode']) else '',
                        opcode_size=int(row['OpCodeSize']) if pd.notna(row['OpCodeSize']) else 32,
                        instruction=str(row['Instruction']) if pd.notna(row['Instruction']) else '',
                        long_name=str(row['LongName']) if pd.notna(row['LongName']) else '',
                        syntax=str(row['Syntax']) if pd.notna(row['Syntax']) else '',
                        reference=str(row['Reference']) if pd.notna(row['Reference']) else '',
                        operand_count=int(row['OperandCount']) if pd.notna(row['OperandCount']) else 0,
                        op1_pos=int(row['op1_pos']) if pd.notna(row['op1_pos']) else 0,
                        op1_len=int(row['op1_len']) if pd.notna(row['op1_len']) else 0,
                        op2_pos=int(row['op2_pos']) if pd.notna(row['op2_pos']) else 0,
                        op2_len=int(row['op2_len']) if pd.notna(row['op2_len']) else 0,
                        op3_pos=int(row['op3_pos']) if pd.notna(row['op3_pos']) else 0,
                        op3_len=int(row['op3_len']) if pd.notna(row['op3_len']) else 0,
                        op4_pos=int(row['op4_pos']) if pd.notna(row['op4_pos']) else 0,
                        op4_len=int(row['op4_len']) if pd.notna(row['op4_len']) else 0,
                        op5_pos=int(row['op5_pos']) if pd.notna(row['op5_pos']) else 0,
                        op5_len=int(row['op5_len']) if pd.notna(row['op5_len']) else 0
                    )
                    
                    # Add to instruction dictionary (grouped by mnemonic)
                    mnemonic = instruction.instruction.upper()
                    if mnemonic not in self.instructions:
                        self.instructions[mnemonic] = []
                    self.instructions[mnemonic].append(instruction)
                    self._instruction_list.append(instruction)
                    instructions_loaded += 1
                    
                except Exception as e:
                    logger.warning(f"Skipping invalid instruction row: {e}")
            
            logger.info(f"Successfully loaded {instructions_loaded} instruction definitions")
            logger.info(f"Unique instruction mnemonics: {len(self.instructions)}")
            return instructions_loaded > 0
            
        except Exception as e:
            logger.error(f"Failed to load Excel file: {e}")
            return False
    
    def _load_json(self, file_path: Path) -> bool:
        """Load instruction set from JSON file."""
        logger.info(f"Loading instruction set from JSON file: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Expected JSON format:
            # {
            #   "instructions": [
            #     {
            #       "opcode": "0x01C0000B",
            #       "instruction": "ABS",
            #       "syntax": "ABS D[c],D[b]",
            #       ...
            #     }
            #   ]
            # }
            
            instructions_data = data.get('instructions', [])
            instructions_loaded = 0
            
            for instr_data in instructions_data:
                instruction = InstructionDefinition(
                    opcode=instr_data.get('opcode', ''),
                    opcode_size=instr_data.get('opcode_size', 32),
                    instruction=instr_data.get('instruction', ''),
                    long_name=instr_data.get('long_name', ''),
                    syntax=instr_data.get('syntax', ''),
                    reference=instr_data.get('reference', ''),
                    operand_count=instr_data.get('operand_count', 0),
                    op1_pos=instr_data.get('op1_pos', 0),
                    op1_len=instr_data.get('op1_len', 0),
                    op2_pos=instr_data.get('op2_pos', 0),
                    op2_len=instr_data.get('op2_len', 0),
                    op3_pos=instr_data.get('op3_pos', 0),
                    op3_len=instr_data.get('op3_len', 0),
                    op4_pos=instr_data.get('op4_pos', 0),
                    op4_len=instr_data.get('op4_len', 0),
                    op5_pos=instr_data.get('op5_pos', 0),
                    op5_len=instr_data.get('op5_len', 0)
                )
                
                mnemonic = instruction.instruction.upper()
                if mnemonic not in self.instructions:
                    self.instructions[mnemonic] = []
                self.instructions[mnemonic].append(instruction)
                self._instruction_list.append(instruction)
                instructions_loaded += 1
            
            logger.info(f"Successfully loaded {instructions_loaded} instruction definitions from JSON")
            return instructions_loaded > 0
            
        except Exception as e:
            logger.error(f"Failed to load JSON file: {e}")
            return False
    
    def _load_xml(self, file_path: Path) -> bool:
        """Load instruction set from XML file."""
        logger.info(f"Loading instruction set from XML file: {file_path}")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Expected XML format:
            # <instruction_set>
            #   <instruction opcode="0x01C0000B" mnemonic="ABS" syntax="ABS D[c],D[b]" ...>
            #   </instruction>
            # </instruction_set>
            
            instructions_loaded = 0
            
            for instr_elem in root.findall('.//instruction'):
                instruction = InstructionDefinition(
                    opcode=instr_elem.get('opcode', ''),
                    opcode_size=int(instr_elem.get('opcode_size', 32)),
                    instruction=instr_elem.get('mnemonic', ''),
                    long_name=instr_elem.get('long_name', ''),
                    syntax=instr_elem.get('syntax', ''),
                    reference=instr_elem.get('reference', ''),
                    operand_count=int(instr_elem.get('operand_count', 0)),
                    op1_pos=int(instr_elem.get('op1_pos', 0)),
                    op1_len=int(instr_elem.get('op1_len', 0)),
                    op2_pos=int(instr_elem.get('op2_pos', 0)),
                    op2_len=int(instr_elem.get('op2_len', 0)),
                    op3_pos=int(instr_elem.get('op3_pos', 0)),
                    op3_len=int(instr_elem.get('op3_len', 0)),
                    op4_pos=int(instr_elem.get('op4_pos', 0)),
                    op4_len=int(instr_elem.get('op4_len', 0)),
                    op5_pos=int(instr_elem.get('op5_pos', 0)),
                    op5_len=int(instr_elem.get('op5_len', 0))
                )
                
                mnemonic = instruction.instruction.upper()
                if mnemonic not in self.instructions:
                    self.instructions[mnemonic] = []
                self.instructions[mnemonic].append(instruction)
                self._instruction_list.append(instruction)
                instructions_loaded += 1
            
            logger.info(f"Successfully loaded {instructions_loaded} instruction definitions from XML")
            return instructions_loaded > 0
            
        except Exception as e:
            logger.error(f"Failed to load XML file: {e}")
            return False
    
    def get_instruction_variants(self, mnemonic: str) -> List[InstructionDefinition]:
        """Get all variants of an instruction by mnemonic."""
        return self.instructions.get(mnemonic.upper(), [])
    
    def get_all_instructions(self) -> List[InstructionDefinition]:
        """Get all loaded instruction definitions."""
        return self._instruction_list.copy()
    
    def get_instruction_count(self) -> int:
        """Get total number of loaded instructions."""
        return len(self._instruction_list)
    
    def get_mnemonic_count(self) -> int:
        """Get number of unique instruction mnemonics."""
        return len(self.instructions)
    
    def find_instruction(self, mnemonic: str, operand_count: int, 
                        operands: Optional[Any] = None) -> Optional[InstructionDefinition]:
        """
        Find instruction definition by mnemonic, operand count, and operand types.
        
        Simple and lean matching logic:
        1. Match operand types exactly (reg_d, reg_a, reg_e, reg_p, imm)
        2. For multiple matches with same types, use range-based scoring
        
        Args:
            mnemonic: Instruction mnemonic (case insensitive)
            operand_count: Number of operands
            operands: List of ParsedOperand objects or strings (optional)
            
        Returns:
            InstructionDefinition if found, None otherwise
        """
        variants = self.get_instruction_variants(mnemonic)
        
        # TEMPORARY: For LOOP instructions with labels, always use the largest variant
        # This ensures that large branch displacements can be encoded
        if mnemonic.upper() == 'LOOP' and operands:
            operand_strs = [op.text if hasattr(op, 'text') else str(op) for op in operands]
            # Check if any operand looks like a label (not a register or immediate)
            has_label = False
            for op in operand_strs:
                op_clean = op.strip()
                # Check if it's NOT a register pattern: d1, D1, d[1], a2, A2, etc.
                if not re.match(r'^%?[dDaAeEpP](\d+|\\d+\\])$', op_clean) and not op_clean.startswith('#'):
                    has_label = True
                    break
            
            if has_label:
                matching_by_count = [v for v in variants if v.operand_count == operand_count]
                if len(matching_by_count) > 1:
                    # Return largest variant for LOOP with labels
                    matching_by_count.sort(key=lambda v: v.opcode_size, reverse=True)
                    logger.info(f"LOOP with label detected - using largest variant: {matching_by_count[0].syntax}")
                    return matching_by_count[0]
        
        # Filter by operand count first
        matching_variants = [v for v in variants if v.operand_count == operand_count]
        
        if not matching_variants:
            return None
        
        # Apply force_32bit filter if enabled
        if self.force_32bit:
            matching_variants = [v for v in matching_variants if v.opcode_size >= 32]
            if not matching_variants:
                return None
        
        # Apply no_implicit filter if enabled (filter out variants with A[10] or A[15] in syntax)
        if self.no_implicit:
            matching_variants = [v for v in matching_variants 
                               if 'a[10]' not in v.syntax.lower() and 'a[15]' not in v.syntax.lower()
                               and 'a10' not in v.syntax.lower() and 'a15' not in v.syntax.lower()]
            if not matching_variants:
                return None
        
        # If only one variant matches, return it
        if len(matching_variants) == 1:
            return matching_variants[0]
        
        # Multiple variants - apply type-based filtering
        if operands:
            # Extract operand types from parsed operands
            if hasattr(operands[0], 'type'):
                # New ParsedOperand objects with type attribute
                operand_types = [op.type for op in operands]
            else:
                # Legacy string operands - classify them
                operand_types = [self._classify_operand_type_simple(op) for op in operands]
            
            # Filter variants by exact type match
            type_matched_variants = []
            for variant in matching_variants:
                syntax_types = variant.syntax_operand_types
                if len(syntax_types) == len(operand_types):
                    # Check if all types match
                    if all(st == ot for st, ot in zip(syntax_types, operand_types)):
                        # Additional check: filter out variants with specific register constraints
                        # that don't match the actual operand registers
                        # Example: MOV D[15], const8 should only match if operand is actually D15
                        is_compatible = True
                        
                        # Parse syntax to check for specific register requirements
                        parts = variant.syntax.split(None, 1)
                        if len(parts) >= 2:
                            operands_part = parts[1].strip()
                            operands_part = re.sub(r'\{[^\}]+\}', '', operands_part)
                            syntax_operands_list = [op.strip() for op in operands_part.split(',')]
                            
                            for i, syntax_op in enumerate(syntax_operands_list):
                                if i >= len(operands):
                                    break
                                
                                # Check if syntax specifies a specific register number
                                spec_reg_match = re.match(r'^([DAEP])\[(\d+)\]', syntax_op.upper())
                                if spec_reg_match:
                                    reg_type = spec_reg_match.group(1)
                                    reg_num = int(spec_reg_match.group(2))
                                    
                                    # Extract actual register from operand
                                    if hasattr(operands[i], 'text'):
                                        actual_operand = operands[i].text
                                    else:
                                        actual_operand = operands[i]
                                    
                                    actual_operand_clean = actual_operand.strip().replace('[', '').replace(']', '').upper()
                                    actual_reg_match = re.match(r'^([DAEP])(\d+)$', actual_operand_clean)
                                    
                                    if actual_reg_match:
                                        actual_type = actual_reg_match.group(1)
                                        actual_num = int(actual_reg_match.group(2))
                                        
                                        # Check if types and numbers match
                                        if actual_type != reg_type or actual_num != reg_num:
                                            is_compatible = False
                                            logger.debug(
                                                f"Variant '{variant.syntax}' filtered: "
                                                f"requires {reg_type}[{reg_num}] but operand is {actual_type}{actual_num}"
                                            )
                                            break
                        
                        if is_compatible:
                            type_matched_variants.append(variant)
            
            # If we have exact type matches, use them
            if type_matched_variants:
                matching_variants = type_matched_variants
                
                # ALWAYS apply range-based selection when multiple matches exist
                # This ensures immediate/offset values fit in bit fields
                if len(matching_variants) > 1:
                    # Get operand text values
                    operand_strs = [op.text if hasattr(op, 'text') else op for op in operands]
                    logger.info(f"[FIND] Multiple type-matched variants ({len(matching_variants)}) for {mnemonic}, applying range-based selection")
                    best_match = self._find_best_variant_by_operand_range(matching_variants, operand_strs)
                    if best_match:
                        logger.info(f"[FIND] Range-based selection succeeded: {best_match.syntax} ({best_match.opcode_size} bits)")
                        return best_match
                    else:
                        # Range-based selection failed - fall back to largest variant (most likely to fit)
                        logger.info(f"[FIND] Range-based selection returned None - falling back to largest variant")
                        matching_variants.sort(key=lambda v: v.opcode_size, reverse=True)
                        return matching_variants[0]
                
                # Only one type-matched variant - return it
                logger.info(f"[FIND] Returning single type-matched variant for {mnemonic}: {matching_variants[0].syntax}")
                return matching_variants[0]
        
        # Fallback: return smallest variant
        matching_variants.sort(key=lambda v: v.opcode_size)
        return matching_variants[0]
    
    def _classify_operand_type_simple(self, operand: str) -> str:
        """
        Simple operand type classification for legacy string operands.
        
        Args:
            operand: Operand string
            
        Returns:
            Type string: 'reg_d', 'reg_a', 'reg_e', 'reg_p', or 'imm'
        """
        clean = operand.strip().replace('[', '').replace(']', '').replace('#', '').lower()
        
        if clean and len(clean) >= 1:
            first_char = clean[0]
            if first_char == 'd':
                return 'reg_d'
            elif first_char == 'a':
                return 'reg_a'
            elif first_char == 'e':
                return 'reg_e'
            elif first_char == 'p':
                return 'reg_p'
        
        return 'imm'
    
    def _find_best_variant_with_scoring(self, variants: List[InstructionDefinition], operands: List[str]) -> Optional[InstructionDefinition]:
        """
        Select best instruction variant using scoring system with format hierarchy.
        
        Scoring criteria:
        - +100 points for 16-bit encoding (compact code)
        - +50 points for specific register constraints (e.g., A[15] vs A[x])
        - +20 points for tighter operand ranges (smaller bit fields)
        
        Format hierarchy preference:
        1. Specialized formats (specific registers, tight constraints)
        2. Compact formats (16-bit encodings)
        3. General-purpose formats (flexible but larger)
        
        Args:
            variants: List of instruction variants with same operand count
            operands: List of operand strings from the parsed instruction
            
        Returns:
            Best matching variant or None if no variant matches
        """
        scored_variants = []
        
        # Debug logging
        debug_mode = logger.isEnabledFor(logging.DEBUG)
        if debug_mode:
            logger.debug(f"Scoring {len(variants)} variants for operands: {operands}")
        
        for variant in variants:
            # Start with base score
            score = 0
            
            if debug_mode:
                logger.debug(f"  Checking variant: {variant.syntax} (opcode_size={variant.opcode_size})")
            
            # Verify operand types match (filter out incompatible variants)
            if not self._check_operand_type_match(variant, operands):
                if debug_mode:
                    logger.debug(f"    Rejected: operand type mismatch")
                continue
            
            # Verify operand values fit in bit fields (filter out variants with insufficient range)
            if not self._check_operand_range_match(variant, operands):
                if debug_mode:
                    logger.debug(f"    Rejected: operand range mismatch")
                continue
            
            # SCORING CRITERION 1: Prefer smaller opcodes (compact code)
            if variant.opcode_size == 16:
                score += 100
            elif variant.opcode_size == 32:
                score += 50
            
            # SCORING CRITERION 2: Prefer specific register constraints (specialized formats)
            specificity_bonus = self._calculate_specificity_score(variant.syntax)
            score += specificity_bonus
            
            # SCORING CRITERION 3: Prefer tighter operand ranges (smaller bit fields)
            tightness_bonus = self._calculate_tightness_score(variant)
            score += tightness_bonus
            
            if debug_mode:
                logger.debug(f"    Accepted: score={score} (size:{variant.opcode_size}bit +{100 if variant.opcode_size==16 else 50}, specificity:+{specificity_bonus}, tightness:+{tightness_bonus})")
            
            scored_variants.append((score, variant))
        
        # No valid variants after filtering
        if not scored_variants:
            if debug_mode:
                logger.debug(f"  No variants matched all criteria")
            return None
        
        # Sort by score (descending) and return highest-scored variant
        scored_variants.sort(key=lambda x: x[0], reverse=True)
        best_score, best_variant = scored_variants[0]
        
        if debug_mode:
            logger.debug(f"  Selected: {best_variant.syntax} with score={best_score}")
        
        return best_variant
    
    def _check_operand_type_match(self, variant: InstructionDefinition, operands: List[str]) -> bool:
        """
        
        Args:
            variant: Instruction variant to check
            operands: Operands from parsed instruction
            
        Returns:
            True if operand types match, False otherwise
        """
        # Extract syntax operands from variant
        syntax_parts = variant.syntax.split()
        if len(syntax_parts) < 2:
            return True  # No operands in syntax
        
        syntax_operands = syntax_parts[1].split(',') if len(syntax_parts) > 1 else []
        
        # Check each operand type
        for i, (syntax_op, actual_op) in enumerate(zip(syntax_operands, operands)):
            syntax_type = self._extract_syntax_operand_type(syntax_op)
            actual_type = self._extract_operand_type(actual_op)
            
            # Type mismatch check
            if syntax_type != actual_type:
                # Syntax expects immediate - actual can be immediate or register-as-value
                if syntax_type == 'imm':
                    # Allow any operand type when syntax expects immediate
                    continue
                
                # Syntax expects register but actual is immediate - REJECT
                # This prevents matching "MOV D[a], D[b]" when operand is "#1"
                if syntax_type in ['a', 'd', 'e', 'p'] and actual_type == 'imm':
                    return False
                
                # Other type mismatches - reject
                return False
            
            # Check specific register requirements (e.g., A[15] vs A[b])
            is_specific, reg_type, reg_number = self._is_specific_register_syntax(syntax_op)
            if is_specific and reg_number is not None:
                actual_reg_num = self._extract_register_number(actual_op)
                
                if actual_reg_num is not None:
                    if reg_number != actual_reg_num:
                        return False
        
        return True
    
    def _check_operand_range_match(self, variant: InstructionDefinition, operands: List[str]) -> bool:
        """
        
        Args:
            variant: Instruction variant to check
            operands: Operands from parsed instruction
            
        Returns:
            True if all operands fit, False otherwise
        """
        # Reuse existing range checking logic
        result = self._find_best_variant_by_operand_range([variant], operands)
        return result is not None
    
    def _calculate_specificity_score(self, syntax: str) -> int:
        """
        Calculate specificity bonus based on register constraints in syntax.
        
        Examples:
            "ST.W [A[15]],off4,D[a]" -> +50 (A15 is specific)
            "ST.W [A[b]],off10,D[a]" -> 0 (no specific registers)
            "ADD D[15],D[a]" -> +50 (D15 is specific)
        
        Args:
            syntax: Instruction syntax string
            
        Returns:
            Specificity bonus points (0-50)
        """
        bonus = 0
        
        # Check for specific register constraints
        import re
        
        # Pattern: Register with specific number like A[15], D[15], E[14]
        specific_pattern = r'[ADEP]\[\d+\]'
        matches = re.findall(specific_pattern, syntax)
        
        if matches:
            bonus += 50  # Award bonus for any specific register constraint
        
        return bonus
    
    def _calculate_tightness_score(self, variant: InstructionDefinition) -> int:
        """
        Calculate tightness bonus based on operand bit field sizes.
        
        Smaller bit fields indicate tighter constraints:
        - 4-bit field (off4): more constrained
        - 10-bit field (off10): less constrained
        
        Args:
            variant: Instruction variant
            
        Returns:
            Tightness bonus points (0-20)
        """
        bonus = 0
        
        # Sum all operand lengths (smaller total = tighter constraints)
        total_bits = 0
        for i in range(1, 6):  # op1 through op5
            op_len = getattr(variant, f'op{i}_len', None)
            if op_len and op_len > 0:
                total_bits += op_len
        
        # Award bonus inversely proportional to total bits
        # Fewer bits = tighter constraints = higher bonus
        if total_bits > 0:
            # Scale: 20 points for very tight (e.g., 8 bits), 0 for loose (e.g., 40+ bits)
            bonus = max(0, 20 - (total_bits // 2))
        
        return bonus
    
    def _extract_required_register(self, syntax_operand: str) -> Optional[int]:
        """
        Extract specific register number from syntax operand.
        
        Examples:
            "A[15]" -> 15
            "D[1]" -> 1
            "A[b]" -> None (variable)
        
        Args:
            syntax_operand: Operand from syntax string
            
        Returns:
            Register number or None if variable
        """
        import re
        match = re.search(r'\[(\d+)\]', syntax_operand)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_register_number(self, operand: str) -> Optional[int]:
        """
        Extract register number from actual operand.
        
        Examples:
            "a15" -> 15
            "d0" -> 0
            "[a15]" -> 15
        
        Args:
            operand: Actual operand string
            
        Returns:
            Register number or None if not a register
        """
        import re
        clean = operand.replace('[', '').replace(']', '').strip().lower()
        match = re.search(r'[ade](\d+)', clean)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_operand_type(self, operand_str: str) -> str:
        """
        Extract operand type from operand string.
        
        Examples:
            "[a0]" -> "a"  (address register, memory indirect)
            "a0" -> "a"    (address register)
            "d0" -> "d"    (data register)
            "D[1]" -> "d"  (data register)
            "#0x100" -> "imm" (immediate value)
            "0x100" -> "imm"  (immediate value)
            "label" -> "imm"  (label/offset, treated as immediate)
        
        Args:
            operand_str: Operand string from parsed instruction
            
        Returns:
            Operand type identifier
        """
        import re
        
        operand_str = operand_str.strip()
        
        # Remove memory indirect brackets and immediate prefix
        clean = operand_str.replace('[', '').replace(']', '').replace('#', '').strip()
        
        # Check first character (after cleaning)
        if clean:
            first_char = clean[0].lower()
            if first_char == 'a':
                return 'a'  # Address register
            elif first_char == 'd':
                return 'd'  # Data register
            elif first_char == 'e':
                return 'e'  # Extended register
            elif first_char == 'p':
                return 'p'  # Pointer register
        
        # If starts with digit or 0x, it's immediate/offset
        if clean and (clean[0].isdigit() or clean.startswith('0x')):
            return 'imm'
        
        # Default to immediate (could be label or constant)
        return 'imm'
    
    def _extract_syntax_operand_type(self, syntax_operand: str) -> str:
        """
        Extract operand type from syntax definition.
        
        Examples:
            "A[b]" -> "a"     (address register)
            "D[a]" -> "d"     (data register)
            "off18" -> "imm"  (offset/immediate)
            "disp24" -> "imm" (displacement/immediate)
            "const9" -> "imm" (constant/immediate)
        
        Args:
            syntax_operand: Operand from syntax string
            
        Returns:
            Operand type identifier
        """
        import re
        
        # Remove split operand markers {...}
        syntax_operand = re.sub(r'\{[^\}]+\}', '', syntax_operand).strip()
        
        # Remove brackets
        clean = syntax_operand.replace('[', '').replace(']', '').strip()
        
        if not clean:
            return 'unknown'
        
        first_char = clean[0].upper()
        
        # Check for register patterns
        if first_char == 'A':
            return 'a'  # Address register
        elif first_char == 'D':
            return 'd'  # Data register
        elif first_char == 'E':
            return 'e'  # Extended register
        elif first_char == 'P':
            return 'p'  # Pointer register
        
        # Check for immediate/offset patterns
        if any(keyword in clean.lower() for keyword in ['off', 'disp', 'const', 'imm', 'rel']):
            return 'imm'
        
        return 'unknown'
    
    def _find_best_variant_by_operand_range(self, variants: List[InstructionDefinition],
                                            operands: List[str]) -> Optional[InstructionDefinition]:
        """
        Find the best matching variant based on operand value ranges.
        
        Selects the smallest instruction size (opcode_size) that can accommodate
        the operand values. This optimizes for code size.
        
        Example: J instruction with disp8 (8-bit, 16-bit opcode) vs disp24 (24-bit, 32-bit opcode)
        - If displacement fits in 8 bits: select 16-bit instruction
        - If displacement requires more than 8 bits: select 32-bit instruction
        
        Args:
            variants: List of instruction variants with same operand count
            operands: Operand strings from parsed instruction
            
        Returns:
            Best matching InstructionDefinition (smallest that fits) or None
        """
        # Parse operand values
        try:
            from numeric_parser import parse_numeric
        except ImportError:
            # Fallback if numeric_parser is not available
            def parse_numeric(s):
                s = s.strip()
                if s.startswith('0x') or s.startswith('0X'):
                    return int(s, 16)
                elif s.startswith('0b') or s.startswith('0B'):
                    return int(s, 2)
                else:
                    return int(s)
        
        operand_values = []
        for operand_str in operands:
            try:
                # Try to parse as immediate value
                # Remove prefixes like # or brackets (but be careful with register notation)
                clean_operand = operand_str.strip()
                
                # Check if it's definitely a register before removing brackets
                # Registers start with a, d, e, p (case insensitive)
                # Remove outer brackets for checking
                inner = clean_operand.replace('[', '').replace(']', '').replace('#', '').strip()
                
                # Check if it's a register (skip range checking for registers)
                if inner and inner[0].lower() in ['a', 'd', 'e', 'p']:
                    operand_values.append(None)  # Not an immediate value
                    continue
                
                # Try to parse as numeric constant (remove # prefix if present)
                clean_numeric = clean_operand.replace('#', '').strip()
                value = parse_numeric(clean_numeric)
                operand_values.append(value)
            except (ValueError, Exception):
                # Not a numeric value (could be label, register, etc.)
                operand_values.append(None)
        
        # Filter variants that can accommodate all operand values
        suitable_variants = []
        
        # Get syntax operands for register checking
        import re
        
        for variant in variants:
            can_fit = True
            
            # Parse syntax to extract operand patterns
            syntax_parts = variant.syntax.split(None, 1)
            if len(syntax_parts) < 2:
                syntax_operands = []
            else:
                syntax_operands_str = syntax_parts[1]
                syntax_for_split = re.sub(r'\{[^\}]+\}', '', syntax_operands_str)
                syntax_operands = [op.strip() for op in syntax_for_split.split(',')]
            
            # Check each operand
            for i, orig_value in enumerate(operand_values):
                if orig_value is None:
                    # Non-immediate operand (could be register or label/symbol)
                    if i < len(syntax_operands) and i < len(operands):
                        parsed_op = operands[i]
                        syntax_op = syntax_operands[i]
                        
                        # Check if the operand is a register
                        clean_operand = parsed_op.strip().replace('[', '').replace(']', '').replace('#', '')
                        is_register = clean_operand and clean_operand[0].lower() in ['a', 'd', 'e', 'p']
                        
                        if is_register:
                            # Check specific register requirements
                            if not self._operand_matches_syntax_register(parsed_op, syntax_op):
                                # Register doesn't match (e.g., D0 vs D[15])
                                can_fit = False
                                break
                        # If it's a label/symbol (not a register), skip range checking
                        # Labels will be resolved during encoding with actual displacement values
                    continue
                
                # Get operand bit length from instruction definition
                # Use get_operand_bit_width to handle split fields correctly
                operand_num = i + 1
                op_len = variant.get_operand_bit_width(operand_num)
                
                if op_len == 0:
                    # Implicit operand or not encoded
                    continue
                
                # Start with original value
                value = orig_value
                
                # Check if this operand has /2 or /4 modifier in syntax (e.g., disp8/2, const8/4)
                # Extract operand patterns from syntax
                syntax_parts = variant.syntax.split(None, 1)
                if len(syntax_parts) > 1:
                    operands_part = syntax_parts[1].strip()
                    # Remove split operand specifications
                    operands_part = __import__('re').sub(r'\{[^\}]+\}', '', operands_part)
                    syntax_operands = [op.strip() for op in operands_part.split(',')]
                    
                    # If this operand has scaling modifier, divide the value before checking fit
                    if i < len(syntax_operands):
                        syntax_op = syntax_operands[i]
                        if '/4' in syntax_op:
                            value = value // 4
                            logger.debug(f"Operand {i+1} has /4 modifier, checking {value} (after division from {orig_value})")
                        elif '/2' in syntax_op:
                            value = value // 2
                            logger.debug(f"Operand {i+1} has /2 modifier, checking {value} (after division from {orig_value})")
                        # Check for 'off' (offset) parameters that need implicit scaling
                        # Word-aligned instructions (LD.W, ST.W, LD.A, LEA) use word offsets (/4)
                        # The Excel doesn't include /4 in syntax, but assembler accepts byte offsets
                        elif 'off' in syntax_op.lower() and '/4' not in syntax_op:
                            # Only scale for word-aligned instructions
                            word_aligned_mnemonics = {'LD.W', 'ST.W', 'LD.A', 'LEA'}
                            if variant.instruction in word_aligned_mnemonics:
                                match = re.search(r'\boff\d+\b', syntax_op, re.IGNORECASE)
                                if match:
                                    value = value // 4
                
                # Calculate value range for this operand width
                # For signed values: -(2^(n-1)) to 2^(n-1)-1
                # For unsigned values: 0 to 2^n-1
                # We'll use signed range as it's more conservative
                max_signed = (1 << (op_len - 1)) - 1
                min_signed = -(1 << (op_len - 1))
                max_unsigned = (1 << op_len) - 1
                
                # Check if value fits (try both signed and unsigned)
                if not ((min_signed <= value <= max_signed) or (0 <= value <= max_unsigned)):
                    can_fit = False
                    logger.debug(
                        f"Variant '{variant.syntax}' (opcode_size={variant.opcode_size}): "
                        f"operand {i+1} value {value} doesn't fit in {op_len} bits "
                        f"(range: signed [{min_signed}, {max_signed}], unsigned [0, {max_unsigned}])"
                    )
                    break
            
            if can_fit:
                suitable_variants.append(variant)
        
        if not suitable_variants:
            # No variant can fit the operands - return None (will use fallback)
            logger.debug(
                f"Range-based selection: No suitable variants found "
                f"(checked {len(variants)} variants)"
            )
            return None
        
        # Check if any operands are labels/symbols (non-numeric, non-register)
        # For labels, we should prefer larger variants (more accommodating displacement fields)
        has_labels = any(val is None and i < len(operand_values) for i, val in enumerate(operand_values))
        
        # Calculate how many operands DON'T match specific register requirements
        # Lower mismatch count = better match
        def calculate_non_specific_matches(variant):
            """Count operands that use variable registers when instruction uses specific values."""
            non_specific_count = 0
            syntax_parts = variant.syntax.split(None, 1)
            if len(syntax_parts) < 2:
                return 0
            
            operands_part = syntax_parts[1].strip()
            operands_part = re.sub(r'\{[^\}]+\}', '', operands_part)
            syntax_operands = [op.strip() for op in operands_part.split(',')]
            
            for i, syntax_op in enumerate(syntax_operands):
                if i >= len(operands):
                    break
                    
                # Check if syntax allows variable register but operand is specific value
                is_specific_syntax, _, _ = self._is_specific_register_syntax(syntax_op)
                if not is_specific_syntax:
                    # Syntax is variable (D[a], A[b], etc.)
                    # Check if operand is a specific register
                    op_type, op_num = self._extract_register_info(operands[i])
                    if op_type is not None and op_num is not None:
                        # Operand is specific (e.g., D15, A15) but syntax is variable
                        # This is less optimal - increment mismatch count
                        non_specific_count += 1
            
            return non_specific_count
        
        # Sort variants based on whether we have labels or not
        if has_labels:
            # When operands contain labels (unknown displacement values), prefer LARGER variants
            # This ensures labels can reach farther distances (e.g., LOOP with disp15 vs disp4)
            # Sort by: 1) fewest non-specific matches, 2) opcode size (LARGER first)
            suitable_variants.sort(key=lambda v: (calculate_non_specific_matches(v), -v.opcode_size))
            logger.debug(f"Operands contain labels/symbols - preferring larger instruction variants")
        else:
            # When all operands are numeric, prefer SMALLER variants (code size optimization)
            # Sort by: 1) fewest non-specific matches, 2) opcode size (smaller first)
            suitable_variants.sort(key=lambda v: (calculate_non_specific_matches(v), v.opcode_size))
        
        best = suitable_variants[0]
        logger.debug(
            f"Range-based selection: Selected '{best.syntax}' with opcode_size={best.opcode_size} "
            f"non_specific_matches={calculate_non_specific_matches(best)} "
            f"(from {len(variants)} candidates, {len(suitable_variants)} suitable)"
        )
        
        return best
    
    def _is_specific_register_syntax(self, syntax_part: str) -> tuple:
        """
        Check if syntax part specifies a specific register number.
        
        Examples:
            'D[15]' -> (True, 'D', 15)  - Specific register D15
            'D[b]' -> (False, 'D', None) - Variable register
            'A[15]' -> (True, 'A', 15)   - Specific address register A15
            'disp8' -> (False, None, None) - Not a register
        
        Args:
            syntax_part: Part of syntax string
            
        Returns:
            Tuple of (is_specific, reg_type, reg_number)
        """
        import re
        
        # Match pattern like D[15] or A[7] (specific register number)
        match = re.match(r'([DAEPC])\[(\d+)\]', syntax_part, re.IGNORECASE)
        if match:
            return (True, match.group(1).upper(), int(match.group(2)))
        
        # Match pattern like D[b] or A[a] (variable register)
        match = re.match(r'([DAEPC])\[[a-z]\]', syntax_part, re.IGNORECASE)
        if match:
            return (False, match.group(1).upper(), None)
        
        return (False, None, None)
    
    def _extract_register_info(self, operand: str) -> tuple:
        """
        Extract register type and number from operand.
        
        Tolerant parser that accepts multiple equivalent formats:
        - 'D[4]' or 'd[4]' -> ('D', 4)
        - 'd4' or 'D4' -> ('D', 4)
        - 'A[15]' or 'a[15]' -> ('A', 15)
        - 'a0' or 'A0' -> ('A', 0)
        - '[a2]' or '[A2]' -> ('A', 2)
        - '[a[2]]' or '[A[2]]' -> ('A', 2)
        - '[d15]' or '[D15]' -> ('D', 15)
        - '[d[15]]' or '[D[15]]' -> ('D', 15)
        
        Args:
            operand: Operand string from parsed instruction
            
        Returns:
            Tuple of (reg_type, reg_number)
        """
        import re
        
        operand = operand.strip()
        # If operand contains a bracketed register followed by a number, split and extract
        import re
        compound_pattern = r'^\[([DAEPCaepc][0-9]+)\](\d+)$'
        m = re.match(compound_pattern, operand)
        if m:
            # Return register info for first part, number for second
            return (m.group(1)[0].upper(), int(m.group(1)[1:])), int(m.group(2))
        # Otherwise, handle as before
        # Match [D[n]] or [A[n]] pattern (double brackets with inner bracket notation)
        match = re.match(r'\[([DAEPC])\[(\d+)\]\]', operand, re.IGNORECASE)
        if match:
            return (match.group(1).upper(), int(match.group(2)))
        # Match D[n] or A[n] pattern
        match = re.match(r'([DAEPC])\[(\d+)\]', operand, re.IGNORECASE)
        if match:
            return (match.group(1).upper(), int(match.group(2)))
        # Match [D[n]] or [A[n]] pattern (single bracket with Dn/An notation)
        match = re.match(r'\[([DAEPC])(\d+)\]', operand, re.IGNORECASE)
        if match:
            return (match.group(1).upper(), int(match.group(2)))
        # Match Dn or An pattern (e.g., d4, a0, D4, A0)
        match = re.match(r'([DAEPC])(\d+)', operand, re.IGNORECASE)
        if match:
            return (match.group(1).upper(), int(match.group(2)))
        return (None, None)
    
    def _operand_matches_syntax_register(self, operand: str, syntax: str) -> bool:
        """
        Check if operand matches syntax pattern for registers, considering specific numbers.
        
        This is the key function for the new selection logic:
        - If syntax is 'D[15]' (specific), operand MUST be 'D[15]' (exact match)
        - If syntax is 'D[b]' (variable), operand can be any D register
        
        Args:
            operand: Parsed operand (e.g., 'D[4]', 'D[15]')
            syntax: Syntax pattern (e.g., 'D[15]', 'D[b]')
            
        Returns:
            True if operand matches syntax pattern
        """
        # Get operand register info
        op_type, op_num = self._extract_register_info(operand)
        if op_type is None:
            # Not a register operand, use generic type matching
            return True
        
        # Get syntax register info
        is_specific, syn_type, syn_num = self._is_specific_register_syntax(syntax)
        if syn_type is None:
            # Syntax is not a register pattern
            return True
        
        # Check register type match
        if op_type != syn_type:
            return False
        
        # If syntax specifies specific register number, operand must match exactly
        if is_specific:
            return op_num == syn_num
        
        # Variable register - any number is OK as long as type matches
        return True
    
    def _find_best_variant_by_operand_types(self, variants: List[InstructionDefinition], 
                                           operands: List[str]) -> Optional[InstructionDefinition]:
        """
        Find the best matching variant based on operand types.
        
        Enhanced selection logic (Nov 2025):
        1. Match by operand type (D, A, immediate)
        2. Match by specific register numbers (e.g., D[15] vs D[b])
           - D[15] in syntax -> ONLY matches D[15] in code
           - D[b] in syntax -> matches ANY D register
        3. Prefer variable register variants over specific ones
        
        Args:
            variants: List of instruction variants with same operand count
            operands: Operand strings from parsed instruction
            
        Returns:
            Best matching InstructionDefinition or None
        """
        import re
        
        best_match = None
        best_score = -1
        
        for variant in variants:
            # Parse syntax to extract operand types
            # Remove instruction mnemonic
            syntax_parts = variant.syntax.split(None, 1)
            if len(syntax_parts) < 2:
                continue
            
            syntax_operands_str = syntax_parts[1]
            
            # Split by comma, but be careful with {...} content
            # Remove {...} content first for splitting
            syntax_for_split = re.sub(r'\{[^\}]+\}', '', syntax_operands_str)
            syntax_operands = [op.strip() for op in syntax_for_split.split(',')]
            
            if len(syntax_operands) != len(operands):
                continue
            
            # Calculate match score
            score = 0
            all_operands_match = True
            
            for i, (syntax_op, parsed_op) in enumerate(zip(syntax_operands, operands)):
                # Check specific register matching first
                if not self._operand_matches_syntax_register(parsed_op, syntax_op):
                    # Operand doesn't match syntax (e.g., D[4] vs D[15])
                    all_operands_match = False
                    break
                
                # Get operand types
                syntax_type = self._extract_syntax_operand_type(syntax_op)
                parsed_type = self._extract_operand_type(parsed_op)
                
                if syntax_type == parsed_type:
                    # Exact type match - but treat immediate vs register differently
                    if syntax_type == 'imm':
                        # Both immediate - low score, let range checking decide optimal size
                        score += 1
                    else:
                        # Register type match - high score
                        score += 10
                    
                        # CRITICAL: Check for exact register number match
                        # If syntax is D[15] and operand is D[15], give HUGE bonus
                        # This ensures D[15] variant wins over D[b] variant when operand is D[15]
                        is_specific, syn_type, syn_num = self._is_specific_register_syntax(syntax_op)
                        if is_specific and syntax_type in ['d', 'a', 'e', 'p']:
                            op_type, op_num = self._extract_register_info(parsed_op)
                            if op_type == syn_type and op_num == syn_num:
                                score += 100  # HUGE bonus for exact register match (D[15] == D[15])
                    
                elif syntax_type == 'imm' and parsed_type == 'imm':
                    # Both immediate - compatible, but low score (let range checking decide)
                    score += 1
                elif syntax_type == 'imm' and parsed_type not in ['d', 'a', 'e', 'p']:
                    # Immediate syntax can match unknown/label operands, but NOT registers
                    score += 1
                elif parsed_type == 'imm' and syntax_type in ['d', 'a', 'e', 'p']:
                    # Immediate operand vs register syntax - REJECT (e.g., #1 vs D[b])
                    all_operands_match = False
                    break
                elif parsed_type == 'imm' and syntax_type not in ['d', 'a', 'e', 'p']:
                    # Immediate operand can match unknown syntax types
                    score += 1
                elif parsed_type in ['d', 'a', 'e', 'p'] and syntax_type == 'imm':
                    # Register operand vs immediate syntax - REJECT (e.g., D5 vs const8)
                    all_operands_match = False
                    break
                elif syntax_type in ['d', 'a', 'e', 'p'] and parsed_type not in ['d', 'a', 'e', 'p']:
                    # Register syntax vs non-register operand - REJECT
                    all_operands_match = False
                    break
            
            # Skip variants where operands don't match
            if not all_operands_match:
                logger.debug(
                    f"Variant '{variant.syntax}' REJECTED: "
                    f"operands don't match (e.g., D[4] vs D[15])"
                )
                continue
            
            logger.debug(
                f"Variant '{variant.syntax}' score: {score} "
                f"(operands: {operands})"
            )
            
            # Prefer higher score, but if scores are equal, prefer smaller opcode size
            if score > best_score or (score == best_score and best_match and variant.opcode_size < best_match.opcode_size):
                best_score = score
                best_match = variant
        
        # Only return a match if we have a meaningful type-based score
        # If best_score is low or only from exact register type matches without strong differentiation,
        # let range-based matching decide. This allows operand range checking to select optimal instruction size.
        #
        # Score breakdown:
        #   +100 = exact register number match (D[15] == D[15])
        #   +10 = exact type match (register type or immediate type)
        #   +1 = loose immediate match
        #
        # CRITICAL: If we rejected some variants due to type mismatch AND best match has register operands
        # (score >= 10), return it. This prevents falling back to variants that expect registers when we have immediates.
        # Example: MOV with ['d4', '#1'] should match "MOV D[a], const4" (score=11) and reject
        # "MOV D[a], D[b]" (type mismatch). We return const4 variant to prevent selecting D[b] variant.
        #
        # However, if best_score is low (only immediate matches), defer to range checking to select
        # the variant with appropriate bit width (const4 vs const16).
        
        # Decision logic: When to use type-based match vs. defer to range checking
        #
        # Only use type-based match if score >= 20 (at least 2 operands match perfectly).
        # Otherwise ALWAYS defer to range checking, which will:
        # 1. Naturally reject register variants for immediate operands (type mismatch)
        # 2. Select the appropriate bit width (const4 vs const16) based on value range
        #
        # This handles both cases correctly:
        # - "mov d4,#1" (score 11) → range checking → rejects D[b], selects const4 (fits in 4 bits)
        # - "mov d5,#76" (score 11) → range checking → rejects D[b] and const4, selects const16
        # - "mov d4,d1" (score 20) → type match → selects D[b] variant
        
        if best_score >= 20:
            # High confidence - at least 2 operands match perfectly (e.g., register-to-register)
            logger.debug(
                f"Type-based matching: high confidence score={best_score}, using variant: {best_match.syntax if best_match else 'None'}"
            )
            return best_match
        
        # Medium/low score - defer to range checking for bit width selection
        logger.debug(
            f"Type-based matching: score={best_score}, deferring to range-based selection"
        )
        return None
    
    def export_to_json(self, file_path: Union[str, Path]) -> bool:
        # Export loaded instruction set to JSON format.
        try:
            file_path = Path(file_path)
            
            # Convert instruction definitions to dictionaries
            instructions_data = []
            for instruction in self._instruction_list:
                instructions_data.append({
                    'opcode': instruction.opcode,
                    'opcode_size': instruction.opcode_size,
                    'instruction': instruction.instruction,
                    'long_name': instruction.long_name,
                    'syntax': instruction.syntax,
                    'reference': instruction.reference,
                    'operand_count': instruction.operand_count,
                    'op1_pos': instruction.op1_pos,
                    'op1_len': instruction.op1_len,
                    'op2_pos': instruction.op2_pos,
                    'op2_len': instruction.op2_len,
                    'op3_pos': instruction.op3_pos,
                    'op3_len': instruction.op3_len,
                    'op4_pos': instruction.op4_pos,
                    'op4_len': instruction.op4_len,
                    'op5_pos': instruction.op5_pos,
                    'op5_len': instruction.op5_len
                })
            
            data = {
                'metadata': {
                    'version': '1.0',
                    'format': 'tricore_instruction_set',
                    'instruction_count': len(instructions_data),
                    'mnemonic_count': len(self.instructions)
                },
                'instructions': instructions_data
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Exported {len(instructions_data)} instructions to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export instruction set to JSON: {e}")
            return False


def main():
    # Test the instruction loader with the tricore Excel file.
    logging.basicConfig(level=logging.INFO)
    
    # Load the tricore instruction set
    loader = InstructionSetLoader()
    
    # Get path from config
    if not CONFIG_AVAILABLE:
        print("❌ Config loader not available")
        return
    
    config = get_config()
    excel_path = Path(config.instruction_set_path)
    
    if loader.load_instruction_set(excel_path):
        print(f"✅ Loaded {loader.get_instruction_count()} instructions")
        print(f"✅ Found {loader.get_mnemonic_count()} unique mnemonics")
        
        # Test finding specific instructions
        abs_instruction = loader.find_instruction('ABS', 2)
        if abs_instruction:
            print(f"\n🔍 Found ABS instruction:")
            print(f"   Syntax: {abs_instruction.syntax}")
            print(f"   OpCode: {abs_instruction.opcode}")
            print(f"   Op1 pos/len: {abs_instruction.op1_pos}/{abs_instruction.op1_len}")
            print(f"   Op2 pos/len: {abs_instruction.op2_pos}/{abs_instruction.op2_len}")
        
        # Export to JSON for future use
        json_path = Path('output/tricore_instruction_set.json')
        json_path.parent.mkdir(exist_ok=True)
        if loader.export_to_json(json_path):
            print(f"✅ Exported instruction set to {json_path}")
    # End of main()
