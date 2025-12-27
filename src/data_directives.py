"""
NASM-Compatible Data Directives and Pseudo-Instructions

This module implements NASM-style data declaration directives:
- DB, DW, DD, DQ, DT, DO, DY, DZ: Declaring initialized data
- RESB, RESW, RESD, RESQ, REST, RESO, RESY, RESZ: Declaring uninitialized data
- INCBIN: Including external binary files
- EQU: Defining constants
- TIMES: Repeating instructions or data
"""

from pathlib import Path
from typing import List, Tuple, Optional, Union
import struct
import re
from numeric_parser import parse_numeric


class DataDirective:
    """Handles NASM-compatible data directives."""
    
    # Data size mappings
    DATA_SIZES = {
        'DB': 1,   # Define Byte (8-bit)
        'DW': 2,   # Define Word (16-bit)
        'DD': 4,   # Define Double-word (32-bit)
        'DQ': 8,   # Define Quad-word (64-bit)
        'DT': 10,  # Define Ten bytes (80-bit)
        'DO': 16,  # Define Octa-word (128-bit)
        'DY': 32,  # Define 32 bytes (256-bit)
        'DZ': 64,  # Define 64 bytes (512-bit)
    }
    
    RESERVE_SIZES = {
        'RESB': 1,   # Reserve Bytes
        'RESW': 2,   # Reserve Words
        'RESD': 4,   # Reserve Double-words
        'RESQ': 8,   # Reserve Quad-words
        'REST': 10,  # Reserve Ten bytes
        'RESO': 16,  # Reserve Octa-words
        'RESY': 32,  # Reserve 32 bytes
        'RESZ': 64,  # Reserve 64 bytes
    }
    
    def __init__(self, endianness: str = 'little', labels: dict = None):
        """
        Initialize data directive handler.
        
        Args:
            endianness: 'little' or 'big' for byte ordering
            labels: Dictionary of labels/symbols for resolution
        """
        self.endianness = endianness
        self.constants = {}  # EQU constants
        self.labels = labels or {}  # Symbol table for label resolution
    
    def is_data_directive(self, line: str) -> bool:
        """Check if line contains a data directive."""
        parts = line.strip().upper().split()
        if not parts:
            return False
        
        mnemonic = parts[0]
        return (mnemonic in self.DATA_SIZES or 
                mnemonic in self.RESERVE_SIZES or
                mnemonic in ['INCBIN', 'EQU', 'TIMES'])
    
    def parse_value(self, value_str: str) -> Union[int, float, bytes, str]:
        """
        Parse a value from string representation.
        
        Supports:
        - NASM numeric formats (all variants from NASM 3.4.1)
        - Characters: 'A', 'Hello'
        - Strings: "Hello, World!"
        - Floating point: 3.14, 1.5e-10
        - Constants: EQU symbols
        - Labels: resolved to addresses
        """
        value_str = value_str.strip()
        
        # String literals (double quotes)
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1].encode('utf-8')
        
        # Character literals (single quotes)
        if value_str.startswith("'") and value_str.endswith("'"):
            char_str = value_str[1:-1]
            if len(char_str) == 1:
                return ord(char_str)
            else:
                # Multiple characters - return as bytes
                return char_str.encode('utf-8')
        
        # Floating point (check before numeric parsing)
        if '.' in value_str or ('e' in value_str.lower() and 'h' not in value_str.lower()):
            try:
                return float(value_str)
            except ValueError:
                pass
        
        # Check if it's a constant (EQU symbol) before trying numeric parsing
        if value_str in self.constants:
            return self.constants[value_str]
        
        # Check if it's a label
        if value_str in self.labels:
            label_obj = self.labels[value_str]
            # Return the address associated with the label
            return label_obj.address if hasattr(label_obj, 'address') else label_obj
        
        # Try NASM-compatible numeric parsing
        try:
            return parse_numeric(value_str)
        except ValueError:
            pass
        
        # If all else fails, return 0 (placeholder for unresolved symbols)
        # This allows two-pass assembly where symbols are resolved later
        return 0
    
    def parse_data_list(self, operands_str: str) -> List[Union[int, float, bytes]]:
        """
        Parse comma-separated list of data values.
        
        Example: "1, 2, 'A', 0x10, \"Hello\""
        """
        # Remove comments first
        if ';' in operands_str:
            comment_pos = operands_str.find(';')
            # Make sure it's not inside quotes
            in_quotes = False
            quote_char = None
            for i, char in enumerate(operands_str):
                if char in ['"', "'"] and (not in_quotes or char == quote_char):
                    in_quotes = not in_quotes
                    if in_quotes:
                        quote_char = char
                elif char == ';' and not in_quotes:
                    operands_str = operands_str[:i]
                    break
        
        values = []
        
        # Split by commas, but respect quotes
        in_quotes = False
        quote_char = None
        current = []
        
        for char in operands_str:
            if char in ['"', "'"] and (not in_quotes or char == quote_char):
                in_quotes = not in_quotes
                if in_quotes:
                    quote_char = char
                current.append(char)
            elif char == ',' and not in_quotes:
                if current:
                    values.append(''.join(current).strip())
                    current = []
            else:
                current.append(char)
        
        if current:
            values.append(''.join(current).strip())
        
        # Parse each value
        parsed_values = []
        for value_str in values:
            parsed = self.parse_value(value_str)
            parsed_values.append(parsed)
        
        return parsed_values
    
    def encode_data(self, directive: str, values: List[Union[int, float, bytes]]) -> bytes:
        """
        Encode data according to directive size.
        
        Args:
            directive: DB, DW, DD, etc.
            values: List of parsed values
            
        Returns:
            Encoded bytes
        """
        size = self.DATA_SIZES[directive.upper()]
        result = bytearray()
        
        for value in values:
            if isinstance(value, bytes):
                # String/character data - append as-is
                result.extend(value)
            elif isinstance(value, float):
                # Floating point encoding
                if size == 4:
                    result.extend(struct.pack(f'<f' if self.endianness == 'little' else '>f', value))
                elif size == 8:
                    result.extend(struct.pack(f'<d' if self.endianness == 'little' else '>d', value))
                else:
                    raise ValueError(f"Cannot encode float with size {size}")
            elif isinstance(value, int):
                # Integer encoding
                try:
                    if self.endianness == 'little':
                        result.extend(value.to_bytes(size, 'little', signed=(value < 0)))
                    else:
                        result.extend(value.to_bytes(size, 'big', signed=(value < 0)))
                except OverflowError:
                    raise ValueError(f"Value {value} too large for {directive} (max {size} bytes)")
        
        return bytes(result)
    
    def calculate_size(self, line: str, current_address: int = 0) -> int:
        """
        Calculate the size in bytes that this directive will generate.
        
        Args:
            line: Assembly line
            current_address: Current address (for $ references)
            
        Returns:
            Size in bytes
        """
        # Remove comments first (but respect quotes)
        if ';' in line:
            in_quotes = False
            quote_char = None
            for i, char in enumerate(line):
                if char in ['"', "'"] and (not in_quotes or char == quote_char):
                    in_quotes = not in_quotes
                    if in_quotes:
                        quote_char = char
                elif char == ';' and not in_quotes:
                    line = line[:i]
                    break
        
        parts = line.strip().split(None, 1)
        if not parts:
            return 0
        
        directive = parts[0].upper()
        
        # TIMES directive
        if directive == 'TIMES':
            return self._calculate_times_size(line, current_address)
        
        # Reserve directives
        if directive in self.RESERVE_SIZES:
            if len(parts) < 2:
                return 0
            count = self.parse_value(parts[1])
            return count * self.RESERVE_SIZES[directive]
        
        # Data directives
        if directive in self.DATA_SIZES:
            if len(parts) < 2:
                return 0
            
            values = self.parse_data_list(parts[1])
            size = self.DATA_SIZES[directive]
            total_size = 0
            
            for value in values:
                if isinstance(value, bytes):
                    total_size += len(value)
                else:
                    total_size += size
            
            return total_size
        
        # INCBIN
        if directive == 'INCBIN':
            return self._calculate_incbin_size(parts[1] if len(parts) > 1 else '')
        
        # EQU doesn't generate code
        if directive == 'EQU':
            return 0
        
        return 0
    
    def _calculate_times_size(self, line: str, current_address: int) -> int:
        """Calculate size for TIMES directive."""
        # TIMES count instruction/data
        match = re.match(r'TIMES\s+(\S+)\s+(.+)', line, re.IGNORECASE)
        if not match:
            return 0
        
        count_str, rest = match.groups()
        count = self.parse_value(count_str)
        
        # Calculate size of the repeated part
        inner_size = self.calculate_size(rest, current_address)
        return count * inner_size
    
    def _calculate_incbin_size(self, operands: str) -> int:
        """Calculate size for INCBIN directive."""
        # Parse INCBIN operands: filename [,start [,length]]
        parts = [p.strip() for p in operands.split(',')]
        
        if not parts:
            return 0
        
        filename = parts[0].strip('"\'')
        start = 0
        length = None
        
        if len(parts) > 1:
            start = self.parse_value(parts[1])
        if len(parts) > 2:
            length = self.parse_value(parts[2])
        
        try:
            file_path = Path(filename)
            if not file_path.exists():
                return 0
            
            file_size = file_path.stat().st_size
            
            if length is not None:
                return min(length, file_size - start)
            else:
                return file_size - start
        except Exception:
            return 0
    
    def process_equ(self, line: str) -> Tuple[str, int]:
        """
        Process EQU directive.
        
        Args:
            line: Assembly line with EQU
            
        Returns:
            Tuple of (symbol_name, value)
        """
        # Format: symbol EQU value
        parts = line.split(None, 2)
        if len(parts) < 3 or parts[1].upper() != 'EQU':
            raise ValueError(f"Invalid EQU directive: {line}")
        
        symbol = parts[0]
        value = self.parse_value(parts[2])
        
        if not isinstance(value, int):
            raise ValueError(f"EQU value must be an integer, got {type(value)}")
        
        self.constants[symbol] = value
        return symbol, value
    
    def process_incbin(self, operands: str, base_dir: Optional[Path] = None) -> bytes:
        """
        Process INCBIN directive.
        
        Args:
            operands: INCBIN operands (filename [,start [,length]])
            base_dir: Base directory for relative paths
            
        Returns:
            Binary data from file
        """
        # Parse operands: filename [,start [,length]]
        parts = [p.strip() for p in operands.split(',')]
        
        filename = parts[0].strip('"\'')
        start = 0
        length = None
        
        if len(parts) > 1:
            start = self.parse_value(parts[1])
        if len(parts) > 2:
            length = self.parse_value(parts[2])
        
        # Resolve file path
        file_path = Path(filename)
        if base_dir and not file_path.is_absolute():
            file_path = base_dir / file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"INCBIN file not found: {file_path}")
        
        # Read file
        with open(file_path, 'rb') as f:
            f.seek(start)
            if length is not None:
                data = f.read(length)
            else:
                data = f.read()
        
        return data
    
    def process_times(self, line: str, current_address: int = 0) -> Tuple[int, bytes]:
        """
        Process TIMES directive.
        
        Args:
            line: Assembly line with TIMES
            current_address: Current address for $ references
            
        Returns:
            Tuple of (count, data_to_repeat)
        """
        # TIMES count instruction/data
        match = re.match(r'TIMES\s+(\S+)\s+(.+)', line, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid TIMES directive: {line}")
        
        count_str, rest = match.groups()
        count = self.parse_value(count_str)
        
        if not isinstance(count, int) or count < 0:
            raise ValueError(f"TIMES count must be a non-negative integer: {count_str}")
        
        # Process the repeated part
        # This is a simplified version - full implementation would need
        # to recursively handle instructions/data
        return count, rest
