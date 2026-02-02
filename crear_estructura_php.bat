@echo off
echo Creando estructura PHP...

cd /d "C:\xampp_new\htdocs"
mkdir incidencias_php 2>nul
cd incidencias_php

mkdir config 2>nul
mkdir includes 2>nul
mkdir assets 2>nul
mkdir assets\css 2>nul
mkdir assets\js 2>nul
mkdir assets\img 2>nul
mkdir pages 2>nul
mkdir pages\incidencias 2>nul
mkdir pages\sensores 2>nul
mkdir pages\reportes 2>nul
mkdir api 2>nul
mkdir uploads 2>nul

echo Estructura creada en: C:\xampp_new\htdocs\incidencias_php
echo.
echo Ahora copiare los archivos PHP...
pause
