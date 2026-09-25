from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select

from database import inicializar_bd, obtener_sesion
from models import (
    Producto, ProductoCrear, ProductoModificar,
    Pedido, PedidoCrear, PedidoModificar
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_bd()
    yield

app = FastAPI(
    title="API de Comercio - FastAPI & Amazon RDS",
    description="Gestión integral de Productos y Pedidos conectada a PostgreSQL en AWS RDS",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Estado"])
def health_check():
    return {"estado": "en linea", "base_de_datos": "Amazon RDS PostgreSQL", "docs": "/docs"}

@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(payload: ProductoCrear, db: Session = Depends(obtener_sesion)):
    nuevo = Producto.model_validate(payload)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/productos", response_model=List[Producto], tags=["Productos"])
def listar_productos(db: Session = Depends(obtener_sesion)):
    return db.exec(select(Producto)).all()

@app.get("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def detalle_producto(producto_id: int, db: Session = Depends(obtener_sesion)):
    item = db.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.put("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def actualizar_producto(producto_id: int, datos: ProductoModificar, db: Session = Depends(obtener_sesion)):
    item = db.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
def eliminar_producto(producto_id: int, db: Session = Depends(obtener_sesion)):
    item = db.get(Producto, producto_id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(item)
    db.commit()
    return None

@app.post("/pedidos", response_model=Pedido, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(payload: PedidoCrear, db: Session = Depends(obtener_sesion)):
    nuevo = Pedido.model_validate(payload)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/pedidos", response_model=List[Pedido], tags=["Pedidos"])
def listar_pedidos(db: Session = Depends(obtener_sesion)):
    return db.exec(select(Pedido)).all()

@app.get("/pedidos/{pedido_id}", response_model=Pedido, tags=["Pedidos"])
def detalle_pedido(pedido_id: int, db: Session = Depends(obtener_sesion)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.put("/pedidos/{pedido_id}", response_model=Pedido, tags=["Pedidos"])
def actualizar_pedido(pedido_id: int, datos: PedidoModificar, db: Session = Depends(obtener_sesion)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(pedido, key, value)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido

@app.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pedidos"])
def eliminar_pedido(pedido_id: int, db: Session = Depends(obtener_sesion)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    db.commit()
    return None