# backend/routes/__init__.py
from .usuarios import router as usuarios_router
from .cinemas import router as cinemas_router
from .servicos import router as servicos_router

# Opcional: criar uma lista com todos os routers para iteração no app principal
routers = [usuarios_router, cinemas_router, servicos_router]
