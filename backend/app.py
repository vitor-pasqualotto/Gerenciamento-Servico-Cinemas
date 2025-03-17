from fastapi import FastAPI
from .database import engine, Base
from .routes import routers  # Importa a lista de routers

# Cria as tabelas (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Serviços de Limpeza para Cinemas")

# Inclui todos os routers importados
for router in routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Sistema de Gestão de Serviços de Limpeza para Cinemas"}