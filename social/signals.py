import logging
import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Post

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Post)
def post_delete_post(sender, instance, **kwargs):
    logger.debug(
        f'post_delete_post: sender:{sender}, instance:{instance}, kwargs:{kwargs}')

    if not instance.image:
        logger.debug('Post has no image. Nothing to delete from storage.')
        return

    fullpath = instance.image.path
    filename = fullpath.split('\\')[-1]

    if os.path.exists(fullpath):
        logger.debug(f'Removing: {filename}...')
        os.remove(fullpath)
        logger.debug(f'Removed: {fullpath}.')
    else:
        logger.debug("File: {fullpath} does not exist.")
