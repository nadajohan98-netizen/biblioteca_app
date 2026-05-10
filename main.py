"""
main.py — Capa de presentación (CLI).
SRP: muestra menús y captura input. No contiene lógica de negocio.

Ejecutar desde la carpeta biblioteca_app/:
    python main.py
"""
import sys
import os

# Asegura que 'biblioteca' sea importable desde cualquier ubicación
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from biblioteca.container import build_services
from biblioteca.services import BibliotecaError
from biblioteca.models.prestamo import EstadoPrestamo


def sep(titulo: str = ""):
    print("\n" + "─" * 52)
    if titulo:
        print(f"  {titulo}")
        print("─" * 52)


# ──────────────────────────────────────────────────────────────
# Menú Libros
# ──────────────────────────────────────────────────────────────

def menu_libros(srv):
    while True:
        sep("📚  Gestión de Libros")
        print("  1. Listar libros")
        print("  2. Crear libro")
        print("  3. Editar libro")
        print("  4. Eliminar libro")
        print("  0. Volver")
        op = input("\nOpción: ").strip()

        if op == "1":
            libros = srv.listar()
            if not libros:
                print("  (sin libros registrados)")
            for l in libros:
                print(f"\n  [{l.id[:8]}] {l.titulo}  —  {l.autor}")
                print(f"           ISBN: {l.isbn}  |  Stock: {l.stock_disponible}/{l.stock_total}")

        elif op == "2":
            titulo = input("Título  : ").strip()
            autor  = input("Autor   : ").strip()
            isbn   = input("ISBN    : ").strip()
            stock  = int(input("Stock   : ").strip())
            try:
                l = srv.crear(titulo, autor, isbn, stock)
                print(f"\n  ✅ Creado [{l.id[:8]}] {l.titulo}")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "3":
            _listar_ids_libros(srv)
            lid = input("ID libro (primeros 8): ").strip()
            libro = _buscar_libro(srv, lid)
            if not libro:
                continue
            titulo = input(f"  Título [{libro.titulo}]: ").strip() or None
            autor  = input(f"  Autor  [{libro.autor}]: ").strip() or None
            st_s   = input(f"  Stock total [{libro.stock_total}]: ").strip()
            stock  = int(st_s) if st_s else None
            try:
                l = srv.editar(libro.id, titulo=titulo, autor=autor, stock_total=stock)
                print(f"\n  ✅ Actualizado: {l.titulo}")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "4":
            _listar_ids_libros(srv)
            lid = input("ID libro (primeros 8): ").strip()
            libro = _buscar_libro(srv, lid)
            if not libro:
                continue
            if input(f"  ¿Eliminar '{libro.titulo}'? (s/n): ").strip() == "s":
                try:
                    srv.eliminar(libro.id)
                    print("  ✅ Eliminado.")
                except BibliotecaError as e:
                    print(f"\n  ❌ {e}")

        elif op == "0":
            break


def _listar_ids_libros(srv):
    for l in srv.listar():
        print(f"  [{l.id[:8]}] {l.titulo}  (disponibles: {l.stock_disponible})")


def _buscar_libro(srv, prefijo):
    libro = next((l for l in srv.listar() if l.id.startswith(prefijo)), None)
    if not libro:
        print("  Libro no encontrado.")
    return libro


# ──────────────────────────────────────────────────────────────
# Menú Usuarios
# ──────────────────────────────────────────────────────────────

def menu_usuarios(srv):
    while True:
        sep("👤  Gestión de Usuarios")
        print("  1. Listar usuarios")
        print("  2. Registrar usuario")
        print("  3. Editar usuario")
        print("  4. Desactivar usuario")
        print("  0. Volver")
        op = input("\nOpción: ").strip()

        if op == "1":
            usuarios = srv.listar()
            if not usuarios:
                print("  (sin usuarios registrados)")
            for u in usuarios:
                est = "✅ activo" if u.activo else "🔴 inactivo"
                print(f"\n  [{u.id[:8]}] {u.nombre}  —  {u.email}")
                print(f"           Estado: {est}  |  Límite préstamos: {u.max_prestamos}")

        elif op == "2":
            nombre = input("Nombre      : ").strip()
            email  = input("Email       : ").strip()
            lim_s  = input("Límite préstamos [3]: ").strip()
            limite = int(lim_s) if lim_s else 3
            try:
                u = srv.registrar(nombre, email, max_prestamos=limite)
                print(f"\n  ✅ Registrado [{u.id[:8]}] {u.nombre}")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "3":
            _listar_ids_usuarios(srv)
            uid = input("ID usuario (primeros 8): ").strip()
            usuario = _buscar_usuario(srv, uid)
            if not usuario:
                continue
            nombre = input(f"  Nombre [{usuario.nombre}]: ").strip() or None
            lim_s  = input(f"  Límite [{usuario.max_prestamos}]: ").strip()
            limite = int(lim_s) if lim_s else None
            try:
                u = srv.editar(usuario.id, nombre=nombre, max_prestamos=limite)
                print(f"\n  ✅ Actualizado: {u.nombre}")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "4":
            _listar_ids_usuarios(srv)
            uid = input("ID usuario (primeros 8): ").strip()
            usuario = _buscar_usuario(srv, uid)
            if not usuario:
                continue
            try:
                srv.desactivar(usuario.id)
                print(f"  ✅ '{usuario.nombre}' desactivado.")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "0":
            break


def _listar_ids_usuarios(srv):
    for u in srv.listar():
        est = "activo" if u.activo else "inactivo"
        print(f"  [{u.id[:8]}] {u.nombre}  ({est})")


def _buscar_usuario(srv, prefijo):
    usuario = next((u for u in srv.listar() if u.id.startswith(prefijo)), None)
    if not usuario:
        print("  Usuario no encontrado.")
    return usuario


