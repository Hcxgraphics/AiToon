from fastapi import FastAPI
from routes import setup
from config.db import db


app = FastAPI()

app.include_router(setup.router)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/test-db")
def test_db():
    db.projects.insert_one({"test": "wohooo! working :) "})
    return {"message": "DB connection successful!"}