from pydantic import BaseModel

from app.db.models.user import Gender


class CreateUserDB(BaseModel):
    gender: Gender
    name: str
    surname: str
    phone_number: str
    email: str
    country: str
    state: str
    city: str
    street: str
    photo_url: str

class GetUserDB(BaseModel):
    id: int
    gender: str
    name: str
    surname: str
    phone_number: str
    email: str
    country: str
    state: str
    city: str
    street: str
    photo_url: str
