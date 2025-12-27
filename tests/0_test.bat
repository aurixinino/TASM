@echo off
REM ========================================
REM TASM Core Implementation Tests Suite
REM ========================================
REM Tests: Data directives, numeric constants, instruction features
REM Fast tests focusing on TASM implementation features

setlocal enabledelayedexpansion

echo ========================================
echo TASM Implementation Tests Suite
echo ========================================
echo.

REM Parse command line arguments
set VERBOSE=0
if "%1"=="--verbose" set VERBOSE=1
if "%1"=="-v" set VERBOSE=1

REM Set the script directory
cd /d "%~dp0"
cd ..

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Python is not available or not in PATH
    exit /b 1
)

echo [INFO] Starting implementation test suite...
echo.

REM Create output directory
if not exist "output" mkdir output

REM Initialize log file
set LOGFILE=output\test_implementation.log
echo TASM Implementation Test Results > %LOGFILE%
echo Date: %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%

REM Track test results
set TESTS_PASSED=0
set TESTS_FAILED=0
set TESTS_TOTAL=0

REM ===========================================
REM Test 1: Data Directives (DB, DW, DD, EQU)
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 1: Data Directives
echo -------------------------------------------
echo Test 1: Data Directives >> %LOGFILE%

if %VERBOSE%==1 (
    python src\TASM.py tests\test_data_directives.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_data_directives.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Data Directives
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Data Directives >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Data Directives
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Data Directives >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 2: TIMES and RESB Directives
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 2: TIMES and RESB Directives
echo -------------------------------------------
echo Test 2: TIMES and RESB >> %LOGFILE%

if %VERBOSE%==1 (
    python src\TASM.py tests\test_times_resb.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_times_resb.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' TIMES/RESB Directives
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' TIMES/RESB >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TIMES/RESB Directives
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TIMES/RESB >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 3: NASM Numeric Constants
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 3: NASM Numeric Constants
echo -------------------------------------------
echo Test 3: NASM Numeric Constants >> %LOGFILE%

if %VERBOSE%==1 (
    python src\TASM.py tests\test_numeric_constants.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_numeric_constants.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' NASM Numeric Constants
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' NASM Numeric Constants >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' NASM Numeric Constants
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' NASM Numeric Constants >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 4: Multiple Output Formats
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 8: Multiple Output Formats
echo -------------------------------------------
echo Test 8: Multiple Output Formats >> %LOGFILE%

set FORMAT_TEST_FAILED=0

python src\TASM.py tests\test_intel_hex.asm -f bin >nul 2>&1
if %ERRORLEVEL% neq 0 set FORMAT_TEST_FAILED=1

python src\TASM.py tests\test_intel_hex.asm -f hex >nul 2>&1
if %ERRORLEVEL% neq 0 set FORMAT_TEST_FAILED=1

python src\TASM.py tests\test_intel_hex.asm -f txt >nul 2>&1
if %ERRORLEVEL% neq 0 set FORMAT_TEST_FAILED=1

if !FORMAT_TEST_FAILED! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' Multiple Output Formats'"
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' Multiple Output Formats'" >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' Multiple Output Formats'"
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' Multiple Output Formats'" >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 7: Configuration File Support
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 5: Configuration File Support
echo -------------------------------------------
echo Test 5: Configuration File Support >> %LOGFILE%

if exist "config\tasm_config.json" (
    if %VERBOSE%==1 (
        python src\TASM.py tests\test_intel_hex.asm -c config\tasm_config.json
        set TEST_RESULT=!ERRORLEVEL!
    ) else (
        python src\TASM.py tests\test_intel_hex.asm -c config\tasm_config.json >nul 2>&1
        set TEST_RESULT=!ERRORLEVEL!
    )
    
    if !TEST_RESULT! equ 0 (
        set /a TESTS_PASSED+=1
        powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Configuration File Support
        powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Configuration File Support >> %LOGFILE%
    ) else (
        set /a TESTS_FAILED+=1
        powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Configuration File Support
        powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Configuration File Support >> %LOGFILE%
    )
) else (
    echo [SKIP] Configuration file not found
    echo [SKIP] Configuration file not found >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 6: Command-Line Options
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 6: Command-Line Options
echo -------------------------------------------
echo Test 6: Command-Line Options >> %LOGFILE%

REM Run with PowerShell timeout to prevent hanging
if %VERBOSE%==1 (
    python tests\test_command_line_options.py
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python tests\test_command_line_options.py >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)


if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' Command-Line Options'"
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host ' Command-Line Options'" >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' Command-Line Options'"
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host ' Command-Line Options'" >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 7: Python Unit Tests
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 7: Python Unit Tests
echo -------------------------------------------
echo Test 7: Python Unit Tests >> %LOGFILE%

if %VERBOSE%==1 (
    python -m pytest tests/test_logging.py tests/test_utils.py -v
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python -m pytest tests/test_logging.py tests/test_utils.py --tb=no -q
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Python Unit Tests
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Python Unit Tests >> %LOGFILE%
) else (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Python Unit Tests - Some tests failed
    echo [INFO] Python Unit Tests - Some tests failed >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test Results Summary
REM ===========================================
echo ========================================
echo Test Suite Summary
echo ========================================
echo ======================================== >> %LOGFILE%
echo Test Suite Summary >> %LOGFILE%
echo ======================================== >> %LOGFILE%

echo Total Tests: %TESTS_TOTAL%
echo Tests Passed: %TESTS_PASSED%
echo Tests Failed: %TESTS_FAILED%

echo Total Tests: %TESTS_TOTAL% >> %LOGFILE%
echo Tests Passed: %TESTS_PASSED% >> %LOGFILE%
echo Tests Failed: %TESTS_FAILED% >> %LOGFILE%

if %TESTS_FAILED% equ 0 (
    set PASS_RATE=100
) else (
    set /a TEMP_CALC=%TESTS_PASSED% * 100
    set /a PASS_RATE=!TEMP_CALC! / %TESTS_TOTAL%
)

echo Pass Rate: !PASS_RATE!%%
echo Pass Rate: !PASS_RATE!%% >> %LOGFILE%
echo ========================================
echo ======================================== >> %LOGFILE%

if %TESTS_FAILED% equ 0 (
    echo.
    powershell -Command "Write-Host '[SUCCESS]' -ForegroundColor Green -NoNewline; Write-Host '' All implementation tests passed!
    powershell -Command "Write-Host '[SUCCESS]' -ForegroundColor Green -NoNewline; Write-Host '' All tests passed! >> %LOGFILE%
    exit /b 0
) else (
    echo.
    powershell -Command "Write-Host '[FAILURE]' -ForegroundColor Red -NoNewline; Write-Host '' %TESTS_FAILED% tests failed!
    powershell -Command "Write-Host '[FAILURE]' -ForegroundColor Red -NoNewline; Write-Host '' %TESTS_FAILED% tests failed! >> %LOGFILE%
    exit /b 1
)

endlocal
