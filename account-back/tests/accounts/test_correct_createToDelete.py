import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import random

signup_url = "http://localhost:8000/accounts/signup/"
login_url = "http://localhost:8000/accounts/login/"
detail_url = "http://localhost:8000/accounts/detail/"

n = random.randrange(100,999)
signup_data = {
    "email": f"{n}@gmail.com",
    "username": f"t_{n}",
    "nickname": f"nick_{n}",
    "password": f"aA!123{n}",
}
login_data = {
    "email": f"{n}@gmail.com",
    "password": f"aA!123{n}"
}

change_data = {
    "email": f"{n}@gmail.com",
    "nickname": f"{n}",
    "current_password": f"aA!123{n}",
    "password": "A1q2w3e4r!!",
    "password_check": "A1q2w3e4r!!"
}

delete_data = {
    "email": f"{n}@gmail.com",
    "password": f"A1q2w3e4r!!"
}


def test_correct_create():
    response = requests.post(signup_url, signup_data)

    assert response.status_code == 201

def test_exsist_user_login():
    response = requests.post(url=login_url, data=login_data)
    
    assert response.status_code == 200

def test_correct_user_detail():
    response = requests.post(url=login_url, data=login_data)
    
    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}
    data = {
        'email': login_data["email"]
    }
    response = requests.get(url=detail_url, headers=headers, params=data)

    assert response.json()["email"] == login_data["email"]
    assert response.status_code == 200

def test_exsist_user_change():
    response = requests.post(url=login_url, data=login_data)
    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}

    response = requests.patch(url=detail_url, data=change_data, headers=headers)
    
    assert response.status_code == 200
    
def test_exsist_user_delete():
    response = requests.post(url=login_url, data=delete_data)

    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}
    response = requests.delete(url=detail_url, data=delete_data, headers=headers)
    
    assert response.status_code == 204