from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import setup, project
from config.db import get_db
from routes import ai, editor, generate
from fastapi.staticfiles import StaticFiles
import os



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(setup.router)
app.include_router(project.router)
app.include_router(ai.router)
app.include_router(generate.router)
app.include_router(editor.router)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "..", "image_gen", "outputs")

print("Serving images from:", IMAGE_DIR)  # debug

app.mount(
    "/image_gen/outputs",
    StaticFiles(directory=IMAGE_DIR),
    name="images"
)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/test-db")
def test_db():
    db.projects.insert_one({"test": "working"})
    return {"message": "DB connection successful!"}
