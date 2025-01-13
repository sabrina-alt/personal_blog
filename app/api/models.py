from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey  # Corrigindo a importação
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///./blog.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, nullable=True)
    
    def __init__(self, name, email, password, phone=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone

# class Post(Base):
#     __tablename__ = 'posts'
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     content = Column(String)
#     created_at = Column(DateTime)
    
#     user_id = Column(Integer, ForeignKey('users.id'))  # Agora com ForeignKey
    
#     owner = relationship("User", back_populates="posts")
Base.metadata.create_all(bind=db)