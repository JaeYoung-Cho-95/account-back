import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import random
from secret import duplicated_user_signup

url = "http://localhost:8000/accounts/signup/"


def make_random_data():
    n = random.randrange(999)
    data = {
        "email": f"{n}@gmail.com",
        "username": f"t_{n}",
        "nickname": f"nick_{n}",
        "password": f"aA!123{n}",
    }
    return data


def test_correct_create():
    data = make_random_data()
    response = requests.post(url, data)

    assert response.status_code == 201


def test_duplicated_create():
    data = duplicated_user_signup
    response = requests.post(url, data)

    assert response.status_code == 400
