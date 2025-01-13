from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    phone: Optional[str] = None
    email: str
    name: str
    
    class Config:
            from_attributes = True  # Para permitir conversão automática do SQLAlchemy para Pydantic