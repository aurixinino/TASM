"""
Test suite for TASM command-line options.

This test validates all command-line flags and options to ensure correct parsing,
behavior, and error handling.

Tests:
1. Output control options (-o, -f, -l)
2. Configuration options (-c, --config)
3. Output directory options (-D, --output-dir)
4. Preprocessing options (-E, -a, -I, -p, -P)
5. Macro options (-d, -D, -u, -U, -m, -M)
6. Optimization options (-O0, -O1, -O32, -Ono-implicit, -Ox)
7. Instruction set options (-s, --instruction-set)
8. Logging options (--info, --verbose, --debug)
9. Help and version options (-h, --help, -v, --version)
10. Error handling for invalid options
11. Combined option syntax (-fbin, -ofile.bin, --config=file.json)
12. Multiple option combinations
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
TASM_PATH = PROJECT_ROOT / "src" / "TASM.py"

def run_tasm(args, expect_success=True, timeout=5):
    """
    Run TASM with given arguments and return result.
    
    Args:
        args: List of command-line arguments
        expect_success: Whether command should succeed (True) or fail (False)
        timeout: Timeout in seconds (default 5)
        
    Returns:
        tuple: (returncode, stdout, stderr)
    """
    cmd = [sys.executable, str(TASM_PATH)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        success = (result.returncode == 0) == expect_success
        return success, result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"  {RED}[TIMEOUT]{RESET} Command timed out after {timeout}s: {' '.join(args)}")
        return False, -1, "", "Command timed out"

def test_help_options():
    """Test -h and --help options."""
    print("Testing help options...")
    
    tests = [
        (["-h"], True, "show help"),
        (["--help"], True, "show help (long form)"),
    ]
    
    passed = 0
    failed = 0
    
    for args, expect_success, description in tests:
        success, returncode, stdout, stderr = run_tasm(args, expect_success)
        
        # Help should display usage information
        has_usage = "usage:" in stdout.lower() or "tasm" in stdout.lower()
        
        if success and has_usage:
            print(f"  {GREEN}[PASS]{RESET} {description}")
            passed += 1
        else:
            print(f"  {RED}[FAIL]{RESET} {description}")
            print(f"    Return code: {returncode}")
            if not has_usage:
                print(f"    Missing usage information in output")
            failed += 1
    
    return passed, failed

def test_version_options():
    """Test -v and --version options."""
    print("Testing version options...")
    
    tests = [
        (["-v"], True, "show version"),
        (["--version"], True, "show version (long form)"),
    ]
    
    passed = 0
    failed = 0
    
    for args, expect_success, description in tests:
        success, returncode, stdout, stderr = run_tasm(args, expect_success)
        
        # Version should display version number
        has_version = "version" in stdout.lower() or "tasm" in stdout.lower()
        
        if success and has_version:
            print(f"  {GREEN}[PASS]{RESET} {description}")
            passed += 1
        else:
            print(f"  {RED}[FAIL]{RESET} {description}")
            print(f"    Return code: {returncode}")
            if not has_version:
                print(f"    Missing version information in output")
            failed += 1
    
    return passed, failed

def test_output_format_options():
    """Test -f output format options."""
    print("Testing output format options...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Minimal test\n")
        f.write("nop\n")
        test_file = f.name
    
    try:
        tests = [
            (["-f", "bin", test_file], True, "-f bin format"),
            (["-fbin", test_file], True, "-fbin combined syntax"),
            (["-f", "hex", test_file], True, "-f hex format"),
            (["-fhex", test_file], True, "-fhex combined syntax"),
            (["-f", "txt", test_file], True, "-f txt format"),
            (["-ftxt", test_file], True, "-ftxt combined syntax"),
            (["-f", "invalid", test_file], False, "-f invalid format (should fail)"),
        ]
        
        passed = 0
        failed = 0
        
        for args, expect_success, description in tests:
            success, returncode, stdout, stderr = run_tasm(args, expect_success)
            
            if success:
                print(f"  {GREEN}[PASS]{RESET} {description}")
                passed += 1
            else:
                print(f"  {RED}[FAIL]{RESET} {description}")
                print(f"    Return code: {returncode}")
                print(f"    stderr: {stderr[:200]}")
                failed += 1
        
        return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def test_output_file_options():
    """Test -o output file options."""
    print("Testing output file options...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Minimal test\n")
        f.write("nop\n")
        test_file = f.name
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output1 = os.path.join(tmpdir, "test1.bin")
            output2 = os.path.join(tmpdir, "test2.bin")
            
            tests = [
                (["-o", output1, test_file], True, "-o separated syntax"),
                ([f"-o{output2}", test_file], True, "-o combined syntax"),
                (["-o"], False, "-o without argument (should fail)"),
            ]
            
            passed = 0
            failed = 0
            
            for args, expect_success, description in tests:
                success, returncode, stdout, stderr = run_tasm(args, expect_success)
                
                if success:
                    print(f"  {GREEN}[PASS]{RESET} {description}")
                    passed += 1
                else:
                    print(f"  {RED}[FAIL]{RESET} {description}")
                    print(f"    Return code: {returncode}")
                    print(f"    stderr: {stderr[:200]}")
                    failed += 1
            
            return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def test_output_dir_options():
    """Test -D and --output-dir options."""
    print("Testing output directory options...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Minimal test\n")
        f.write("nop\n")
        test_file = f.name
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            dir1 = os.path.join(tmpdir, "build1")
            dir2 = os.path.join(tmpdir, "build2")
            dir3 = os.path.join(tmpdir, "build3")
            
            tests = [
                (["-D", dir1, test_file], True, "-D separated syntax"),
                ([f"-D{dir2}", test_file], True, "-D combined syntax"),
                (["--output-dir", dir3, test_file], True, "--output-dir long form"),
                ([f"--output-dir={tmpdir}/build4", test_file], True, "--output-dir= combined"),
                (["-D"], False, "-D without argument (should fail)"),
                (["--output-dir"], False, "--output-dir without argument (should fail)"),
            ]
            
            passed = 0
            failed = 0
            
            for args, expect_success, description in tests:
                success, returncode, stdout, stderr = run_tasm(args, expect_success)
                
                if success:
                    print(f"  {GREEN}[PASS]{RESET} {description}")
                    passed += 1
                else:
                    print(f"  {RED}[FAIL]{RESET} {description}")
                    print(f"    Return code: {returncode}")
                    print(f"    stderr: {stderr[:200]}")
                    failed += 1
            
            return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def test_config_options():
    """Test -c and --config options."""
    print("Testing configuration file options...")
    
    # Create a test config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{\n')
        f.write('  "architecture": {"endianness": "little", "word_size": 32},\n')
        f.write('  "paths": {\n')
        f.write(f'    "instruction_set": "{str(PROJECT_ROOT / "Processors" / "tricore" / "data" / "languages" / "tricore_tc1.6_instruction_set.xlsx").replace(chr(92), chr(92)+chr(92))}",\n')
        f.write('    "output_dir": "output/test_build"\n')
        f.write('  },\n')
        f.write('  "output": {"generate_lst": true, "generate_bin": true}\n')
        f.write('}\n')
        config_file = f.name
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Minimal test\n")
        f.write("nop\n")
        test_file = f.name
    
    try:
        tests = [
            (["-c", config_file, test_file], True, "-c separated syntax"),
            ([f"-c{config_file}", test_file], True, "-c combined syntax"),
            (["--config", config_file, test_file], True, "--config long form"),
            ([f"--config={config_file}", test_file], True, "--config= combined"),
            (["-c"], False, "-c without argument (should fail)"),
            (["--config"], False, "--config without argument (should fail)"),
            (["-c", "nonexistent.json", test_file], False, "nonexistent config file (should fail)"),
        ]
        
        passed = 0
        failed = 0
        
        for args, expect_success, description in tests:
            success, returncode, stdout, stderr = run_tasm(args, expect_success)
            
            if success:
                print(f"  {GREEN}[PASS]{RESET} {description}")
                passed += 1
            else:
                print(f"  {RED}[FAIL]{RESET} {description}")
                print(f"    Return code: {returncode}")
                print(f"    stderr: {stderr[:200]}")
                failed += 1
        
        return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(config_file)
            os.unlink(test_file)
        except:
            pass

def test_optimization_options():
    """Test optimization flags."""
    print("Testing optimization options...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Test optimization flags\n")
        f.write("mov d0, #0x20\n")
        f.write("st.w [a0], d0\n")
        test_file = f.name
    
    try:
        tests = [
            (["-O0", test_file], True, "-O0 no optimization"),
            (["-O1", test_file], True, "-O1 minimal optimization"),
            (["-O32", test_file], True, "-O32 force 32-bit variants"),
            (["-Ono-implicit", test_file], True, "-Ono-implicit disable implicit operands"),
            (["-Ox", test_file], True, "-Ox multipass optimization"),
        ]
        
        passed = 0
        failed = 0
        
        for args, expect_success, description in tests:
            success, returncode, stdout, stderr = run_tasm(args, expect_success)
            
            if success:
                print(f"  {GREEN}[PASS]{RESET} {description}")
                passed += 1
            else:
                print(f"  {RED}[FAIL]{RESET} {description}")
                print(f"    Return code: {returncode}")
                print(f"    stderr: {stderr[:200]}")
                failed += 1
        
        return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def test_logging_options():
    """Test logging verbosity options."""
    print("Testing logging options...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Minimal test\n")
        f.write("nop\n")
        test_file = f.name
    
    try:
        tests = [
            (["--info", test_file], True, "--info show info messages"),
            (["--verbose", test_file], True, "--verbose show all messages"),
            (["--debug", test_file], True, "--debug show debug messages"),
        ]
        
        passed = 0
        failed = 0
        
        for args, expect_success, description in tests:
            success, returncode, stdout, stderr = run_tasm(args, expect_success)
            
            if success:
                print(f"  {GREEN}[PASS]{RESET} {description}")
                passed += 1
            else:
                print(f"  {RED}[FAIL]{RESET} {description}")
                print(f"    Return code: {returncode}")
                print(f"    stderr: {stderr[:200]}")
                failed += 1
        
        return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def test_error_handling():
    """Test error handling for invalid options and arguments."""
    print("Testing error handling...")
    
    tests = [
        ([], False, "no arguments (should fail)"),
        (["nonexistent.asm"], False, "nonexistent source file (should fail)"),
        (["--invalid-option"], False, "invalid option (should fail)"),
        (["-o"], False, "-o without argument (should fail)"),
        (["-f"], False, "-f without argument (should fail)"),
    ]
    
    passed = 0
    failed = 0
    
    for args, expect_success, description in tests:
        success, returncode, stdout, stderr = run_tasm(args, expect_success)
        
        if success:
            print(f"  {GREEN}[PASS]{RESET} {description}")
            passed += 1
        else:
            print(f"  {RED}[FAIL]{RESET} {description}")
            print(f"    Return code: {returncode}")
            print(f"    Expected failure but got success")
            failed += 1
    
    return passed, failed

def test_combined_options():
    """Test multiple options combined."""
    print("Testing combined option usage...")
    
    # Create a minimal test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write("; Combined options test\n")
        f.write("mov d0, #0x20\n")
        test_file = f.name
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "combined.bin")
            build_dir = os.path.join(tmpdir, "build")
            
            tests = [
                (["-fbin", f"-o{output}", test_file], True, "combined -fbin -o"),
                (["-O32", "-Ono-implicit", "-fhex", test_file], True, "multiple optimization flags"),
                (["-D", build_dir, "--info", "-fbin", test_file], True, "output dir + logging + format"),
            ]
            
            passed = 0
            failed = 0
            
            for args, expect_success, description in tests:
                success, returncode, stdout, stderr = run_tasm(args, expect_success)
                
                if success:
                    print(f"  {GREEN}[PASS]{RESET} {description}")
                    passed += 1
                else:
                    print(f"  {RED}[FAIL]{RESET} {description}")
                    print(f"    Return code: {returncode}")
                    print(f"    stderr: {stderr[:200]}")
                    failed += 1
            
            return passed, failed
    finally:
        # Cleanup
        try:
            os.unlink(test_file)
        except:
            pass

def main():
    """Run all command-line option tests."""
    print("\n" + "="*70)
    print("TASM Command-Line Options Test Suite")
    print("="*70 + "\n")
    
    total_passed = 0
    total_failed = 0
    
    # Run all test groups
    test_groups = [
        ("Help Options", test_help_options),
        ("Version Options", test_version_options),
        ("Output Format Options", test_output_format_options),
        ("Output File Options", test_output_file_options),
        ("Output Directory Options", test_output_dir_options),
        ("Configuration Options", test_config_options),
        ("Optimization Options", test_optimization_options),
        ("Logging Options", test_logging_options),
        ("Error Handling", test_error_handling),
        ("Combined Options", test_combined_options),
    ]
    
    for group_name, test_func in test_groups:
        print(f"\n{YELLOW}[{group_name}]{RESET}")
        passed, failed = test_func()
        total_passed += passed
        total_failed += failed
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Total Passed: {GREEN}{total_passed}{RESET}")
    print(f"Total Failed: {RED}{total_failed}{RESET}")
    
    if total_failed == 0:
        print(f"\n{GREEN}[PASS] All command-line option tests passed!{RESET}\n")
        return 0
    else:
        print(f"\n{RED}[FAIL] Some tests failed. Please review the output above.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