# ──────────────────────────────────────────────────────────────
# Menú Préstamos
# ──────────────────────────────────────────────────────────────

def menu_prestamos(p_srv, l_srv, u_srv):
    while True:
        sep("📖  Gestión de Préstamos")
        print("  1. Listar todos los préstamos")
        print("  2. Préstamos activos de un usuario")
        print("  3. Realizar préstamo")
        print("  4. Devolver libro")
        print("  5. Ver préstamos vencidos")
        print("  0. Volver")
        op = input("\nOpción: ").strip()

        if op == "1":
            prestamos = p_srv.listar_todos()
            if not prestamos:
                print("  (sin préstamos)")
            libros   = {l.id: l for l in l_srv.listar()}
            usuarios = {u.id: u for u in u_srv.listar()}
            for p in prestamos:
                titulo = libros.get(p.libro_id, type("", (), {"titulo": p.libro_id[:8]})()).titulo
                nombre = usuarios.get(p.usuario_id, type("", (), {"nombre": p.usuario_id[:8]})()).nombre
                vc = "  ⚠️ VENCIDO" if p.esta_vencido() else ""
                print(f"\n  [{p.id[:8]}] '{titulo}'  →  {nombre}")
                print(f"           Estado: {p.estado}{vc}  |  Vence: {p.fecha_vencimiento[:10]}")

        elif op == "2":
            _listar_ids_usuarios(u_srv)
            uid = input("ID usuario (primeros 8): ").strip()
            usuario = _buscar_usuario(u_srv, uid)
            if not usuario:
                continue
            activos = p_srv.listar_por_usuario(usuario.id)
            libros  = {l.id: l for l in l_srv.listar()}
            print(f"\n  Préstamos activos de {usuario.nombre}: {len(activos)}")
            for p in activos:
                titulo = libros.get(p.libro_id, type("", (), {"titulo": p.libro_id[:8]})()).titulo
                print(f"  [{p.id[:8]}] '{titulo}'  |  vence: {p.fecha_vencimiento[:10]}")

        elif op == "3":
            print("\n  — Usuarios activos —")
            for u in u_srv.listar():
                if u.activo:
                    n = len(p_srv.listar_por_usuario(u.id))
                    print(f"  [{u.id[:8]}] {u.nombre}  ({n}/{u.max_prestamos} préstamos)")
            uid = input("ID usuario (primeros 8): ").strip()

            print("\n  — Libros disponibles —")
            for l in l_srv.listar():
                if l.stock_disponible > 0:
                    print(f"  [{l.id[:8]}] {l.titulo}  (disponibles: {l.stock_disponible})")
            lid = input("ID libro (primeros 8): ").strip()

            usuario = _buscar_usuario(u_srv, uid)
            libro   = _buscar_libro(l_srv, lid)
            if not usuario or not libro:
                continue
            try:
                p = p_srv.prestar(usuario.id, libro.id)
                print(f"\n  ✅ Préstamo creado  [{p.id[:8]}]")
                print(f"     '{libro.titulo}'  →  {usuario.nombre}")
                print(f"     Vence: {p.fecha_vencimiento[:10]}")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "4":
            activos = [p for p in p_srv.listar_todos() if p.estado == EstadoPrestamo.ACTIVO]
            if not activos:
                print("  (no hay préstamos activos)")
                continue
            libros   = {l.id: l for l in l_srv.listar()}
            usuarios = {u.id: u for u in u_srv.listar()}
            for p in activos:
                titulo = libros.get(p.libro_id, type("", (), {"titulo": p.libro_id[:8]})()).titulo
                nombre = usuarios.get(p.usuario_id, type("", (), {"nombre": p.usuario_id[:8]})()).nombre
                print(f"  [{p.id[:8]}] '{titulo}'  →  {nombre}  |  vence: {p.fecha_vencimiento[:10]}")
            pid = input("ID préstamo (primeros 8): ").strip()
            prestamo = next((p for p in activos if p.id.startswith(pid)), None)
            if not prestamo:
                print("  Préstamo no encontrado.")
                continue
            try:
                p_srv.devolver(prestamo.id)
                print("  ✅ Devolución registrada. Stock restaurado.")
            except BibliotecaError as e:
                print(f"\n  ❌ {e}")

        elif op == "5":
            vencidos = p_srv.listar_vencidos()
            if not vencidos:
                print("  🎉 No hay préstamos vencidos.")
            libros   = {l.id: l for l in l_srv.listar()}
            usuarios = {u.id: u for u in u_srv.listar()}
            for p in vencidos:
                titulo = libros.get(p.libro_id, type("", (), {"titulo": p.libro_id[:8]})()).titulo
                nombre = usuarios.get(p.usuario_id, type("", (), {"nombre": p.usuario_id[:8]})()).nombre
                print(f"\n  [{p.id[:8]}] '{titulo}'  →  {nombre}")
                print(f"           Vencido desde: {p.fecha_vencimiento[:10]}")

        elif op == "0":
            break


# ──────────────────────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────────────────────

def main():
    libro_srv, usuario_srv, prestamo_srv = build_services()

    while True:
        sep("🏛️   Sistema de Gestión de Biblioteca")
        print("  1. Libros")
        print("  2. Usuarios")
        print("  3. Préstamos")
        print("  0. Salir")
        op = input("\nOpción: ").strip()

        if op == "1":
            menu_libros(libro_srv)
        elif op == "2":
            menu_usuarios(usuario_srv)
        elif op == "3":
            menu_prestamos(prestamo_srv, libro_srv, usuario_srv)
        elif op == "0":
            print("\n  ¡Hasta luego!\n")
            break


if __name__ == "__main__":
    main()
