"""
Diagnostic test for ST.B encoding issue.

This test investigates why ST.B instructions with large offsets are not encoding
despite matching the instruction format in the Excel file.

Expected: ST.B A[b],off16 {[9:6][15:10][5:0]},D[a]
Where:
- A[b] should match [a2], a[2], or A2
- off16 should support values up to 65535 (16-bit)
- D[a] should match d15

Reference opcode: 46302FE9
Test instruction: st.b [a2], 0x6130, d15
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.instruction_loader import InstructionSetLoader
from src.instruction_encoder import InstructionEncoder
from src.config_loader import TASMConfig


class STBEncodingDiagnostic:
    """Diagnostic test for ST.B encoding issues."""
    
    def __init__(self):
        self.config = TASMConfig()
        self.loader = InstructionSetLoader()
        success = self.loader.load_instruction_set(self.config.instruction_set_path)
        if not success:
            raise RuntimeError("Failed to load instruction set")
        
        self.encoder = InstructionEncoder(self.loader)
    
    def test_stb_variants_available(self):
        """Check what ST.B variants are available in the instruction set."""
        print("\n" + "="*80)
        print("TEST 1: Available ST.B Variants")
        print("="*80)
        
        stb_variants = [inst for inst in self.loader._instruction_list 
                       if inst.instruction.upper() == 'ST.B']
        
        print(f"\nFound {len(stb_variants)} ST.B variants:")
        for i, variant in enumerate(stb_variants, 1):
            print(f"\n{i}. Syntax: {variant.syntax}")
            print(f"   OpCode: {variant.opcode}")
            print(f"   Size: {variant.opcode_size}-bit")
            print(f"   Reference: {variant.reference}")
            print(f"   Operand count: {variant.operand_count}")
        
        return stb_variants
    
    def test_register_extraction(self):
        """Test register extraction for various formats."""
        print("\n" + "="*80)
        print("TEST 2: Register Extraction")
        print("="*80)
        
        test_operands = [
            'a2',
            'A2',
            'a[2]',
            'A[2]',
            '[a2]',
            '[A2]',
            '[a[2]]',
            '[A[2]]',
            'd15',
            'D15',
            'd[15]',
            'D[15]',
        ]
        
        print("\nTesting register extraction:")
        for operand in test_operands:
            reg_type, reg_num = self.loader._extract_register_info(operand)
            print(f"  '{operand:<12}' -> Type: {reg_type}, Num: {reg_num}")
    
    def test_instruction_lookup(self):
        """Test if ST.B instruction can be found with different syntaxes."""
        print("\n" + "="*80)
        print("TEST 3: Instruction Lookup")
        print("="*80)
        
        test_cases = [
            ('ST.B', ['a2', '0x6130', 'd15']),
            ('ST.B', ['A2', '0x6130', 'd15']),
            ('ST.B', ['a[2]', '0x6130', 'd15']),
            ('ST.B', ['A[2]', '0x6130', 'd15']),
            ('ST.B', ['[a2]', '0x6130', 'd15']),
            ('ST.B', ['[A2]', '0x6130', 'd15']),
            ('ST.B', ['[a[2]]', '0x6130', 'd15']),
            ('ST.B', ['[A[2]]', '0x6130', 'd15']),
        ]
        
        print("\nTesting instruction lookup with get_instruction_variants:")
        for mnemonic, operands in test_cases:
            variants = self.loader.get_instruction_variants(mnemonic)
            # Filter by operand count
            variants_with_3_ops = [v for v in variants if v.operand_count == len(operands)]
            operand_str = ', '.join(operands)
            print(f"\n  {mnemonic} {operand_str}")
            print(f"    Found {len(variants)} total variants, {len(variants_with_3_ops)} with 3 operands")
            
            if variants_with_3_ops:
                print(f"    Variants with 3 operands:")
                for variant in variants_with_3_ops:
                    print(f"      - {variant.syntax}")
    
    def test_offset_range(self):
        """Test if offset 0x6130 (24880 decimal) is within valid range."""
        print("\n" + "="*80)
        print("TEST 4: Offset Range Validation")
        print("="*80)
        
        offset_hex = 0x6130
        offset_dec = 24880
        
        print(f"\nOffset value:")
        print(f"  Hex: 0x{offset_hex:04X}")
        print(f"  Decimal: {offset_dec}")
        print(f"  Binary: {bin(offset_hex)[2:].zfill(16)}")
        print(f"  Bit length: {offset_hex.bit_length()} bits")
        
        print(f"\nFor 16-bit offset (off16):")
        print(f"  Max value: 65535 (0xFFFF)")
        print(f"  Test value: {offset_dec}")
        if offset_dec <= 65535:
            print(f"  ✓ Within range")
        else:
            print(f"  ✗ Out of range")
    
    def test_actual_encoding(self):
        """Test actual encoding with encoder."""
        print("\n" + "="*80)
        print("TEST 5: Actual Encoding Attempts")
        print("="*80)
        
        test_cases = [
            'st.b a2, 0x6130, d15',
            'st.b A2, 0x6130, d15',
            'st.b a[2], 0x6130, d15',
            'st.b A[2], 0x6130, d15',
            'st.b [a2], 0x6130, d15',
            'st.b [A2], 0x6130, d15',
            'st.b [a[2]], 0x6130, d15',
            'st.b [A[2]], 0x6130, d15',
            # Try with decimal
            'st.b a2, 24880, d15',
            # Try smaller offsets
            'st.b a2, 0x10, d15',
            'st.b a2, 0x100, d15',
            'st.b a2, 0x1000, d15',
        ]
        
        print("\nAttempting to encode:")
        print(f"{'Instruction':<35} {'Result':<20} {'Opcode'}")
        print("-" * 80)
        
        for test in test_cases:
            # Parse the instruction manually to see what's happening
            parts = test.split(None, 1)
            if len(parts) < 2:
                continue
            
            mnemonic = parts[0].upper()
            operands_str = parts[1]
            
            # Try to encode through the validation test's method
            from tests.test_encoder_validation import EncoderValidationTest
            validator = EncoderValidationTest(None, None)
            
            # Use parse_assembly_instruction to get ParsedInstruction
            parsed = validator.parse_assembly_instruction(operands_str, 0)
            
            if parsed:
                # Try to encode
                result = self.encoder.encode_instruction(parsed)
                if result:
                    print(f"{test:<35} {'✓ SUCCESS':<20} {result.hex_value}")
                else:
                    print(f"{test:<35} {'✗ FAILED':<20} Not supported")
            else:
                print(f"{test:<35} {'✗ PARSE ERROR':<20} Could not parse")
    
    def test_syntax_operand_types(self):
        """Test how syntax operand types are parsed."""
        print("\n" + "="*80)
        print("TEST 6: Syntax Operand Type Parsing")
        print("="*80)
        
        stb_variants = [inst for inst in self.loader._instruction_list 
                       if inst.instruction.upper() == 'ST.B']
        
        print("\nAnalyzing ST.B syntax patterns:")
        for i, variant in enumerate(stb_variants, 1):
            print(f"\n{i}. {variant.syntax}")
            
            # Try to parse the operand types from syntax
            operand_types = variant._parse_syntax_operand_types()
            print(f"   Parsed operand types: {operand_types}")
            
            # Check if it would match our test case
            test_operands = ['[a2]', '0x6130', 'd15']
            print(f"   Testing match with: {test_operands}")
            
            if len(operand_types) == len(test_operands):
                print(f"   ✓ Operand count matches ({len(operand_types)})")
                for j, (expected, actual) in enumerate(zip(operand_types, test_operands)):
                    print(f"     Operand {j+1}: expected type '{expected}', got '{actual}'")
            else:
                print(f"   ✗ Operand count mismatch: expected {len(operand_types)}, got {len(test_operands)}")
    
    def run_diagnostics(self):
        """Run all diagnostic tests."""
        print("\n" + "="*80)
        print("ST.B ENCODING DIAGNOSTIC TEST")
        print("="*80)
        print("\nInvestigating why: st.b [a2], 0x6130, d15")
        print("Expected opcode: 46302FE9")
        print("Expected format: ST.B A[b],off16 {[9:6][15:10][5:0]},D[a]")
        
        self.test_stb_variants_available()
        self.test_register_extraction()
        self.test_instruction_lookup()
        self.test_offset_range()
        self.test_syntax_operand_types()
        self.test_actual_encoding()
        
        print("\n" + "="*80)
        print("DIAGNOSTIC COMPLETE")
        print("="*80)


def main():
    """Main entry point."""
    try:
        diagnostic = STBEncodingDiagnostic()
        diagnostic.run_diagnostics()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
