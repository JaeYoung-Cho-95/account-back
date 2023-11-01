from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, userID ,email, phone_number, password=None,**extra_fields):
        if not username:
            raise ValueError("반드시 이름을 입력해야합니다.")
        
        if not userID:
            raise ValueError("반드시 아이디를 입력해야합니다.")    
        
        if not email:
            raise ValueError("반드시 email 주소를 입력해야합니다.")
        
        user = self.model(
            username = username,
            userID = userID,
            email = email,
            phone_number = phone_number,
            **extra_fields
            )
        
        user.set_password(password)
        user.save()
        
        return user


    def create_superuser(self, username, userID, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, userID, email, phone_number, password, **extra_fields)