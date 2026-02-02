@echo off
echo ========================================
echo REPARACION MYSQL - XAMPP_NEW
echo ========================================
echo.
echo IMPORTANTE: Cierra XAMPP completamente antes de continuar
echo.
pause

echo.
echo [1/3] Deteniendo servicios MySQL...
net stop MySQL 2>nul
net stop MySQL80 2>nul
echo.

echo [2/3] Eliminando archivos corruptos...
cd /d "C:\xampp_new\mysql\data"

if exist ibdata1 (
    echo Eliminando ibdata1...
    del /F /Q ibdata1
)
if exist ib_logfile0 (
    echo Eliminando ib_logfile0...
    del /F /Q ib_logfile0
)
if exist ib_logfile1 (
    echo Eliminando ib_logfile1...
    del /F /Q ib_logfile1
)
if exist aria_log_control (
    echo Eliminando aria_log_control...
    del /F /Q aria_log_control
)
if exist aria_log.00000001 (
    echo Eliminando aria_log.00000001...
    del /F /Q aria_log.00000001
)
echo.

echo [3/3] Verificando si hay backup disponible...
if exist "C:\xampp_new\mysql\backup\ibdata1" (
    echo Copiando archivos desde backup...
    copy "C:\xampp_new\mysql\backup\ibdata1" "C:\xampp_new\mysql\data\"
    copy "C:\xampp_new\mysql\backup\ib_logfile0" "C:\xampp_new\mysql\data\"
    copy "C:\xampp_new\mysql\backup\ib_logfile1" "C:\xampp_new\mysql\data\"
    echo Archivos restaurados desde backup
) else (
    echo No hay backup, MySQL creara archivos nuevos
)
echo.

echo ========================================
echo REPARACION COMPLETADA
echo ========================================
echo.
echo SIGUIENTE PASO:
echo 1. Abre XAMPP Control Panel
echo 2. Click en START de MySQL
echo 3. Deberia iniciar correctamente
echo.
echo Si sigue fallando, presiona "Logs" en XAMPP
echo y copia el contenido del error aqui
echo.
pause
