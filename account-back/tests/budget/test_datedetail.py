import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from secret import duplicated_user_login, create_data
import requests

login_url = "http://localhost:8000/accounts/login/"
datedetail_url = "http://localhost:8000/budget/datedetail/"

duplicated_user_login = {"email": "test@test.com", "password": "A1q2w3e4r!!"}

def test_create_datedetail():
    response = requests.post(url=login_url, json=duplicated_user_login)
    headers = {
        "Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"
    }

    response = requests.post(url=datedetail_url, headers=headers, json=create_data)
    print(response.json())
    
    assert response.status_code == 200
