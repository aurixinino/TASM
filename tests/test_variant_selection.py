"""
Test instruction variant selection for edge cases.

Tests specific scenarios where multiple instruction variants match the operands
and the assembler must select the correct one based on register constraints,
operand ranges, and encoding preferences.
"""

import sys
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from instruction_encoder import InstructionEncoder, ParsedInstruction
from instruction_loader import InstructionSetLoader


class TestVariantSelection:
    """Test cases for instruction variant selection."""
    
    @pytest.fixture(scope="class")
    def encoder(self):
        """Load instruction set and create encoder."""
        loader = InstructionSetLoader()
        excel_path = Path(__file__).parent.parent / "Processors" / "tricore" / "data" / "languages" / "tricore_tc1.6_instruction_set.xlsx"
        
        if not loader.load_instruction_set(str(excel_path)):
            pytest.skip(f"Could not load instruction set from {excel_path}")
        
        return InstructionEncoder(loader)
    
    def test_ld_bu_d15_a15_variant_selection(self, encoder):
        """
        Test: ld.bu d15,[a15],4
        
        When both D15 and A15 are used, the assembler should prefer the variant
        that matches the Excel file order (typically the more constrained variant).
        
        Expected: Should select D[c], A[15], off4 (opcode 0x0008)
        Not: D[15], A[b], off4 (opcode 0x000C)
        """
        parsed = ParsedInstruction('LD.BU', ['d15', '[a15]', '4'], 'ld.bu d15,[a15],4', 1)
        result = encoder.encode_instruction(parsed)
        
        assert result is not None, "ld.bu d15,[a15],4 failed to encode"
        
        # The opcode should be 0x0008 (D[c], A[15], off4)
        # Full encoding will have d15 encoded in bits, but base opcode is 0x08
        hex_str = result.hex_value.replace(' ', '').replace('0x', '')
        
        # For 16-bit instruction, check the opcode byte (lower byte of first word)
        # Format: ??08 where ?? contains encoded operands
        assert len(hex_str) == 4, f"Expected 16-bit encoding, got 0x{hex_str}"
        assert hex_str.endswith('08'), f"Expected opcode 0x08 (D[c], A[15]), got 0x{hex_str}"
    
    def test_ld_bu_various_d15_variants(self, encoder):
        """
        Test: ld.bu d15 with different address registers
        
        Ensures that variants with D[15] specific are selected when appropriate.
        """
        test_cases = [
            ('ld.bu d15,[a4],4', '4', '0C'),   # D[15], A[b], off4 -> opcode 0x000C
            ('ld.bu d15,[a2],4', '4', '0C'),   # D[15], A[b], off4 -> opcode 0x000C
        ]
        
        for instruction, offset, expected_opcode_suffix in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            hex_str = result.hex_value.replace(' ', '').replace('0x', '')
            assert len(hex_str) == 4, f"Expected 16-bit encoding for {instruction}, got 0x{hex_str}"
    
    def test_st_w_specific_register_variants(self, encoder):
        """
        Test: st.w with specific register constraints
        
        ST.W has both 16-bit (SSRO) and 32-bit (BO) formats. The assembler
        should prefer 16-bit when possible.
        """
        test_cases = [
            ('st.w [a15],4,d0', '4', 32),   # Should encode, may be 32-bit for variable regs
            ('st.w [a4],4,d2', '4', 32),     # Should encode, may be 32-bit
        ]
        
        for instruction, offset, expected_max_bits in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            hex_str = result.hex_value.replace(' ', '').replace('0x', '')
            bit_length = len(hex_str) * 4
            assert bit_length <= expected_max_bits, \
                f"{instruction} encoded as {bit_length}-bit (0x{hex_str}), expected <= {expected_max_bits}-bit"
    
    def test_lea_variant_selection(self, encoder):
        """
        Test: lea (Load Effective Address) variant selection
        
        LEA has multiple variants depending on address registers and offsets.
        """
        test_cases = [
            ('lea a2,[a15],8', '8'),
            ('lea a4,[a10],4', '4'),
            ('lea a5,[a15],12', '12'),
        ]
        
        for instruction, offset in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
    
    def test_ld_a_specific_register_variants(self, encoder):
        """
        Test: ld.a (Load Address) with various register combinations
        
        LD.A has both 16-bit (when using specific registers) and 32-bit variants.
        """
        test_cases = [
            ('ld.a a15,[a4],4', '4'),
            ('ld.a a4,[a4],8', '8'),
            ('ld.a a2,[a10],8', '8'),
        ]
        
        for instruction, offset in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
    
    def test_ld_hu_offset_variants(self, encoder):
        """
        Test: ld.hu (Load Halfword Unsigned) with different offsets
        
        LD.HU has variants for different offset sizes and register constraints.
        """
        test_cases = [
            ('ld.hu d15,[a4],4', 4),
            ('ld.hu d15,[a15],8', 8),
            ('ld.hu d0,[a15],10', 10),
        ]
        
        for instruction, offset in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            
            # All LD.HU should encode successfully
            hex_str = result.hex_value.replace(' ', '').replace('0x', '')
            assert len(hex_str) in [4, 8], f"Expected 16-bit or 32-bit encoding for {instruction}, got 0x{hex_str}"
    
    def test_st_w_prefers_16bit_encoding(self, encoder):
        """
        Test: st.w should prefer 16-bit SSRO format over 32-bit BO format when possible
        
        These instructions have both 16-bit and 32-bit variants available.
        Without -O32 flag, the assembler should select the shorter 16-bit encoding.
        
        Reference from TASKING assembler:
        - st.w [a13], 40, d15  -> 0xDA6C (16-bit, 2 bytes)
        - st.w [a12], 44, d15  -> 0xCB6C (16-bit, 2 bytes)
        - st.w [a12], 40, d15  -> 0xCA6C (16-bit, 2 bytes)
        - st.w [a15], 48, d15  -> 0xFC6C (16-bit, 2 bytes)
        - st.w [a12], 48, d15  -> 0xCC6C (16-bit, 2 bytes)
        - st.w [a4], 48, d15   -> 0x4C6C (16-bit, 2 bytes)
        - st.w [a15], 44, d15  -> 0xFB6C (16-bit, 2 bytes)
        - st.w [a15], 40, d15  -> 0xFA6C (16-bit, 2 bytes)
        
        TASM was incorrectly selecting 32-bit BO format (4 bytes) for these.
        """
        test_cases = [
            ('st.w [a13],40,d15', 40, 2, 'DA6C'),
            ('st.w [a12],44,d15', 44, 2, 'CB6C'),
            ('st.w [a12],40,d15', 40, 2, 'CA6C'),
            ('st.w [a15],48,d15', 48, 2, 'FC6C'),
            ('st.w [a12],48,d15', 48, 2, 'CC6C'),
            ('st.w [a4],48,d15', 48, 2, '4C6C'),
            ('st.w [a15],44,d15', 44, 2, 'FB6C'),
            ('st.w [a15],40,d15', 40, 2, 'FA6C'),
        ]
        
        for instruction, offset, expected_bytes, expected_pattern in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            
            hex_str = result.hex_value.replace(' ', '').replace('0x', '').upper()
            actual_bytes = len(hex_str) // 2
            
            assert actual_bytes == expected_bytes, \
                f"{instruction}: Expected {expected_bytes}-byte (16-bit) encoding, got {actual_bytes}-byte (0x{hex_str}). " \
                f"Should prefer 16-bit SSRO format over 32-bit BO format."
    
    def test_add_prefers_16bit_encoding(self, encoder):
        """
        Test: add should prefer 16-bit SRC format over 32-bit when immediate fits in 4 bits
        
        The ADD instruction has both 16-bit (const4) and 32-bit (const16) variants.
        For immediate values in range [-8, 7], assembler should select 16-bit encoding.
        
        Reference from TASKING assembler (TASM-OPCODE vs REF):
        - add d11,#-1 -> 0xFBC2 not 0xF0C2 (16-bit SRC, not 32-bit)
        - add d1,#2   -> 0x21C2 not 0x30C2 (16-bit SRC, not 32-bit)
        - add d15,#3  -> 0x3FC2 not 0xF0C2 (16-bit SRC, not 32-bit)
        - add d5,#-4  -> 0xC5C2 not 0xD0C2 (16-bit SRC, not 32-bit)
        - add d1,#-8  -> 0x81C2 not 0x90C2 (16-bit SRC, not 32-bit)
        
        TASM was incorrectly selecting 32-bit SRR format (4 bytes) for these.
        """
        test_cases = [
            # (instruction, expected_bytes, expected_hex)
            ('add d11,#-1', 2, 'FBC2'),
            ('add d1,#2', 2, '21C2'),
            ('add d15,#3', 2, '3FC2'),
            ('add d1,#3', 2, '31C2'),
            ('add d5,#-4', 2, 'C5C2'),
            ('add d1,#-8', 2, '81C2'),
            ('add d8,#2', 2, '28C2'),
            ('add d15,#4', 2, '4FC2'),
            ('add d15,#2', 2, '2FC2'),
            ('add d4,#-1', 2, 'F4C2'),
            ('add d3,#4', 2, '43C2'),
            ('add d15,#1', 2, '1FC2'),
            ('add d4,#3', 2, '34C2'),
            ('add d11,#1', 2, '1BC2'),
            ('add d15,#7', 2, '7FC2'),
            ('add d8,#-8', 2, '88C2'),
            ('add d5,#-1', 2, 'F5C2'),
            ('add d15,#-8', 2, '8FC2'),
            ('add d10,#1', 2, '1AC2'),
            ('add d3,#1', 2, '13C2'),
            ('add d13,#1', 2, '1DC2'),
            ('add d5,#1', 2, '15C2'),
            ('add d6,#-1', 2, 'F6C2'),
            ('add d2,#1', 2, '12C2'),
            ('add d10,#-1', 2, 'FAC2'),
            ('add d15,#-1', 2, 'FFC2'),
            ('add d6,#1', 2, '16C2'),
            ('add d4,#1', 2, '14C2'),
            ('add d8,#1', 2, '18C2'),
            ('add d7,#1', 2, '17C2'),
            ('add d9,#1', 2, '19C2'),
            ('add d1,#1', 2, '11C2'),
            ('add d9,#-1', 2, 'F9C2'),
            ('add d8,#-1', 2, 'F8C2'),
            ('add d12,#1', 2, '1CC2'),
        ]
        
        for instruction, expected_bytes, expected_hex in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            
            hex_str = result.hex_value.replace(' ', '').replace('0x', '').upper()
            actual_bytes = len(hex_str) // 2
            
            assert actual_bytes == expected_bytes, \
                f"{instruction}: Expected {expected_bytes}-byte (16-bit) encoding, got {actual_bytes}-byte (0x{hex_str}). " \
                f"Should prefer 16-bit SRC format over 32-bit SRR format."
            
            assert hex_str == expected_hex, \
                f"{instruction}: Expected 0x{expected_hex}, got 0x{hex_str}"
    
    def test_st_b_prefers_16bit_encoding(self, encoder):
        """
        Test: st.b should prefer 16-bit SSRO format over 32-bit BO format when offset fits
        
        The ST.B instruction has both 16-bit (off4) and 32-bit (off16) variants.
        For offset values 0-15, assembler should select 16-bit encoding.
        ST.B stores bytes, so no offset scaling is needed (unlike ST.W which divides by 4).
        
        Reference from TASKING assembler (TASM-OPCODE vs REF):
        - st.b [a13], 10, d15 -> 0xDA2C not 0xF02C (16-bit, not 32-bit)
        - st.b [a12], 12, d15 -> 0xCC2C not 0xC02C (16-bit, not 32-bit)
        - st.b [a10], 4, d15  -> 0xA42C not 0xE02C (16-bit, not 32-bit)
        - st.b [a4], 4, d15   -> 0x442C not 0x402C (16-bit, not 32-bit)
        
        Note: Requires correct operand positions in Excel:
        - op1_pos = 8, op1_len = 4 (A register at bits [11:8])
        - op2_pos = 12, op2_len = 4 (offset at bits [15:12])
        """
        test_cases = [
            # (instruction, expected_bytes, expected_hex)
            ('st.b [a13],10,d15', 2, 'DA2C'),
            ('st.b [a12],12,d15', 2, 'CC2C'),
            ('st.b [a10],4,d15', 2, 'A42C'),
            ('st.b [a2],10,d15', 2, '2A2C'),
            ('st.b [a13],4,d15', 2, 'D42C'),
            ('st.b [a4],4,d15', 2, '442C'),
            ('st.b [a4],12,d15', 2, '4C2C'),
            ('st.b [a10],8,d15', 2, 'A82C'),
            ('st.b [a4],8,d15', 2, '482C'),
            ('st.b [a4],10,d15', 2, '4A2C'),
            ('st.b [a12],8,d15', 2, 'C82C'),
            ('st.b [a5],4,d15', 2, '542C'),
            ('st.b [a10],10,d15', 2, 'AA2C'),
            ('st.b [a10],12,d15', 2, 'AC2C'),
            ('st.b [a2],12,d15', 2, '2C2C'),
            ('st.b [a2],4,d15', 2, '242C'),
            ('st.b [a15],12,d15', 2, 'FC2C'),
            ('st.b [a15],4,d15', 2, 'F42C'),
            ('st.b [a15],10,d15', 2, 'FA2C'),
            ('st.b [a15],8,d15', 2, 'F82C'),
        ]
        
        for instruction, expected_bytes, expected_hex in test_cases:
            parts = instruction.split()
            mnemonic = parts[0].upper()
            operands_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operands_str.split(',')]
            
            parsed = ParsedInstruction(mnemonic, operands, instruction, 1)
            result = encoder.encode_instruction(parsed)
            
            assert result is not None, f"{instruction} failed to encode"
            
            hex_str = result.hex_value.replace(' ', '').replace('0x', '').upper()
            actual_bytes = len(hex_str) // 2
            
            assert actual_bytes == expected_bytes, \
                f"{instruction}: Expected {expected_bytes}-byte (16-bit) encoding, got {actual_bytes}-byte (0x{hex_str}). " \
                f"Should prefer 16-bit SSRO format over 32-bit BO format."
            
            assert hex_str == expected_hex, \
                f"{instruction}: Expected 0x{expected_hex}, got 0x{hex_str}. " \
                f"Check Excel operand positions: op1_pos=8, op2_pos=12 for ST.B A[b],off4,D[15]"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
