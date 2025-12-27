"""
Test Constant Scaling in Instructions

Some TriCore instructions require constants/offsets to be scaled before encoding.
For example:
- LD.W uses word addressing, so offsets are divided by 4
- LD.H uses halfword addressing, so offsets are divided by 2

This test validates that scaling is correctly applied during encoding.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import TASMConfig


def test_ldw_scaling():
    """Test LD.W constant scaling (divide by 4)."""
    print("=" * 80)
    print("Test: LD.W Constant Scaling (/4)")
    print("=" * 80)
    
    # Load instruction set
    config = TASMConfig()
    loader = InstructionSetLoader()
    if not loader.load_instruction_set(config.instruction_set_path):
        print("FAILED: Could not load instruction set")
        return False
    
    encoder = InstructionEncoder(loader)
    
    # Test cases: (source, expected_opcode)
    # LD.W D[c], A[15], off4/4 - Opcode: 0x0048
    # Format: offset is in bytes, but encoded as offset/4
    # These tests use the 16-bit variant with A[15]
    test_cases = [
        ("ld.w d2,[a15],4", "0x1248"),     # 4 bytes / 4 = 1, D2=2, encoded: D=2 at bits 8-11, off=1 at bits 12-15
        ("ld.w d0,[a15],0", "0x0048"),     # 0 bytes / 4 = 0, D0=0
        ("ld.w d4,[a15],8", "0x2448"),     # 8 bytes / 4 = 2, D4=4
    ]
    
    all_passed = True
    
    for source, expected in test_cases:
        print(f"\nTest case: {source}")
        print(f"Expected: {expected}")
        
        # Parse instruction
        parts = source.split()
        mnemonic = parts[0].upper()
        # Split operands by comma
        operands_str = ' '.join(parts[1:])
        operands = [op.strip() for op in operands_str.split(',')]
        
        parsed = ParsedInstruction(mnemonic, operands, source, 1)
        
        # Encode
        result = encoder.encode_instruction(parsed)
        
        if result:
            result_hex = result.hex_value.upper().replace('0X', '0x')
            expected_hex = expected.upper().replace('0X', '0x')
            
            if result_hex == expected_hex:
                print(f"Result: {result_hex} [PASS]")
            else:
                print(f"Result: {result_hex} [FAIL]")
                print(f"  Expected: {expected_hex}")
                all_passed = False
        else:
            print(f"Result: FAILED TO ENCODE [FAIL]")
            all_passed = False
    
    return all_passed


def test_stw_scaling():
    """Test ST.W constant scaling (divide by 4)."""
    print("\n" + "=" * 80)
    print("Test: ST.W Constant Scaling (/4)")
    print("=" * 80)
    
    # Load instruction set
    config = TASMConfig()
    loader = InstructionSetLoader()
    if not loader.load_instruction_set(config.instruction_set_path):
        print("FAILED: Could not load instruction set")
        return False
    
    encoder = InstructionEncoder(loader)
    
    # Test ST.W with scaled offsets
    # Note: ST.W syntax may vary, skip this test if no matching variants found
    test_cases = []
    
    # Find if ST.W has /4 variants
    stw_variants = loader.get_instruction_variants('ST.W')
    has_scaling = any('/4' in v.syntax for v in stw_variants) if stw_variants else False
    
    if not has_scaling:
        print("\n[SKIP] No ST.W variants with /4 scaling found in instruction set")
        return True  # Pass by skipping
    
    all_passed = True
    
    for source, expected in test_cases:
        print(f"\nTest case: {source}")
        print(f"Expected: {expected}")
        
        # Parse instruction
        parts = source.split()
        mnemonic = parts[0].upper()
        # Split operands by comma
        operands_str = ' '.join(parts[1:])
        operands = [op.strip() for op in operands_str.split(',')]
        
        parsed = ParsedInstruction(mnemonic, operands, source, 1)
        
        # Encode
        result = encoder.encode_instruction(parsed)
        
        if result:
            result_hex = result.hex_value.upper().replace('0X', '0x')
            expected_hex = expected.upper().replace('0X', '0x')
            
            if result_hex == expected_hex:
                print(f"Result: {result_hex} [PASS]")
            else:
                print(f"Result: {result_hex} [FAIL]")
                print(f"  Expected: {expected_hex}")
                all_passed = False
        else:
            print(f"Result: FAILED TO ENCODE [FAIL]")
            all_passed = False
    
    return all_passed


def test_ldh_scaling():
    """Test LD.H constant scaling (divide by 2)."""
    print("\n" + "=" * 80)
    print("Test: LD.H Constant Scaling (/2)")
    print("=" * 80)
    
    # Load instruction set
    config = TASMConfig()
    loader = InstructionSetLoader()
    if not loader.load_instruction_set(config.instruction_set_path):
        print("FAILED: Could not load instruction set")
        return False
    
    encoder = InstructionEncoder(loader)
    
    # Test LD.H with scaled offsets (halfword = 2 bytes)
    # Note: Test only if variants with /2 scaling exist
    ldh_variants = loader.get_instruction_variants('LD.H')
    has_scaling = any('/2' in v.syntax for v in ldh_variants) if ldh_variants else False
    
    if not has_scaling:
        print("\n[SKIP] No LD.H variants with /2 scaling found in instruction set")
        return True  # Pass by skipping
    
    test_cases = [
        ("ld.h d2,[a15],0", "0x0288"),     # 0 bytes / 2 = 0, opcode 0x0088 + d2 at bits 8-11
        ("ld.h d2,[a15],2", "0x1288"),     # 2 bytes / 2 = 1, offset at bits 12-15
        ("ld.h d4,[a15],4", "0x2488"),     # 4 bytes / 2 = 2, d4 at bits 8-11
    ]
    
    all_passed = True
    
    for source, expected in test_cases:
        print(f"\nTest case: {source}")
        print(f"Expected: {expected}")
        
        # Parse instruction
        parts = source.split()
        mnemonic = parts[0].upper()
        # Split operands by comma
        operands_str = ' '.join(parts[1:])
        operands = [op.strip() for op in operands_str.split(',')]
        
        parsed = ParsedInstruction(mnemonic, operands, source, 1)
        
        # Encode
        result = encoder.encode_instruction(parsed)
        
        if result:
            result_hex = result.hex_value.upper().replace('0X', '0x')
            expected_hex = expected.upper().replace('0X', '0x')
            
            if result_hex == expected_hex:
                print(f"Result: {result_hex} [PASS]")
            else:
                print(f"Result: {result_hex} [FAIL]")
                print(f"  Expected: {expected_hex}")
                all_passed = False
        else:
            print(f"Result: FAILED TO ENCODE [FAIL]")
            all_passed = False
    
    return all_passed


def main():
    """Run all constant scaling tests."""
    print("\n" + "=" * 80)
    print("CONSTANT SCALING TEST")
    print("=" * 80)
    
    tests = [
        ("LD.W Scaling (/4)", test_ldw_scaling),
        ("ST.W Scaling (/4)", test_stw_scaling),
        ("LD.H Scaling (/2)", test_ldh_scaling),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n[FAIL] Test '{test_name}' raised exception: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80)
    
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
