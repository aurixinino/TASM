@echo off
REM ========================================
REM TASM Comprehensive Test Suite
REM ========================================
REM Runs all individual test suites in sequence
REM Last updated: December 27, 2025

setlocal enabledelayedexpansion

REM Set the script directory
cd /d "%~dp0"

REM Initialize counters
set TESTS_TOTAL=0
set TESTS_PASSED=0
set TESTS_FAILED=0

REM Initialize verbose mode (0 = quiet, 1 = verbose)
set VERBOSE=0
if "%1"=="-v" set VERBOSE=1
if "%1"=="--verbose" set VERBOSE=1

REM Create output directory
if not exist output mkdir output
set LOGFILE=output\test_suite_results.log

REM Clear log file
echo. > %LOGFILE%
echo ======================================== >> %LOGFILE%
echo TASM Comprehensive Test Suite >> %LOGFILE%
echo Run Date: %DATE% %TIME% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%

echo.
echo ========================================
echo TASM Comprehensive Test Suite
echo ========================================
echo.

REM ===========================================
REM Test Suite 0: Basic Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 0: Basic Tests
echo -------------------------------------------
echo Test Suite 0: Basic Tests >> %LOGFILE%

if %VERBOSE%==1 (
    call 0_test.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 0_test.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Basic Tests
    echo [PASS] Basic Tests >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Basic Tests
    echo [FAIL] Basic Tests >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Suite 1: Register Encoding Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 1: Register Encoding Tests
echo -------------------------------------------
echo Test Suite 1: Register Encoding Tests >> %LOGFILE%

if %VERBOSE%==1 (
    call 1_test.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 1_test.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Register Encoding Tests
    echo [PASS] Register Encoding Tests >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Register Encoding Tests
    echo [FAIL] Register Encoding Tests >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Suite 2: Advanced Encoding Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 2: Advanced Encoding Tests
echo -------------------------------------------
echo Test Suite 2: Advanced Encoding Tests >> %LOGFILE%

if %VERBOSE%==1 (
    call 2_test.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 2_test.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Advanced Encoding Tests
    echo [PASS] Advanced Encoding Tests >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Advanced Encoding Tests
    echo [FAIL] Advanced Encoding Tests >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Suite 3: Operand Format Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 3: Operand Format Tests
echo -------------------------------------------
echo Test Suite 3: Operand Format Tests >> %LOGFILE%

if %VERBOSE%==1 (
    call 3_test.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 3_test.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Operand Format Tests
    echo [PASS] Operand Format Tests >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Operand Format Tests
    echo [FAIL] Operand Format Tests >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Suite 4: Encoder Validation (4617 instructions)
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 4: Encoder Validation
echo -------------------------------------------
echo Test Suite 4: Encoder Validation (4617 instructions) >> %LOGFILE%

if %VERBOSE%==1 (
    call 4_test.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 4_test.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Encoder Validation
    echo [PASS] Encoder Validation >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Encoder Validation
    echo [FAIL] Encoder Validation >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Suite 6: Macro Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test Suite 6: Macro Tests
echo -------------------------------------------
echo Test Suite 6: Macro Tests >> %LOGFILE%

if %VERBOSE%==1 (
    call 6_test_macros.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call 6_test_macros.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    echo [PASS] Macro Tests
    echo [PASS] Macro Tests >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    echo [FAIL] Macro Tests
    echo [FAIL] Macro Tests >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Summary
REM ===========================================
echo ========================================
echo Test Suite Summary
echo ========================================
echo Total Test Suites: %TESTS_TOTAL%
echo Test Suites Passed: %TESTS_PASSED%
echo Test Suites Failed: %TESTS_FAILED%

REM Calculate pass rate
set /a PASS_RATE=(%TESTS_PASSED% * 100) / %TESTS_TOTAL%
echo Pass Rate: %PASS_RATE%%%
echo ========================================

REM Write summary to log
echo. >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Test Suite Summary >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Total Test Suites: %TESTS_TOTAL% >> %LOGFILE%
echo Test Suites Passed: %TESTS_PASSED% >> %LOGFILE%
echo Test Suites Failed: %TESTS_FAILED% >> %LOGFILE%
echo Pass Rate: %PASS_RATE%%% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%
echo Run completed: %DATE% %TIME% >> %LOGFILE%

REM Exit with appropriate code
if %TESTS_FAILED% gtr 0 (
    echo.
    echo [FAILURE] %TESTS_FAILED% test suite(s) failed
    echo [FAILURE] %TESTS_FAILED% test suite(s) failed >> %LOGFILE%
    echo See %LOGFILE% for details
    exit /b 1
) else (
    echo.
    echo [SUCCESS] All test suites passed
    echo [SUCCESS] All test suites passed >> %LOGFILE%
    exit /b 0
)
