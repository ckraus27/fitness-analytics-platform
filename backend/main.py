from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
        "carbs_goal": 300,
        "fat": 0,
        "fat_goal": 70
    }