import logging
from typing import Any

from app.db.models.user import Gender
from app.schemas.user import CreateUserDB

logger = logging.getLogger("development")

def process_user_data(data: list[dict[str, Any]]):
    return [
            CreateUserDB(
                gender=Gender.MALE if d["gender"] == "male" else Gender.FEMALE,
                name=d["name"]["first"],
                surname=d["name"]["last"],
                phone_number=d["phone"],
                email=d["email"],
                country=d["location"]["country"],
                state=d["location"]["state"],
                city=d["location"]["city"],
                street=d["location"]["street"]["name"] + " " + str(d["location"]["street"]["number"]),
                photo_url=d["picture"]["thumbnail"]
            ) for d in data
        ]

