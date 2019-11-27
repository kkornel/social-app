import logging

from django.core.files.storage import default_storage as storage
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Post

logger = logging.getLogger(__name__)


"""Removing old images from AWS S3 Bucket after updating with new ones """
@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, *args, **kwargs):
    logger.debug('Signal received: pre_save_post')
    new_image = instance.image
    if instance.pk and new_image:
        try:
            old_image = Post.objects.get(pk=instance.pk).image
            logger.debug(f'Old image: {old_image}')
            logger.debug(f'New image: {new_image}')
        except:
            logger.error(f'Image does not exist.')
            return
        else:
            old_image_name = old_image.name

            if old_image and storage.exists(old_image_name) and old_image != new_image:
                logger.debug(f'Removing old image: {old_image_name}...')
                old_image.delete(save=False)
                logger.debug(f'Old image removed.')


"""Removing from AWS S3 Bucket"""
@receiver(post_delete, sender=Post)
def post_delete_post(sender, instance, **kwargs):
    logger.debug('Signal received: post_delete_post')
    if not instance.image:
        logger.debug('Post has no image. Nothing to delete from storage.')
        return

    image_name = instance.image.name

    if storage.exists(image_name):
        logger.debug(f'Removing: {image_name}...')
        storage.delete(image_name)
        logger.debug(f'Image removed.')
    else:
        logger.debug(f'Image: {image_name} does not exist.')


"""Removing old images from local drive after updating with new ones """
# @receiver(pre_save, sender=Post)
# def pre_save_post(sender, instance, *args, **kwargs):
#     logger.debug('Signal received: pre_save_post')
#     new_image = instance.image
#     if instance.pk and new_image:
#         try:
#             old_image = Post.objects.get(pk=instance.pk).image
#             logger.debug(f'Old image: {old_image}')
#             logger.debug(f'New image: {new_image}')
#         except:
#             logger.error(f'Image does not exist.')
#             return
#         else:
#             old_image_name = old_image.name

#             if old_image and old_image != new_image:
#                 logger.debug(f'Removing old image: {old_image_name}...')
#                 old_image.delete(save=False)
#                 logger.debug(f'Old image removed.')


"""Removing from local drive"""
# @receiver(post_delete, sender=Post)
# def post_delete_post(sender, instance, **kwargs):
#     logger.debug('Signal received: post_delete_post')
#     if not instance.image:
#         logger.debug('Post has no image. Nothing to delete from storage.')
#         return

#     image_path = instance.image.path
#     image_name = image_path.split('\\')[-1]

#     if os.path.exists(image_path):
#         logger.debug(f'Removing: {image_name}...')
#         storage.exists(image_name)
#         os.remove(image_path)
#         logger.debug(f'Removed: {image_path}.')
#     else:
#         logger.debug(f'File: {image_path} does not exist.')
