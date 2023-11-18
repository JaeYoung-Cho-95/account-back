from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from traitlets import default
from .managers import UserManager

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=200, default="images/basic_profile/account_profile_0.png")
    
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = [
        "username",
        "nickname"
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.username