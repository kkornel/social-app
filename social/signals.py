import logging
import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from users.decorators import func_log

from .models import Post

logger = logging.getLogger(__name__)


@func_log
@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, *args, **kwargs):
    if instance.pk and instance.image:
        try:
            old_img = Post.objects.get(pk=instance.pk).image
        except:
            return
        else:
            if old_img:
                fullpath = old_img.path
                logger.debug(f'Removing: {old_img}...')
                old_img.delete(save=False)
                logger.debug(f'Removed: {fullpath}.')


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
