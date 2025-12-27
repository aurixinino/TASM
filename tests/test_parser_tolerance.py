"""
Test suite for tolerant assembler parser.

This test validates that the assembler parser correctly handles multiple
equivalent register notation formats:
- a2, A2 (plain notation)
- a[2], A[2] (bracket notation)
- [a2], [A2] (memory reference)
- [a[2]], [A[2]] (double bracket notation)

The parser should accept all formats as equivalent when matching instruction
syntax patterns.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.instruction_loader import InstructionSetLoader
from src.config_loader import TASMConfig


class ParserToleranceTest:
    def test_compound_operand_splitting(self):
        """Test splitting and extraction of compound operands like '[a15]14,d1'."""
        print("\n" + "="*80)
        print("TEST 5: Compound Operand Splitting")
        print("="*80)
        test_cases = [
            ('[a15]14,d1', ['a15', '14', 'd1']),
            ('d15,[a5]18', ['d15', 'a5', '18']),
            ('[a15]2,d15', ['a15', '2', 'd15']),
            ('d15,[a2]6', ['d15', 'a2', '6']),
        ]
        for input_str, expected in test_cases:
            result = self.loader.split_compound_operands(input_str)
            if result == expected:
                print(f"  ✓ '{input_str}' -> {result}")
                self.passed += 1
            else:
                print(f"  ✗ '{input_str}' -> Expected {expected}, got {result}")
                self.failed += 1
                print(f"  ✗ '{input_str}' -> Expected {expected}, got {result}")
                self.failed += 1
    
    def __init__(self):
        self.config = TASMConfig()
        self.loader = InstructionSetLoader()
        success = self.loader.load_instruction_set(self.config.instruction_set_path)
        if not success:
            raise RuntimeError("Failed to load instruction set")
        
        self.passed = 0
        self.failed = 0
        self.test_cases = []
    
    def test_register_extraction(self):
        """Test that _extract_register_info handles all notation formats."""
        print("\n" + "="*80)
        print("TEST 1: Register Extraction Tolerance")
        print("="*80)
        
        test_cases = [
            # (input, expected_type, expected_num)
            ('d4', 'D', 4),
            ('D4', 'D', 4),
            ('d[4]', 'D', 4),
            ('D[4]', 'D', 4),
            ('[d4]', 'D', 4),
            ('[D4]', 'D', 4),
            ('[d[4]]', 'D', 4),
            ('[D[4]]', 'D', 4),
            ('a15', 'A', 15),
            ('A15', 'A', 15),
            ('a[15]', 'A', 15),
            ('A[15]', 'A', 15),
            ('[a15]', 'A', 15),
            ('[A15]', 'A', 15),
            ('[a[15]]', 'A', 15),
            ('[A[15]]', 'A', 15),
            ('a2', 'A', 2),
            ('A2', 'A', 2),
            ('a[2]', 'A', 2),
            ('A[2]', 'A', 2),
            ('[a2]', 'A', 2),
            ('[A2]', 'A', 2),
            ('[a[2]]', 'A', 2),
            ('[A[2]]', 'A', 2),
        ]
        
        for operand, expected_type, expected_num in test_cases:
            reg_type, reg_num = self.loader._extract_register_info(operand)
            if reg_type == expected_type and reg_num == expected_num:
                print(f"  ✓ '{operand:<12}' -> {reg_type}[{reg_num}]")
                self.passed += 1
            else:
                print(f"  ✗ '{operand:<12}' -> Expected {expected_type}[{expected_num}], got {reg_type}[{reg_num}]")
                self.failed += 1
    
    def test_case_insensitivity(self):
        """Test that register matching is case-insensitive."""
        print("\n" + "="*80)
        print("TEST 2: Case Insensitivity")
        print("="*80)
        
        test_cases = [
            # (input, expected_type, expected_num)
            ('d0', 'D', 0),
            ('D0', 'D', 0),
            ('a10', 'A', 10),
            ('A10', 'A', 10),
            ('e2', 'E', 2),
            ('E2', 'E', 2),
        ]
        
        for operand, expected_type, expected_num in test_cases:
            reg_type, reg_num = self.loader._extract_register_info(operand)
            if reg_type == expected_type and reg_num == expected_num:
                print(f"  ✓ '{operand:<6}' -> {reg_type}[{reg_num}]")
                self.passed += 1
            else:
                print(f"  ✗ '{operand:<6}' -> Expected {expected_type}[{expected_num}], got {reg_type}[{reg_num}]")
                self.failed += 1
    
    def test_mixed_formats_equivalence(self):
        """Test that different formats for same register are recognized as equivalent."""
        print("\n" + "="*80)
        print("TEST 3: Format Equivalence")
        print("="*80)
        
        # Test groups - all formats in each group should extract to same register
        test_groups = [
            (['d15', 'D15', 'd[15]', 'D[15]', '[d15]', '[D15]', '[d[15]]', '[D[15]]'], 'D', 15),
            (['a2', 'A2', 'a[2]', 'A[2]', '[a2]', '[A2]', '[a[2]]', '[A[2]]'], 'A', 2),
            (['a0', 'A0', 'a[0]', 'A[0]', '[a0]', '[A0]', '[a[0]]', '[A[0]]'], 'A', 0),
        ]
        
        for formats, expected_type, expected_num in test_groups:
            print(f"\n  Register {expected_type}[{expected_num}] formats:")
            all_match = True
            for fmt in formats:
                reg_type, reg_num = self.loader._extract_register_info(fmt)
                if reg_type == expected_type and reg_num == expected_num:
                    print(f"    ✓ '{fmt:<12}' -> {reg_type}[{reg_num}]")
                else:
                    print(f"    ✗ '{fmt:<12}' -> Expected {expected_type}[{expected_num}], got {reg_type}[{reg_num}]")
                    all_match = False
            
            if all_match:
                self.passed += 1
            else:
                self.failed += 1
    
    def test_non_register_operands(self):
        """Test that non-register operands are not misidentified."""
        print("\n" + "="*80)
        print("TEST 4: Non-Register Operand Detection")
        print("="*80)
        
        test_cases = [
            # These should NOT be identified as registers
            '0x100',
            '256',
            '#10',
            'label',
            '[0x1000]',
        ]
        
        for operand in test_cases:
            reg_type, reg_num = self.loader._extract_register_info(operand)
            if reg_type is None and reg_num is None:
                print(f"  ✓ '{operand:<12}' -> Correctly identified as non-register")
                self.passed += 1
            else:
                print(f"  ✗ '{operand:<12}' -> Incorrectly identified as {reg_type}[{reg_num}]")
                self.failed += 1
    
    def run_all_tests(self):
        """Run all parser tolerance tests."""
        print("\n" + "="*80)
        print("TOLERANT ASSEMBLER PARSER TEST SUITE")
        print("="*80)
        print("\nTesting parser's ability to handle multiple register notation formats")
        
        self.test_register_extraction()
        self.test_case_insensitivity()
        self.test_mixed_formats_equivalence()
        self.test_non_register_operands()
        self.test_compound_operand_splitting()
        
        # Print summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n✓ All tests PASSED")
            return 0
        else:
            print(f"\n✗ {self.failed} test(s) FAILED")
            return 1


def main():
    """Main entry point for parser tolerance tests."""
    try:
        test = ParserToleranceTest()
        exit_code = test.run_all_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
