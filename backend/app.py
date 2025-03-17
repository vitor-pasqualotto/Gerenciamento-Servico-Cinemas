from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import routers  # Importa a lista de routers
import uvicorn
import subprocess
import threading

# Cria as tabelas (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Serviços de Limpeza para Cinemas")

# Inclui todos os routers importados
for router in routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Sistema de Gestão de Serviços de Limpeza para Cinemas"}


# ALTERACOES
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501", "--server.adress=0.0.0.0"])

if __name__ == "__main__":
    thread_fast_api = threading.Thread(target=run_fastapi)
    thread_streamlit = threading.Thread(target=run_streamlit)

    thread_fast_api.start()
    thread_streamlit.start()

    thread_fast_api.join()
    thread_streamlit.join()