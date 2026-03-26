from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.base import router as base_router
from api.users import users_router
from api.posts import posts_router
from api.comments import comments_router
from api.categories import categories_router
from api.locations import locations_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    app.include_router(users_router, prefix="/users", tags=["User APIs"])
    app.include_router(posts_router,prefix="/posts", tags=["Post APIs"])
    app.include_router(comments_router,prefix="/comments", tags=["Comment APIs"])
    app.include_router(categories_router, prefix="/categories", tags=["Category APIs"])
    app.include_router(locations_router, prefix="/locations", tags=["Location APIs"])

    return app
