"""
Interfaces de repositorios.
ISP: cada interfaz expone solo lo que su módulo necesita.
DIP: los servicios dependen de estas abstracciones, no de JSON ni SQLite.
"""
from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.models import Libro, Usuario, Prestamo


class ILibroRepository(ABC):
    @abstractmethod
    def guardar(self, libro: Libro) -> Libro: ...

    @abstractmethod
    def obtener_por_id(self, libro_id: str) -> Optional[Libro]: ...

    @abstractmethod
    def obtener_todos(self) -> list[Libro]: ...

    @abstractmethod
    def actualizar(self, libro: Libro) -> Libro: ...

    @abstractmethod
    def eliminar(self, libro_id: str) -> bool: ...


class IUsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def obtener_por_id(self, usuario_id: str) -> Optional[Usuario]: ...

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]: ...

    @abstractmethod
    def obtener_todos(self) -> list[Usuario]: ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def eliminar(self, usuario_id: str) -> bool: ...


class IPrestamoRepository(ABC):
    @abstractmethod
    def guardar(self, prestamo: Prestamo) -> Prestamo: ...

    @abstractmethod
    def obtener_por_id(self, prestamo_id: str) -> Optional[Prestamo]: ...

    @abstractmethod
    def obtener_activos_por_usuario(self, usuario_id: str) -> list[Prestamo]: ...

    @abstractmethod
    def obtener_activos_por_libro(self, libro_id: str) -> list[Prestamo]: ...

    @abstractmethod
    def obtener_todos(self) -> list[Prestamo]: ...

    @abstractmethod
    def actualizar(self, prestamo: Prestamo) -> Prestamo: ...
