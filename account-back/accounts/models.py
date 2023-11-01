from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    userID = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(db_index=True, unique=True)

    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'userID'
    
    REQUIRED_FIELDS = [
        "username",
        "email",
        "phone_number"
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.username