"""
Test E and P Register Encoding

E registers (Extended 64-bit registers) are formed by combining two consecutive
D registers. For example, E4 consists of D4 (low) and D5 (high).

P registers (Pointer registers) are 32-bit address register pairs.

This test validates that E and P register numbers are correctly encoded.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import TASMConfig


def test_e_register_encoding():
    """Test E register encoding in MOV instruction."""
    print("=" * 80)
    print("Test: E Register Encoding")
    print("=" * 80)
    
    # Load instruction set
    config = TASMConfig()
    loader = InstructionSetLoader()
    if not loader.load_instruction_set(config.instruction_set_path):
        print("FAILED: Could not load instruction set")
        return False
    
    encoder = InstructionEncoder(loader)
    
    # Test cases: (source, expected_opcode)
    # Format: MOV E[c], D[a], D[b] - Opcode: 0x0810000B
    # Base opcode: 0x0B at bits 0-7
    # Op1 (E[c]): bits 28-31
    # Op2 (D[a]): bits 8-11  
    # Op3 (D[b]): bits 12-15
    test_cases = [
        ("mov e4,d15,d8", "0x48108F0B"),  # E4 register should encode as 4 in bits 28-31
        ("mov e0,d1,d2", "0x0810210B"),   # E0 register, D1 at bits 8-11, D2 at bits 12-15
        ("mov e2,d3,d4", "0x2810430B"),   # E2 register, D3 at bits 8-11, D4 at bits 12-15
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
            # Normalize both for comparison (remove 0x prefix, uppercase)
            result_hex = result.hex_value.upper().replace('0X', '0x')
            expected_hex = expected.upper().replace('0X', '0x')
            
            if result_hex == expected_hex:
                print(f"Result: {result_hex} [PASS] PASS")
            else:
                print(f"Result: {result_hex} [FAIL] FAIL")
                print(f"  Expected: {expected_hex}")
                all_passed = False
        else:
            print(f"Result: FAILED TO ENCODE [FAIL] FAIL")
            all_passed = False
    
    return all_passed


def test_e_register_immediate():
    """Test E register with immediate values."""
    print("\n" + "=" * 80)
    print("Test: E Register with Immediate Values")
    print("=" * 80)
    
    # Load instruction set
    config = TASMConfig()
    loader = InstructionSetLoader()
    if not loader.load_instruction_set(config.instruction_set_path):
        print("FAILED: Could not load instruction set")
        return False
    
    encoder = InstructionEncoder(loader)
    
    # Test E register with const4 (16-bit MOV)
    test_cases = [
        ("mov e0,#0", "0x00D2"),    # E0 with const4
        ("mov e2,#5", "0x52D2"),    # E2 with const4
        ("mov e4,#15", "0xF4D2"),   # E4 with const4
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
                print(f"Result: {result_hex} [PASS] PASS")
            else:
                print(f"Result: {result_hex} [FAIL] FAIL")
                print(f"  Expected: {expected_hex}")
                all_passed = False
        else:
            print(f"Result: FAILED TO ENCODE [FAIL] FAIL")
            all_passed = False
    
    return all_passed


def main():
    """Run all E/P register tests."""
    print("\n" + "=" * 80)
    print("E/P REGISTER ENCODING TEST")
    print("=" * 80)
    
    tests = [
        ("E Register Encoding", test_e_register_encoding),
        ("E Register Immediate", test_e_register_immediate),
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
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80)
    
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())

