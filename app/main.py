import uuid
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db, SessionLocal
from app.models import Producto as ProductoModel
from app import schemas
from app.services import productos as productos_service

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Carga inicial de productos (seeding) si la base de datos está vacía
db = SessionLocal()
try:
    if db.query(ProductoModel).count() == 0:
        productos_defecto = [
            ProductoModel(nombre="Hamburguesa (Banana y avena)", precio_final=9500.0, cuotas_cantidad=3, cuotas_valor=3166.67, garantia_meses=0, stock=15),
            ProductoModel(nombre="Esponja (Bizcochuelo)", precio_final=12500.0, cuotas_cantidad=3, cuotas_valor=4166.67, garantia_meses=0, stock=10),
            ProductoModel(nombre="Huevo (Gelatina)", precio_final=6000.0, cuotas_cantidad=1, cuotas_valor=6000.0, garantia_meses=0, stock=20),
            ProductoModel(nombre="Vela (Chocolate blanco y negro)", precio_final=9000.0, cuotas_cantidad=3, cuotas_valor=3000.0, garantia_meses=0, stock=12),
            ProductoModel(nombre="Tomate (Alfajor de maicena)", precio_final=11000.0, cuotas_cantidad=3, cuotas_valor=3666.67, garantia_meses=0, stock=18),
        ]
        db.bulk_save_objects(productos_defecto)
        db.commit()
        print("Base de datos inicializada y poblada con productos por defecto.")
except Exception as e:
    print(f"Error al poblar la base de datos: {e}")
finally:
    db.close()

app = FastAPI(title="E-commerce Trampantojos - Ley 24.240")

# Permitir CORS para desarrollo local y peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir al dominio correspondiente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESQUEMAS PYDANTIC (en app/schemas.py) ---

from pydantic import BaseModel

class SolicitudArrepentimiento(BaseModel):
    email: str
    codigo_compra: str
    detalle: str | None = None

# Base de datos en memoria para arrepentimientos (por ahora)
arrepentimientos_db = []

# --- ENDPOINTS DE PRODUCTOS ---

@app.get("/productos", response_model=list[schemas.ProductoOut])
def obtener_productos(
    skip: int = Query(default=0, ge=0, description="Registros a saltar (offset)"),
    limit: int = Query(default=100, ge=1, le=500, description="Maximo de resultados"),
    nombre: str | None = Query(default=None, description="Filtrar por nombre parcial (case-insensitive)"),
    precio_max: float | None = Query(default=None, ge=0, description="Precio maximo inclusive"),
    db: Session = Depends(get_db),
):
    return productos_service.listar_productos(db, skip=skip, limit=limit, nombre=nombre, precio_max=precio_max)

@app.post("/productos", response_model=schemas.ProductoOut, status_code=201)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return productos_service.crear_producto(db, producto)

# --- ENDPOINT DE ARREPENTIMIENTO (Resolución 424/2020) ---

@app.post("/arrepentimiento")
def registrar_arrepentimiento(solicitud: SolicitudArrepentimiento):
    codigo_tramite = f"REV-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
    registro = {
        "id": len(arrepentimientos_db) + 1,
        "email": solicitud.email,
        "codigo_compra": solicitud.codigo_compra,
        "detalle": solicitud.detalle,
        "codigo_tramite": codigo_tramite,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    arrepentimientos_db.append(registro)
    return {
        "mensaje": "Trámite de revocación de compra iniciado con éxito (Resolución 424/2020).",
        "codigo_tramite": codigo_tramite,
        "registro": registro
    }