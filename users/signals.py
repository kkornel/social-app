import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .decorators import func_log
from .models import UserProfile

logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


@func_log
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    logger.debug(
        f'create_user_profile signal: sender:{sender}, instance:{instance}, created:{created}, kwargs:{kwargs}')
    if created:
        UserProfile.objects.create(user=instance)


@func_log
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    logger.debug(
        f'save_user_profile signal: sender:{sender}, instance:{instance}, kwargs:{kwargs}')
    instance.userprofile.save()
