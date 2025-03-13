from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field 

class TaskSchema(BaseModel):
    title: str = Field(...)
    description: Optional[str]
    priority: str = Field(..., pattern="^(high|medium|low)$")
    complexity: str = Field(..., pattern="^(high|medium|low)$")
    status: str = Field(..., pattern="^(open|in-progress|completed|suspended)$")
    dueDate: datetime = Field(...) 

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Task 1",
                "description": "This is a description",
                "priority": "high",
                "complexity": "high", 
                "status": "in-progress",
                "dueDate": "2025-03-15T14:30:00"
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}