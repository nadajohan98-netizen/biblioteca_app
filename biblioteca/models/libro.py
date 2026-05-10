from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Libro:
    """
    Modelo de dominio puro.
    SRP: única responsabilidad = representar un libro.
    """
    titulo: str
    autor: str
    isbn: str
    stock_total: int
    stock_disponible: int
    id: str = field(default="")
    fecha_registro: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_dict(data: dict) -> "Libro":
        return Libro(**data)
