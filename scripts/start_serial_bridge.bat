@echo off
title SolanaWatch - USB Serial to Cloud Bridge
echo ==================================================================
echo   SOLANAWATCH: USB SERIAL TO CLOUD BRIDGE (LAPTOP FORWARDER)
echo ==================================================================
echo.
set /p CLOUD_URL="Enter your live Vercel URL (or press Enter for http://localhost:5000/api/telemetry): "

if "%CLOUD_URL%"=="" (
    set CLOUD_URL=http://localhost:5000/api/telemetry
)

echo.
echo Starting bridge to: %CLOUD_URL%
echo.
python "%~dp0serial_bridge.py" --url %CLOUD_URL%
pause
