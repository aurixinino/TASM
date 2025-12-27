@echo off
REM ========================================
REM C-Macro Test Suite
REM ========================================
REM Tests C-like macro library functionality

setlocal enabledelayedexpansion

echo ========================================
echo C-Macro Test Suite
echo ========================================
echo.

REM Set the script directory
cd /d "%~dp0"
cd ..

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' Python is not available or not in PATH'"
    exit /b 1
)

echo [INFO] Starting C-macro test suite...
echo.

REM Create output directory
if not exist "output" mkdir output

REM Track test results
set TESTS_PASSED=0
set TESTS_FAILED=0
set TESTS_TOTAL=0

REM ===========================================
REM Test 1: Simple C-Macro Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 1: Simple C-Macro Tests (Basic)
echo -------------------------------------------

python src\TASM.py -m data\macros\C_instructions.asm -l tests\test_c_macros_simple.asm >nul 2>&1
set TEST_RESULT=!ERRORLEVEL!

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' C-Macro Simple Tests'"
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' C-Macro Simple Tests'"
    echo   Run: python src\TASM.py -m data\macros\C_instructions.asm -l tests\test_c_macros_simple.asm
)
echo.

REM ===========================================
REM Test 2: Comprehensive C-Macro Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 2: Comprehensive C-Macro Tests (Full)
echo -------------------------------------------

python src\TASM.py -m data\macros\C_instructions.asm -l tests\test_c_macros.asm >nul 2>&1
set TEST_RESULT=!ERRORLEVEL!

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' C-Macro Comprehensive Tests'"
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' C-Macro Comprehensive Tests'"
    echo   Run: python src\TASM.py -m data\macros\C_instructions.asm -l tests\test_c_macros.asm
)
echo.

REM ===========================================
REM Test 3: C-Macro with Verbose Output
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 3: C-Macro Verbose Compilation
echo -------------------------------------------

python src\TASM.py -m data\macros\C_instructions.asm --info tests\test_c_macros_simple.asm >nul 2>&1
set TEST_RESULT=!ERRORLEVEL!

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' C-Macro Verbose Compilation'"
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' C-Macro Verbose Compilation'"
)
echo.

REM ===========================================
REM Test Results Summary
REM ===========================================
echo ========================================
echo Test Suite Summary
echo ========================================

echo Total Tests: %TESTS_TOTAL%
echo Tests Passed: %TESTS_PASSED%
echo Tests Failed: %TESTS_FAILED%

if %TESTS_FAILED% equ 0 (
    set PASS_RATE=100
) else (
    set /a TEMP_CALC=%TESTS_PASSED% * 100
    set /a PASS_RATE=!TEMP_CALC! / %TESTS_TOTAL%
)

echo Pass Rate: !PASS_RATE!%%
echo ========================================

if %TESTS_FAILED% equ 0 (
    echo.
    powershell -Command "Write-Host '[SUCCESS]' -ForegroundColor Green -NoNewline; Write-Host ' All C-macro tests passed!'"
    exit /b 0
) else (
    echo.
    powershell -Command "Write-Host '[FAILURE]' -ForegroundColor Red -NoNewline; Write-Host ' %TESTS_FAILED% tests failed!'"
    echo.
    echo To debug, run individual tests with:
    echo   python src\TASM.py -m data\macros\C_instructions.asm --info tests\test_c_macros_simple.asm
    exit /b 1
)

endlocal
