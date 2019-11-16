import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .decorators import func_log
from .models import MyUser, Profile

logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


@func_log
@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    logger.debug(
        f'create_profile signal: sender:{sender}, instance:{instance}, created:{created}, kwargs:{kwargs}')
    if created:
        Profile.objects.create(user=instance)


@func_log
@receiver(post_save, sender=MyUser)
def save_profile(sender, instance, **kwargs):
    logger.debug(
        f'save_profile signal: sender:{sender}, instance:{instance}, kwargs:{kwargs}')
    instance.profile.save()
