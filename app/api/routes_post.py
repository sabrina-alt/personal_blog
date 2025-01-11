from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
def get_post():
    return {"message": "Rota de posts funcionando!"}
