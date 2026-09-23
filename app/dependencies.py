from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import SessionLocal

# El tokenUrl apunta al endpoint de login para que /docs muestre el botón Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Decodifica el JWT y devuelve el usuario de la base. Lanza 401 si el token es inválido."""
    # Import local para evitar importación circular
    from app.models import Usuario

    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise error_credenciales

    if payload.get("tipo") != "access":
        raise error_credenciales

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise error_credenciales

    usuario = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if usuario is None:
        raise error_credenciales

    return usuario


def require_admin(usuario=Depends(get_current_user)):
    """Verifica que el usuario autenticado tenga rol 'admin'. Lanza 403 si no."""
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador para esta acción.",
        )
    return usuario
