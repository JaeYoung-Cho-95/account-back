from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("반드시 email 주소를 입력해야합니다.")
        
        if not username:
            raise ValueError("반드시 이름을 입력해야합니다.")

        if not nickname:
            raise ValueError("반드시 별명를 입력해야합니다.")


        user = self.model(
            email=email,
            username=username,
            nickname=nickname,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, nickname, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, nickname, password, **extra_fields)
