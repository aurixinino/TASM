"""
NASM-compatible Numeric Constants Parser
Implements NASM 3.4.1 numeric constant formats

Supports all NASM numeric formats:
- Decimal: 200, 0200, 0200d, 0d200
- Hexadecimal: 0xc8, 0Xc8, 0c8h, 0hc8, $0c8 (deprecated)
- Octal: 310q, 310o, 0o310, 0q310
- Binary: 11001000b, 1100_1000b, 1100_1000y, 0b1100_1000, 0y1100_1000
- Underscores allowed in numbers for readability: 1_000_000
"""

import re
from typing import Union


class NumericParser:
    """Parser for NASM-compatible numeric constants"""
    
    @staticmethod
    def parse(value_str: str) -> int:
        """
        Parse a numeric constant in NASM format.
        
        Args:
            value_str: String representation of the number
            
        Returns:
            Integer value
            
        Raises:
            ValueError: If the string cannot be parsed as a number
        """
        original_str = value_str
        value_str = value_str.strip()
        
        if not value_str:
            raise ValueError(f"Empty numeric string: '{original_str}'")
        
        # Remove underscores (allowed for readability in NASM)
        value_str = value_str.replace('_', '')
        
        # Hexadecimal formats
        # 0xc8, 0Xc8 - standard prefix
        if value_str.lower().startswith('0x'):
            try:
                return int(value_str, 16)
            except ValueError:
                raise ValueError(f"Invalid hexadecimal number: '{original_str}'")
        
        # 0hc8, 0Hc8 - alternative prefix
        if len(value_str) > 2 and value_str[0] == '0' and value_str[1].lower() == 'h':
            try:
                return int(value_str[2:], 16)
            except ValueError:
                raise ValueError(f"Invalid hexadecimal number: '{original_str}'")
        
        # 0c8h, 0C8H - suffix format (must start with 0 if first digit is A-F)
        if value_str.lower().endswith('h'):
            hex_str = value_str[:-1]
            # NASM requires leading 0 if first digit is A-F
            if hex_str and hex_str[0].lower() in 'abcdef':
                if not hex_str[0] == '0':
                    raise ValueError(f"Hexadecimal number starting with A-F must begin with 0: '{original_str}'")
            try:
                return int(hex_str, 16)
            except ValueError:
                raise ValueError(f"Invalid hexadecimal number: '{original_str}'")
        
        # $0c8 - deprecated hex format (must have leading 0)
        if value_str.startswith('$'):
            hex_str = value_str[1:]
            if not hex_str:
                raise ValueError(f"Invalid hexadecimal number: '{original_str}'")
            # NASM deprecated syntax requires leading 0
            if hex_str[0].lower() in 'abcdef':
                raise ValueError(f"Deprecated $ hex format requires leading 0: '{original_str}'")
            try:
                return int(hex_str, 16)
            except ValueError:
                raise ValueError(f"Invalid hexadecimal number: '{original_str}'")
        
        # Binary formats
        # 0b1100_1000, 0B1100_1000 - standard prefix
        if value_str.lower().startswith('0b'):
            try:
                return int(value_str[2:], 2)
            except ValueError:
                raise ValueError(f"Invalid binary number: '{original_str}'")
        
        # 0y1100_1000, 0Y1100_1000 - alternative prefix
        if len(value_str) > 2 and value_str[0] == '0' and value_str[1].lower() == 'y':
            try:
                return int(value_str[2:], 2)
            except ValueError:
                raise ValueError(f"Invalid binary number: '{original_str}'")
        
        # 11001000b, 11001000B - suffix format
        if value_str.lower().endswith('b'):
            try:
                return int(value_str[:-1], 2)
            except ValueError:
                raise ValueError(f"Invalid binary number: '{original_str}'")
        
        # 1100_1000y, 1100_1000Y - alternative suffix
        if value_str.lower().endswith('y'):
            try:
                return int(value_str[:-1], 2)
            except ValueError:
                raise ValueError(f"Invalid binary number: '{original_str}'")
        
        # Octal formats
        # 0o310, 0O310 - standard prefix
        if value_str.lower().startswith('0o'):
            try:
                return int(value_str[2:], 8)
            except ValueError:
                raise ValueError(f"Invalid octal number: '{original_str}'")
        
        # 0q310, 0Q310 - alternative prefix
        if len(value_str) > 2 and value_str[0] == '0' and value_str[1].lower() == 'q':
            try:
                return int(value_str[2:], 8)
            except ValueError:
                raise ValueError(f"Invalid octal number: '{original_str}'")
        
        # 310q, 310Q - suffix format
        if value_str.lower().endswith('q'):
            try:
                return int(value_str[:-1], 8)
            except ValueError:
                raise ValueError(f"Invalid octal number: '{original_str}'")
        
        # 310o, 310O - alternative suffix
        if value_str.lower().endswith('o'):
            try:
                return int(value_str[:-1], 8)
            except ValueError:
                raise ValueError(f"Invalid octal number: '{original_str}'")
        
        # Decimal formats
        # 0d200, 0D200 - explicit decimal prefix
        if len(value_str) > 2 and value_str[0] == '0' and value_str[1].lower() == 'd':
            try:
                return int(value_str[2:], 10)
            except ValueError:
                raise ValueError(f"Invalid decimal number: '{original_str}'")
        
        # 0200d, 0200D - explicit decimal suffix
        if value_str.lower().endswith('d'):
            try:
                return int(value_str[:-1], 10)
            except ValueError:
                raise ValueError(f"Invalid decimal number: '{original_str}'")
        
        # Plain decimal: 200, 0200, -42
        # Note: In NASM, leading zeros do NOT make it octal (unlike C)
        # unless it has an explicit octal suffix (q, o, 0q, 0o)
        try:
            return int(value_str, 10)
        except ValueError:
            raise ValueError(f"Invalid numeric constant: '{original_str}'")
    
    @staticmethod
    def parse_with_sign(value_str: str) -> int:
        """
        Parse a numeric constant that may have a sign prefix.
        
        Args:
            value_str: String representation, possibly with + or - prefix
            
        Returns:
            Signed integer value
        """
        value_str = value_str.strip()
        
        if value_str.startswith('+'):
            return NumericParser.parse(value_str[1:])
        elif value_str.startswith('-'):
            return -NumericParser.parse(value_str[1:])
        else:
            return NumericParser.parse(value_str)


