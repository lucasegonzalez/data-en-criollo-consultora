from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# --- Client ---
class ClientBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    rubro: Optional[str] = None
    notas: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# --- Contract ---
class ContractBase(BaseModel):
    client_id: int
    tipo: str
    fee: Optional[float] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    detalle: Optional[str] = None

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    estado: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- Meeting ---
class MeetingBase(BaseModel):
    client_id: int
    fecha: datetime
    duracion_minutos: Optional[int] = 30
    notas: Optional[str] = None
    link: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingResponse(MeetingBase):
    id: int
    estado: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- Task ---
class TaskBase(BaseModel):
    client_id: Optional[int] = None
    titulo: str
    descripcion: Optional[str] = None
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    estado: Optional[str] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    deadline: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    estado: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Health ---
class HealthResponse(BaseModel):
    status: str = "ok"
