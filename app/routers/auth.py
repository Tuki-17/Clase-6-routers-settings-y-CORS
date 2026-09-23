from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import crear_token, hash_password, verificar_password
from app.dependencies import get_current_user, get_db
from app.models import Usuario
from app.schemas.usuario import Token, UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/auth", tags=["Auth"])


# ── Registro ────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un usuario nuevo con contraseña hasheada."""
    # Verificar que el email no esté ya registrado
    existente = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese email.",
        )

    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        hashed_password=hash_password(datos.password),
        rol="customer",
        acepto_tratamiento=datos.acepto_tratamiento,
        fecha_consentimiento=datetime.now(timezone.utc),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── Login ────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login con email (campo username del formulario OAuth2) y contraseña.
    Devuelve access_token y refresh_token.
    """
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    # Mensaje genérico: no revelar si falló el email o la contraseña
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not usuario or not verificar_password(form.password, usuario.hashed_password):
        raise credenciales_invalidas

    payload = {"sub": str(usuario.id), "rol": usuario.rol}
    return Token(
        access_token=crear_token(payload, "access"),
        refresh_token=crear_token(payload, "refresh"),
    )


# ── Refresh ───────────────────────────────────────────────────────────────────

@router.post("/refresh", response_model=Token)
def refresh(body: dict, db: Session = Depends(get_db)):
    """
    Genera un nuevo par de tokens a partir de un refresh_token válido.
    Rechaza cualquier token cuyo campo 'tipo' no sea 'refresh'.
    """
    token = body.get("refresh_token", "")
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido o expirado.",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise error

    if payload.get("tipo") != "refresh":
        raise error

    usuario = db.query(Usuario).filter(Usuario.id == int(payload["sub"])).first()
    if not usuario:
        raise error

    data = {"sub": str(usuario.id), "rol": usuario.rol}
    return Token(
        access_token=crear_token(data, "access"),
        refresh_token=crear_token(data, "refresh"),
    )


# ── Me ────────────────────────────────────────────────────────────────────────

@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(get_current_user)):
    """Devuelve los datos del usuario autenticado (sin hash ni contraseña)."""
    return usuario
