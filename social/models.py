import datetime
import io
import logging
import os
import uuid
from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.core.validators import MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from social_app.utils import get_file_path_folder
from users.models import UserProfile

logger = logging.getLogger(__name__)


def get_file_path(instance, filename):
    folder_name = 'posts_images/'
    return get_file_path_folder(instance, folder_name, filename)


class Post(models.Model):
    # It is 'one to many' relation, because 1 user can have multiple posts.
    # It is done by ForeginKey.
    # on_delete means what happens when user is deleted, CASCADE means delete all his posts.
    author = models.ForeignKey(UserProfile,
                               on_delete=models.CASCADE,
                               related_name='posts')
    content = models.TextField(max_length=280,
                               validators=[MaxLengthValidator(280)])
    # content = models.CharField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True)
    # likes = models.ManyToManyField(Profile, blank=True)
    likes = models.ManyToManyField(UserProfile,
                                   blank=True,
                                   through='Like',
                                   related_name='likes')

    def save(self, *args, **kwargs):
        """ Resizing images on S3.
        Calculates height based on desired width.
        """
        super().save(*args, **kwargs)

        if not self.image:
            return

        desired_width = 600

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > desired_width or img.width > desired_width:
            extension = os.path.splitext(self.image.name)[1].lower()

            if extension in ['.jpeg', '.jpg']:
                format = 'JPEG'
            if extension in ['.png']:
                format = 'PNG'

            wpercent = (desired_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((desired_width, hsize), Image.ANTIALIAS)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format=format)
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()

    # def save(self, *args, **kwargs):
        """Resizing images on local storage.
        Hardcoded output_size.
        """
        # super().save(*args, **kwargs)

        # if not self.image:
        #     return

        # img = Image.open(self.image.path)

        # if img.height > 510 or img.width > 515:
        #     # TODO split in 2 mote ifs?
        #     output_size = (510, 515)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

    # def save(self, *args, **kwargs):
        """ Resizing images on S3.
        Hardcoded output_size.
        """
        # super().save(*args, **kwargs)

        # if not self.image:
        #     return

        # img_read = storage.open(self.image.name, 'r')
        # img = Image.open(img_read)

        # if img.height > 300 or img.width > 300:
        #     extension = os.path.splitext(self.image.name)[1].lower()

        #     if extension in ['.jpeg', '.jpg']:
        #         format = 'JPEG'
        #     if extension in ['.png']:
        #         format = 'PNG'

        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     in_mem_file = io.BytesIO()
        #     img.save(in_mem_file, format=format)
        #     img_write = storage.open(self.image.name, 'w+')
        #     img_write.write(in_mem_file.getvalue())
        #     img_write.close()

        # img_read.close()

    # def save(self, *args, **kwargs):
        """ Resizing images on S3.
        Using AWS example - divides size by 2.
        """
        # super().save(*args, **kwargs)

        # if not self.image:
        #     return

        # img_read = storage.open(self.image.name, 'r')
        # img = Image.open(img_read)

        # if img.height > 300 or img.width > 300:
        #     extension = os.path.splitext(self.image.name)[1].lower()

        #     if extension in ['.jpeg', '.jpg']:
        #         format = 'JPEG'
        #     if extension in ['.png']:
        #         format = 'PNG'

        #     img.thumbnail(tuple(x / 2 for x in img.size))
        #     in_mem_file = io.BytesIO()
        #     img.save(in_mem_file, format='JPEG')
        #     img_write = storage.open(self.image.name, 'w+')
        #     img_write.write(in_mem_file.getvalue())
        #     img_write.close()

        # img_read.close()

    def __str__(self):
        return f'Post#{self.id} by {self.author.user.username}#{self.author.user.id} -> {self.content[:10]}... '

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Like(models.Model):
    author = models.ForeignKey(UserProfile,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like#{self.id} for Post#{self.post.id} by {self.author.user.username}#{self.author.user.id}  -> Content {self.post.content[:10]}... '


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(UserProfile,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=280)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment#{self.id} for Post#{self.post.id} by {self.author.user.username}#{self.author.user.id}  -> Content {self.text[:10]}... '
