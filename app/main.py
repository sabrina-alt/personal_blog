# app/main.py
from fastapi import FastAPI
from app.api.routes_user import router as user_router
from app.api.routes_post import router as post_router
from app.api.routes_public import router as public_router

app = FastAPI()

# Incluindo as rotas corretamente
app.include_router(user_router)
app.include_router(post_router)
app.include_router(public_router)

def home():
    return {"message": "API de Usuários Rodando!"}
