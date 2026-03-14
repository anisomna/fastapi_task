import asyncio
import uvicorn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from app import create_app
from infrastructure.sqlite.database import database, Base

app = create_app()


@app.on_event("startup")
def startup():
    from infrastructure.sqlite.models import users, posts, comments, categories
    Base.metadata.create_all(bind=database._engine)


async def run() -> None:
    config = uvicorn.Config(
        "main:app", host="127.0.0.1", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
