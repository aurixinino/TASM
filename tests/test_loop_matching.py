"""Test LOOP instruction matching logic"""
import sys
sys.path.insert(0, 'src')

from instruction_loader import InstructionSetLoader
from instruction_encoder import ParsedOperand
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Load instruction set
loader = InstructionSetLoader()
loader.load_instruction_set('Processors/tricore/data/languages/tricore_tc1.6_instruction_set.xlsx')

# Get LOOP variants
loop_instructions = [inst for inst in loader._instruction_list if inst.instruction == 'LOOP']

print(f'\n=== Found {len(loop_instructions)} LOOP variants ===')
for inst in loop_instructions:
    print(f'\nSyntax: {inst.syntax}')
    print(f'Opcode: {inst.opcode}, Size: {inst.opcode_size}-bit')
    print(f'Op1: pos={inst.op1_pos} len={inst.op1_len}, Op2: pos={inst.op2_pos} len={inst.op2_len}')
    print(f'Syntax types: {inst.syntax_operand_types}')

# Test matching with actual operands (register + displacement)
print('\n=== Testing instruction matching ===')
operands = [
    ParsedOperand('d4', 'reg_a'),  # Address register
    ParsedOperand('for_loop_7', 'imm')  # Label (immediate/displacement)
]

print(f'Operands: {[str(op) for op in operands]}')

result = loader.find_instruction('LOOP', 2, operands)
if result:
    print(f'\nMatched variant: {result.syntax}')
    print(f'Opcode: {result.opcode}, Size: {result.opcode_size}-bit')
else:
    print('\nNo variant matched!')
