from flask_pymongo import PyMongo
from pymongo.collection import Collection

from app.api.config.config import LocalConfig

pymongo = PyMongo()
users_coll: Collection = pymongo.db[LocalConfig.USER_COLL]
# Create a unique index

users_coll.create_index([("name", 1)], unique=True)

tests_coll: Collection = pymongo.db[LocalConfig.TEST_COLL]
