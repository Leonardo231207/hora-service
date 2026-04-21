@echo off
chcp 65001 >nul 2>&1
title HoraService - Configuracion
cd /d "%~dp0"

echo ========================================
echo   HoraService - Configuracion
echo ========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no instalado
    echo Descarga de: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
) else (
    echo Entorno virtual ya existe
)

echo.
echo Instalando dependencias...
call venv\Scripts\pip.exe install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo Verificando base de datos...
call venv\Scripts\python.exe -c "from application import app, db; app.app_context().push(); db.create_all()"

echo.
echo ========================================
echo   Listo! Ejecuta iniciar.bat para arrancar
echo ========================================
pause