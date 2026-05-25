from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from application.api.users import users_router
from application.api.posts import posts_router
from application.api.comments import comments_router
from application.api.categories import categories_router
from application.api.locations import locations_router
from application.api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/images", StaticFiles(directory="/fastapi_app/images"), name="images")
    app.mount("/comment_images", StaticFiles(directory="/fastapi_app/comment_images"), name="comment_images")
    app.include_router(users_router, prefix="/users", tags=["User APIs"])
    app.include_router(posts_router,prefix="/posts", tags=["Post APIs"])
    app.include_router(comments_router,prefix="/comments", tags=["Comment APIs"])
    app.include_router(categories_router, prefix="/categories", tags=["Category APIs"])
    app.include_router(locations_router, prefix="/locations", tags=["Location APIs"])
    app.include_router(auth_router, tags=["Auth APIs"])

    return app
