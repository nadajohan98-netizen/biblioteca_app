from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Usuario:
    """
    Modelo de dominio puro.
    SRP: única responsabilidad = representar un usuario.
    """
    nombre: str
    email: str
    id: str = field(default="")
    activo: bool = True
    max_prestamos: int = 3
    fecha_registro: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_dict(data: dict) -> "Usuario":
        return Usuario(**data)
