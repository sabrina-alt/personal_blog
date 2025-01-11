from fastapi import APIRouter, HTTPException
from app.schemas import UserLogin, UserCreate, UserUpdate, UserResponse
from app.utils import create_access_token, verify_password
from datetime import timedelta
from app.utils import get_password_hash
from typing import List

router = APIRouter()
fake_users_db = {
    "sabrina@example.com": {
        "password": "$2b$12$e8JkQyx7gMtv3E/FtAKyhuDYbcXc4s41Blw5jfbOAfO4ayw.Vq9Ge" 
    }
}

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    if user.email in user.fake_users_db:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.email] = {"name": user.name, "password": hashed_password}

    return {"email": user.email, "name": user.name }

## 🔹 Listar usuários
@router.get("/users/", response_model=List[UserResponse])
def list_users():
    """
    Retorna a lista de usuários cadastrados.
    """
    return [{"email": email, "name": data["name"]} for email, data in fake_users_db.items()]

## 🔹 Editar usuário
@router.put("/users/{email}", response_model=UserResponse)
def update_user(email: str, user_update: UserUpdate):
    """
    Atualiza o nome de um usuário. Retorna erro se o usuário não existir.
    """
    if email not in fake_users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if user_update.name:
        fake_users_db[email]["name"] = user_update.name

    return {"email": email, "name": fake_users_db[email]["name"]}

## 🔹 Deletar usuário
@router.delete("/users/{email}")
def delete_user(email: str):
    """
    Remove um usuário do banco de dados fake.
    """
    if email not in fake_users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    del fake_users_db[email]
    return {"message": "Usuário deletado com sucesso"}

@router.post("/login")
def login(user: UserLogin):
    if user.email not in fake_users_db:
        raise HTTPException(status_code=400, detail="E-mail não cadastrado.")
    stored_password = fake_users_db[user.email]["password"]
    if not verify_password(user.password, stored_password):
        raise HTTPException(status_code=400, detail="Senha incorreta.")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


## criar usuario
## editar usuario
## listar usuario
## deletar usuario