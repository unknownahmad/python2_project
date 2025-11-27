from auth import register_user, authenticate
from db import init_db
import random

def test_register_and_authenticate_user():
    init_db(test=True)

    username = "user_" + str(random.randint(10000, 99999))
    password = "pass1234"
    age = 25

    result = register_user(username, password, age, test=True)
    assert result == "success"

    user = authenticate(username, password, test=True)
    assert user is not None
    assert user.username == username
