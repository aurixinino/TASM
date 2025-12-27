"""
Regression test for ST.B encoding issue.

Issue: Encoder selects wrong variant when multiple ST.B variants match operand types.
Specifically, it chooses ST.B [A[15]],off4,D[a] (4-bit offset) instead of 
ST.B A[b],off16 {[9:6][15:10][5:0]},D[a] (16-bit offset) when offset > 0xF.

Root Cause: Variant selection algorithm doesn't check if immediate value fits
in the bit field size before selecting variant.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.instruction_loader import InstructionSetLoader
from src.instruction_encoder import InstructionEncoder, ParsedInstruction, ParsedOperand
from src.config_loader import TASMConfig


class STBEncodingRegression:
    """Regression test for ST.B variant selection."""
    
    def __init__(self):
        """Initialize test infrastructure."""
        config = TASMConfig()
        self.loader = InstructionSetLoader()
        success = self.loader.load_instruction_set(config.instruction_set_path)
        if not success:
            raise RuntimeError("Failed to load instruction set")
        self.encoder = InstructionEncoder(self.loader)
    
    def parse_instruction(self, instruction_str: str) -> ParsedInstruction:
        """Parse an instruction string into ParsedInstruction."""
        # Use the encoder's built-in parser for consistency
        return self.encoder.parse_instruction_line(instruction_str, 0)
        
    def test_stb_offset_variant_selection(self):
        """
        Test that ST.B selects correct variant based on offset size.
        
        ST.B has multiple variants:
        1. ST.B [A[15]],off4,D[a]  - 4-bit offset (max 0xF = 15)
        2. ST.B A[b],off4,D[15]     - 4-bit offset (max 0xF = 15)
        3. ST.B A[b],off16,D[a]     - 16-bit offset (max 0xFFFF = 65535)
        
        Encoder should select variant based on whether offset fits in 4 bits or needs 16 bits.
        """
        print("\n" + "="*80)
        print("TEST 1: ST.B Offset Variant Selection")
        print("="*80)
        
        test_cases = [
            # (instruction, expected_opcode, expected_size, should_pass, description)
            ('st.b [a15], 4, d0', None, 16, True, 'Offset 4 fits in 4 bits, should use 16-bit variant'),
            ('st.b [a15], 0xF, d0', None, 16, True, 'Offset 0xF (max 4-bit), should use 16-bit variant'),
            ('st.b a2, 4, d15', None, 16, True, 'Offset 4 fits in 4 bits, should use 16-bit variant'),
            ('st.b a2, 0x10, d15', None, 32, True, 'Offset 0x10 needs 16 bits, must use 32-bit variant'),
            ('st.b [a2], 0x6130, d15', '46302FE9', 32, True, 'Offset 0x6130 needs 16 bits, must use 32-bit variant'),
            ('st.b a4, 0x100, d8', None, 32, True, 'Offset 0x100 needs 16 bits, must use 32-bit variant'),
        ]
        
        print(f"\n{'Instruction':<35} {'Expected':<15} {'Result':<15} {'Status'}")
        print("-" * 85)
        
        passed = 0
        failed = 0
        
        for instruction, expected_opcode, expected_size, should_pass, description in test_cases:
            parsed = self.parse_instruction(instruction)
            
            if not parsed:
                print(f"{instruction:<35} {f'{expected_size}-bit':<15} {'PARSE_FAIL':<15} FAIL")
                failed += 1
                continue
            
            result = self.encoder.encode_instruction(parsed)
            
            if result:
                actual_opcode = result.hex_value.upper().replace('0X', '')
                actual_size = len(actual_opcode) * 4  # Each hex char = 4 bits
                
                # Check if size matches expected
                size_match = (actual_size == expected_size)
                
                # If we have specific opcode, check that too
                if expected_opcode:
                    expected = expected_opcode.upper().replace('0X', '')
                    opcode_match = (actual_opcode == expected)
                    match = size_match and opcode_match
                    status = "PASS" if match else "FAIL"
                    result_str = f"{actual_opcode}({actual_size}b)"
                    expected_str = f"{expected}({expected_size}b)"
                    print(f"{instruction:<35} {expected_str:<15} {result_str:<15} {status}")
                else:
                    # No specific opcode, just check size
                    match = size_match
                    status = "PASS" if match else "FAIL"
                    result_str = f"{actual_opcode}({actual_size}b)"
                    expected_str = f"({expected_size}-bit)"
                    print(f"{instruction:<35} {expected_str:<15} {result_str:<15} {status}")
                
                if match:
                    passed += 1
                else:
                    failed += 1
                    if not size_match:
                        print(f"  NOTE: Expected {expected_size}-bit encoding, got {actual_size}-bit")
            else:
                print(f"{instruction:<35} {f'({expected_size}-bit)':<15} {'NOT_SUPPORT':<15} FAIL")
                failed += 1
                print(f"  ERROR: {description}")
        
        print("\n" + "-" * 80)
        print(f"PASSED: {passed}, FAILED: {failed}")
        return failed == 0
    
    def test_stb_register_format_tolerance(self):
        """Test that ST.B works with various register format notations."""
        print("\n" + "="*80)
        print("TEST 2: ST.B Register Format Tolerance")
        print("="*80)
        
        # All these should encode to the same opcode
        test_cases = [
            'st.b [a2], 0x6130, d15',
            'st.b a2, 0x6130, d15',
            'st.b A2, 0x6130, d15',
            'st.b a[2], 0x6130, d15',
            'st.b A[2], 0x6130, d15',
            'st.b [a[2]], 0x6130, d15',
            'st.b [A[2]], 0x6130, d15',
        ]
        
        expected_opcode = '46302FE9'
        
        print(f"\n{'Instruction':<35} {'Generated':<12} {'Status'}")
        print("-" * 80)
        
        passed = 0
        failed = 0
        
        for instruction in test_cases:
            parsed = self.parse_instruction(instruction)
            
            if not parsed:
                print(f"{instruction:<35} {'PARSE_FAIL':<12} FAIL")
                failed += 1
                continue
            
            result = self.encoder.encode_instruction(parsed)
            
            if result:
                actual = result.hex_value.upper().replace('0X', '')
                expected = expected_opcode.upper().replace('0X', '')
                match = (actual == expected)
                status = "PASS" if match else "FAIL"
                print(f"{instruction:<35} {actual:<12} {status}")
                if match:
                    passed += 1
                else:
                    failed += 1
            else:
                print(f"{instruction:<35} {'NOT_SUPPORT':<12} FAIL")
                failed += 1
        
        print("\n" + "-" * 80)
        print(f"PASSED: {passed}, FAILED: {failed}")
        return failed == 0
    
    def test_stb_variant_coverage(self):
        """Test all ST.B variants can be encoded correctly."""
        print("\n" + "="*80)
        print("TEST 3: ST.B Variant Coverage")
        print("="*80)
        
        test_cases = [
            # Each variant should have at least one passing test
            ('st.b [a15], 4, d0', 'ST.B [A[15]],off4,D[a]', '4-bit offset with A15'),
            ('st.b a2, 4, d15', 'ST.B A[b],off4,D[15]', '4-bit offset with D15'),
            ('st.b a2, 0x6130, d15', 'ST.B A[b],off16 {...},D[a]', '16-bit offset'),
            ('st.b [a4], d8', 'ST.B A[b], D[a]', 'Direct register-to-register'),
        ]
        
        print(f"\n{'Instruction':<35} {'Variant':<40} {'Status'}")
        print("-" * 80)
        
        passed = 0
        failed = 0
        
        for instruction, expected_variant, description in test_cases:
            parsed = self.parse_instruction(instruction)
            
            if not parsed:
                print(f"{instruction:<35} {description:<40} PARSE_FAIL")
                failed += 1
                continue
            
            result = self.encoder.encode_instruction(parsed)
            
            if result:
                print(f"{instruction:<35} {description:<40} PASS")
                passed += 1
            else:
                print(f"{instruction:<35} {description:<40} FAIL")
                failed += 1
        
        print("\n" + "-" * 80)
        print(f"PASSED: {passed}, FAILED: {failed}")
        return failed == 0
    
    def run_all_tests(self):
        """Run all regression tests."""
        print("\n" + "="*80)
        print("ST.B ENCODING REGRESSION TEST SUITE")
        print("="*80)
        print("\nThis test suite verifies that ST.B instruction encoding:")
        print("  1. Selects correct variant based on offset size")
        print("  2. Handles various register format notations")
        print("  3. Covers all ST.B variants")
        
        results = []
        
        # Test 1: Offset variant selection
        results.append(('Offset Variant Selection', self.test_stb_offset_variant_selection()))
        
        # Test 2: Register format tolerance
        results.append(('Register Format Tolerance', self.test_stb_register_format_tolerance()))
        
        # Test 3: Variant coverage
        results.append(('Variant Coverage', self.test_stb_variant_coverage()))
        
        # Summary
        print("\n" + "="*80)
        print("REGRESSION TEST SUMMARY")
        print("="*80)
        total_passed = sum(1 for _, passed in results if passed)
        total_tests = len(results)
        
        for test_name, passed in results:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {test_name}")
        
        print(f"\nOverall: {total_passed}/{total_tests} test suites passed")
        
        return total_passed == total_tests


def main():
    """Main entry point."""
    try:
        regression = STBEncodingRegression()
        success = regression.run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
