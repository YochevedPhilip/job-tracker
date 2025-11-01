from fastapi import status

# ---------------------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------------------
def test_create_user_success(client):
    user_data = {
        "name": "New User",
        "email": "newuser6@example.com",
        "password": "strongpass"
    }


    response = client.post("/users/", json=user_data)
    print("\nRESPONSE JSON:", response.json())

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data


def test_create_user_duplicate_email(client, user_fixture):
    user_data = {
        "name": "Duplicate User",
        "email": user_fixture.email,
        "password": "somepass"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

# ---------------------------------------------------------------------
# READ USERS
# ---------------------------------------------------------------------
def test_read_users(client, user_fixture):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(u["email"] == user_fixture.email for u in data)


def test_read_user_by_id(client, user_fixture):
    response = client.get(f"/users/{user_fixture.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_fixture.id
    assert data["email"] == user_fixture.email


def test_read_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

# ---------------------------------------------------------------------
# UPDATE USER
# ---------------------------------------------------------------------
def test_update_user_success(client, user_fixture):
    update_data = {
        "id": user_fixture.id,
        "password": "updatedpass"
    }
    response = client.patch(f"/users/{user_fixture.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_fixture.id


def test_update_user_not_found(client):
    update_data = {"id": 9999, "password": "doesnotexist"}
    response = client.patch("/users/9999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

# ---------------------------------------------------------------------
# DELETE USER
# ---------------------------------------------------------------------
def test_delete_user_success(client, user_fixture):
    response = client.delete(f"/users/{user_fixture.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
