from biblioteca.models import Usuario
from biblioteca.repositories import IUsuarioRepository
from biblioteca.services.exceptions import UsuarioNoEncontrado, EmailYaRegistrado


class UsuarioService:
    """SRP: solo orquesta operaciones sobre usuarios."""

    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo

    def registrar(self, nombre: str, email: str, max_prestamos: int = 3) -> Usuario:
        if self._repo.obtener_por_email(email):
            raise EmailYaRegistrado(f"El email '{email}' ya está registrado.")
        return self._repo.guardar(
            Usuario(nombre=nombre, email=email, max_prestamos=max_prestamos)
        )

    def obtener(self, usuario_id: str) -> Usuario:
        usuario = self._repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado(f"Usuario '{usuario_id}' no existe.")
        return usuario

    def listar(self) -> list[Usuario]:
        return self._repo.obtener_todos()

    def editar(self, usuario_id: str, nombre: str = None,
               max_prestamos: int = None) -> Usuario:
        usuario = self.obtener(usuario_id)
        if nombre:
            usuario.nombre = nombre
        if max_prestamos is not None:
            usuario.max_prestamos = max_prestamos
        return self._repo.actualizar(usuario)

    def desactivar(self, usuario_id: str) -> Usuario:
        usuario = self.obtener(usuario_id)
        usuario.activo = False
        return self._repo.actualizar(usuario)

    def eliminar(self, usuario_id: str) -> bool:
        self.obtener(usuario_id)
        return self._repo.eliminar(usuario_id)
