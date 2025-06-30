@echo off

REM Configuration variables
set EXE_NAME=extend-pq
set WINDOW_MODE=--console

echo Building Power Query Extensions API executable...
echo =============================================
echo Configuration:
echo   EXE Name: %EXE_NAME%
echo   Window Mode: %WINDOW_MODE%
echo.

REM Clean previous builds
echo Cleaning previous builds...
REM Kill any running instances of the exe
taskkill /f /im "%EXE_NAME%.exe" 2>nul
timeout /t 2 /nobreak >nul
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
REM Also clean any leftover exe files in root
if exist "%EXE_NAME%.exe" del /q "%EXE_NAME%.exe"
echo Cleanup completed.

REM Activate virtual environment
echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Warning: Virtual environment not found at venv\Scripts\activate.bat
    echo Continuing with current Python environment...
)

REM Build the executable
echo Building executable...
echo This may take a few minutes...
pyinstaller --onefile %WINDOW_MODE% --name %EXE_NAME% main.py

REM Check if build was successful
if exist "dist\%EXE_NAME%.exe" (
    echo.
    echo Build successful!
    echo Executable created: dist\%EXE_NAME%.exe
    echo.
    echo Usage:
    echo   1. Run: dist\%EXE_NAME%.exe
    echo   2. Server will start at: http://127.0.0.1:8000
    echo   3. API docs: http://127.0.0.1:8000/docs
) else (
    echo.
    echo Build failed! Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo Build process completed!
pause