from pydantic import BaseModel

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str
#     full_name: str
#     role: str
#     is_active: bool

#     class Config:
#         orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    username: str