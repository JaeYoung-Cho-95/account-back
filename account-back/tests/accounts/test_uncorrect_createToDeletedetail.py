import os, sys
from venv import logger
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import random
from secret import duplicated_user_signup, duplicated_user_login

signup_url = "http://localhost:8000/accounts/signup/"
login_url = "http://localhost:8000/accounts/login/"
detail_url = "http://localhost:8000/accounts/detail/"


def test_uncorrect_create():
    data = duplicated_user_signup
    response = requests.post(signup_url, data)

    assert response.status_code == 400
    
def test_noexsist_user_login():
    n = random.randrange(1000)
    data = {"email": f"{n}@gmail.com", "password": f"{n}"}
    response = requests.post(url=login_url, data=data)

    assert response.status_code == 400

def test_uncorrect_user_detail():
    n = random.randrange(1000)
    data = {"email": f"{n}@gmail.com", "password": f"{n}"}
    response = requests.post(detail_url, data)

    assert response.status_code == 401

def test_noexsist_user_change():
    change_data = {
    "email": f"@gmail.com",
    "nickname": f"",
    "password": "A1q!w3@!"
    }
    
    response = requests.patch(url=detail_url, data=change_data)
    assert response.status_code == 401
    
    response = requests.post(url=login_url, data=duplicated_user_login)
    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}

    response = requests.patch(url=detail_url, data=change_data, headers=headers)
    
    assert response.status_code == 400

def test_exsist_user_delete():
    response = requests.delete(url=detail_url, data=duplicated_user_login)
    
    temp_data = duplicated_user_login.copy()
    response = requests.post(url=login_url, data=temp_data)
    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}
    
    temp_data["email"] = "333@gmail.com"
    response = requests.delete(url=detail_url, data=temp_data, headers=headers)
    
    assert response.status_code == 400
    
    temp_data = duplicated_user_login.copy()
    response = requests.post(url=login_url, data=temp_data)
    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}
    
    duplicated_user_login["password"] = "1234qqqq"
    response = requests.delete(url=detail_url, data=duplicated_user_login, headers=headers)
    assert response.status_code == 401
    