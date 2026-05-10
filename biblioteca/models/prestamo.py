from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class EstadoPrestamo(str, Enum):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"


@dataclass
class Prestamo:
    """
    Modelo de dominio puro.
    SRP: única responsabilidad = representar un préstamo.
    """
    usuario_id: str
    libro_id: str
    id: str = field(default="")
    estado: str = EstadoPrestamo.ACTIVO
    fecha_prestamo: str = field(default_factory=lambda: datetime.now().isoformat())
    fecha_vencimiento: str = field(
        default_factory=lambda: (datetime.now() + timedelta(days=14)).isoformat()
    )
    fecha_devolucion: str = ""

    def esta_vencido(self) -> bool:
        if self.estado == EstadoPrestamo.DEVUELTO:
            return False
        return datetime.now() > datetime.fromisoformat(self.fecha_vencimiento)

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_dict(data: dict) -> "Prestamo":
        return Prestamo(**data)
