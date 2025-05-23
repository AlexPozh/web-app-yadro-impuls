from unittest.mock import patch, Mock

import httpx
import pytest

from app.utils.process_data import process_user_data
from app.utils.api_client import fetch_api_data
from app.schemas.user import CreateUserDB
from app.db.models.user import Gender

def test_process_user_data():
    raw_data = [
        {
            "gender": "female",
            "name": {
                "title": "Ms",
                "first": "Aria",
                "last": "Chen"
            },
            "location": {
                "street": {
                    "number": 9835,
                    "name": "Ponsonby Road"
                },
                "city": "Auckland",
                "state": "Manawatu-Wanganui",
                "country": "New Zealand",
                "postcode": 23095,
                "coordinates": {
                    "latitude": "52.3288",
                    "longitude": "99.7408"
                },
                "timezone": {
                    "offset": "-10:00",
                    "description": "Hawaii"
                }
            },
            "email": "aria.chen@example.com",
            "phone": "(333)-132-9777",
            "picture": {
                "large": "https://randomuser.me/api/portraits/women/17.jpg",
                "medium": "https://randomuser.me/api/portraits/med/women/17.jpg",
                "thumbnail": "https://randomuser.me/api/portraits/thumb/women/17.jpg"
            }
        }
    ]
    
    expected_data = CreateUserDB(
        gender=Gender.MALE if raw_data[0]["gender"] == "male" else Gender.FEMALE,
        name=raw_data[0]["name"]["first"],
        surname=raw_data[0]["name"]["last"],
        phone_number=raw_data[0]["phone"],
        email=raw_data[0]["email"],
        country=raw_data[0]["location"]["country"],
        state=raw_data[0]["location"]["state"],
        city=raw_data[0]["location"]["city"],
        street=raw_data[0]["location"]["street"]["name"] + " " + str(raw_data[0]["location"]["street"]["number"]),
        photo_url=raw_data[0]["picture"]["thumbnail"]
    )

    assert process_user_data(raw_data)[0] == expected_data

@pytest.mark.asyncio
async def test_fetch_api_data():
    response_json = {
        "results": [
            {
                "gender": "female",
                "name": {
                    "title": "Ms",
                    "first": "Aria",
                    "last": "Chen"
                },
                "location": {
                    "street": {
                        "number": 9835,
                        "name": "Ponsonby Road"
                    },
                    "city": "Auckland",
                    "state": "Manawatu-Wanganui",
                    "country": "New Zealand",
                    "postcode": 23095,
                    "coordinates": {
                        "latitude": "52.3288",
                        "longitude": "99.7408"
                    },
                    "timezone": {
                        "offset": "-10:00",
                        "description": "Hawaii"
                    }
                },
                "email": "aria.chen@example.com",
                "phone": "(333)-132-9777",
                "picture": {
                    "large": "https://randomuser.me/api/portraits/women/17.jpg",
                    "medium": "https://randomuser.me/api/portraits/med/women/17.jpg",
                    "thumbnail": "https://randomuser.me/api/portraits/thumb/women/17.jpg"
                }
            }
        ],
        "info": {
            "seed": "d53cf6bc611130d7",
            "results": 1,
            "page": 1,
            "version": "1.4"
        }
    }
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = response_json

    with patch("app.utils.api_client.httpx.AsyncClient.get", return_value=response_mock):
        url = "https://randomuser.me/api/?inc=gender,name,email,phone,location,picture"
        result = await fetch_api_data(url)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"]["first"] == "Aria"


@pytest.mark.asyncio
async def test_fetch_api_data_http_error():
    response_mock = Mock()
    response_mock.status_code = 500
    response_mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Server error",
        request=Mock(),
        response=response_mock
    )

    with patch("app.utils.api_client.httpx.AsyncClient.get", return_value=response_mock):
        url = "https://randomuser.me/api/?inc=gender,name,email,phone,location,picture"
        result = await fetch_api_data(url)

    assert result is None


@pytest.mark.asyncio
async def test_fetch_api_data_request_error():
    response_mock = Mock()
    response_mock.status_code = 500
    response_mock.raise_for_status.side_effect = httpx.RequestError(
        message="Request failed",
        request=Mock()
    )

    with patch("app.utils.api_client.httpx.AsyncClient.get", return_value=response_mock):
        url = "https://randomuser.me/api/?inc=gender,name,email,phone,location,picture"
        result = await fetch_api_data(url)

    assert result is None