import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from secret import duplicated_user_login, create_data
import requests
import datetime

login_url = "http://localhost:8000/accounts/login/"
datedetail_url = "http://localhost:8000/budget/datedetail/"
            
def test_create_datedetail():
    response = requests.post(url=login_url, json=duplicated_user_login)
    headers = {"Authorization" : f"Bearer {response.json()['jwt_token']['access_token']}"}
    
    response = requests.post(url=datedetail_url, json=create_data)
    
    assert response.status == 200
    
    
if __name__ == "__main__":
    date = "2023-08-20"
    print(date.split("-"))
    print()