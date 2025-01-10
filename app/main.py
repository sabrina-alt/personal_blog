from fastapi import FastAPI
from app.api.routes_user import router as user_router
from app.api.routes_post import router as post_router

app = FastAPI()

# Registrar as rotas no FastAPI
app.include_router(user_router, prefix="/api")
app.include_router(post_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "API está rodando!"}
