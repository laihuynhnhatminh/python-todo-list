from pydantic import BaseModel, Field
from typing import Optional


class CreateTodoDTO(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    completed: bool = Field(default=False)
    user_id: int = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample Todo",
                "description": "This is a sample todo item.",
                "priority": 3,
                "completed": False,
                "user_id": 1,
            }
        }
    }


class UpdateTodoDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3, max_length=100)
    priority: Optional[int] = Field(None, ge=1, le=5)
    completed: Optional[bool] = Field(None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Updated Todo",
                "description": "This is an updated todo item.",
                "priority": 2,
                "completed": True,
            }
        }
    }
