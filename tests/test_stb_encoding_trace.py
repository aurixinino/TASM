"""
Deep trace diagnostic for ST.B encoding issue.
Traces every step of the encoding process to identify where matching fails.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.instruction_loader import InstructionSetLoader
from src.instruction_encoder import InstructionEncoder
from src.config_loader import TASMConfig
from tests.test_encoder_validation import EncoderValidationTest


class STBEncodingTrace:
    """Trace ST.B encoding process step by step."""
    
    def __init__(self):
        """Initialize with loader and encoder."""
        config = TASMConfig()
        self.loader = InstructionSetLoader()
        success = self.loader.load_instruction_set(config.instruction_set_path)
        if not success:
            raise RuntimeError("Failed to load instruction set")
        self.encoder = InstructionEncoder(self.loader)
        
    def trace_complete_encoding(self, test_instruction, expected_opcode=None):
        """Trace complete encoding process for one instruction."""
        print("\n" + "="*80)
        print(f"ENCODING TRACE: {test_instruction}")
        if expected_opcode:
            print(f"Expected opcode: {expected_opcode}")
        print("="*80)
        
        # Step 1: Parse instruction string
        print("\n[STEP 1] Parse instruction string")
        parts = test_instruction.split(None, 1)
        mnemonic = parts[0].upper()
        operands_str = parts[1] if len(parts) > 1 else ''
        operands = [op.strip() for op in operands_str.split(',')]
        print(f"  Mnemonic: {mnemonic}")
        print(f"  Operands string: {operands_str}")
        print(f"  Operands list: {operands}")
        print(f"  Operand count: {len(operands)}")
        
        # Step 2: Get all variants
        print("\n[STEP 2] Get instruction variants from instruction set")
        variants = self.loader.get_instruction_variants(mnemonic)
        print(f"  Found {len(variants)} total {mnemonic} variants")
        
        # Filter by operand count
        matching_count = [v for v in variants if v.operand_count == len(operands)]
        print(f"  {len(matching_count)} variants with {len(operands)} operands:")
        for i, v in enumerate(matching_count, 1):
            print(f"    {i}. {v.syntax}")
            print(f"       OpCode: {v.opcode}, Size: {v.opcode_size}-bit")
        
        # Step 3: Analyze each operand from user input
        print("\n[STEP 3] Analyze user operands")
        user_operand_info = []
        for i, operand in enumerate(operands):
            print(f"\n  Operand {i+1}: '{operand}'")
            
            # Try register extraction
            reg_type, reg_num = self.loader._extract_register_info(operand)
            if reg_type:
                info = {'type': 'register', 'reg_type': reg_type, 'reg_num': reg_num}
                print(f"    Type: Register")
                print(f"    Register type: {reg_type}")
                print(f"    Register number: {reg_num}")
            else:
                # Try immediate value
                if operand.startswith('0x') or operand.startswith('0X'):
                    val = int(operand, 16)
                    info = {'type': 'immediate', 'value': val, 'format': 'hex'}
                    print(f"    Type: Immediate (hex)")
                    print(f"    Value: {val} (0x{val:04X})")
                    print(f"    Bit length: {val.bit_length()} bits")
                elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
                    val = int(operand)
                    info = {'type': 'immediate', 'value': val, 'format': 'dec'}
                    print(f"    Type: Immediate (decimal)")
                    print(f"    Value: {val}")
                    print(f"    Bit length: {abs(val).bit_length()} bits")
                else:
                    info = {'type': 'unknown'}
                    print(f"    Type: Unknown")
            
            user_operand_info.append(info)
        
        # Step 4: Analyze syntax patterns for each matching variant
        print("\n[STEP 4] Analyze syntax patterns for matching variants")
        for i, variant in enumerate(matching_count, 1):
            print(f"\n  Variant {i}: {variant.syntax}")
            
            # Get syntax operand types
            syntax_types = variant.syntax_operand_types
            print(f"    Syntax operand types: {syntax_types}")
            
            # Try to match each user operand against syntax
            print(f"    Matching analysis:")
            all_match = True
            for j, (user_info, syntax_type) in enumerate(zip(user_operand_info, syntax_types)):
                print(f"\n      Position {j+1}:")
                print(f"        User operand: {operands[j]}")
                print(f"        User type: {user_info.get('type')}")
                print(f"        Syntax expects: {syntax_type}")
                
                # Determine if it should match
                if user_info['type'] == 'register':
                    # Check if syntax expects a register of this type
                    expected_reg = None
                    if syntax_type.startswith('reg_'):
                        expected_reg = syntax_type.split('_')[1].upper()
                    
                    if expected_reg:
                        match = (expected_reg == user_info['reg_type'])
                        print(f"        Expected register type: {expected_reg}")
                        print(f"        Match: {'YES' if match else 'NO'}")
                        if not match:
                            all_match = False
                    else:
                        print(f"        Cannot determine expected register type from '{syntax_type}'")
                        all_match = False
                        
                elif user_info['type'] == 'immediate':
                    # Check if syntax expects immediate/offset
                    is_imm = syntax_type.startswith('imm') or syntax_type.startswith('off')
                    print(f"        Syntax expects immediate/offset: {is_imm}")
                    
                    if is_imm:
                        # Check value range
                        if syntax_type.startswith('off'):
                            # Extract bit width (e.g., "off16" -> 16)
                            try:
                                bit_width = int(syntax_type[3:])
                                max_val = (1 << bit_width) - 1
                                in_range = user_info['value'] <= max_val
                                print(f"        Offset bit width: {bit_width}")
                                print(f"        Max value: {max_val} (0x{max_val:X})")
                                print(f"        User value: {user_info['value']} (0x{user_info['value']:X})")
                                print(f"        In range: {'YES' if in_range else 'NO'}")
                                if not in_range:
                                    all_match = False
                            except:
                                print(f"        Could not extract bit width from '{syntax_type}'")
                        else:
                            print(f"        Match: YES (immediate)")
                    else:
                        print(f"        Match: NO (syntax does not expect immediate)")
                        all_match = False
                else:
                    print(f"        Match: NO (unknown operand type)")
                    all_match = False
            
            if all_match:
                print(f"\n    >>> VARIANT {i} SHOULD MATCH ALL OPERANDS <<<")
            else:
                print(f"\n    Variant {i} does NOT match all operands")
        
        # Step 5: Try encoding through parser
        print("\n[STEP 5] Attempt encoding through EncoderValidationTest parser")
        validator = EncoderValidationTest(None, None)
        
        try:
            # Pass the FULL instruction, not just operands
            parsed = validator.parse_assembly_instruction(test_instruction, 0)
            
            if parsed:
                print(f"  Parse SUCCESS")
                print(f"    Parsed mnemonic: {parsed.mnemonic}")
                print(f"    Parsed operands: {parsed.operands}")
                print(f"    Parsed operand count: {len(parsed.operands)}")
                
                # Step 6: Encode
                print("\n[STEP 6] Attempt encoding with InstructionEncoder")
                result = self.encoder.encode_instruction(parsed)
                
                if result:
                    print(f"  ENCODING SUCCESS!")
                    print(f"    Generated opcode: {result.hex_value}")
                    if expected_opcode:
                        match = result.hex_value.upper() == expected_opcode.upper()
                        print(f"    Expected opcode:  {expected_opcode}")
                        print(f"    Match: {'YES - PERFECT!' if match else 'NO - Opcode mismatch'}")
                    return True
                else:
                    print(f"  ENCODING FAILED")
                    print(f"    Encoder returned None")
                    print(f"    This means no variant was selected by _find_best_variant_by_operand_types()")
                    return False
            else:
                print(f"  PARSE FAILED")
                print(f"    Parser returned None")
                return False
                
        except Exception as e:
            print(f"  EXCEPTION during encoding: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_batch_trace(self):
        """Run trace for multiple test cases."""
        print("\n" + "="*80)
        print("ST.B ENCODING BATCH TRACE")
        print("="*80)
        
        test_cases = [
            ('st.b [a2], 0x6130, d15', '46302FE9'),
            ('st.b a2, 0x6130, d15', '46302FE9'),
            ('st.b A[2], 0x6130, D[15]', '46302FE9'),
            ('st.b a2, 0x10, d15', None),
            ('st.b [a15], 4, d0', None),
        ]
        
        results = []
        for instruction, expected in test_cases:
            success = self.trace_complete_encoding(instruction, expected)
            results.append((instruction, success))
            print("\n" + "-"*80)
        
        # Summary
        print("\n" + "="*80)
        print("BATCH TRACE SUMMARY")
        print("="*80)
        passed = sum(1 for _, success in results if success)
        total = len(results)
        print(f"\nTotal tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print("\nResults:")
        for instruction, success in results:
            status = "PASS" if success else "FAIL"
            print(f"  [{status}] {instruction}")


def main():
    """Main entry point."""
    try:
        trace = STBEncodingTrace()
        
        # Run single detailed trace
        trace.trace_complete_encoding('st.b [a2], 0x6130, d15', '46302FE9')
        
        # Run batch trace
        # trace.run_batch_trace()
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
