import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from secret import duplicated_user_login

login_url = "http://localhost:8000/accounts/login/"
detail_url = "http://localhost:8000/accounts/detail/"


# 정상계정으로 마이페이지 요청
def test_correct_user_detail():
    data = duplicated_user_login
    response = requests.post(url=login_url, data=data)

    headers = {"Authorization": f"Bearer {response.json()['jwt_token']['access_token']}"}
    data = {
        'email': duplicated_user_login["email"]
    }
    response = requests.get(url=detail_url, headers=headers, params=data)
    
    assert response.json()["email"] == duplicated_user_login["email"]
    assert response.status_code == 200