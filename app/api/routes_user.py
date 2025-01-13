from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import sessionmaker
from app.api import models
from app.schemas import UserLogin, UserCreate, UserUpdate, UserResponse
from app.utils import create_access_token, verify_password
from datetime import timedelta
from app.utils import get_password_hash
from typing import List
from sqlalchemy import create_engine

router = APIRouter()

db = create_engine("sqlite:///./blog.db")
Session = sessionmaker(bind=db)
session = Session()
## 🔹 criar usuários
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # Verificar se o usuário já existe
    db_user = session.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    hashed_password = get_password_hash(user.password)
    # Criar o novo usuário no banco de dados
    new_user = models.User(email=user.email, name=user.name, password=hashed_password, phone=user.phone)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Para garantir que o objeto esteja sincronizado com o banco

    return db_user

## 🔹 Listar usuários
@router.get("/users/", response_model=List[UserResponse])
def list_users():
    return session.query(models.User).all()

## 🔹 Editar usuário
@router.put("/users/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user_update: UserUpdate):
    db_user = session.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user_update.name:
        db_user.name = user_update.name
    if user_update.phone:
        db_user.phone = user_update.phone
    session.commit()
    session.refresh(db_user)
    return db_user

## 🔹 Deletar usuário
@router.delete("/delete/{user_id}", response_model=str)
def delete_user(user_id: int):
    db_user = session.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    session.delete(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "Usuário deletado com sucesso"}

@router.post("/login")
def login(user: UserLogin):
    # if user.email not in fake_users_db:
    #     raise HTTPException(status_code=400, detail="E-mail não cadastrado.")
    # stored_password = fake_users_db[user.email]["password"]
    # if not verify_password(user.password, stored_password):
    #     raise HTTPException(status_code=400, detail="Senha incorreta.")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


