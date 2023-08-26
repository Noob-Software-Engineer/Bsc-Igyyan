from app.api.config.config import LocalConfig
from app.unit_tests.common.utils import get_mock_student_token, get_mock_test_model_obj
from bson.objectid import ObjectId
from typing import Optional, Any

base_url = LocalConfig.LOCALHOST


def create_mock_test_model(
    client,
    payload: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
):
    if not payload:
        payload = get_mock_test_model_obj()
    if not headers:
        headers = {"Authorization": f"Bearer {get_mock_student_token()}"}

    response = client.post(f"{base_url}/tests", json=payload, headers=headers)
    assert response.status_code == 201
    return response.get_json()


def test_create_test_model(client):
    headers = {"Authorization": f"Bearer {get_mock_student_token()}"}
    payload = get_mock_test_model_obj(title="Testing for create_test_model")
    test_model = create_mock_test_model(client, payload)
    assert test_model["title"] == "Testing for create_test_model"


def test_get_test_model_by_id(client):
    headers = {"Authorization": f"Bearer {get_mock_student_token()}"}
    test_model = create_mock_test_model(client)
    test_id = test_model["id"]
    response = client.get(f"{base_url}/tests/{test_id}", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["id"] == test_id

    test_id = str(ObjectId())
    response = client.get(f"{base_url}/tests/{test_id}", headers=headers)
    assert response.status_code == 404
    assert response.get_json()["detail"] == "No test document found"


def test_search_test_model(client):
    headers = {"Authorization": f"Bearer {get_mock_student_token()}"}
    number_of_test_models = 20
    test_models = [create_mock_test_model(client) for _ in range(number_of_test_models)]
    response = client.get(f"{base_url}/tests?limit=5", headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()["tests"]) == 5
    assert response.get_json()["total_count"] == number_of_test_models

    response = client.get(f"{base_url}/tests?limit=-1", headers=headers)
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


def test_delete_test_model_by_id(client):
    headers = {"Authorization": f"Bearer {get_mock_student_token()}"}
    test_model = create_mock_test_model(client)
    test_id = test_model["id"]
    response = client.delete(f"{base_url}/tests/{test_id}", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["detail"] == "Test document deleted"

    test_id = str(ObjectId())
    response = client.get(f"{base_url}/tests/{test_id}", headers=headers)
    assert response.status_code == 404
    assert response.get_json()["detail"] == "No test document found"
