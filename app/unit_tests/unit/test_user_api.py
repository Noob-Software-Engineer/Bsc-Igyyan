from app.api.config.config import LocalConfig

# from app.unit_tests.common.utils import get_mock_student_token
from bson.objectid import ObjectId

base_url = LocalConfig.LOCALHOST


def test_login(client, setup_test_data):
    get_user = {"name": "ashraf", "password": "1234"}
    response = client.post(
        f"{base_url}/auth/login", json=get_user
    )  # Replace with your API endpoint
    # print(response)
    assert response.status_code == 200
    assert (
        "access_token" in response.get_json()
    )  # Assert based on your expected response
