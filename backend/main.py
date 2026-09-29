from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from models import Base, User, FoodEntry
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

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

class FoodEntryCreate(BaseModel):
    user_id: int
    food_id: int
    amount_grams: float
    consumed_at: datetime

class FoodEntryUpdate(BaseModel):
    amount_grams: float

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

@app.post("/api/food-entries")
def create_food_entry(food_entry: FoodEntryCreate, db: Session=Depends(get_db)):
    new_food_entry = FoodEntry(
        user_id=food_entry.user_id,
        food_id=food_entry.food_id,
        amount_grams=food_entry.amount_grams,
        consumed_at=food_entry.consumed_at
    )

    db.add(new_food_entry)
    db.commit()
    db.refresh(new_food_entry)

    return new_food_entry

@app.get("/api/food-entries")
def get_food_entries(db: Session = Depends(get_db)):
    food_entries = db.query(FoodEntry).all()
    return food_entries

@app.get("/api/food-entries/{entry_id}")
def get_food_entry(entry_id: int, db: Session = Depends(get_db)):
    food_entry = db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()

    if food_entry is None:
        raise HTTPException(status_code=404, detail="Food entry not found")

    return food_entry

@app.put("/api/food-entries/{entry_id}")
def update_food_entry(
    entry_id: int,
    food_entry: FoodEntryUpdate,
    db: Session = Depends(get_db)
):
    food_entry_to_update = db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()

    if food_entry_to_update is None:
        raise HTTPException(status_code=404, detail="Food entry not found")

    food_entry_to_update.amount_grams = food_entry.amount_grams

    db.commit()
    db.refresh(food_entry_to_update)

    return food_entry_to_update