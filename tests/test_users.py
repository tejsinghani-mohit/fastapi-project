from app import schemas
from .database import client, session

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "rock@gmail.com", "password": "rock234"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "rock@gmail.com"
    assert res.status_code == 201    

