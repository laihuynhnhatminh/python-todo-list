import uvicorn

from fastapi import FastAPI
from router import router as todos_router

def create_app():
    app = FastAPI()

    common_prefix = f"/api"
    app.include_router(todos_router, prefix=common_prefix)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000)
