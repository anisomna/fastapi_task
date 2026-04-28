from application.domain.user.use_cases.get_all_users import GetAllUsersUseCase
from application.domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from application.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.domain.user.use_cases.delete_user import DeleteUserUseCase

from application.domain.post.use_cases.get_all_posts import GetAllPostsUseCase
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.delete_post import DeletePostUseCase

from application.domain.comments.use_cases.get_all_comments import GetAllCommentsUseCase
from application.domain.comments.use_cases.get_comment_by_id import GetCommentByIdUseCase
from application.domain.comments.use_cases.create_comment import CreateCommentUseCase
from application.domain.comments.use_cases.delete_comment import DeleteCommentUseCase

from application.domain.location.use_cases.get_all_locations import GetAllLocationsUseCase
from application.domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from application.domain.location.use_cases.get_published_locations import GetPublishedLocationsUseCase
from application.domain.location.use_cases.create_location import CreateLocationUseCase
from application.domain.location.use_cases.delete_location import DeleteLocationUseCase

from application.domain.category.use_cases.get_all_categories import GetAllCategoriesUseCase
from application.domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from application.domain.category.use_cases.get_published_categories import GetPublishedCategoriesUseCase
from application.domain.category.use_cases.create_category import CreateCategoryUseCase
from application.domain.category.use_cases.delete_category import DeleteCategoryUseCase

from application.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from application.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()

def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()

def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()

def get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()

def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()

def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()


def get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()

def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()

def add_post_image_use_case() -> AddPostImageUseCase:
    return AddPostImageUseCase()

def get_post_image_use_case() -> GetPostImageUseCase:
    return GetPostImageUseCase()

def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()

def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_all_comments_use_case() -> GetAllCommentsUseCase:
    return GetAllCommentsUseCase()

def get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()

def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()

def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()

def get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()

def get_published_locations_use_case() -> GetPublishedLocationsUseCase:
    return GetPublishedLocationsUseCase()

def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()

def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()

def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()

def get_published_categories_use_case() -> GetPublishedCategoriesUseCase:
    return GetPublishedCategoriesUseCase()

def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()

def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()
