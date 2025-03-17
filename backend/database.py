from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregando variáveis de ambiente
load_dotenv()

# Definindo valor para DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Se não for definida lança um erro
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida no .env")

# Se for SQLite, adicionamos um parâmetro extra para evitar bloqueios de escrita concorrente
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Cria engine
engine = create_engine(DATABASE_URL, connect_args={"client_encoding": "utf8"})

# Definindo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()