import pytest
import os
from fastapi.testclient import TestClient
from application.config import Config

TEST_USERNAME = " johnn"
TEST_PASSWORD = "testpass"
TEST_EMAIL = "gop88315@gmail.com"


@pytest.fixture
def app(monkeypatch):
    """a fake app but in my case it has to be adjusted manually by switching databases in .env"""
    monkeypatch.setenv('SQLALCHEMY_DATABASE_URI', Config.MOCK_SQLALCHEMY_DATABASE_URI)
    from application.main import create_app

    app = create_app()
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return TestClient(app)


@pytest.fixture
def authentication_headers(client):
    """authentication for getting tokens"""
    def _authentication_headers(type="acc"):
        username = TEST_USERNAME
        password = TEST_PASSWORD

        resp = client.post(
            '/auth/login',
            json={
                "username": username,
                "password": password,
            }
        )

        if resp.status_code == 401:
            resp = client.post(
                '/auth/register',
                json={
                    "email": TEST_EMAIL,
                    "username": username,
                    "password": password,

                }
            )
        if type == "acc":
            auth_token = resp.json()['access_token']
        else:
            auth_token = resp.json()['refresh_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        return headers

    return _authentication_headers
