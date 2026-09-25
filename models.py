from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class ProductoBase(SQLModel):
    nombre: str
    categoria: str
    precio: float
    stock: int

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductoCrear(ProductoBase):
    pass

class ProductoModificar(SQLModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

class PedidoBase(SQLModel):
    cliente: str
    producto_id: int
    cantidad: int
    total: float
    estado: str = "pendiente" 

class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PedidoCrear(PedidoBase):
    pass

class PedidoModificar(SQLModel):
    cliente: Optional[str] = None
    producto_id: Optional[int] = None
    cantidad: Optional[int] = None
    total: Optional[float] = None
    estado: Optional[str] = None
