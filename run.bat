@echo off
title C-TRONICS SOLUCIONES - Sistema de Gestion Comercial
echo ================================================================
echo   C-TRONICS SOLUCIONES - Iniciando el sistema...
echo ================================================================
echo.

REM Verificar que Python este instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo         Descargalo desde: https://www.python.org/downloads/
    echo         Marca la casilla "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

REM Instalar Flask si no esta instalado
echo [1/2] Verificando dependencias...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo [2/2] Iniciando servidor Flask...
echo.
echo   Cuando aparezca "Running on http://127.0.0.1:5000"
echo   abre tu navegador en:  http://localhost:5000
echo   Usuario: admin   Contrasena: admin123
echo.
echo ================================================================

REM Abrir navegador despues de 3 segundos
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

python app.py
pause
