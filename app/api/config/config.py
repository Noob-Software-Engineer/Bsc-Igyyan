from datetime import timedelta


class LocalConfig:
    MONGO_URI = "mongodb://localhost:27017/bsc"
    USER_COLL = "users"
    TEST_COLL = "tests"
    POST_COLL = "posts"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    MAX_ITEMS_PER_PAGE = 1000
    DEFAULT_ITEMS_PER_PAGE = 25
    MONGO_TEST_URI = "mongodb://localhost:27017/test_bsc"
    JWT_SECRET_KEY = "your-secret-key"
    LOCALHOST = "http://127.0.0.1:5000"
