# Instalación para Sistema PHP

## ✅ Lo Que Ya Tienes

- **XAMPP** (Apache + MySQL + PHP)
- **Navegador web**

## 📦 Lo Que Necesitas Instalar

### 1. Composer (Gestor de dependencias PHP)

**Descargar:**
https://getcomposer.org/Composer-Setup.exe

**Instalación:**
1. Ejecutar el instalador
2. Seleccionar el PHP de XAMPP: `C:\xampp\php\php.exe`
3. Siguiente → Siguiente → Instalar
4. Verificar instalación:
```cmd
composer --version
```

### 2. Extensiones PHP (Ya incluidas en XAMPP)

Verificar que estén habilitadas en `C:\xampp\php\php.ini`:

```ini
extension=mysqli
extension=pdo_mysql
extension=mbstring
extension=openssl
extension=curl
extension=fileinfo
extension=gd
extension=zip
```

**Para habilitar una extensión:**
1. Abrir `C:\xampp\php\php.ini`
2. Buscar la línea (ejemplo: `;extension=mysqli`)
3. Quitar el `;` al inicio: `extension=mysqli`
4. Guardar y reiniciar Apache en XAMPP

## 🔧 Configuración Inicial

### Paso 1: Reparar MySQL

Ejecuta el script que creamos:
```cmd
reparar_mysql_xampp.bat
```

### Paso 2: Iniciar Servicios XAMPP

1. Abrir XAMPP Control Panel
2. Start → **Apache**
3. Start → **MySQL**
4. Ambos deben aparecer en verde

### Paso 3: Verificar phpMyAdmin

Abrir navegador: http://localhost/phpmyadmin

Deberías ver la interfaz de phpMyAdmin sin errores.

## 📚 Librerías PHP que Instalaremos (Opcional)

Estas se instalan después con Composer:

```bash
# PHPSpreadsheet - Para leer/escribir Excel
composer require phpoffice/phpspreadsheet

# PHPMailer - Para enviar emails
composer require phpmailer/phpmailer

# Chart.js - Para gráficos (vía CDN, no requiere Composer)
```

## 🚀 Estructura del Proyecto PHP

```
C:\xampp\htdocs\incidencias\
├── config/
│   ├── database.php          # Conexión MySQL
│   └── config.php            # Configuración general
├── includes/
│   ├── header.php            # Header común
│   ├── footer.php            # Footer común
│   └── functions.php         # Funciones auxiliares
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── img/
├── pages/
│   ├── login.php
│   ├── dashboard.php
│   ├── incidencias/
│   │   ├── nueva.php
│   │   ├── lista.php
│   │   └── ver.php
│   ├── sensores/
│   │   ├── control_diario.php
│   │   └── historial.php
│   └── reportes/
│       └── camaras.php
├── api/
│   ├── guardar_incidencia.php
│   ├── guardar_control_diario.php
│   └── obtener_sensores.php
├── index.php                 # Página principal
└── logout.php
```

## 🗄️ Base de Datos

Crearemos estas tablas en MySQL:

1. **usuarios** - Login del sistema
2. **incidencias** - Registro de incidencias
3. **sensores** - Catálogo de sensores
4. **control_diario** - Lecturas diarias de sensores
5. **reporte_camaras** - Reportes de cámaras

## ⚡ Ventajas de PHP vs Django

| Característica | Django (Actual) | PHP (Nuevo) |
|----------------|-----------------|-------------|
| Hosting | Requiere VPS/PaaS | Hosting compartido barato |
| Despliegue | Complejo | Subir archivos por FTP |
| Base de datos | SQLite (limitado) | MySQL (robusto) |
| Integración Excel | Compleja | PHPSpreadsheet nativo |
| Curva aprendizaje | Alta | Media-baja |
| Mantenimiento | Requiere conocimientos Python | Más simple |

## 📝 Próximos Pasos

1. ✅ Instalar Composer
2. ✅ Reparar MySQL en XAMPP
3. ✅ Verificar que Apache y MySQL funcionen
4. ⏳ Crear estructura del proyecto
5. ⏳ Crear base de datos
6. ⏳ Implementar sistema

## 🆘 Solución de Problemas

### Apache no inicia
- Puerto 80 ocupado por Skype/IIS
- Cambiar puerto en `C:\xampp\apache\conf\httpd.conf`
- Buscar: `Listen 80` → Cambiar a: `Listen 8080`

### MySQL no inicia
- Ejecutar `reparar_mysql_xampp.bat`
- Ver `SOLUCION_MYSQL_XAMPP.md`

### Composer no se instala
- Verificar que PHP esté en PATH
- Usar el PHP de XAMPP: `C:\xampp\php\php.exe`

## 📞 ¿Listo para Continuar?

Una vez que tengas:
- ✅ XAMPP funcionando (Apache + MySQL en verde)
- ✅ Composer instalado
- ✅ phpMyAdmin accesible

Avísame y empezamos a crear el sistema PHP completo.
