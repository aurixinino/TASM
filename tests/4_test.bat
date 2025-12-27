@echo off
REM ========================================
REM TASM Encoder Validation Test
REM ========================================
REM This test validates the TASM encoder against reference opcodes
REM from the TriCore instruction set
REM
REM Usage: test_encoder_validation.bat [--verbose]

setlocal enabledelayedexpansion

echo ========================================
echo TASM Encoder Validation Test
echo ========================================
echo.

REM Parse command line arguments
set VERBOSE_FLAG=
if "%1"=="--verbose" set VERBOSE_FLAG=--verbose
if "%1"=="-v" set VERBOSE_FLAG=--verbose

REM Set the script directory
cd /d "%~dp0"
cd ..

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python is not available or not in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

REM Run the encoder validation test
python tests\test_encoder_validation.py %VERBOSE_FLAG%

set TEST_RESULT=%ERRORLEVEL%

REM ===========================================
REM Test: EXTR.U Encoding Regression
REM ===========================================
set /a TESTS_TOTAL+=1
set TEST_RESULT=1
if %VERBOSE%==1 (
    python tests\test_extru_encoding_regression.py
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python tests\test_extru_encoding_regression.py >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)
if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' EXTR.U Encoding Regression
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' EXTR.U Encoding Regression >> %LOGFILE%"
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' EXTR.U Encoding Regression
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' EXTR.U Encoding Regression >> %LOGFILE%"
)
echo. >> %LOGFILE%
echo.

echo.
echo ========================================
if %TEST_RESULT% equ 0 (
    echo [SUCCESS] Encoder validation completed
) else (
    echo [FAILURE] Encoder validation failed
)
echo ========================================

exit /b %TEST_RESULT%

endlocal
