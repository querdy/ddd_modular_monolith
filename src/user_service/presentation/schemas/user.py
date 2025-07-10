from dataclasses import dataclass


@dataclass
class CreateUserRequestSchema:
    username: str
    email: str
    password: str
    repeat_password: str


@dataclass
class LoginRequestSchema:
    email: str
    password: str


@dataclass
class TokenResponseSchema:
    access_token: str
    token_type: str = "Bearer"
