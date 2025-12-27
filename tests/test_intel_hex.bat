@echo off
REM Test Intel HEX output format
REM Verifies that data at 0x08000000-0x08000007 is correctly formatted

echo ========================================
echo Intel HEX Format Test
echo ========================================
echo.

echo Test: Generating Intel HEX with data at 0x08000000
echo Expected output:
echo   :020000040800F2          (Extended Linear Address)
echo   :08000000123456789ABCDEF0C0 (Data record)
echo   :00000001FF              (EOF)
echo.

REM Compile the test file
python src\TASM.py tests\test_intel_hex.asm -f hex >nul 2>&1

if %ERRORLEVEL% neq 0 (
    echo [FAIL] Compilation failed
    exit /b 1
)

echo [PASS] Compilation succeeded
echo.

REM Verify the output
echo Verifying Intel HEX format...
python tests\verify_intel_hex.py | findstr /C:"[OK] Matches expected" >nul

if %ERRORLEVEL% neq 0 (
    echo [FAIL] Intel HEX format verification failed
    echo.
    echo Generated file content:
    type output\assembly_build\test_intel_hex.hex
    exit /b 1
)

echo [PASS] All Intel HEX records match expected format
echo.

REM Count the lines
for /f %%a in ('type output\assembly_build\test_intel_hex.hex ^| find /c /v ""') do set LINE_COUNT=%%a

if "%LINE_COUNT%"=="3" (
    echo [PASS] Correct number of records: 3
) else (
    echo [FAIL] Wrong number of records: %LINE_COUNT% ^(expected 3^)
    exit /b 1
)

echo.
echo ========================================
echo Intel HEX Test: PASSED
echo ========================================
exit /b 0
