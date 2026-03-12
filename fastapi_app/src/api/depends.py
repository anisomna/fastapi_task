from domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.delete_user import DeleteUserUseCase

from domain.posts.use_cases.get_all_posts import GetAllPostsUseCase
from domain.posts.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.posts.use_cases.get_published_posts import GetPublishedPostsUseCase
from domain.posts.use_cases.create_post import CreatePostUseCase
from domain.posts.use_cases.delete_post import DeletePostUseCase

from domain.comments.use_cases.get_all_comments import GetAllCommentsUseCase
from domain.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from domain.comments.use_cases.create_comment import CreateCommentUseCase
from domain.comments.use_cases.delete_comment import DeleteCommentUseCase

from domain.location.use_cases.get_all_locations import GetAllLocationsUseCase
from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.location.use_cases.get_published_locations import GetPublishedLocationsUseCase
from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase

from domain.category.use_cases.get_all_categories import GetAllCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.get_published_categories import GetPublishedCategoriesUseCase


def get_get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()

def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()

def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()

def get_delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()


def get_get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()

def get_get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()

def get_published_posts_use_case() -> GetPublishedPostsUseCase:
    return GetPublishedPostsUseCase()

def get_create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()

def get_delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_get_all_comments_use_case() -> GetAllCommentsUseCase:
    return GetAllCommentsUseCase()

def get_get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()

def get_create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()

def get_delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def get_get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()

def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()

def get_get_published_locations_use_case() -> GetPublishedLocationsUseCase:
    return GetPublishedLocationsUseCase()

def get_create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()

def get_delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()

def get_get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()

def get_get_published_categories_use_case() -> GetPublishedCategoriesUseCase:
    return GetPublishedCategoriesUseCase()
