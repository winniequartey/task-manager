from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from app.server.database import (
    add_task,
    retrieve_tasks,
    retrieve_task,
    update_task,
    delete_task
)
from app.server.models.task import (
    ErrorResponseModel,
    ResponseModel,
    TaskSchema
)
router = APIRouter()

@router.post("/add", response_description="Task added into the database")
async def add_task_data(task: TaskSchema = Body(...)):
    task = jsonable_encoder(task)
    task['dueDate'] = datetime.strptime(task['dueDate'], '%Y-%m-%dT%H:%M:%S')
    task['dateCreated'] = datetime.now()
    new_task = await add_task(task)
    return ResponseModel(new_task, "Task added successfully.")

@router.get("/", response_description="Tasks retrieved")
async def get_tasks():
    tasks = await retrieve_tasks()
    if tasks:
        return ResponseModel(tasks, "Tasks retrieved successfully")
    return ResponseModel(tasks, "Empty list returned")

@router.get("/{id}", response_description="Task retrieved")
async def get_task_data(id):
    task = await retrieve_task(id)
    if task:
        return ResponseModel(task, "Task retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Task doesn't exist.")

@router.put("/{id}", response_description="Task data updated")
async def update_task_data(id: str, req: TaskSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_task = await update_task(id, req)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} update is successful".format(id),
            "Task updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )

@router.delete("/{id}", response_description="Task data deleted from the database")
async def delete_task_data(id: str):
    deleted_task = await delete_task(id)
    if deleted_task:
        return ResponseModel(
            "Task with ID: {} removed".format(id), "Task deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Task with id {0} doesn't exist".format(id)
    )