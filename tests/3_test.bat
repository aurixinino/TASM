@echo off
REM ========================================
REM TASM Integration Tests Suite
REM ========================================
REM Tests: Complete source file compilation and output comparison
REM Focus on end-to-end compilation correctness

setlocal enabledelayedexpansion

echo ========================================
echo TASM Integration Tests Suite
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

echo [INFO] Starting integration test suite...
echo.

REM Create output directory
if not exist "output" mkdir output

REM Initialize log file
set LOGFILE=output\test_integration.log
echo TASM Integration Test Results > %LOGFILE%
echo Date: %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%

REM Track test results
set TESTS_PASSED=0
set TESTS_FAILED=0
set TESTS_TOTAL=0

REM ===========================================
REM Test 1: Intel HEX Format
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 1: Intel HEX Format
echo -------------------------------------------
echo Test 1: Intel HEX Format >> %LOGFILE%

if %VERBOSE%==1 (
    call tests\test_intel_hex.bat
    set TEST_RESULT=!ERRORLEVEL!
) else (
    call tests\test_intel_hex.bat >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Intel HEX Format
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Intel HEX Format >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Intel HEX Format
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Intel HEX Format >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 2: TriCore Sample Programs (test1.asm)
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 2: TriCore Sample Program - test1.asm
echo -------------------------------------------
echo Test 2: test1.asm >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test1.asm...
    python src\TASM.py tests\test1.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test1.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' test1.asm Compilation
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' test1.asm >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' test1.asm Compilation
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' test1.asm >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 3: TriCore Sample Programs (test2.asm)
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 3: TriCore Sample Program - test2.asm
echo -------------------------------------------
echo Test 3: test2.asm >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test2.asm...
    python src\TASM.py tests\test2.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test2.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' test2.asm Compilation
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' test2.asm >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' test2.asm Compilation
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' test2.asm >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 4: TriCore LED Output Validation
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 4: TriCore LED Output Validation
echo -------------------------------------------
echo Test 4: TriCore LED Output >> %LOGFILE%

REM Compile the test file with -l (listing) and -f txt options
if %VERBOSE%==1 (
    echo Compiling tricore_set_LED1.asm with -l and -f txt...
    python src\TASM.py -l -f txt tests\tricore_set_LED1.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py -l -f txt tests\tricore_set_LED1.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

REM Check if compilation succeeded
if !TEST_RESULT! neq 0 (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TriCore LED Output - Compilation failed
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TriCore LED Output - Compilation failed >> %LOGFILE%
    echo. >> %LOGFILE%
    echo.
    goto :skip_led_comparison
)

REM The TXT format file is generated in output\assembly_build\
REM Compare that output with target
if %VERBOSE%==1 (
    echo Comparing output with target file...
)

fc /b output\assembly_build\tricore_set_LED1.txt tests\tricore_set_LED1_target.txt >nul 2>&1
set COMPARE_RESULT=!ERRORLEVEL!

if !COMPARE_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' TriCore LED Output Validation
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' TriCore LED Output Validation >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TriCore LED Output Validation - Output differs from target
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' TriCore LED Output - Output differs >> %LOGFILE%
    if %VERBOSE%==1 (
        echo   Expected: tests\tricore_set_LED1_target.txt
        echo   Got:      output\assembly_build\tricore_set_LED1.txt
        echo   Run: fc output\assembly_build\tricore_set_LED1.txt tests\tricore_set_LED1_target.txt
    )
)

:skip_led_comparison
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 5: Data Directives Full Source
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 5: Data Directives Full Source
echo -------------------------------------------
echo Test 5: Data Directives Full >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test_data_directives.asm...
    python src\TASM.py tests\test_data_directives.asm -l -f bin
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_data_directives.asm -l -f bin >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Data Directives Full Source
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Data Directives Full >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Data Directives Full Source
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Data Directives Full >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 6: Forward Jumps Full Source
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 6: Forward Jumps Full Source
echo -------------------------------------------
echo Test 6: Forward Jumps Full >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test_forward_jumps.asm...
    python src\TASM.py tests\test_forward_jumps.asm -l -f txt
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_forward_jumps.asm -l -f txt >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Forward Jumps Full Source
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Forward Jumps Full >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Forward Jumps Full Source
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Forward Jumps Full >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 7: Instruction Size Selection Full
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 7: Instruction Size Selection Full
echo -------------------------------------------
echo Test 7: Instruction Size Full >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test_instruction_size_selection.asm...
    python src\TASM.py tests\test_instruction_size_selection.asm -l -f bin -O32
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_instruction_size_selection.asm -l -f bin -O32 >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Instruction Size Selection Full
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Instruction Size Full >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Instruction Size Selection Full
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Instruction Size Full >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 8: Numeric Constants Full Source
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 8: Numeric Constants Full Source
echo -------------------------------------------
echo Test 8: Numeric Constants Full >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test_numeric_constants.asm...
    python src\TASM.py tests\test_numeric_constants.asm -l -f bin
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py tests\test_numeric_constants.asm -l -f bin >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Numeric Constants Full Source
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' Numeric Constants Full >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Numeric Constants Full Source
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' Numeric Constants Full >> %LOGFILE%
)
echo. >> %LOGFILE%
echo.

REM ===========================================
REM Test 7: --no-macros Option Test
REM ===========================================
set /a TESTS_TOTAL+=1
echo -------------------------------------------
echo Test 7: --no-macros Option Test
echo -------------------------------------------
echo Test 7: --no-macros Option >> %LOGFILE%

if %VERBOSE%==1 (
    echo Compiling test_no_macros.asm with --no-macros...
    python src\TASM.py --no-macros tests\test_no_macros.asm
    set TEST_RESULT=!ERRORLEVEL!
) else (
    python src\TASM.py --no-macros tests\test_no_macros.asm >nul 2>&1
    set TEST_RESULT=!ERRORLEVEL!
)

if !TEST_RESULT! equ 0 (
    set /a TESTS_PASSED+=1
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' --no-macros Option Test
    powershell -Command "Write-Host '[PASS]' -ForegroundColor Green -NoNewline; Write-Host '' --no-macros Option >> %LOGFILE%
) else (
    set /a TESTS_FAILED+=1
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' --no-macros Option Test
    powershell -Command "Write-Host '[FAIL]' -ForegroundColor Red -NoNewline; Write-Host '' --no-macros Option >> %LOGFILE%
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
    powershell -Command "Write-Host '[SUCCESS]' -ForegroundColor Green -NoNewline; Write-Host '' All integration tests passed!
    powershell -Command "Write-Host '[SUCCESS]' -ForegroundColor Green -NoNewline; Write-Host '' All tests passed! >> %LOGFILE%
    exit /b 0
) else (
    echo.
    powershell -Command "Write-Host '[FAILURE]' -ForegroundColor Red -NoNewline; Write-Host '' %TESTS_FAILED% tests failed!
    powershell -Command "Write-Host '[FAILURE]' -ForegroundColor Red -NoNewline; Write-Host '' %TESTS_FAILED% tests failed! >> %LOGFILE%
    exit /b 1
)

endlocal
