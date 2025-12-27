@echo off
REM Test implicit operand validation with -Ono-implicit flag
echo ========================================
echo Testing Implicit Operand Validation
echo ========================================

REM Change to parent directory if we're in tests folder
cd /d "%~dp0"
cd ..

python tests\test_implicit_operand_validation.py
if errorlevel 1 (
    echo FAILED: Implicit operand validation failed
    exit /b 1
)
echo PASSED: Implicit operand validation successful
exit /b 0
