import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_STRING")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.task_manager
tasks_collection = database.get_collection("tasks")

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "priority": task["priority"],
        "complexity": task["complexity"],
        "status": task["status"],
        "dateCreated": task["dateCreated"],
        "dueDate": task["dueDate"]
    }

# Retrieve all tasks present in the database
async def retrieve_tasks():
    tasks = []
    async for task in tasks_collection.find():
        tasks.append(task_helper(task))
    return tasks

# Add a new task into to the database
async def add_task(task_data: dict) -> dict:
    task = await tasks_collection.insert_one(task_data)
    new_task = await tasks_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)

# Retrieve a task with a matching ID
async def retrieve_task(id: str) -> dict:
    task = await tasks_collection.find_one({"_id": ObjectId(id)})
    if task:
        return task_helper(task)
    
# Update a task with a matching ID
async def update_task(id: str, data: dict):
    # Return false if an empty request body is sent
    if len(data) < 1:
        return False
    task = await tasks_collection.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = await tasks_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task:
            return True
        return

# Delete a task from the database
async def delete_task(id: str):
    task = await tasks_collection.find_one({"_id": ObjectId(id)})
    if task:
        await tasks_collection.delete_one({"_id": ObjectId(id)})
        return True

# Retrieve all tasks with a matching priority
async def retrieve_tasks_by_priority(priority: str):
    tasks = []
    async for task in tasks_collection.find({"priority": priority}):
        tasks.append(task_helper(task))
    return tasks

# Retrieve all tasks due on a specific date
async def retrieve_tasks_by_due_date(due_date: datetime):
    tasks = []
    async for task in tasks_collection. find({"dueDate": due_date}):
        tasks.append(task_helper(task))
    return tasks