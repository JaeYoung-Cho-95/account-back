import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import random
from secret import duplicated_user_login

url = "http://localhost:8000/accounts/login/"


def test_noexsist_user():
    n = random.randrange(100000)

    data = {"email": f"{n}@gmail.com", "password": f"{n}"}

    response = requests.post(url=url, data=data)

    assert response.status_code == 400


def test_exsist_user():
    data = duplicated_user_login
    response = requests.post(url=url, data=data)    
    assert response.status_code == 200