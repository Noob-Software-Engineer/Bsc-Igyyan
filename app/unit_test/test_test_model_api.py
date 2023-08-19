# test_routes.py
from app.api.config.config import LocalConfig
from app.api.common.common import get_student_token
from bson.objectid import ObjectId

base_url = LocalConfig.LOCALHOST


def test_your_api_route(client, setup_test_data):
    get_user = {"name": "ashraf", "password": "1234"}
    response = client.post(
        f"{base_url}/auth/login", json=get_user
    )  # Replace with your API endpoint
    # print(response)
    assert response.status_code == 200
    assert (
        "access_token" in response.get_json()
    )  # Assert based on your expected response


def test_create_test_model(client):
    payload = {
        "creator_id": "64e0ea89d26d3a10b816a2e0",
        "title": "New title",
        "content": "New content",
        "type": None,
        "tags": None,
        "review": None,
    }
    headers = {"Authorization": f"Bearer {get_student_token()}"}
    response = client.post(f"{base_url}/tests/", json=payload, headers=headers)
    print(response.get_json())
    assert response.status_code == 201


def test_get_test_model_by_id(client):
    payload = {
        "creator_id": "64e0ea89d26d3a10b816a2e0",
        "title": "New title",
        "content": "New content",
        "type": None,
        "tags": None,
        "review": None,
    }
    headers = {"Authorization": f"Bearer {get_student_token()}"}
    response = client.post(f"{base_url}/tests/", json=payload, headers=headers)
    test_id = response.get_json()["id"]
    response = client.get(f"{base_url}/tests/{test_id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["id"] == test_id

    test_id = str(ObjectId())
    response = client.get(f"{base_url}/tests/{test_id}", json=payload, headers=headers)
    assert response.status_code == 404


def test_search_test_model(client):
    payload = {
        "creator_id": "64e0ea89d26d3a10b816a2e0",
        "title": "New title",
        "content": "New content",
        "type": None,
        "tags": None,
        "review": None,
    }
    headers = {"Authorization": f"Bearer {get_student_token()}"}
    response = client.post(f"{base_url}/tests/", json=payload, headers=headers)
    response = client.get(f"{base_url}/tests/?limit=5", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["total_count"] == 1

    response = client.get(f"{base_url}/tests/?limit=-1", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.get_json() == {
        "validation_error": {
            "query_params": [
                {
                    "ctx": {"limit_value": 0},
                    "loc": ["limit"],
                    "msg": "ensure this value is greater than or equal to 0",
                    "type": "value_error.number.not_ge",
                }
            ]
        }
    }
