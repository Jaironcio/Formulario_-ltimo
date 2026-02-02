@echo off
echo ========================================
echo SOLUCION RAPIDA MYSQL XAMPP
echo ========================================
echo.
echo Este script eliminara archivos corruptos de MySQL
echo IMPORTANTE: Cierra XAMPP antes de continuar
echo.
pause

echo.
echo Eliminando archivos corruptos...
cd /d C:\xampp\mysql\data

if exist ibdata1 del /F /Q ibdata1
if exist ib_logfile0 del /F /Q ib_logfile0
if exist ib_logfile1 del /F /Q ib_logfile1
if exist aria_log_control del /F /Q aria_log_control
if exist aria_log.00000001 del /F /Q aria_log.00000001

echo.
echo Archivos eliminados.
echo.
echo SIGUIENTE PASO:
echo 1. Abre XAMPP Control Panel
echo 2. Click en START de MySQL
echo 3. MySQL creara archivos nuevos automaticamente
echo.
echo Si sigue sin funcionar, revisa los logs:
echo - Click en "Logs" de MySQL en XAMPP
echo - Busca el error especifico
echo.
pause
