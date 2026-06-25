from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class ContractType(str, enum.Enum):
    mensual = "mensual"
    proyecto = "proyecto"
    consulting = "consulting"

class ContractStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class MeetingStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(50))
    rubro = Column(String(255))
    notas = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    contracts = relationship("Contract", back_populates="client", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="client", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="client", cascade="all, delete-orphan")

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    tipo = Column(SAEnum(ContractType), nullable=False)
    fee = Column(Float)
    estado = Column(SAEnum(ContractStatus), default=ContractStatus.active)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    detalle = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="contracts")

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    duracion_minutos = Column(Integer, default=30)
    notas = Column(Text)
    link = Column(String(500))
    estado = Column(SAEnum(MeetingStatus), default=MeetingStatus.scheduled)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="meetings")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    deadline = Column(DateTime)
    estado = Column(SAEnum(TaskStatus), default=TaskStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = relationship("Client", back_populates="tasks")
