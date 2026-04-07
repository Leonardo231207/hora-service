@echo off
chcp 65001 >nul
title HoraService

echo ========================================
echo   HoraService - Iniciando servicios
echo ========================================
echo.

REM Verificar si existe entorno virtual
if not exist "venv" (
    echo [1/3] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar e instalar dependencias
echo.
echo [2/3] Instalando/actualizando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Fallo al instalar dependencias
    pause
    exit /b 1
)

REM Verificar base de datos
echo.
echo [3/3] Verificando base de datos...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de datos OK')" 2>nul
if errorlevel 1 (
    echo WARNING: Problema al verificar DB, se creara al iniciar
)

REM Iniciar servidor
echo.
echo ========================================
echo   Servidor iniciando en http://127.0.0.1:5000
echo   Presiona CTRL+C para detener
echo ========================================
echo.

python application.py