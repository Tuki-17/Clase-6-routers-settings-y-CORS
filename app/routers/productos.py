from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.schemas import ProductoCreate, ProductoOut
from app.services import productos as productos_service

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoOut])
def listar_productos(
    skip: int = Query(default=0, ge=0, description="Registros a saltar (offset)"),
    limit: int = Query(default=10, ge=1, le=500, description="Maximo de resultados"),
    nombre: str | None = Query(default=None, description="Filtrar por nombre parcial (case-insensitive)"),
    precio_max: float | None = Query(default=None, ge=0, description="Precio maximo inclusive"),
    db: Session = Depends(get_db),
):
    return productos_service.listar_productos(db, skip, limit, nombre, precio_max)


@router.post("/", response_model=ProductoOut, status_code=201)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    """Crea un producto nuevo. Requiere rol admin."""
    return productos_service.crear_producto(db, producto)

