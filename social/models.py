import io
import logging
import os
import uuid
from datetime import date

from django.db import models
from django.utils import timezone
from PIL import Image

from users.models import MyUser

logger = logging.getLogger(__name__)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('posts_images/', filename)


class Post(models.Model):
    # It is 'one to many' relation, because 1 user can have multiple posts.
    # It is done by ForeginKey.
    # on_delete means what happens when user is deleted, CASCADE means delete all his posts.
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=40)
    image = models.ImageField(upload_to=get_file_path)

    """ Resizing images on local storage """

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 510 or img.width > 515:
            # TODO split in 2 mote ifs?
            output_size = (510, 515)
            img.thumbnail(output_size)
            logger.debug(self.image.path)
            img.save(self.image.path)
