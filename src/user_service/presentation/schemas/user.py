from dataclasses import dataclass, field, Field


@dataclass
class CreateUserRequestSchema:
    username: str
    email: str
    password: str
    repeat_password: str


@dataclass
class LoginRequestSchema:
    email: str = field(default="email@gmail.com")
    password: str = field(default="")


@dataclass
class ChangePasswordRequestSchema:
    old_password: str = field(default="")
    new_password: str = field(default="")
    repeat_password: str = field(default="")


@dataclass
class TokenResponseSchema:
    access_token: str
    token_type: str = "Bearer"
