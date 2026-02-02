@echo off
echo ========================================
echo DIAGNOSTICO Y SOLUCION MYSQL XAMPP
echo ========================================
echo.

echo [1/5] Verificando puertos ocupados...
netstat -ano | findstr :3306
echo.

echo [2/5] Verificando servicios MySQL activos...
sc query MySQL
sc query MySQL80
echo.

echo [3/5] Deteniendo servicios MySQL si existen...
net stop MySQL 2>nul
net stop MySQL80 2>nul
echo.

echo [4/5] Verificando procesos mysqld.exe...
tasklist | findstr mysqld.exe
echo.

echo ========================================
echo SOLUCIONES POSIBLES:
echo ========================================
echo.
echo Si hay un proceso usando el puerto 3306:
echo   - Opcion A: Detener el proceso con: taskkill /F /PID [numero_pid]
echo   - Opcion B: Cambiar puerto de XAMPP MySQL a 3307
echo.
echo Si hay archivos corruptos en C:\xampp\mysql\data:
echo   1. Hacer backup de la carpeta 'data'
echo   2. Eliminar: ibdata1, ib_logfile0, ib_logfile1
echo   3. Copiar archivos limpios desde C:\xampp\mysql\backup
echo.
echo Si MySQL corre como servicio Windows:
echo   - Ya se intento detener arriba
echo   - Verificar en services.msc y deshabilitarlo
echo.
pause
