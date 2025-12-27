"""
Test specific register number matching in instruction selection.

This test validates that the instruction encoder properly selects instruction
variants based on whether the syntax specifies:
- A specific register number (e.g., D[15]) - matches ONLY that register
- A variable register (e.g., D[b]) - matches ANY register in that class

Example:
    Code: JNZ D[4], switch_on
    
    Available variants:
    - JNZ D[15], disp8 (0xEE) - ONLY accepts D15
    - JNZ D[b], disp4 (0xF6) - Accepts ANY D register
    
    Expected: Should select 0xF6 because D[4] != D[15]
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import TASMConfig


class TestSpecificRegisterMatching:
    """Test instruction variant selection with specific register numbers."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Load instruction set
        config = TASMConfig()
        self.loader = InstructionSetLoader()
        success = self.loader.load_instruction_set(config.instruction_set_path)
        assert success, "Failed to load instruction set"
        
        # Create encoder
        self.encoder = InstructionEncoder(self.loader)
    
    def test_jnz_d15_variant_selection(self):
        """Test that JNZ D[15] selects the D[15]-specific variant."""
        # Get JNZ variants
        variants = self.loader.get_instruction_variants('JNZ')
        assert len(variants) == 2, f"Expected 2 JNZ variants, got {len(variants)}"
        
        # Parse instruction with D[15]
        parsed = ParsedInstruction(
            mnemonic='JNZ',
            operands=['D[15]', '0x10'],
            original_line='JNZ D[15], 0x10',
            line_number=1
        )
        
        # Find instruction
        instr = self.loader.find_instruction('JNZ', 2, parsed.operands)
        assert instr is not None, "Should find JNZ instruction"
        
        # Should select the D[15] variant (0x00EE)
        assert instr.opcode == '0x00EE', \
            f"Expected D[15]-specific variant (0x00EE), got {instr.opcode} - {instr.syntax}"
    
    def test_jnz_d4_variant_selection(self):
        """Test that JNZ D[4] selects the D[b] variable variant."""
        # Get JNZ variants
        variants = self.loader.get_instruction_variants('JNZ')
        assert len(variants) == 2, f"Expected 2 JNZ variants, got {len(variants)}"
        
        # Parse instruction with D[4]
        parsed = ParsedInstruction(
            mnemonic='JNZ',
            operands=['D[4]', 'switch_on'],
            original_line='JNZ D[4], switch_on',
            line_number=1
        )
        
        # Find instruction
        instr = self.loader.find_instruction('JNZ', 2, parsed.operands)
        assert instr is not None, "Should find JNZ instruction"
        
        # Should select the D[b] variant (0x00F6), NOT the D[15] variant
        assert instr.opcode == '0x00F6', \
            f"Expected D[b] variable variant (0x00F6) for D[4], got {instr.opcode} - {instr.syntax}"
    
    def test_jnz_various_registers(self):
        """Test JNZ with various D register numbers."""
        test_cases = [
            ('D[0]', '0x00F6', 'D[b]'),   # D0 -> variable variant
            ('D[1]', '0x00F6', 'D[b]'),   # D1 -> variable variant
            ('D[4]', '0x00F6', 'D[b]'),   # D4 -> variable variant
            ('D[7]', '0x00F6', 'D[b]'),   # D7 -> variable variant
            ('D[15]', '0x00EE', 'D[15]'), # D15 -> specific variant
        ]
        
        for reg, expected_opcode, expected_pattern in test_cases:
            parsed = ParsedInstruction(
                mnemonic='JNZ',
                operands=[reg, '0x10'],
                original_line=f'JNZ {reg}, 0x10',
                line_number=1
            )
            
            instr = self.loader.find_instruction('JNZ', 2, parsed.operands)
            assert instr is not None, f"Should find JNZ instruction for {reg}"
            assert instr.opcode == expected_opcode, \
                f"For {reg}: expected {expected_pattern} variant ({expected_opcode}), " \
                f"got {instr.opcode} - {instr.syntax}"
    
    def test_syntax_pattern_extraction(self):
        """Test that we can correctly identify specific register patterns in syntax."""
        test_cases = [
            ('D[15]', True, 15),    # Specific register D15
            ('D[b]', False, None),   # Variable register
            ('D[a]', False, None),   # Variable register
            ('A[15]', True, 15),     # Specific address register A15
            ('A[b]', False, None),   # Variable address register
            ('disp8', False, None),  # Not a register
            ('off16', False, None),  # Not a register
        ]
        
        for syntax_part, is_specific, expected_num in test_cases:
            # Test helper function (we'll implement this)
            is_spec, num = self._is_specific_register_syntax(syntax_part)
            assert is_spec == is_specific, \
                f"For '{syntax_part}': expected specific={is_specific}, got {is_spec}"
            assert num == expected_num, \
                f"For '{syntax_part}': expected number={expected_num}, got {num}"
    
    def _is_specific_register_syntax(self, syntax_part: str) -> tuple[bool, int]:
        """
        Check if syntax part specifies a specific register number.
        
        Args:
            syntax_part: Part of syntax string (e.g., 'D[15]', 'D[b]', 'A[a]')
            
        Returns:
            Tuple of (is_specific, register_number)
            - is_specific: True if syntax specifies exact register number
            - register_number: The number if specific, None otherwise
        """
        import re
        
        # Match pattern like D[15] or A[7]
        match = re.match(r'([DAEPC])\[(\d+)\]', syntax_part, re.IGNORECASE)
        if match:
            return (True, int(match.group(2)))
        
        # Match pattern like D[b] or A[a] (variable)
        match = re.match(r'([DAEPC])\[[a-z]\]', syntax_part, re.IGNORECASE)
        if match:
            return (False, None)
        
        return (False, None)
    
    def test_operand_matches_specific_register(self):
        """Test matching operand against specific register syntax."""
        test_cases = [
            ('D[4]', 'D[15]', False),   # D4 doesn't match D[15]
            ('D[15]', 'D[15]', True),    # D15 matches D[15]
            ('D[0]', 'D[15]', False),    # D0 doesn't match D[15]
            ('D[4]', 'D[b]', True),      # D4 matches D[b] (any D register)
            ('D[15]', 'D[b]', True),     # D15 matches D[b] (any D register)
            ('A[0]', 'A[15]', False),    # A0 doesn't match A[15]
            ('A[15]', 'A[15]', True),    # A15 matches A[15]
        ]
        
        for operand, syntax, should_match in test_cases:
            result = self._operand_matches_syntax(operand, syntax)
            assert result == should_match, \
                f"Operand '{operand}' vs syntax '{syntax}': " \
                f"expected match={should_match}, got {result}"
    
    def _operand_matches_syntax(self, operand: str, syntax: str) -> bool:
        """
        Check if operand matches syntax pattern, considering specific register numbers.
        
        Args:
            operand: Parsed operand (e.g., 'D[4]', 'D[15]')
            syntax: Syntax pattern (e.g., 'D[15]', 'D[b]')
            
        Returns:
            True if operand matches syntax pattern
        """
        import re
        
        # Extract register type and number from operand
        op_match = re.match(r'([DAEPC])\[(\d+)\]', operand, re.IGNORECASE)
        if not op_match:
            return False  # Can't parse operand
        
        op_type = op_match.group(1).upper()
        op_num = int(op_match.group(2))
        
        # Check if syntax is specific register (e.g., D[15])
        syn_match = re.match(r'([DAEPC])\[(\d+)\]', syntax, re.IGNORECASE)
        if syn_match:
            # Specific register in syntax - must match exactly
            syn_type = syn_match.group(1).upper()
            syn_num = int(syn_match.group(2))
            return op_type == syn_type and op_num == syn_num
        
        # Check if syntax is variable register (e.g., D[b])
        syn_match = re.match(r'([DAEPC])\[[a-z]\]', syntax, re.IGNORECASE)
        if syn_match:
            # Variable register - only type must match
            syn_type = syn_match.group(1).upper()
            return op_type == syn_type
        
        return False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
