from fastapi import APIRouter, status, HTTPException
from schemas.users import User
from schemas.posts import Post
from schemas.comments import Comment
from schemas.locations import Location
from schemas.categories import Category


router = APIRouter()


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    response = {"text": "Hello, World!"}

    return response


@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post) -> dict:
    if len(post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    response = {
        "post_text": post.text,
        "author_name": post.author.login
    }

    return Post.model_validate(obj=response)


@router.put("/update_post", status_code=status.HTTP_200_OK)
async def update_post(updated_post: Post) -> dict:
    if len(updated_post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
    
    return {
        "message": "Информация успешно обновлена!",
        "updated_post": Post.model_validate({
            "post_text": updated_post.text,
            "author_name": updated_post.author.login
        })
    }

@app.delete("/delete_post", status_code=status.HTTP_200_OK)
async def delete_post(post: Post):
    # check to delete post
    if check:
        return {"message": "Публикация успешно удалена!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении публикации")
