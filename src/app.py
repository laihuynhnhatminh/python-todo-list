import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers.todos import router as todos_router
from routers.auth import router as auth_router
from database.db import engine


# TODO: Add config module function here to load environment variables


def create_app(lifespan=None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # TODO: Middleware configuration here

    # Routes configuration
    common_prefix = f"/api"
    app.include_router(todos_router, prefix=common_prefix)
    app.include_router(auth_router, prefix=common_prefix)

    # TODO Remove docs from production

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    from database.db import Base  # Import base that all models inherit from

    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

    yield  # App runs here

    # Shutdown: cleanup if needed
    engine.dispose()
    print("✓ Database connections closed")


app = create_app(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
