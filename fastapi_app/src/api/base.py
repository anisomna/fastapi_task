from fastapi import APIRouter, status, HTTPException
from schemas.users import User
from schemas.posts import Post
from schemas.comments import Comment
from schemas.locations import Location
from schemas.categories import Category


router = APIRouter()
