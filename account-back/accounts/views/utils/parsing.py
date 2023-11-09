from django.contrib.auth import get_user_model


class Parsing:
    def parse_user_info(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 데이터 추출
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
        data.pop("password", None)
        password = data.pop("change_password", None)
        data["password"] = password
        return data