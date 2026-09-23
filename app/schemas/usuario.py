from pydantic import BaseModel, EmailStr, field_validator


class UsuarioCreate(BaseModel):
    """Schema de entrada para el registro de un usuario."""
    nombre: str
    email: EmailStr
    password: str
    acepto_tratamiento: bool

    @field_validator("acepto_tratamiento")
    @classmethod
    def debe_aceptar_tratamiento(cls, v: bool) -> bool:
        if not v:
            raise ValueError(
                "Debe aceptar el tratamiento de datos personales (Ley 25.326) para registrarse."
            )
        return v


class UsuarioOut(BaseModel):
    """Schema de salida para usuarios. Nunca expone la contraseña ni el hash."""
    id: int
    nombre: str
    email: str
    rol: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Respuesta del endpoint de login y refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
