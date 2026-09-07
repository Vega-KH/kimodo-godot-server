@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: The project virtual environment was not found.
    echo Expected: %CD%\.venv\Scripts\python.exe
    echo Complete the development installation before using this launcher.
    pause
    exit /b 1
)

set "TEXT_ENCODER_MODE=local"
set "TEXT_ENCODER_DEVICE=cpu"

echo Starting Kimodo Godot Server on http://127.0.0.1:8000
echo Motion model: automatic CUDA device selection
echo Text encoder: full local LLM2Vec on CPU
echo Press Ctrl+C to stop the server.
echo.

".venv\Scripts\python.exe" -m motionmcp_kimodo --text-encoder-mode local %*
set "KIMODO_SERVER_EXIT=%ERRORLEVEL%"

echo.
if not "%KIMODO_SERVER_EXIT%"=="0" echo Server exited with code %KIMODO_SERVER_EXIT%.
if not defined KIMODO_NO_PAUSE pause
exit /b %KIMODO_SERVER_EXIT%
