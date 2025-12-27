@echo off
REM ============================================================================
REM TASM Parser Tests - Batch Runner
REM ============================================================================
REM This batch file runs all parser-related tests to validate the assembler's
REM ability to handle various input formats and syntax variations.
REM ============================================================================

setlocal enabledelayedexpansion

set PASSED=0
set FAILED=0
set TOTAL=0

echo.
echo ========================================================================
echo                     TASM PARSER TEST SUITE
echo ========================================================================
echo.

REM Change to project root directory
cd /d "%~dp0"
cd ..

REM ----------------------------------------------------------------------------
REM Test 1: Parser Tolerance Test
REM ----------------------------------------------------------------------------
set /a TOTAL+=1
echo.
echo ------------------------------------------------------------------------
powershell -Command "Write-Host 'Test 1: Parser Tolerance Test' -ForegroundColor Cyan"
echo ------------------------------------------------------------------------
echo Testing parser's ability to handle multiple register notation formats...
echo Testing parser's ability to split compound operand formats: [a15]14,d1, d15,[a5]18, [a15]2,d15, d15,[a2]6 ...
echo.

python tests\test_parser_tolerance.py
if %ERRORLEVEL% equ 0 (
    set /a PASSED+=1
    powershell -Command "Write-Host '[PASS] Parser tolerance test passed' -ForegroundColor Green"
) else (
    set /a FAILED+=1
    powershell -Command "Write-Host '[FAIL] Parser tolerance test failed' -ForegroundColor Red"
)

REM ----------------------------------------------------------------------------
REM Summary
REM ----------------------------------------------------------------------------
echo.
echo ========================================================================
powershell -Command "Write-Host 'TEST SUMMARY' -ForegroundColor Cyan"
echo ========================================================================
echo Total Tests: %TOTAL%
powershell -Command "Write-Host 'Passed:      %PASSED%' -ForegroundColor Green"
if %FAILED% gtr 0 (
    powershell -Command "Write-Host 'Failed:      %FAILED%' -ForegroundColor Red"
) else (
    powershell -Command "Write-Host 'Failed:      %FAILED%' -ForegroundColor Green"
)
echo ========================================================================

if %FAILED% gtr 0 (
    echo.
    powershell -Command "Write-Host 'Some tests FAILED!' -ForegroundColor Red"
    exit /b 1
) else (
    echo.
    powershell -Command "Write-Host 'All tests PASSED!' -ForegroundColor Green"
    exit /b 0
)
