# Guía de Instalación - Sistema PHP

## ✅ Sistema Creado Exitosamente

He creado un sistema PHP completo con **todas las funcionalidades de seguridad** equivalentes a Django.

## 📁 Ubicación del Sistema

```
C:\xampp_new\htdocs\incidencias_php\
```

## 🚀 Pasos de Instalación

### 1. Verificar que MySQL esté funcionando

1. Abrir XAMPP Control Panel
2. Verificar que **Apache** y **MySQL** estén en verde (iniciados)
3. Si MySQL no inicia, ejecutar: `fix_mysql_xampp_new.bat`

### 2. Crear la Base de Datos

**Opción A - Desde phpMyAdmin (Recomendado):**

1. Abrir navegador: http://localhost/phpmyadmin
2. Click en "SQL" (pestaña superior)
3. Copiar y pegar el contenido de: `C:\xampp_new\htdocs\incidencias_php\crear_base_datos.sql`
4. Click en "Continuar"

**Opción B - Desde línea de comandos:**

```cmd
cd C:\xampp_new\mysql\bin
mysql -u root -p < C:\xampp_new\htdocs\incidencias_php\crear_base_datos.sql
```
(Presionar Enter cuando pida contraseña, está vacía)

### 3. Acceder al Sistema

1. Abrir navegador
2. Ir a: **http://localhost/incidencias_php**
3. Login con credenciales por defecto:
   - **Usuario:** admin
   - **Contraseña:** admin123

### 4. Cambiar Contraseña del Administrador

1. Ir a phpMyAdmin: http://localhost/phpmyadmin
2. Base de datos: `cermaq_incidencias`
3. Tabla: `usuarios`
4. Editar el usuario `admin`
5. En el campo `password`, usar este generador: https://bcrypt-generator.com/
6. Generar hash de tu nueva contraseña
7. Reemplazar el hash en la base de datos

## 🔒 Características de Seguridad Implementadas

### ✅ Autenticación
- Login con contraseñas hasheadas (bcrypt)
- Sessions seguras con regeneración de ID
- Protección contra fuerza bruta
- Logout seguro

### ✅ Protección CSRF
- Token único por sesión
- Validación en todos los formularios POST
- Función `csrf_field()` en cada formulario

### ✅ Protección SQL Injection
- PDO con Prepared Statements
- NUNCA concatenación directa de SQL
- Validación de tipos de datos

### ✅ Protección XSS
- Sanitización de todos los inputs
- `htmlspecialchars()` en todos los outputs
- Validación de archivos subidos

### ✅ Control de Acceso
- Middleware `verificar_login()` en todas las páginas
- Sistema de roles (admin/usuario)
- Protección de rutas sensibles

## 📊 Funcionalidades del Sistema

### 1. Dashboard
- Estadísticas de incidencias
- Últimas incidencias registradas
- Accesos rápidos

### 2. Incidencias
- **Nueva Incidencia:** Formulario completo con validación
- **Lista de Incidencias:** Filtros por centro, estado, prioridad, fechas
- **Ver Detalle:** Información completa + actualización de estado
- **Adjuntar Archivos:** Soporte para imágenes y PDFs

### 3. Control Diario de Sensores
- Registro por fecha y centro
- Organizado por sistemas
- Tres turnos: Mañana, Tarde, Noche
- Estados: NORMAL, ALTO, BAJO
- Valores numéricos con límites configurados
- Observaciones por sensor

### 4. Historial de Sensores
- Consulta histórica
- Filtros por centro y rango de fechas
- Visualización de estados y valores

### 5. Reporte de Cámaras
- Registro de estado de cámaras
- Estados: Operativa, Falla, Mantenimiento
- Historial de reportes recientes

## 🗄️ Estructura de la Base de Datos

### Tablas Creadas:

1. **usuarios** - Autenticación y perfiles
2. **incidencias** - Registro de incidencias
3. **sensores** - Catálogo de sensores por centro
4. **control_diario** - Lecturas diarias de sensores
5. **reporte_camaras** - Reportes de cámaras

## 📝 Migrar Datos de Django (Opcional)

Si quieres migrar tus datos existentes de SQLite a MySQL:

### Opción 1: Exportar/Importar Manual

1. Desde Django, exportar datos:
```bash
python manage.py dumpdata incidencias --indent 2 > datos.json
```

2. Crear script PHP para importar (te lo puedo crear si lo necesitas)

### Opción 2: Copiar Manualmente

Abrir ambas bases de datos y copiar registros importantes manualmente desde phpMyAdmin.

## 🎨 Personalización

### Cambiar Colores/Estilos

Editar: `C:\xampp_new\htdocs\incidencias_php\assets\css\style.css`

### Agregar Nuevos Centros

Editar: `C:\xampp_new\htdocs\incidencias_php\includes\functions.php`

Función: `obtener_centros()`

### Agregar Sensores

1. Ir a phpMyAdmin
2. Tabla: `sensores`
3. Insertar nuevos registros con:
   - centro
   - sistema
   - equipo
   - tipo_medicion
   - limite_min
   - limite_max
   - unidad

## 🔧 Solución de Problemas

### Error: "Cannot connect to database"

- Verificar que MySQL esté corriendo en XAMPP
- Verificar credenciales en `config/database.php`

### Error: "Table doesn't exist"

- Ejecutar el archivo `crear_base_datos.sql` en phpMyAdmin

### No puedo subir archivos

- Verificar permisos de carpeta `uploads/`
- Verificar `upload_max_filesize` en `php.ini`

### Páginas en blanco

- Activar errores en `php.ini`:
  ```ini
  display_errors = On
  error_reporting = E_ALL
  ```

## 📱 Acceso desde Otros Dispositivos

Para acceder desde otros equipos en la red local:

1. Obtener IP del servidor:
```cmd
ipconfig
```

2. En otros dispositivos, abrir:
```
http://[IP_DEL_SERVIDOR]/incidencias_php
```

Ejemplo: `http://192.168.1.100/incidencias_php`

## 🚀 Próximos Pasos Recomendados

1. ✅ Cambiar contraseña del admin
2. ✅ Crear usuarios para cada centro
3. ✅ Configurar sensores en la base de datos
4. ✅ Probar el sistema con datos reales
5. ⏳ Migrar datos de Django (si aplica)
6. ⏳ Configurar backup automático de MySQL

## 💾 Backup de la Base de Datos

### Backup Manual

Desde phpMyAdmin:
1. Seleccionar base de datos `cermaq_incidencias`
2. Click en "Exportar"
3. Método: Rápido
4. Formato: SQL
5. Click en "Continuar"

### Backup por Línea de Comandos

```cmd
cd C:\xampp_new\mysql\bin
mysqldump -u root cermaq_incidencias > backup_cermaq_%date%.sql
```

## ✅ Checklist de Instalación

- [ ] MySQL funcionando en XAMPP
- [ ] Base de datos creada (`cermaq_incidencias`)
- [ ] Tablas creadas correctamente
- [ ] Login funciona con admin/admin123
- [ ] Cambiar contraseña del admin
- [ ] Crear usuarios adicionales
- [ ] Configurar sensores
- [ ] Probar crear incidencia
- [ ] Probar control diario
- [ ] Probar reporte de cámaras

## 📞 Resumen

**Sistema PHP completo y funcional** con:
- ✅ Seguridad nivel profesional
- ✅ Todas las funcionalidades de Django
- ✅ Interfaz moderna con Bootstrap 5
- ✅ Base de datos MySQL robusta
- ✅ Fácil de mantener y extender

**URL del sistema:** http://localhost/incidencias_php

**Usuario inicial:** admin / admin123
