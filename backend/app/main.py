from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, predict, students
from app.database import Base, engine
from app import models
from app.routes import dashboard
from app.routes import interventions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FAILSAFE API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/auth")
app.include_router(predict.router, prefix="/predict")
app.include_router(students.router,prefix="/students")
app.include_router(
    dashboard.router,
    prefix="/dashboard"
)
app.include_router(
    interventions.router,
    prefix="/interventions",
    tags=["Interventions"]
)

@app.get("/health")
def health():
    return {"status": "ok"}