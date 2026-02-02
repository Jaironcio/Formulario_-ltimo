# Solución Error MySQL XAMPP

## Problema
MySQL no inicia en XAMPP con error: "shutdown unexpectedly" o "blocked port, missing dependencies"

## Soluciones en Orden de Prioridad

### Solución 1: Puerto 3306 Ocupado (MÁS COMÚN)

**Verificar:**
```cmd
netstat -ano | findstr :3306
```

**Si aparece un PID usando el puerto:**

**Opción A - Detener el proceso:**
```cmd
taskkill /F /PID [numero_que_aparece]
```

**Opción B - Cambiar puerto XAMPP:**
1. Abrir `C:\xampp\mysql\bin\my.ini`
2. Buscar línea: `port=3306`
3. Cambiar a: `port=3307`
4. Guardar y reiniciar XAMPP

**Si usas puerto 3307, actualizar conexión Django:**
```python
# En config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'incidencias_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3307',  # Cambiar aquí
    }
}
```

### Solución 2: MySQL como Servicio Windows

**Detener servicio:**
```cmd
net stop MySQL
net stop MySQL80
```

**Deshabilitar permanentemente:**
1. Presionar `Win + R`
2. Escribir: `services.msc`
3. Buscar "MySQL" o "MySQL80"
4. Click derecho → Propiedades
5. Tipo de inicio: **Deshabilitado**
6. Aplicar y Aceptar

### Solución 3: Archivos Corruptos

**IMPORTANTE: Hacer backup primero**

```cmd
# 1. Detener XAMPP completamente
# 2. Ir a: C:\xampp\mysql\data
# 3. Copiar toda la carpeta 'data' a otro lugar (backup)
# 4. Eliminar estos archivos:
#    - ibdata1
#    - ib_logfile0
#    - ib_logfile1
# 5. Copiar archivos limpios desde: C:\xampp\mysql\backup
# 6. Iniciar MySQL en XAMPP
```

### Solución 4: Reinstalar MySQL en XAMPP

Si nada funciona:
1. Backup de bases de datos importantes
2. Desinstalar XAMPP
3. Eliminar carpeta `C:\xampp`
4. Descargar XAMPP nuevo desde: https://www.apachefriends.org
5. Instalar y configurar

## Script Automático

Ejecutar el archivo `fix_mysql_xampp.bat` para diagnóstico automático.

## Verificación Final

Después de aplicar solución:
1. Abrir XAMPP Control Panel
2. Click en "Start" de MySQL
3. Debe aparecer en verde sin errores
4. Verificar en navegador: http://localhost/phpmyadmin

## Notas para tu Proyecto

Tu proyecto Django usa SQLite por defecto (`db.sqlite3`), pero si necesitas MySQL:

1. Instalar conector:
```cmd
pip install mysqlclient
```

2. Crear base de datos en phpMyAdmin:
```sql
CREATE DATABASE incidencias_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Actualizar `config/settings.py` con configuración MySQL (ver arriba)

4. Migrar:
```cmd
python manage.py migrate
```
