"""Test MOV register-to-register encoding to verify correct variant selection.

This test ensures that MOV D15, D5 correctly selects the MOV D[a], D[b] variant
instead of incorrectly treating D5 as a constant and selecting MOV D[15], const8.
"""

import sys
from pathlib import Path

# Add parent src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction

# Load config
from config_loader import TASMConfig
config = TASMConfig()

# Load instruction set
loader = InstructionSetLoader()
loader.load_instruction_set(config.instruction_set_path)

# Create encoder
encoder = InstructionEncoder(loader)

# Test MOV D15, D5
parsed = ParsedInstruction(
    mnemonic='MOV',
    operands=['D15', 'D5'],
    original_line='MOV D15, D5',
    line_number=1
)

print(f"[TEST] Encoding: {parsed.original_line}")

# Encode
encoded = encoder.encode_instruction(parsed)

if encoded:
    actual_hex = encoded.hex_value
    actual_int = int(actual_hex, 16)
    
    print(f"\n[RESULT]")
    print(f"   Generated: 0x{actual_int:04X}")
    print(f"   Expected:  0x5F02 (little-endian)")
    print(f"   Breakdown:")
    print(f"     - Base opcode: 0x0002")
    print(f"     - D[a] = D[15] = 0xF at bits [11:8]")
    print(f"     - D[b] = D[5] = 0x5 at bits [7:4]")
    print(f"     - Result: 0x0F50 -> swap bytes -> 0x5F02")
    
    if actual_int == 0x5F02:
        print(f"\n   [OK] CORRECT ENCODING!")
    else:
        print(f"\n   [ERROR] WRONG! Expected 0x5F02")
        sys.exit(1)
else:
    print(f"[ERROR] Encoding failed!")
    sys.exit(1)
