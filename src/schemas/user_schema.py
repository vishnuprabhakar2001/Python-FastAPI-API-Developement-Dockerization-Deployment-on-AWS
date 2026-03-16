from pydantic import BaseModel

class RegisterUser(BaseModel):
    f_name: str
    l_name: str
    email: str
    phone: str
    address: str


class UpdateUser(BaseModel):
    userId: str
    token: str
    f_name: str | None = None
    l_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None

class GetProfileRequest(BaseModel):
    userId: str
    token: str    