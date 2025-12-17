@echo off
REM Script para ejecutar la aplicación de selección de transportistas
REM Activa el entorno virtual y ejecuta el programa principal

echo ====================================
echo   Transportistas - Sistema de Seleccion
echo ====================================
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Ejecutar aplicación
python main.py

REM Pausar al finalizar (comentar esta línea si no se desea)
pause
