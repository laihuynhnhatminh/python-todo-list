import uvicorn

from fastapi import FastAPI

import models
from router import router as todos_router
from database import engine


#TODO: Add config module function here to load environment variables

def create_app():
    app = FastAPI()

    #TODO: Middleware configuration here

    #Routes configuration
    common_prefix = f"/api"
    app.include_router(todos_router, prefix=common_prefix)

    #TODO Remove docs from production

    return app


app = create_app()
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
