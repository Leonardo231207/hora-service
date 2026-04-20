@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title HoraService

cd /d "%~dp0"

echo ========================================
echo   HoraService - Iniciando servicios
echo ========================================
echo.

set "PYTHON_FOUND=0"

python --version >nul 2>&1
if not errorlevel 1 set "PYTHON_FOUND=1"

if !PYTHON_FOUND! EQU 0 (
    if exist "C:\Python313\python.exe" set "PYTHON_FOUND=1"
    if exist "C:\Python312\python.exe" set "PYTHON_FOUND=1"
)

if !PYTHON_FOUND! EQU 0 (
    if exist "%APPDATA%\Python\Python313\python.exe" set "PYTHON_FOUND=1"
)

if !PYTHON_FOUND! EQU 0 (
    echo [1/5] Python no detectado
    echo.
    echo Descargando Python...
    
    if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set "PYFILE=python-3.13.1-amd64.exe"
    ) else (
        set "PYFILE=python-3.13.1.exe"
    )
    
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.1/!PYFILE!' -OutFile 'python-installer.exe'" 2>nul
    
    if not exist "python-installer.exe" (
        echo ERROR: No se pudo descargar.
        echo Descarga Python manualmente desde:
        echo https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo Instalando Python (3-5 minutos)...
    echo Cuando te pregunte, marca "Add Python to PATH"
    start /wait python-installer.exe /quiet PrependPath=1 Include_pip=1
    del python-installer.exe
    timeout /t 15 /nobreak >nul
)

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no disponible
    pause
    exit /b 1
)

python --version
echo [2/5] Python OK

if not exist "venv" (
    echo [3/5] Creando entorno virtual...
    python -m venv venv
) else (
    echo [3/5] Entorno virtual OK
)

echo.
echo [4/5] Instalando dependencias...
call venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Fallo al instalar
    pause
    exit /b 1
)

echo.
echo [5/5] Verificando base de datos...
call venv\Scripts\python.exe -c "from application import app, db; app.app_context().push(); db.create_all()" 2>nul
echo Base de datos OK

echo.
echo ========================================
echo   http://127.0.0.1:5000
echo   CTRL+C para detener
echo ========================================
echo.

start http://127.0.0.1:5000
start "" venv\Scripts\python.exe application.py
pause