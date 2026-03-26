from fastapi import FastAPI
from routes import setup

app = FastAPI()

app.include_router(setup.router)

@app.get("/")
def root():
    return {"message": "Backend running"}