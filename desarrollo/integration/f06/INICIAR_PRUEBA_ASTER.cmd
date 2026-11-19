@echo off
setlocal
cd /d "%~dp0"
echo Preparando prueba F06 - Sistema Aster...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INICIAR_PRUEBA_ASTER.ps1"
if errorlevel 1 (
 echo.
 echo La preparacion ha fallado. Copia o fotografia el mensaje anterior.
 pause
)
endlocal
