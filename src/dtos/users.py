from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "test@test.com",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "password": "password123",
                "role": "user",
            }
        }
    }

class LoginUserDTO(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "test@test.com",
                "password": "password123",
            }
        }
    }