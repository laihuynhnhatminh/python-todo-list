from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session

from database.db import get_db
from dtos.todos import CreateTodoDTO, UpdateTodoDTO
from models.todos import Todo
from services.auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(Todo).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user["id"]).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: CreateTodoDTO):
    todo_model = Todo(**todo.model_dump(), user_id=user["id"])

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.patch("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    update_todo: UpdateTodoDTO = None,
    todo_id: int = Path(gt=0),
):
    existing_todo = (
        db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user["id"]).first()
    )

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    for field, value in update_todo.model_dump(exclude_unset=True).items():
        setattr(existing_todo, field, value)

    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    rows_deleted = (
        db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user["id"]).delete()
    )

    if rows_deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    db.commit()
