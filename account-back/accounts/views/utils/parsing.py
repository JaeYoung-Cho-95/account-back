from venv import logger
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("A")


class Parsing:
    def parse_user_info(self, request):
        if request.method == "GET":
            email = request.query_params.get("email")
            password = None
            
        elif request.method == "PATCH":
            email = request.data.get("email")
            password = request.data.get("current_password")

        else:
            email = request.data.get("email")
            password = request.data.get("password")

        User = get_user_model()
        user = User.objects.filter(email=email).first()

        return user, password

    @staticmethod
    def pop_email_username(data):
        data = data.copy()
        data.pop("email", None)
        data.pop("username", None)

        return data
    
    
    @staticmethod
    def pop_change_password(data):
        data = data.copy()
        data.pop("current_password", None)
        data.pop("password_check", None)
        password = data.pop("password", None)
        data["password"] = password
        return data
