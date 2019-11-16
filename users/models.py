import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('PIL').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pics/', filename)


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
    last_login = models.DateTimeField('last login', blank=True, null=True)

    is_admin = models.BooleanField(
        'admin status',
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

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


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    website = models.CharField(max_length=40)
    image = models.ImageField(default='default.jpg', upload_to=get_file_path)

    def __str__(self):
        return f'{self.user.username} Profile'

    """ Resizing images on local storage """

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        logger.debug(self.image.path)
        img = Image.open(self.image.path)
        logger.debug(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            logger.debug(self.image.path)
            img.save(self.image.path)

    """ Resizing images on S3 """

    # def save(self, *args, **kwargs):
    #         super().save(*args, **kwargs)
    #         logger.debug("Saving image!")
    #         img_read = storage.open(self.image.name, 'r')
    #         logger.debug(img_read)
    #         img = Image.open(img_read)
    #         logger.debug(img)

    #         if img.height > 300 or img.width > 300:
    #             logger.debug("Resizing!")
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             in_mem_file = io.BytesIO()
    #             img.save(in_mem_file, format='JPEG')
    #             img_write = storage.open(self.image.name, 'w+')
    #             img_write.write(in_mem_file.getvalue())
    #             img_write.close()
    #             logger.debug("Resized successfully!")

    #         img_read.close()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
