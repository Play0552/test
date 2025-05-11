from fastapi import FastAPI
import uvicorn

from app.config.settings import settings
from app.routers.api import api_router


app = FastAPI()

app.include_router(api_router)


def run():
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.API_WORKERS,
    )


if __name__ == "__main__":
    run()
