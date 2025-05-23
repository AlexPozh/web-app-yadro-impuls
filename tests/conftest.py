import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.user import router as users_router


@pytest.fixture
def client():
    test_app = FastAPI()
    test_app.include_router(users_router)
    return TestClient(test_app)
