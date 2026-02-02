@echo off
echo ========================================
echo REPARACION MYSQL XAMPP
echo ========================================
echo.
echo IMPORTANTE: Este script hara backup y reparara archivos de MySQL
echo.
pause

set XAMPP_PATH=C:\xampp
set MYSQL_DATA=%XAMPP_PATH%\mysql\data
set BACKUP_PATH=%XAMPP_PATH%\mysql\backup

echo.
echo [1/4] Verificando rutas...
if not exist "%MYSQL_DATA%" (
    echo ERROR: No se encuentra %MYSQL_DATA%
    echo Verifica que XAMPP este instalado en C:\xampp
    pause
    exit /b
)
echo Ruta encontrada: %MYSQL_DATA%
echo.

echo [2/4] Creando backup de seguridad...
set BACKUP_FOLDER=%MYSQL_DATA%_backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_FOLDER=%BACKUP_FOLDER: =0%
echo Backup en: %BACKUP_FOLDER%
xcopy "%MYSQL_DATA%" "%BACKUP_FOLDER%\" /E /I /H /Y
echo.

echo [3/4] Eliminando archivos corruptos...
cd /d "%MYSQL_DATA%"
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
if exist aria_log.* (
    echo Eliminando aria_log.*...
    del /F /Q aria_log.*
)
echo.

echo [4/4] Copiando archivos limpios desde backup...
if exist "%BACKUP_PATH%\ibdata1" (
    copy "%BACKUP_PATH%\ibdata1" "%MYSQL_DATA%\"
    copy "%BACKUP_PATH%\ib_logfile0" "%MYSQL_DATA%\"
    copy "%BACKUP_PATH%\ib_logfile1" "%MYSQL_DATA%\"
    echo Archivos restaurados desde backup de XAMPP
) else (
    echo No se encontro backup de XAMPP, MySQL creara archivos nuevos
)
echo.

echo ========================================
echo REPARACION COMPLETADA
echo ========================================
echo.
echo Backup guardado en: %BACKUP_FOLDER%
echo.
echo SIGUIENTE PASO:
echo 1. Abre XAMPP Control Panel
echo 2. Click en START de MySQL
echo 3. Deberia iniciar correctamente
echo.
pause
