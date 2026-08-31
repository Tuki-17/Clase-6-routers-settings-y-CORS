import uuid
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import engine, Base, get_db, SessionLocal
from app.models import Producto as ProductoModel

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

# --- ESQUEMAS PYDANTIC (Validación HTTP) ---

class ProductoSchema(BaseModel):
    id: int | None = None
    nombre: str
    precio_final: float
    cuotas_cantidad: int
    cuotas_valor: float
    garantia_meses: int
    stock: int

    class Config:
        from_attributes = True

class SolicitudArrepentimiento(BaseModel):
    email: str
    codigo_compra: str
    detalle: str | None = None

# Base de datos en memoria para arrepentimientos (por ahora)
arrepentimientos_db = []

# --- ENDPOINTS DE PRODUCTOS (Conectados a PostgreSQL) ---

@app.get("/productos", response_model=list[ProductoSchema])
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(ProductoModel).all()

@app.post("/productos", response_model=ProductoSchema)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    nuevo_producto = ProductoModel(**producto.model_dump(exclude={"id"}))
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

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