from datetime import datetime

from biblioteca.models import Prestamo
from biblioteca.models.prestamo import EstadoPrestamo
from biblioteca.repositories import (
    IPrestamoRepository, ILibroRepository, IUsuarioRepository,
)
from biblioteca.services.exceptions import (
    StockInsuficiente, LimitePrestamosAlcanzado, UsuarioInactivo,
    LibroNoEncontrado, UsuarioNoEncontrado,
    PrestamoNoEncontrado, PrestamoYaDevuelto,
)


class PrestamoService:
    """
    SRP: gestiona únicamente los préstamos.
    DIP: recibe las tres interfaces como dependencias inyectadas.

    Reglas de negocio que aplica:
      - El libro debe tener stock_disponible > 0
      - El usuario debe estar activo
      - El usuario no puede superar su límite de préstamos activos
      - Al devolver, el stock se restaura automáticamente
    """

    def __init__(
        self,
        prestamo_repo: IPrestamoRepository,
        libro_repo: ILibroRepository,
        usuario_repo: IUsuarioRepository,
    ):
        self._prestamos = prestamo_repo
        self._libros = libro_repo
        self._usuarios = usuario_repo

    # ──────────────────────────────────────────────────────────
    # Realizar préstamo
    # ──────────────────────────────────────────────────────────

    def prestar(self, usuario_id: str, libro_id: str) -> Prestamo:
        usuario = self._usuarios.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado(f"Usuario '{usuario_id}' no encontrado.")
        if not usuario.activo:
            raise UsuarioInactivo(f"El usuario '{usuario.nombre}' está inactivo.")

        libro = self._libros.obtener_por_id(libro_id)
        if not libro:
            raise LibroNoEncontrado(f"Libro '{libro_id}' no encontrado.")
        if libro.stock_disponible <= 0:
            raise StockInsuficiente(
                f"No hay ejemplares disponibles de '{libro.titulo}'."
            )

        activos = self._prestamos.obtener_activos_por_usuario(usuario_id)
        if len(activos) >= usuario.max_prestamos:
            raise LimitePrestamosAlcanzado(
                f"'{usuario.nombre}' ya tiene {len(activos)} préstamos activos "
                f"(límite: {usuario.max_prestamos})."
            )

        libro.stock_disponible -= 1
        self._libros.actualizar(libro)
        return self._prestamos.guardar(Prestamo(usuario_id=usuario_id, libro_id=libro_id))

    # ──────────────────────────────────────────────────────────
    # Devolver libro
    # ──────────────────────────────────────────────────────────

    def devolver(self, prestamo_id: str) -> Prestamo:
        prestamo = self._prestamos.obtener_por_id(prestamo_id)
        if not prestamo:
            raise PrestamoNoEncontrado(f"Préstamo '{prestamo_id}' no encontrado.")
        if prestamo.estado == EstadoPrestamo.DEVUELTO:
            raise PrestamoYaDevuelto("Este préstamo ya fue devuelto.")

        libro = self._libros.obtener_por_id(prestamo.libro_id)
        if libro:
            libro.stock_disponible = min(libro.stock_disponible + 1, libro.stock_total)
            self._libros.actualizar(libro)

        prestamo.estado = EstadoPrestamo.DEVUELTO
        prestamo.fecha_devolucion = datetime.now().isoformat()
        return self._prestamos.actualizar(prestamo)

    # ──────────────────────────────────────────────────────────
    # Consultas
    # ──────────────────────────────────────────────────────────

    def listar_todos(self) -> list[Prestamo]:
        return self._prestamos.obtener_todos()

    def listar_por_usuario(self, usuario_id: str) -> list[Prestamo]:
        return self._prestamos.obtener_activos_por_usuario(usuario_id)

    def listar_vencidos(self) -> list[Prestamo]:
        return [p for p in self._prestamos.obtener_todos() if p.esta_vencido()]
