"""Test MOV.AA address register encoding to verify correct variant selection.

This test ensures that MOV.AA A[x], A[y] correctly selects the 16-bit variant
instead of incorrectly using the 32-bit variant.

Based on mismatch report showing:
  TASM: D0007001 (32-bit)  
  REF:  7D40 (16-bit)
  Source: mov.aa a13, a7
"""

import sys
from pathlib import Path

# Add parent src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import TASMConfig

# Load config
config = TASMConfig()

# Load instruction set
loader = InstructionSetLoader()
loader.load_instruction_set(config.instruction_set_path)

# Create encoder
encoder = InstructionEncoder(loader)

# Test cases from mismatch report
test_cases = [
    ("MOV.AA A15, A4", ["A15", "A4"], "0x4F40"),
    ("MOV.AA A13, A7", ["A13", "A7"], "0x7D40"),
    ("MOV.AA A4, A15", ["A4", "A15"], "0xF440"),
    ("MOV.AA A2, A5", ["A2", "A5"], "0x5240"),
    ("MOV.AA A12, A5", ["A12", "A5"], "0x5C40"),
]

print("=" * 80)
print("MOV.AA ADDRESS REGISTER ENCODING TEST")
print("=" * 80)

all_passed = True

for instr_text, operands, expected_hex in test_cases:
    print(f"\n[TEST] {instr_text}")
    print(f"  Expected: {expected_hex}")
    
    parsed = ParsedInstruction(
        mnemonic='MOV.AA',
        operands=operands,
        original_line=instr_text,
        line_number=1
    )
    
    encoded = encoder.encode_instruction(parsed)
    
    if encoded:
        actual_hex = encoded.hex_value
        actual_int = int(actual_hex, 16)
        expected_int = int(expected_hex, 16)
        
        print(f"  Generated: 0x{actual_int:04X}")
        
        if actual_int == expected_int:
            print(f"  [OK] CORRECT!")
        else:
            print(f"  [ERROR] WRONG! Expected 0x{expected_int:04X}")
            all_passed = False
    else:
        print(f"  [ERROR] Encoding failed!")
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("ALL TESTS PASSED!")
    sys.exit(0)
else:
    print("SOME TESTS FAILED!")
    sys.exit(1)
