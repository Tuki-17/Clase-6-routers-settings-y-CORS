from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI(title="E-commerce Trampantojos - Ley 24.240")

# Permitir CORS para desarrollo local y peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir al dominio correspondiente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Producto(BaseModel):
    id: int
    nombre: str
    precio_final: float
    cuotas_cantidad: int
    cuotas_valor: float
    garantia_meses: int
    stock: int

class SolicitudArrepentimiento(BaseModel):
    email: str
    codigo_compra: str
    detalle: str | None = None

# Base de datos en memoria para productos
productos_db: list[Producto] = [
    Producto(id=1, nombre="Hamburguesa (Banana y avena)", precio_final=9500.0, cuotas_cantidad=3, cuotas_valor=3166.67, garantia_meses=0, stock=15),
    Producto(id=2, nombre="Esponja (Bizcochuelo)", precio_final=12500.0, cuotas_cantidad=3, cuotas_valor=4166.67, garantia_meses=0, stock=10),
    Producto(id=3, nombre="Huevo (Gelatina)", precio_final=6000.0, cuotas_cantidad=1, cuotas_valor=6000.0, garantia_meses=0, stock=20),
    Producto(id=4, nombre="Vela (Chocolate blanco y negro)", precio_final=9000.0, cuotas_cantidad=3, cuotas_valor=3000.0, garantia_meses=0, stock=12),
    Producto(id=5, nombre="Tomate (Alfajor de maicena)", precio_final=11000.0, cuotas_cantidad=3, cuotas_valor=3666.67, garantia_meses=0, stock=18),
]

# Base de datos en memoria para arrepentimientos
arrepentimientos_db = []

@app.get("/productos")
def obtener_productos():
    return productos_db

@app.post("/productos")
def crear_producto(producto: Producto):
    productos_db.append(producto)
    return {"mensaje": "Producto agregado con éxito", "producto": producto}

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