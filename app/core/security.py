from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexto de hashing con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Devuelve el hash bcrypt de la contraseña en texto plano."""
    return pwd_context.hash(plain)


def verificar_password(plain: str, hashed: str) -> bool:
    """Compara la contraseña en texto plano contra el hash almacenado."""
    return pwd_context.verify(plain, hashed)


def crear_token(data: dict, tipo: str) -> str:
    """
    Crea un JWT firmado.
    - tipo: "access" (ACCESS_MIN minutos) o "refresh" (REFRESH_MIN minutos)
    """
    minutos = settings.ACCESS_MIN if tipo == "access" else settings.REFRESH_MIN
    expira = datetime.now(timezone.utc) + timedelta(minutes=minutos)

    payload = {**data, "tipo": tipo, "exp": expira}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
