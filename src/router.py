from fastapi import APIRouter

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.get("/")
def get_todos():
    return [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Buy groceries",
            "completed": False,
        },
    ]
