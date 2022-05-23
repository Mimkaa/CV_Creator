def test_register(client, app):
    resonse = client.post(
        '/auth/register',
        json={

            "email": "gop88315@gmail.com",
            "username": " johnn",
            "password": "testpass",
        }
    )
    data = resonse.json()
    assert resonse.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]


def test_login(client, app):
    resonse = client.post(
        '/auth/login',
        json={
            "username": " johnn",
            "password": "testpass",
        }
    )
    data = resonse.json()
    assert resonse.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]


def test_refresh(client, app, authentication_headers):
    resonse = client.post(
        '/auth/refresh',
        headers=authentication_headers(type="refresh")
    )
    data = resonse.json()
    assert resonse.status_code == 200
    assert data["access_token"]


def test_logout_access(client, app, authentication_headers):
    resonse = client.post(
        '/auth/logout_access',
        headers=authentication_headers()
    )
    data = resonse.json()
    assert data['message'] == "Access token has been revoked"


def test_logout_refresh(client, app, authentication_headers):
    resonse = client.post(
        '/auth/logout_refresh',
        headers=authentication_headers(type="refresh")
    )
    data = resonse.json()
    assert data['message'] == "Refresh token has been revoked"
