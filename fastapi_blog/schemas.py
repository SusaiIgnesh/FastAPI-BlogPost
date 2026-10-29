from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

# User( used to validate user creation)


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    # Model_config used for pydantic read from sqlcml model(DB)
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    image_file: str | None
    image_path: str


class UserPrivate(UserPublic):
    email: EmailStr

# Update the user details


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)

# Token schema for login update


class Token(BaseModel):
    access_token: str
    token_type: str


# Posts( Used to validate the post creation)
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    # author :str = Field(min_length=1,max_length=50)

# New post


class PostCreate(PostBase):
    pass  # Tempory (because it will come from seeion when use authetication)

# Updating exiting post


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)

# Final reponse


class PostResponse(PostBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: datetime
    author: UserPublic


# Pagination post response
class PaginatedPostsReponse(BaseModel):
    posts: list[PostResponse]
    total: int
    skip: int
    limit: int
    has_more: bool


# Password Reset Schemas

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=120)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
