"""
Test MOV Immediate Value Encoding

This test validates that MOV instructions with immediate values select the correct
opcode variant (const4/const8/const16) instead of the register-to-register variant.

Bug fix: Previously MOV D[a], #imm would incorrectly match MOV D[a], D[b] (0x02)
instead of MOV D[a], const4 (0x82).
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import get_config


class TestMOVImmediateEncoding:
    """Test MOV instruction with immediate values"""
    
    def setup_method(self):
        """Setup for each test"""
        config = get_config()
        self.loader = InstructionSetLoader()
        assert self.loader.load_instruction_set(config.instruction_set_path)
        self.encoder = InstructionEncoder(self.loader)
    
    def test_mov_d4_imm1(self):
        """Test: mov d4,#1 should use MOV D[a], const4 (0x82), not MOV D[a], D[b] (0x02)"""
        parsed = ParsedInstruction('MOV', ['d4', '#1'], 'mov d4,#1', 1)
        result = self.encoder.encode_instruction(parsed)
        
        assert result is not None, "mov d4,#1 failed to encode"
        assert result.definition.opcode == '0x0082', \
            f"Wrong opcode: expected 0x0082 (MOV D[a], const4), got {result.definition.opcode} ({result.definition.syntax})"
        assert result.hex_value == '0x1482', \
            f"Wrong encoding: expected 0x1482, got {result.hex_value}"
    
    def test_mov_d2_imm1(self):
        """Test: mov d2,#1 should use MOV D[a], const4 (0x82)"""
        parsed = ParsedInstruction('MOV', ['d2', '#1'], 'mov d2,#1', 1)
        result = self.encoder.encode_instruction(parsed)
        
        assert result is not None, "mov d2,#1 failed to encode"
        assert result.definition.opcode == '0x0082', \
            f"Wrong opcode: expected 0x0082 (MOV D[a], const4), got {result.definition.opcode}"
        assert result.hex_value == '0x1282', \
            f"Wrong encoding: expected 0x1282, got {result.hex_value}"
    
    def test_mov_d0_imm0(self):
        """Test: mov d0,#0 should use MOV D[a], const4 (0x82)"""
        parsed = ParsedInstruction('MOV', ['d0', '#0'], 'mov d0,#0', 1)
        result = self.encoder.encode_instruction(parsed)
        
        assert result is not None, "mov d0,#0 failed to encode"
        assert result.definition.opcode == '0x0082', \
            f"Wrong opcode: expected 0x0082 (MOV D[a], const4), got {result.definition.opcode}"
        assert result.hex_value == '0x0082', \
            f"Wrong encoding: expected 0x0082, got {result.hex_value}"
    
    def test_mov_d5_imm15(self):
        """Test: mov d5,#15 should use MOV D[a], const4 (0x82) with max 4-bit value"""
        parsed = ParsedInstruction('MOV', ['d5', '#15'], 'mov d5,#15', 1)
        result = self.encoder.encode_instruction(parsed)
        
        assert result is not None, "mov d5,#15 failed to encode"
        assert result.definition.opcode == '0x0082', \
            f"Wrong opcode: expected 0x0082 (MOV D[a], const4), got {result.definition.opcode}"
        assert result.hex_value == '0xF582', \
            f"Wrong encoding: expected 0xF582, got {result.hex_value}"
    
    def test_mov_register_to_register(self):
        """Test: mov d4,d1 should correctly use MOV D[a], D[b] (0x02)"""
        parsed = ParsedInstruction('MOV', ['d4', 'd1'], 'mov d4,d1', 1)
        result = self.encoder.encode_instruction(parsed)
        
        assert result is not None, "mov d4,d1 failed to encode"
        assert result.definition.opcode == '0x0002', \
            f"Wrong opcode: expected 0x0002 (MOV D[a], D[b]), got {result.definition.opcode}"
        assert result.hex_value == '0x1402', \
            f"Wrong encoding: expected 0x1402, got {result.hex_value}"
    
    def test_mov_immediate_variants(self):
        """Test that different immediate value ranges select appropriate variants"""
        test_cases = [
            # Small values (4-bit): use const4 variant
            ('mov d0,#0', '0x0082'),
            ('mov d0,#1', '0x1082'),
            ('mov d0,#15', '0xF082'),
            
            # Register-to-register: use D[a], D[b] variant
            ('mov d0,d1', '0x1002'),
            ('mov d4,d2', '0x2402'),
        ]
        
        for source, expected_hex in test_cases:
            parts = source.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, source, 1)
            result = self.encoder.encode_instruction(parsed)
            
            assert result is not None, f"{source} failed to encode"
            assert result.hex_value == expected_hex, \
                f"{source}: expected {expected_hex}, got {result.hex_value}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
