"""
Script para corregir comillas tipograficas en archivos HTML
"""
import os
import glob

def fix_quotes_in_file(filepath):
    """Reemplaza comillas tipograficas por comillas rectas"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar comillas tipograficas
        original_content = content
        content = content.replace(''', "'")  # Comilla simple izquierda
        content = content.replace(''', "'")  # Comilla simple derecha
        content = content.replace('"', '"')  # Comilla doble izquierda
        content = content.replace('"', '"')  # Comilla doble derecha
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return False

# Buscar y corregir archivos HTML
templates_dir = 'templates'
fixed_count = 0

if os.path.exists(templates_dir):
    html_files = glob.glob(os.path.join(templates_dir, '*.html'))
    
    print(f"\nEncontrados {len(html_files)} archivos HTML")
    print("Corrigiendo comillas tipograficas...\n")
    
    for html_file in html_files:
        if fix_quotes_in_file(html_file):
            print(f"  Corregido: {os.path.basename(html_file)}")
            fixed_count += 1
        else:
            print(f"  Sin cambios: {os.path.basename(html_file)}")
    
    print(f"\nTotal de archivos corregidos: {fixed_count}")
else:
    print(f"Error: No se encuentra la carpeta {templates_dir}")
