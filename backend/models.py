from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

# Tabela Empresa Cinema
class EmpresaCinema(Base):
    __tablename__ = "empresas_cinema"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=False)
    contato = Column(String(255), nullable=True)
    
    cinemas = relationship("Cinema", back_populates="empresa", cascade="all, delete-orphan")

# Tebla Cinema
class Cinema(Base):
    __tablename__ = "cinemas"
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas_cinema.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=True)
    
    empresa = relationship("EmpresaCinema", back_populates="cinemas")
    salas = relationship("Sala", back_populates="cinema", cascade="all, delete-orphan")

# Tabela Sala
class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(255), nullable=False)
    
    cinema = relationship("Cinema", back_populates="salas")
    servicos = relationship("Servico", back_populates="sala", cascade="all, delete-orphan")

# Tabela Usuário
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_usuario = Column(String(50), nullable=False)  # Admin, Gerente, Representante, Encarregado
    empresa_id = Column(Integer, ForeignKey("empresas_cinema.id", ondelete="SET NULL"), nullable=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id", ondelete="SET NULL"), nullable=True)
    
    servicos = relationship("Servico", back_populates="encarregado")
    historicos = relationship("HistoricoStatus", back_populates="usuario")

# Tabela Serviço
class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    encarregado_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id", ondelete="CASCADE"), nullable=False)
    tipo_servico = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="Pendente")  # Pendente, Aprovado, Recusado, Concluído
    observacoes = Column(Text, nullable=True)
    data = Column(TIMESTAMP, server_default=func.now())
    
    encarregado = relationship("Usuario", back_populates="servicos")
    sala = relationship("Sala", back_populates="servicos")
    fotos = relationship("FotoServico", back_populates="servico", cascade="all, delete-orphan")
    historicos = relationship("HistoricoStatus", back_populates="servico", cascade="all, delete-orphan")

# Tabela Foto Serviço
class FotoServico(Base):
    __tablename__ = "fotos_servico"
    id = Column(Integer, primary_key=True, index=True)
    servico_id = Column(Integer, ForeignKey("servicos.id", ondelete="CASCADE"), nullable=False)
    url_foto = Column(String(255), nullable=False)
    
    servico = relationship("Servico", back_populates="fotos")

# Tabela Historico Status
class HistoricoStatus(Base):
    __tablename__ = "historico_status"
    id = Column(Integer, primary_key=True, index=True)
    servico_id = Column(Integer, ForeignKey("servicos.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)
    observacoes = Column(Text, nullable=True)
    data = Column(TIMESTAMP, server_default=func.now())
    
    servico = relationship("Servico", back_populates="historicos")
    usuario = relationship("Usuario", back_populates="historicos")
