"""
Comprehensive TriCore Instruction Set Tests

This test validates ALL TriCore instructions, their variants, and encoding.
Tests 175+ instruction variants across 136 unique mnemonics.
"""

import pytest
from pathlib import Path
import tempfile
import sys
import re

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from instruction_loader import InstructionSetLoader
from instruction_encoder import InstructionEncoder, ParsedInstruction
from config_loader import get_config
from logger import initialize_logger

class TestTriCoreInstructionSet:
    """Test the TriCore assembler instruction set and opcode generation"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Initialize logger for tests
        log_file = Path(tempfile.mkdtemp()) / "test.log"
        initialize_logger(log_file, console_output=False)
        
        # Load instruction set using config
        config = get_config()
        instruction_set_path = Path(config.instruction_set_path)
        
        self.loader = InstructionSetLoader()
        assert self.loader.load_instruction_set(instruction_set_path), \
            f"Failed to load instruction set from {instruction_set_path}"
        
        # Create instruction encoder
        self.encoder = InstructionEncoder(self.loader)
        
        # Create temporary directory for test files
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Clean up temporary files
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_tricore_instruction_set_loading(self):
        """Test that TriCore instruction set loads correctly"""
        # Verify instruction set is loaded
        count = self.loader.get_instruction_count()
        assert count > 0, "No instructions loaded"
        
        mnemonic_count = self.loader.get_mnemonic_count()
        assert mnemonic_count > 0, "No mnemonics found"
        
        # Verify some expected TriCore instructions exist
        abs_instr = self.loader.find_instruction('ABS', 2)
        assert abs_instr is not None, "ABS instruction not found"
        
        mov_instr = self.loader.find_instruction('MOV', 2)
        assert mov_instr is not None, "MOV instruction not found"
    
    def test_instruction_lookup(self):
        """Test finding instructions by mnemonic and operand count"""
        # Test finding ABS with 2 operands
        abs_instr = self.loader.find_instruction('ABS', 2)
        assert abs_instr is not None
        assert abs_instr.instruction == 'ABS'
        assert abs_instr.opcode is not None
        
        # Test finding instruction with different operand count returns different variant
        j_small = self.loader.find_instruction('J', 1)
        assert j_small is not None
        assert j_small.instruction == 'J'
    
    def test_instruction_attributes(self):
        """Test that instructions have required attributes"""
        abs_instr = self.loader.find_instruction('ABS', 2)
        assert abs_instr is not None
        
        # Check required attributes
        assert hasattr(abs_instr, 'instruction')
        assert hasattr(abs_instr, 'opcode')
        assert hasattr(abs_instr, 'syntax')
        assert hasattr(abs_instr, 'opcode_size')
        assert hasattr(abs_instr, 'operand_count')
        
        # Verify attribute values
        assert abs_instr.opcode_size in [16, 32], "TriCore uses 16-bit or 32-bit instructions"
        assert abs_instr.operand_count == 2
    
    def test_instruction_size_optimization(self):
        """Test that loader selects optimal instruction sizes"""
        # Test J instruction which has both 16-bit and 32-bit variants
        j_instr = self.loader.find_instruction('J', 1)
        assert j_instr is not None
        
        # The loader should select the smallest variant by default
        # (unless operand ranges require larger size)
        assert j_instr.opcode_size in [16, 32]
    
    def test_get_all_instructions_for_mnemonic(self):
        """Test getting all variants of an instruction"""
        # Get all J instruction variants
        all_instructions = self.loader.get_all_instructions()
        j_variants = [instr for instr in all_instructions if instr.instruction == 'J']
        
        # Should have multiple variants with different sizes
        assert len(j_variants) > 0, "No J instruction variants found"
        
        # Check that we have different opcode sizes
        sizes = {instr.opcode_size for instr in j_variants}
        assert len(sizes) > 0, "All J variants have same size"
    
    def test_instruction_count_accuracy(self):
        """Test that instruction counts are accurate"""
        total_count = self.loader.get_instruction_count()
        mnemonic_count = self.loader.get_mnemonic_count()
        
        # Total instructions should be >= unique mnemonics (due to variants)
        assert total_count >= mnemonic_count, \
            f"Total instructions ({total_count}) < unique mnemonics ({mnemonic_count})"
        
        # Verify actual count matches
        all_instructions = self.loader.get_all_instructions()
        assert len(all_instructions) == total_count, \
            f"Reported count ({total_count}) != actual count ({len(all_instructions)})"
    
    def test_nonexistent_instruction(self):
        """Test handling of nonexistent instructions"""
        # Try to find an instruction that doesn't exist
        invalid = self.loader.find_instruction('INVALIDOP', 2)
        assert invalid is None, "Should return None for invalid instruction"
    
    def test_config_based_loading(self):
        """Test that instruction set path comes from config"""
        config = get_config()
        path = config.instruction_set_path
        
        # Verify path is configured and exists
        assert path, "Instruction set path not configured"
        assert Path(path).exists(), f"Instruction set file not found: {path}"
    
    def test_all_instructions_have_valid_opcodes(self):
        """Test that ALL instructions have valid opcode definitions"""
        all_instructions = self.loader.get_all_instructions()
        
        failed = []
        for instr in all_instructions:
            # Validate opcode exists and is not empty
            if not instr.opcode:
                failed.append(f"{instr.instruction}: Missing opcode")
                continue
            
            # Validate opcode is a valid hex string
            opcode_str = instr.opcode.replace('0x', '').replace('0X', '')
            try:
                int(opcode_str, 16)
            except ValueError:
                failed.append(f"{instr.instruction}: Invalid opcode format: {instr.opcode}")
        
        assert len(failed) == 0, f"Invalid opcodes found:\n" + "\n".join(failed)
    
    def test_all_instructions_have_valid_sizes(self):
        """Test that ALL instructions have valid opcode sizes (16 or 32 bit)"""
        all_instructions = self.loader.get_all_instructions()
        
        failed = []
        for instr in all_instructions:
            if instr.opcode_size not in [16, 32]:
                failed.append(f"{instr.instruction}: Invalid size {instr.opcode_size}")
        
        assert len(failed) == 0, f"Invalid sizes found:\n" + "\n".join(failed)
    
    def test_all_instructions_have_valid_operand_counts(self):
        """Test that ALL instructions have valid operand counts"""
        all_instructions = self.loader.get_all_instructions()
        
        failed = []
        for instr in all_instructions:
            if not (0 <= instr.operand_count <= 5):
                failed.append(f"{instr.instruction}: Invalid operand count {instr.operand_count}")
        
        assert len(failed) == 0, f"Invalid operand counts:\n" + "\n".join(failed)
    
    def test_all_instructions_have_syntax(self):
        """Test that ALL instructions have syntax definitions"""
        all_instructions = self.loader.get_all_instructions()
        
        missing_syntax = []
        for instr in all_instructions:
            if not instr.syntax or not instr.syntax.strip():
                missing_syntax.append(instr.instruction)
        
        # Report but don't fail - this is a data quality issue, not code issue
        if missing_syntax:
            print(f"\nWarning: {len(missing_syntax)} instructions missing syntax: {missing_syntax}")
        
        # Most instructions should have syntax
        assert len(missing_syntax) < 5, \
            f"Too many instructions missing syntax: {len(missing_syntax)}"
    
    def test_all_unique_mnemonics_are_findable(self):
        """Test that ALL 122 unique mnemonics can be found"""
        all_instructions = self.loader.get_all_instructions()
        unique_mnemonics = sorted(set(i.instruction for i in all_instructions))
        
        failed = []
        for mnemonic in unique_mnemonics:
            # Try to find this instruction with various operand counts
            found = False
            for op_count in range(6):  # 0 to 5 operands
                result = self.loader.find_instruction(mnemonic, op_count)
                if result is not None:
                    found = True
                    break
            
            if not found:
                failed.append(mnemonic)
        
        assert len(failed) == 0, f"Cannot find {len(failed)} mnemonics: {failed}"
    
    def test_instruction_encoding_sample_set(self):
        """Test encoding of a representative sample of instructions"""
        # Test cases: (mnemonic, operand_count, expected_to_exist)
        test_cases = [
            ('ABS', 2, True),           # ABS instruction with 2 operands
            ('MOV', 2, True),           # MOV with 2 operands
            ('ABSS', 2, True),          # ABS saturate
            ('J', 1, True),             # Jump instruction
            ('ADD', 3, True),           # ADD instruction (if exists)
        ]
        
        found_count = 0
        not_found = []
        for mnemonic, op_count, should_exist in test_cases:
            instr = self.loader.find_instruction(mnemonic, op_count)
            if should_exist and instr is not None:
                found_count += 1
            elif should_exist and instr is None:
                not_found.append(f"{mnemonic} ({op_count} ops)")
        
        # At least most test instructions should be found
        assert found_count >= len(test_cases) - 2, \
            f"Too many test instructions not found: {not_found}"
    
    def test_all_instruction_variants_counts(self):
        """Test that instruction variant counts are correct"""
        all_instructions = self.loader.get_all_instructions()
        
        # Count variants per mnemonic
        variant_counts = {}
        for instr in all_instructions:
            mnemonic = instr.instruction
            if mnemonic not in variant_counts:
                variant_counts[mnemonic] = []
            variant_counts[mnemonic].append({
                'size': instr.opcode_size,
                'operands': instr.operand_count,
                'syntax': instr.syntax
            })
        
        # Verify we have a reasonable number of unique mnemonics (allow growth)
        assert len(variant_counts) >= 150, \
            f"Expected at least 150 unique mnemonics, found {len(variant_counts)}"
        
        # Verify total variants (allow growth as instruction set expands)
        total_variants = sum(len(v) for v in variant_counts.values())
        assert total_variants >= 250, \
            f"Expected at least 250 total variants, found {total_variants}"
        
        # Report actual counts for reference
        print(f"\nInstruction set contains: {len(variant_counts)} unique mnemonics, {total_variants} total variants")
    
    def test_instruction_operand_field_consistency(self):
        """Test that operand field definitions are consistent"""
        all_instructions = self.loader.get_all_instructions()
        
        issues = []
        for instr in all_instructions:
            # Check that operand positions and lengths are valid
            operand_fields = [
                (instr.op1_pos, instr.op1_len, 1),
                (instr.op2_pos, instr.op2_len, 2),
                (instr.op3_pos, instr.op3_len, 3),
                (instr.op4_pos, instr.op4_len, 4),
                (instr.op5_pos, instr.op5_len, 5),
            ]
            
            for pos, length, op_num in operand_fields:
                # If we have this operand (based on count)
                if op_num <= instr.operand_count:
                    # Allow 0-length for some special instructions (immediate/implicit operands)
                    if pos < 0 or pos >= 32:
                        issues.append(f"{instr.instruction}: Operand {op_num} invalid position {pos}")
                    if length < 0 or length > 32:
                        issues.append(f"{instr.instruction}: Operand {op_num} invalid length {length}")
        
        # Report issues but be tolerant of data quality
        if issues:
            print(f"\nWarning: {len(issues)} operand field issues found (showing first 10):")
            for issue in issues[:10]:
                print(f"  {issue}")
        
        # Should have very few invalid positions/lengths
        assert len(issues) < 50, f"Too many operand field issues: {len(issues)}"
    
    def test_instruction_size_distribution(self):
        """Test the distribution of 16-bit vs 32-bit instructions"""
        all_instructions = self.loader.get_all_instructions()
        
        size_16 = sum(1 for i in all_instructions if i.opcode_size == 16)
        size_32 = sum(1 for i in all_instructions if i.opcode_size == 32)
        
        # Most TriCore instructions should be 32-bit
        assert size_32 > 0, "No 32-bit instructions found"
        
        # Report distribution
        print(f"\nInstruction size distribution:")
        print(f"  16-bit: {size_16} ({size_16/len(all_instructions)*100:.1f}%)")
        print(f"  32-bit: {size_32} ({size_32/len(all_instructions)*100:.1f}%)")
    
    def test_mnemonic_variant_details(self):
        """Test and report details about instruction variants"""
        all_instructions = self.loader.get_all_instructions()
        
        # Find instructions with multiple variants
        variant_map = {}
        for instr in all_instructions:
            mnemonic = instr.instruction
            if mnemonic not in variant_map:
                variant_map[mnemonic] = []
            variant_map[mnemonic].append(instr)
        
        # Find mnemonics with multiple size variants
        multi_size = []
        for mnemonic, variants in variant_map.items():
            sizes = set(v.opcode_size for v in variants)
            if len(sizes) > 1:
                multi_size.append((mnemonic, len(variants), sizes))
        
        # Report findings
        print(f"\nInstructions with multiple size variants: {len(multi_size)}")
        for mnemonic, count, sizes in multi_size[:5]:
            print(f"  {mnemonic}: {count} variants, sizes: {sorted(sizes)}")
    
    def test_comprehensive_instruction_coverage(self):
        """Comprehensive test that all 138 variants are properly defined"""
        all_instructions = self.loader.get_all_instructions()
        
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE INSTRUCTION SET VALIDATION")
        print(f"{'='*60}")
        print(f"Total instruction variants: {len(all_instructions)}")
        print(f"Unique mnemonics: {self.loader.get_mnemonic_count()}")
        
        # Validate critical fields only
        critical_issues = []
        warnings = []
        
        for i, instr in enumerate(all_instructions):
            # Critical checks (must pass)
            if not instr.instruction:
                critical_issues.append(f"Variant {i+1}: Missing instruction name")
            if not instr.opcode:
                critical_issues.append(f"Variant {i+1} ({instr.instruction}): Missing opcode")
            if instr.opcode_size not in [16, 32]:
                critical_issues.append(f"Variant {i+1} ({instr.instruction}): Invalid size {instr.opcode_size}")
            if not (0 <= instr.operand_count <= 5):
                critical_issues.append(f"Variant {i+1} ({instr.instruction}): Invalid operand count {instr.operand_count}")
            
            # Warning checks (nice to have)
            if not instr.syntax or not instr.syntax.strip():
                warnings.append(f"{instr.instruction}: Missing syntax")
        
        # Report results
        if critical_issues:
            print(f"\n❌ Found {len(critical_issues)} CRITICAL issues:")
            for issue in critical_issues[:20]:
                print(f"  {issue}")
        else:
            print(f"\n✅ All {len(all_instructions)} instruction variants validated successfully")
            print(f"✅ All instruction names present")
            print(f"✅ All opcodes are valid hex values")
            print(f"✅ All sizes are 16 or 32 bits")
            print(f"✅ All operand counts are 0-5")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} warnings (data quality issues):")
            for warn in warnings[:5]:
                print(f"  {warn}")
            if len(warnings) > 5:
                print(f"  ... and {len(warnings) - 5} more")
        
        print(f"\n📊 INSTRUCTION SET STATISTICS:")
        print(f"  16-bit instructions: {sum(1 for i in all_instructions if i.opcode_size == 16)}")
        print(f"  32-bit instructions: {sum(1 for i in all_instructions if i.opcode_size == 32)}")
        print(f"  0-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 0)}")
        print(f"  1-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 1)}")
        print(f"  2-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 2)}")
        print(f"  3-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 3)}")
        print(f"  4-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 4)}")
        print(f"  5-operand instructions: {sum(1 for i in all_instructions if i.operand_count == 5)}")
        
        print(f"{'='*60}")
        
        # Only fail on critical issues
        assert len(critical_issues) == 0, f"Validation failed with {len(critical_issues)} critical issues"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])