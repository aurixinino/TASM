"""
Implicit Operand Validation Test

This script validates TASM encoder against reference opcodes for instructions
with implicit A[10] or A[15] operands. When using -Ono-implicit flag, TASM
should generate opcodes matching the reference (explicit operands).

Strategy: Create ONE assembly file with all test cases, assemble once, compare.

Usage:
    python tests/test_implicit_operand_validation.py

Generates:
    output/encoder_validation/implicit_operand_report.txt
"""

import sys
from pathlib import Path
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def parse_implicit_mismatches(mismatch_file):
    """Parse mismatch_report.txt to extract implicit operand cases."""
    mismatches = []
    
    with open(mismatch_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('TASM') or line.startswith('=') or line.startswith('Total'):
                continue
            if line.startswith('---'):
                continue
                
            # Parse line format: TASM-OPCODE     REF-OPCODE      SOURCE
            parts = line.split(None, 2)
            if len(parts) < 3:
                continue
                
            tasm_opcode = parts[0]
            ref_opcode = parts[1]
            source = parts[2]
            
            # Check if source contains A[10] or A[15]
            if re.search(r'[,\[]a(10|15)[,\]]', source.lower()):
                mismatches.append({
                    'tasm_opcode': tasm_opcode,
                    'ref_opcode': ref_opcode,
                    'source': source.strip()
                })
    
    return mismatches

def create_batch_test_file(mismatches, output_path):
    """Create a single assembly file with all test cases."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("; Implicit Operand Validation Test\n")
        f.write("; Generated test file with all implicit operand cases\n\n")
        
        for i, case in enumerate(mismatches):
            # Remove comments and clean up source
            source = case['source']
            if ';' in source:
                source = source.split(';')[0].strip()
            
            f.write(f"test_{i}:\n")
            f.write(f"    {source}\n")
        
        f.write("\n; End of test file\n")
    
    return len(mismatches)

def parse_map_output(map_file):
    """Parse MAP output file to extract opcodes in order."""
    opcodes = []
    with open(map_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('0x'):
                # Format: 0x80000000: 2EAFF9  ; st.h    [a10], 46,d15 (implicit_test_batch.obj)
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    opcode_part = parts[1].split(';')[0].strip().upper()
                    opcodes.append(opcode_part)
    return opcodes

def run_validation():
    """Run validation test."""
    import subprocess
    
    project_root = Path(__file__).parent.parent
    mismatch_file = project_root / 'output' / 'encoder_validation' / 'mismatch_report.txt'
    implicit_file = project_root / 'output' / 'encoder_validation' / 'implicit_operand_mismatches.txt'
    output_dir = project_root / 'output' / 'encoder_validation'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / 'implicit_operand_report.txt'
    test_asm = output_dir / 'implicit_test_batch.asm'
    
    # Parse implicit operand mismatches
    if not implicit_file.exists():
        print(f"Error: {implicit_file} not found")
        print("Run extraction script first")
        return False
    
    print("Parsing implicit operand mismatches...")
    mismatches = parse_implicit_mismatches(implicit_file)
    print(f"Found {len(mismatches)} implicit operand test cases")
    
    # Create batch test file
    print("Creating batch test file...")
    create_batch_test_file(mismatches, test_asm)
    
    # Assemble with -Ono-implicit flag
    print("Assembling with -Ono-implicit flag...")
    result = subprocess.run(
        ['python', 'src/TASM.py', '-Ono-implicit', '-f', 'txt', str(test_asm)],
        capture_output=True,
        text=True,
        cwd=project_root
    )
    
    if result.returncode != 0:
        print(f"Assembly failed: {result.stderr}")
        return False
    
    # Find output map file
    map_files = list((project_root / 'output').glob('**/implicit_test_batch.map'))
    if not map_files:
        print("Error: Output MAP file not found")
        return False
    
    map_file = map_files[0]
    print(f"Parsing output: {map_file}")
    opcodes = parse_map_output(map_file)
    
    if len(opcodes) != len(mismatches):
        print(f"Warning: Opcode count mismatch: {len(opcodes)} vs {len(mismatches)}")
    
    # Validate each case
    matches = []
    failures = []
    
    print("\nValidating opcodes...")
    for i, case in enumerate(mismatches):
        if i >= len(opcodes):
            break
            
        expected_opcode = case['ref_opcode'].upper()
        tasm_opcode = opcodes[i]
        
        if tasm_opcode == expected_opcode:
            matches.append({
                'source': case['source'],
                'opcode': tasm_opcode
            })
        else:
            failures.append({
                'source': case['source'],
                'tasm_opcode': tasm_opcode,
                'ref_opcode': expected_opcode
            })
    
    # Generate report
    print(f"\nGenerating report: {report_file}")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("TASM Implicit Operand Validation Report (-Ono-implicit)\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total Test Cases: {len(mismatches)}\n")
        f.write(f"Matches: {len(matches)}\n")
        f.write(f"Failures: {len(failures)}\n")
        f.write(f"Pass Rate: {len(matches) / len(mismatches) * 100:.2f}%\n")
        f.write("=" * 80 + "\n\n")
        
        if matches:
            f.write(f"\nMATCHES ({len(matches)} cases)\n")
            f.write("=" * 80 + "\n")
            f.write(f"{'OPCODE':<16} SOURCE\n")
            f.write("-" * 80 + "\n")
            for match in matches:
                f.write(f"{match['opcode']:<16} {match['source']}\n")
        
        if failures:
            f.write(f"\n\nFAILURES ({len(failures)} cases)\n")
            f.write("=" * 80 + "\n")
            f.write(f"{'TASM-OPCODE':<16} {'REF-OPCODE':<16} SOURCE\n")
            f.write("-" * 80 + "\n")
            for failure in failures:
                f.write(f"{failure['tasm_opcode']:<16} {failure['ref_opcode']:<16} {failure['source']}\n")
    
    # Print summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Test Cases: {len(mismatches)}")
    print(f"Matches: {len(matches)}")
    print(f"Failures: {len(failures)}")
    print(f"Pass Rate: {len(matches) / len(mismatches) * 100:.2f}%")
    print("=" * 80)
    print(f"\nDetailed report saved to: {report_file}")
    
    return len(failures) == 0

if __name__ == '__main__':
    success = run_validation()
    sys.exit(0 if success else 1)
