from app.api.config.config import LocalConfig
from datetime import datetime, timedelta
from jose.jwt import encode


def get_mock_student_token():
    payload = dict(
        id="64e0bc377d008754b4a56f55",
        name="ashraf",
        email="ashraf@gmail.com",
        password="1234",
        role="student",
    )
    return encode(
        {
            "sub": payload,  # Replace with the actual subject (user) identifier
            "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time
        },
        key=LocalConfig.JWT_SECRET_KEY,
    )


def apply_changes(obj, exclude: list = None, **kwargs):
    # Exclude the specified fields
    if exclude is not None:
        for f in exclude:
            del obj[f]

    return obj | kwargs


def get_mock_test_model_obj(exclude: list = None, **kwargs):
    payload = {
        "creator_id": "64e0ea89d26d3a10b816a2e0",
        "title": "New title",
        "content": "New content",
        "type": None,
        "tags": None,
        "review": None,
    }
    return apply_changes(payload, exclude, **kwargs)
