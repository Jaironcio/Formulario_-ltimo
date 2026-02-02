@echo off
echo ========================================
echo LIBERANDO PUERTO 3306 PARA MYSQL
echo ========================================
echo.

echo Deteniendo servicios MySQL de Windows...
net stop MySQL 2>nul
net stop MySQL80 2>nul
net stop MySQLRouter 2>nul
echo.

echo Buscando procesos en puerto 3306...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3306 ^| findstr LISTENING') do (
    echo Encontrado proceso PID: %%a
    echo Deteniendo proceso...
    taskkill /F /PID %%a
)
echo.

echo Verificando si el puerto esta libre...
netstat -ano | findstr :3306
if errorlevel 1 (
    echo.
    echo *** PUERTO 3306 LIBERADO ***
    echo Ahora puedes iniciar MySQL en XAMPP
) else (
    echo.
    echo Aun hay procesos usando el puerto 3306
    echo Intenta reiniciar el equipo
)
echo.
pause
