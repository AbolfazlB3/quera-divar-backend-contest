from cv2 import Algorithm
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from datetime import datetime, timedelta

from django.conf import settings

import jwt


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        if name is None:
            raise TypeError('Users must have a name.')

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", db_index=True, unique=True)
    name = models.CharField(verbose_name="name", max_length=255, unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    @property
    def token(self):
        return self.generate_token()

    def generate_token(self):
        # dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'userId': self.pk,
            'email': self.email,
        }, settings.SECRET_KEY, algorithm='HS256')

        print(token)

        return token
