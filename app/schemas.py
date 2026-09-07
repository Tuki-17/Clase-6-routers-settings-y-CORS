from pydantic import BaseModel


# --- Schemas de Producto ---

class ProductoCreate(BaseModel):
    """Schema para crear un producto. No incluye el id (lo asigna la DB)."""
    nombre: str
    precio_final: float
    cuotas_cantidad: int
    cuotas_valor: float
    garantia_meses: int
    stock: int


class ProductoOut(ProductoCreate):
    """Schema de salida. Hereda todos los campos de ProductoCreate y agrega el id."""
    id: int

    class Config:
        from_attributes = True  # Permite convertir objetos ORM a Pydantic
