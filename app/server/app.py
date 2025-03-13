from fastapi import FastAPI
from app.server.routes.task import router as TaskRouter

app = FastAPI()

app.include_router(TaskRouter, tags=["Task"], prefix="/task")

@app.get("/", tags=["Root"]) # "Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation"
def read_root():
    return {"message": "Welcome to your task manager"}