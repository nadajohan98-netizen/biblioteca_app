"""
container.py — Composición de dependencias (Dependency Injection).

DIP: único lugar del sistema donde se instancian clases concretas.
Si cambias a SQLite, solo modificas este archivo.
"""
from biblioteca.repositories.json_repositories import (
    JsonLibroRepository,
    JsonUsuarioRepository,
    JsonPrestamoRepository,
)
from biblioteca.services import LibroService, UsuarioService, PrestamoService

DATA_DIR = "data"


def build_services():
    libro_repo    = JsonLibroRepository(f"{DATA_DIR}/libros.json")
    usuario_repo  = JsonUsuarioRepository(f"{DATA_DIR}/usuarios.json")
    prestamo_repo = JsonPrestamoRepository(f"{DATA_DIR}/prestamos.json")

    return (
        LibroService(libro_repo),
        UsuarioService(usuario_repo),
        PrestamoService(prestamo_repo, libro_repo, usuario_repo),
    )
