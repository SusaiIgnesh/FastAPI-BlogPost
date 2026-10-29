from datetime import datetime, UTC
from pydantic import BaseModel, ValidationError, Field, EmailStr, SecretStr, HttpUrl, field_validator, model_validator, ValidationInfo, computed_field, ConfigDict
from typing import Literal, Annotated
from uuid import UUID, uuid4
import json

# Whenever we provdi anything in the default value that fields are optional
# Pydnatic variavles are mututable ,which means you can reassign the values,however those reassigned the values not re validated


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True,
                              extra="allow", strict=True, validate_assignment=True, frozen=True)

    uid: UUID = Field(alias="id", default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    password: SecretStr
    websites: HttpUrl | None = None
    age: Annotated[int, Field(ge=13, le=130)]
    bio: str = ""
    is_active: bool = True

    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError(
                "Username must be alphnumeric (underscore allowed)")

        return v.lower()

    @field_validator("websites", mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 50000


class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0


class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content:  Annotated[str, Field(min_length=1)]
    author: User
    view_counrt: int = 0
    is_punlished: bool = False

    tags: list[str] = Field(default_factory=list)

    create_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    status: Literal["draft", "published", "archived"] = "draft"

    comments: list[Comment] = Field(default_factory=list)


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self) -> "UserRegistration":
        if self.password != self.confirm_password:
            raise ValueError("Password do not match")
        return self


# try:
#     registration = UserRegistration(
#         email="Ignesh@gmail.com",
#         password="1234",
#         confirm_password="5678"
#     )
# except ValidationError as e:
#     print(e)
# Valid User
# user = User(
#     username="Ignesh_Susai",
#     email="CoreyMSchafer@gmail.com",
#     age=39,
#     password="secret123",
#     websites="ignesh.com",
#     first_name="Varun",
#     last_name="007"
# )
# print(user)


user_data = {
    "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    "username": "Corey_Schafer",
    "email": "CoreyMSchafer@gmail.com",
    "age": 39,
    "password": "secret123",
    "notes": "Kind've a Karen...",
}
user = User.model_validate_json(json.dumps(user_data))

user.email = "CoreyMSchafer2@gmail.com"

print(user.model_dump_json(indent=2, by_alias=True, exclude={"password"}))
