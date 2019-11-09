import logging

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        logger.debug('MyUserManager called.')

        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        logger.debug('MyUserManager saved a new user.')
        return user

    def create_superuser(self, email, username, password):
        logger.debug('MyUserManager of a superuser called.')
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        logger.debug('MyUserManager saved a new superuser.')
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(max_length=20, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    """
    REQUIRED_FIELDS must contain all required fields on your user model, 
    but should not contain the USERNAME_FIELD or password 
    as these fields will always be prompted for.
    """
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
