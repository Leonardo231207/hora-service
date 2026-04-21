@echo off
chcp 65001 >nul 2>&1
title HoraService
cd /d "%~dp0"

echo Iniciando HoraService...
echo.

if not exist "venv" (
    echo Error: Entorno virtual no encontrado.
    echo Ejecuta primero setup.bat para configurar.
    pause
    exit /b 1
)

start http://127.0.0.1:5000
start cmd /k "venv\Scripts\python.exe application.py"
