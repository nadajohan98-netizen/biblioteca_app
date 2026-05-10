# seed.py - Versión infalible
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from biblioteca.container import build_services

def inicializar_datos():
    print(" Iniciando seed de datos...\n")
    
    libro_srv, usuario_srv, prestamo_srv = build_services()
    
    # VERIFICACIÓN DIRECTA desde el archivo JSON
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'libros.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            libros_en_json = json.load(f)
        isbn_existentes = {libro.get('isbn', '').strip().upper() for libro in libros_en_json}
        print(f"   Libros en base de datos: {len(libros_en_json)}")
        print(f"   ISBNs existentes: {isbn_existentes}\n")
    except:
        isbn_existentes = set()
        print("⚠️ No se encontró archivo de libros o está vacío\n")
    
    # LIBROS A CREAR
    libros_nuevos = [
        {"titulo": "Clean Code", "autor": "Robert Martin", "isbn": "9780132350884", "stock": 5},
        {"titulo": "Design Patterns", "autor": "Gang of Four", "isbn": "9780201633610", "stock": 3},
        {"titulo": "Python Crash Course", "autor": "Eric Matthes", "isbn": "9781593279288", "stock": 10},
        {"titulo": "The Pragmatic Programmer", "autor": "David Thomas", "isbn": "9780135957059", "stock": 4},
    ]
    
    # CREAR SOLO LOS QUE NO EXISTEN
    creados = 0
    saltados = 0
    for book in libros_nuevos:
        isbn_check = book["isbn"].strip().upper()
        if isbn_check in isbn_existentes:
            print(f"⏭️  SKIP: {book['titulo']} (ya existe)")
            saltados += 1
        else:
            try:
                libro_srv.crear(book["titulo"], book["autor"], book["isbn"], book["stock"])
                print(f"✅ CREADO: {book['titulo']}")
                creados += 1
            except Exception as e:
                print(f"❌ ERROR: {book['titulo']} - {e}")
    
    print(f"\n RESUMEN: {creados} creados, {saltados} saltados")
    print("\n ¡Seed completado!")
    print("   Presiona F5 en el navegador para ver los cambios")

if __name__ == "__main__":
    inicializar_datos()