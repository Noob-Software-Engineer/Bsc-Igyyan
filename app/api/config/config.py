from datetime import timedelta


class LocalConfig:
    MONGO_URI = "mongodb://localhost:27017/bsc"
    USER_COLL = "users"
    TEST_COLL = "tests"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    MAX_ITEMS_PER_PAGE = 1000
    DEFAULT_ITEMS_PER_PAGE = 25
