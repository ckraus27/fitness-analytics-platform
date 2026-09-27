from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from models import Base, User
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
engine = create_engine(settings.database_url)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Fitness Analytics API is running!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/dashboard")
def dashboard():
    return{
        "calories": 0,
        "calorie_goal": 2500,
        "protein": 0,
        "protein_goal": 150,
        "carbs": 0,
        "carbs_goal": 300,
        "fat": 0,
        "fat_goal": 70
    }

@app.post("/api/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users")
def get_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user:UserUpdate, db: Session=Depends(get_db)):
    user_to_update = db.query(User).filter(User.id == user_id).first()

    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_update.username = user.username
    user_to_update.email = user.email

    db.commit()

    return user_to_update

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}
