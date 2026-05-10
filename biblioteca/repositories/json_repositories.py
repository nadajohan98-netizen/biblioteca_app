"""
Implementaciones concretas con persistencia en JSON.
OCP: si mañana usas SQLite, creas SqliteLibroRepository sin tocar nada más.
"""
import json
import uuid
from pathlib import Path
from typing import Optional

from biblioteca.models import Libro, Usuario, Prestamo
from biblioteca.repositories import ILibroRepository, IUsuarioRepository, IPrestamoRepository


class _BaseJsonRepository:
    """Lógica de lectura/escritura JSON reutilizable."""

    def __init__(self, filepath: str):
        self._path = Path(filepath)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("[]", encoding="utf-8")

    def _leer(self) -> list[dict]:
        return json.loads(self._path.read_text(encoding="utf-8"))

    def _escribir(self, datos: list[dict]) -> None:
        self._path.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
        )


# ─────────────────────────────────────────────────────────────
# Libros
# ─────────────────────────────────────────────────────────────

class JsonLibroRepository(_BaseJsonRepository, ILibroRepository):

    def guardar(self, libro: Libro) -> Libro:
        libro.id = str(uuid.uuid4())
        datos = self._leer()
        datos.append(libro.to_dict())
        self._escribir(datos)
        return libro

    def obtener_por_id(self, libro_id: str) -> Optional[Libro]:
        return next(
            (Libro.from_dict(d) for d in self._leer() if d["id"] == libro_id), None
        )

    def obtener_todos(self) -> list[Libro]:
        return [Libro.from_dict(d) for d in self._leer()]

    def actualizar(self, libro: Libro) -> Libro:
        datos = self._leer()
        for i, d in enumerate(datos):
            if d["id"] == libro.id:
                datos[i] = libro.to_dict()
                break
        self._escribir(datos)
        return libro

    def eliminar(self, libro_id: str) -> bool:
        datos = self._leer()
        nuevos = [d for d in datos if d["id"] != libro_id]
        if len(nuevos) == len(datos):
            return False
        self._escribir(nuevos)
        return True


# ─────────────────────────────────────────────────────────────
# Usuarios
# ─────────────────────────────────────────────────────────────

class JsonUsuarioRepository(_BaseJsonRepository, IUsuarioRepository):

    def guardar(self, usuario: Usuario) -> Usuario:
        usuario.id = str(uuid.uuid4())
        datos = self._leer()
        datos.append(usuario.to_dict())
        self._escribir(datos)
        return usuario

    def obtener_por_id(self, usuario_id: str) -> Optional[Usuario]:
        return next(
            (Usuario.from_dict(d) for d in self._leer() if d["id"] == usuario_id), None
        )

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return next(
            (Usuario.from_dict(d) for d in self._leer() if d["email"] == email), None
        )

    def obtener_todos(self) -> list[Usuario]:
        return [Usuario.from_dict(d) for d in self._leer()]

    def actualizar(self, usuario: Usuario) -> Usuario:
        datos = self._leer()
        for i, d in enumerate(datos):
            if d["id"] == usuario.id:
                datos[i] = usuario.to_dict()
                break
        self._escribir(datos)
        return usuario

    def eliminar(self, usuario_id: str) -> bool:
        datos = self._leer()
        nuevos = [d for d in datos if d["id"] != usuario_id]
        if len(nuevos) == len(datos):
            return False
        self._escribir(nuevos)
        return True


# ─────────────────────────────────────────────────────────────
# Préstamos
# ─────────────────────────────────────────────────────────────

class JsonPrestamoRepository(_BaseJsonRepository, IPrestamoRepository):

    def guardar(self, prestamo: Prestamo) -> Prestamo:
        prestamo.id = str(uuid.uuid4())
        datos = self._leer()
        datos.append(prestamo.to_dict())
        self._escribir(datos)
        return prestamo

    def obtener_por_id(self, prestamo_id: str) -> Optional[Prestamo]:
        return next(
            (Prestamo.from_dict(d) for d in self._leer() if d["id"] == prestamo_id), None
        )

    def obtener_activos_por_usuario(self, usuario_id: str) -> list[Prestamo]:
        return [
            Prestamo.from_dict(d)
            for d in self._leer()
            if d["usuario_id"] == usuario_id and d["estado"] == "activo"
        ]

    def obtener_activos_por_libro(self, libro_id: str) -> list[Prestamo]:
        return [
            Prestamo.from_dict(d)
            for d in self._leer()
            if d["libro_id"] == libro_id and d["estado"] == "activo"
        ]

    def obtener_todos(self) -> list[Prestamo]:
        return [Prestamo.from_dict(d) for d in self._leer()]

    def actualizar(self, prestamo: Prestamo) -> Prestamo:
        datos = self._leer()
        for i, d in enumerate(datos):
            if d["id"] == prestamo.id:
                datos[i] = prestamo.to_dict()
                break
        self._escribir(datos)
        return prestamo
