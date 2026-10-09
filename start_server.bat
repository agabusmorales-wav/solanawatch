@echo off
title SolanaWatch IoT Backend & Decision Support System
echo ====================================================================
echo  🌿 Starting SolanaWatch IoT REST API Backend Server...
echo ====================================================================
echo.
cd /d "%~dp0backend"
node server.js
pause
