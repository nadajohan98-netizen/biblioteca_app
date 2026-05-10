from biblioteca.models import Libro
from biblioteca.repositories import ILibroRepository
from biblioteca.services.exceptions import LibroNoEncontrado


class LibroService:
    """
    SRP: solo orquesta operaciones sobre libros.
    DIP: recibe ILibroRepository, no una clase concreta.
    """

    def __init__(self, repo: ILibroRepository):
        self._repo = repo

    def crear(self, titulo: str, autor: str, isbn: str, stock: int) -> Libro:
        libro = Libro(
            titulo=titulo, autor=autor, isbn=isbn,
            stock_total=stock, stock_disponible=stock,
        )
        return self._repo.guardar(libro)

    def obtener(self, libro_id: str) -> Libro:
        libro = self._repo.obtener_por_id(libro_id)
        if not libro:
            raise LibroNoEncontrado(f"Libro '{libro_id}' no existe.")
        return libro

    def listar(self) -> list[Libro]:
        return self._repo.obtener_todos()

    def editar(self, libro_id: str, titulo: str = None,
               autor: str = None, stock_total: int = None) -> Libro:
        libro = self.obtener(libro_id)
        if titulo:
            libro.titulo = titulo
        if autor:
            libro.autor = autor
        if stock_total is not None:
            diferencia = stock_total - libro.stock_total
            libro.stock_total = stock_total
            libro.stock_disponible = max(0, libro.stock_disponible + diferencia)
        return self._repo.actualizar(libro)

    def eliminar(self, libro_id: str) -> bool:
        self.obtener(libro_id)
        return self._repo.eliminar(libro_id)
