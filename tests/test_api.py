from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.schemas.user import GetUserDB


def test_get_main_page_returns_200(client: TestClient):
    users = [
        GetUserDB(
            id=1,
            gender="female",
            name="Alice",
            surname="Black",
            phone_number="89502342453",
            email="bla@mail.ru",
            country="Russia",
            state="Moscow",
            city="Moscow",
            street="Walls 1234",
            photo_url="photo.png"
        ),
        GetUserDB(
            id=2,
            gender="female",
            name="Alena",
            surname="Black",
            phone_number="89502342456",
            email="bla@mail.com",
            country="Russia",
            state="Moscow",
            city="Moscow",
            street="Wall 123",
            photo_url="photo34.png"
        ),
    ]
    total_users = 2

    with patch("app.api.user.get_users", AsyncMock(return_value=users)), \
         patch("app.api.user.get_total_users", AsyncMock(return_value=total_users)):
        
        response = client.get("/homepage")
        assert response.status_code == 200
        #TODO проверить шаблон 


def test_get_main_page_returns_404(client: TestClient):
    with patch("app.api.user.get_users", AsyncMock(return_value=None)), \
         patch("app.api.user.get_total_users", AsyncMock(return_value=0)):
        
        response = client.get("/homepage")
        assert response.status_code == 404


def test_get_random_user_returns_200(client: TestClient):
    random_user = GetUserDB(
        id=1,
        gender="female",
        name="Alice",
        surname="Black",
        phone_number="89502342453",
        email="bla@mail.ru",
        country="Russia",
        state="Moscow",
        city="Moscow",
        street="Walls 1234",
        photo_url="photo.png"
    )
    with patch("app.api.user.get_random_user", AsyncMock(return_value=random_user)):
        response = client.get("/homepage/random")
        assert response.status_code == 200


def test_get_random_user_returns_404(client: TestClient):
    with patch("app.api.user.get_random_user", AsyncMock(return_value=None)):
        response = client.get("/homepage/random")
        assert response.status_code == 404


def test_get_user_by_id_returns_200(client: TestClient):
    mock_user = GetUserDB(
        id=1,
        gender="female",
        name="Alice",
        surname="Black",
        phone_number="89502342453",
        email="bla@mail.ru",
        country="Russia",
        state="Moscow",
        city="Moscow",
        street="Walls 1234",
        photo_url="photo.png"
    )

    with patch("app.api.user.get_user", AsyncMock(return_value=mock_user)):
        response = client.get("/homepage/1")
        assert response.status_code == 200


def test_get_user_by_id_returns_404(client: TestClient):
    with patch("app.api.user.get_user", AsyncMock(return_value=None)):
        response = client.get("/homepage/0")
        assert response.status_code == 404


def test_post_new_users(client: TestClient):
    with patch("app.api.user.load_new_users", AsyncMock(return_value=None)), \
         patch("app.api.user.get_total_users", AsyncMock(return_value=1)), \
         patch("app.api.user.get_users", AsyncMock(return_value=[])):
        
        response = client.post("/homepage/load_users", data={"count": "10"}, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers.get("location") == "/homepage"
