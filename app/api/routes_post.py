from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_post():
    return {"message": "Rota de posts funcionando!"}
