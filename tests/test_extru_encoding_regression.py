"""
Regression test for EXTR.U encoding.
Verifies that 'extr.u  d0,d0,#16,#16' is encoded correctly.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.instruction_loader import InstructionSetLoader
from src.instruction_encoder import InstructionEncoder
from src.config_loader import TASMConfig
from tests.test_encoder_validation import EncoderValidationTest

def main():
    config = TASMConfig()
    loader = InstructionSetLoader()
    success = loader.load_instruction_set(config.instruction_set_path)
    if not success:
        print("Failed to load instruction set.")
        sys.exit(1)
    encoder = InstructionEncoder(loader)
    validator = EncoderValidationTest(None, None)
    instruction = "extr.u  d0,d0,#16,#16"
    parsed = validator.parse_assembly_instruction(instruction, 0)
    if not parsed:
        print("[FAIL] Parse failed.")
        sys.exit(1)
    result = encoder.encode_instruction(parsed)
    if result:
        print(f"[PASS] Encoded opcode: {result.hex_value}")
        sys.exit(0)
    else:
        print("[FAIL] Encoder returned None.")
        sys.exit(1)

if __name__ == "__main__":
    main()
