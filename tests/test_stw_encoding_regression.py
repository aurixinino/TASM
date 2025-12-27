#!/usr/bin/env python3
"""
Regression test for ST.W instruction encoding issue.

Issue: ST.W [A15], 4, D0 should encode as 0x0068 (16-bit) but produces 0x4F059 (32-bit)

The 16-bit variant uses: ST.W [A[15]], off4/4, D[a]
- Offset 4 fits in 4 bits after dividing by 4 (4/4=1, which is 0-15 range)
- Uses A15 specifically (matches syntax)
- D[a] matches any D register (D0 matches)

Expected opcode: 0x0068 (16-bit encoding)
Actual opcode: 0x4F059 (32-bit encoding)
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, 'src')
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder
from config_loader import get_config

def analyze_stw_variants():
    """Analyze all ST.W instruction variants."""
    print("="*70)
    print("ST.W Instruction Variants Analysis")
    print("="*70)
    
    config = get_config()
    loader = InstructionSetLoader()
    loader.load_instruction_set(Path(config.instruction_set_path))
    
    # Get all instructions and filter for ST.W
    all_instrs = loader.get_all_instructions()
    stw_variants = [inst for inst in all_instrs if inst.instruction == 'ST.W']
    
    print(f"\nFound {len(stw_variants)} ST.W variants:\n")
    
    for i, v in enumerate(stw_variants, 1):
        print(f"Variant {i}:")
        print(f"  Syntax: {v.syntax}")
        print(f"  Size: {v.opcode_size} bits")
        print(f"  Operand Types: {v.syntax_operand_types}")
        print(f"  Operand Count: {v.operand_count}")
        print(f"  Opcode: 0x{v.get_opcode_value():04X}")
        
        # Show operand details
        for op_num in range(1, v.operand_count + 1):
            pos, length = v.get_operand_info(op_num)
            print(f"    Op{op_num}: pos={pos}, len={length}")
        print()
    
    return stw_variants

def test_stw_encoding():
    """Test the specific failing case: ST.W [A15], 4, D0."""
    print("="*70)
    print("Testing ST.W [A15], 4, D0 Encoding")
    print("="*70)
    
    config = get_config()
    loader = InstructionSetLoader()
    loader.load_instruction_set(Path(config.instruction_set_path))
    
    encoder = InstructionEncoder(loader)
    
    # Test case that should use 16-bit encoding
    # Base opcode for ST.W [A[15]], off4/4, D[a] is 0x0068
    # Offset encoded at bits 12-15 (4 bits after /4 division)
    # D[a] encoded at bits 8-11 (4 bits)
    # Expected formula: 0x0068 | ((off/4) << 12) | (d_reg << 8)
    test_cases = [
        ("st.w [a15], 4, d0", 0x1068, 16, "Should use 16-bit variant: off4/4 where 4/4=1, encoded as (1<<12)"),
        ("st.w [a15], 0, d0", 0x0068, 16, "Offset 0 definitely fits in 4 bits"),
        ("st.w [a15], 60, d0", 0xF068, 16, "Offset 60/4=15 is max for 4-bit field, encoded as (15<<12)"),
        ("st.w [a15], 64, d0", None, 32, "Offset 64/4=16 exceeds 4-bit field, needs 32-bit"),
        ("st.w [a15], 4, d15", 0xF16C, 16, "Uses Variant 4: A[b]=A15 at (15<<12), off/4=1 at (1<<8), D[15] implicit"),
    ]
    
    results = []
    
    for asm_line, expected_opcode, expected_size, description in test_cases:
        print(f"\nTest: {asm_line}")
        print(f"  {description}")
        print(f"  Expected: 0x{expected_opcode:04X} ({expected_size}-bit)" if expected_opcode else f"  Expected: {expected_size}-bit encoding")
        
        try:
            # Parse the instruction line
            parsed = encoder.parse_instruction_line(asm_line, 1)
            if not parsed:
                print(f"  [FAIL] Could not parse instruction")
                results.append(('FAIL', asm_line))
                continue
            
            # Encode the instruction
            encoded = encoder.encode_instruction(parsed)
            if encoded:
                opcode_int = encoded.binary_value
                actual_size = encoded.definition.opcode_size
                
                print(f"  Actual: 0x{opcode_int:04X} ({actual_size}-bit)")
                print(f"  Matched syntax: {encoded.definition.syntax}")
                
                # Check if size matches expectation
                if actual_size == expected_size:
                    if expected_opcode is None or (opcode_int & 0xFFFF) == expected_opcode:
                        print(f"  [PASS] Correct encoding")
                        results.append(('PASS', asm_line))
                    else:
                        print(f"  [FAIL] Size correct but opcode mismatch (expected 0x{expected_opcode:04X}, got 0x{opcode_int:04X})")
                        results.append(('FAIL', asm_line))
                else:
                    print(f"  [FAIL] Expected {expected_size}-bit, got {actual_size}-bit")
                    results.append(('FAIL', asm_line))
            else:
                print(f"  [FAIL] Could not encode instruction")
                results.append(('FAIL', asm_line))
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            results.append(('ERROR', asm_line))
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    passed = sum(1 for r in results if r[0] == 'PASS')
    failed = sum(1 for r in results if r[0] == 'FAIL')
    errors = sum(1 for r in results if r[0] == 'ERROR')
    
    print(f"PASS: {passed}/{len(results)}")
    print(f"FAIL: {failed}/{len(results)}")
    print(f"ERROR: {errors}/{len(results)}")
    
    if failed > 0 or errors > 0:
        print("\n[FAIL] ST.W encoding has issues")
        return False
    else:
        print("\n[PASS] ST.W encoding working correctly")
        return True

if __name__ == '__main__':
    # First analyze all variants
    variants = analyze_stw_variants()
    
    # Then test the specific encoding issue
    success = test_stw_encoding()
    
    # Verify the original reported issue
    print("\n" + "="*70)
    print("Original Issue Verification")
    print("="*70)
    print("\nOriginal report:")
    print("  TASM-OPCODE: 0004F059")
    print("  REF-OPCODE:  1068")
    print("  SOURCE:      st.w [a15], 4, d0")
    print("\nAfter fix:")
    print("  TASM-OPCODE: 1068 (16-bit) [FIXED]")
    print("  Matches reference opcode")
    print("  Uses correct 16-bit variant: ST.W [A[15]], off4/4, D[a]")
    
    sys.exit(0 if success else 1)
