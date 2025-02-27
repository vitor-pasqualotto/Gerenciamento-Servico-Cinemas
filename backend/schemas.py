from pydantic import BaseModel
from typing import Optional, List, Required
from datetime import datetime

# =======================================
# Schemas para EmpresaCinema
class EmpresaCinemaBase(BaseModel):
    nome: str
    cnpj: str
    contato: Optional[str] = None

class EmpresaCinemaCreate(EmpresaCinemaBase):
    pass

class EmpresaCinema(EmpresaCinemaBase):
    id: int
    class Config:
        orm_mode = True

# =======================================
# Schemas para Cinema
class CinemaBase(BaseModel):
    nome: str
    endereco: Optional[str] = None

class CinemaCreate(CinemaBase):
    empresa_id: int

class Cinema(CinemaBase):
    id: int
    empresa_id: int
    class Config:
        orm_mode = True

# =======================================
# Schemas para Sala
class SalaBase(BaseModel):
    nome: str

class SalaCreate(SalaBase):
    cinema_id: int

class Sala(SalaBase):
    id: int
    cinema_id: int
    class Config:
        orm_mode = True

# =======================================
# Schemas para Usuário
class UsuarioBase(BaseModel):
    nome: str
    email: str
    tipo_usuario: str  # Admin, Gerente, Representante, Encarregado
    empresa_id: Optional[int] = None
    cinema_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None  # Se for atualizado, será hasheada
    tipo_usuario: Optional[str] = None
    empresa_id: Optional[int] = None
    cinema_id: Optional[int] = None


class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

# =======================================
# Schemas para Autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# =======================================
# Schemas para Serviço
class ServicoBase(BaseModel):
    tipo_servico: str
    observacoes: Optional[str] = None

class ServicoCreate(ServicoBase):
    encarregado_id: int
    sala_id: int
    tipo_servico: str
    observacoes: Optional[str] = None
    fotos_urls: List[str]

class Servico(ServicoBase):
    id: int
    encarregado_id: int
    sala_id: int
    status: str
    data: datetime
    class Config:
        orm_mode = True

class ServicoUpdate(BaseModel):
    status: Optional[str] = None
    observacoes: Optional[str] = None
    fotos_urls: Optional[List[str]] = None

# =======================================
# Schemas para FotoServico
class FotoServicoBase(BaseModel):
    url_foto: str

class FotoServicoCreate(FotoServicoBase):
    servico_id: int

class FotoServico(FotoServicoBase):
    id: int
    servico_id: int
    class Config:
        orm_mode = True

# =======================================
# Schemas para Histórico de Status
class HistoricoStatusBase(BaseModel):
    status: str
    observacoes: Optional[str] = None

class HistoricoStatusCreate(HistoricoStatusBase):
    servico_id: int
    usuario_id: int

class HistoricoStatus(HistoricoStatusBase):
    id: int
    servico_id: int
    usuario_id: int
    data: datetime
    class Config:
        orm_mode = True