def parse_numeric(value_str: str) -> int:
    """
    Convenience function to parse a numeric constant.
    
    Args:
        value_str: String representation of the number
        
    Returns:
        Integer value
    """
    return NumericParser.parse_with_sign(value_str)


# Self-test
if __name__ == '__main__':
    test_cases = [
        # Decimal
        ('200', 200),
        ('0200', 200),
        ('0200d', 200),
        ('0d200', 200),
        ('-42', -42),
        ('+100', 100),
        ('1_000_000', 1000000),
        
        # Hexadecimal
        ('0c8h', 0xc8),
        ('0xc8', 0xc8),
        ('0hc8', 0xc8),
        ('$0c8', 0xc8),
        ('0XC8', 0xc8),
        ('0abh', 0xab),
        ('0FFh', 0xff),
        
        # Octal
        ('310q', 0o310),
        ('310o', 0o310),
        ('0o310', 0o310),
        ('0q310', 0o310),
        ('0O777', 0o777),
        
        # Binary
        ('11001000b', 0b11001000),
        ('1100_1000b', 0b11001000),
        ('1100_1000y', 0b11001000),
        ('0b1100_1000', 0b11001000),
        ('0y1100_1000', 0b11001000),
        ('0B11110000', 0b11110000),
    ]
    
    print("Testing NASM numeric parser...")
    passed = 0
    failed = 0
    
    for input_str, expected in test_cases:
        try:
            result = parse_numeric(input_str)
            if result == expected:
                print(f"✓ {input_str:20s} = {result:10d} (0x{result:X})")
                passed += 1
            else:
                print(f"✗ {input_str:20s} = {result:10d}, expected {expected}")
                failed += 1
        except Exception as e:
            print(f"✗ {input_str:20s} raised {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
